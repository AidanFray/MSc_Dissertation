

#include <CL/cl.hpp>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string.h>
#include <sstream>
#include <cstdlib>
#include <array>
#include <time.h>

#include <openssl/rsa.h>
#include <openssl/rand.h>
#include <openssl/pem.h>
#include <openssl/sha.h>

#include "Crypto/sha1.cpp"
#include "Crypto/hash_util.cpp"

#include "Util/functions.cpp"
#include "Util/kernel_work.cpp"
#include "Util/OpenCLHelper.cpp"

//########################################################//
//                     ISSUES                             //
//########################################################//
// - Hash outputs from OpenCL all have the same end??     //
//   but not on my CPU, only on the AMD GPU
//########################################################//

int KEY_LENGTH = 2048;
int MAX_EXPONENT = 16777215;
int EXPONENT = 0x01000001;

int NUM_OF_HASHES = MAX_EXPONENT;

// Print vars
bool PRINT_PGPv4_PACKET = true;
bool PRINT_GPG_OUTPUT = false;
bool PRINT_SHA1_TEST = true;


/*
    Function used to print arrays
*/
static void print_hash(uint* hash, int blockLength)
{
    for(size_t i = 0; i < blockLength; i++)
    {
        std::string hexString = integer_to_hex(hash[i]);

        //Pads the string
        while (hexString.length() < 8) hexString = "0" + hexString;

        std::cout << hexString;

        if (i != (blockLength - 1)) std::cout << ":";
    }
    std::cout << std::endl;
}


/*
    Vector that is used to hold to work for OpenCL
*/
static std::vector<KernelWork> kernel_work;

/*
    Converts an integer to multiprecision integer (RFC 4880)
*/
std::string hex_string_to_mpi(std::string hexString)
{
    auto binary_string = hex_to_binary(hexString);
    auto stripped_binary_string = binary_strip_left_zeros(binary_string);
    auto binary_string_len = integer_to_hex(stripped_binary_string.length());

    //Pads to 2 bytes
    while (binary_string_len.length() < 4) binary_string_len = "0" + binary_string_len;

    std::string output = binary_string_len + hexString;
    return output;
}


/*
    Used to test that OpenCL is producing the correst result
*/
void sha1_test()
{
    //OpenGL Hash
    auto platform = GetPlatform();
    auto devices = GetAllDevices(platform, true);
    auto device = devices.front();

    cl::Context context(devices);

    auto program = BuildProgram("./OpenCL/SHA1.cl", context);

    // 160 bit
    uint openclHash[5];

    cl::Buffer valueBuf(context, CL_MEM_READ_WRITE | CL_MEM_HOST_READ_ONLY, sizeof(openclHash));

    cl::Kernel kernel(program, "shaTest");
    kernel.setArg(0, valueBuf);

    cl::CommandQueue queue(context, device);
    queue.enqueueTask(kernel);
    queue.enqueueReadBuffer(valueBuf, CL_TRUE, 0, sizeof(openclHash), openclHash);

    // Prints out the hash
    std::cout << "OpenCL: ";
    std::cout << std::hex << openclHash[0];
    std::cout << std::hex << openclHash[1];
    std::cout << std::hex << openclHash[2];
    std::cout << std::hex << openclHash[3];
    std::cout << std::hex << openclHash[4];
    std::cout << std::endl;

    const char* ibuf = "Hello world!";
    unsigned char obuf[20];

    SHA1((unsigned char*)ibuf, strlen(ibuf), obuf);

    //Prints the has
    std::cout << "Local:  ";
    for (int i = 0; i < 20; ++i) {
        printf("%02x", obuf[i]);
    }
    std::cout << "\n\n";

}

/*
    Converts an RSA key to PGP public key packet defined in RFC 4880
*/
std::string rsa_key_to_pgp(std::string n, std::string e)
{   
    //Structure 2024 key:
    // ############################################################################ //
    //  Start   Length   Version  Timestamp   Algo(RSA)    N len     N    Sep   E                                       
    //  0x98      X       0x04      XXXX        0x01      0x0800   X..X  0011  XXX
    // ############################################################################ //

    //TODO: Make sure these are all inclusive
    // How many characters the packet length is
    int PACKET_LENGTH_CHARS = 4; 
    int TIMESTAMP_LENGTH_CHARS = 8;

    std::string result = "";

    //Version number
    result += "04";

    //Time of creation
    std::string timestamp = integer_to_hex((int)std::time(nullptr));

    //Pads to 4 bytes
    while (timestamp.length() < TIMESTAMP_LENGTH_CHARS)  timestamp = "0" + timestamp;
    result += timestamp;

    // Algo number
    result += "01";

    //MPI (N)
    //TODO: dynamic key length
    result += "0800";
    result += n;

    //MPI (e)
    result += hex_string_to_mpi(e);

    //Encapsulates in a fingerprint packet
    std::string public_packet_len = integer_to_hex(result.length() / 2);
    while (public_packet_len.length() < 4) public_packet_len = "0" + public_packet_len;

    result = "99" + public_packet_len + result;

    return result;
}

/*
    Method that creates PGP fingerprint v4 packet
    and returns it as hex
*/
std::string create_PGP_fingerprint_packet()
{   
    //############################################################ // 
    //TODO: What should be done with RSA's d for the private key?
    //############################################################ // 

    // Generate Key
    RSA *r = RSA_generate_key(KEY_LENGTH, EXPONENT, NULL, NULL);
    
    const BIGNUM *n, *e, *d;
    RSA_get0_key(r, &n, &e, &d);

    //Converts public key sections to hex
    std::string str_n = BN_bn2hex(n);
    std::string str_e = BN_bn2hex(e);

    //Creates the PGP v4 fingerprint packet
    return rsa_key_to_pgp(str_n, str_e);
}

/*
    Communicates with OpenCL and proccess results
*/
void compute(uint* finalBlock, uint* currentHash)
{

    int workSize = 0;
    int workGroupSize = 0;
    int createWorkThreads = 0;

    //Inits OpenCL devices
    auto platform = GetPlatform();
    auto devices = GetAllDevices(platform, false);
    auto device = devices.front();

    cl::Context context(devices);

    auto program = BuildProgram("./OpenCL/SHA1.cl", context);

    workGroupSize = device.getInfo<CL_DEVICE_MAX_WORK_GROUP_SIZE>();
    std::cout << "[*] Work Group size set to: " << workGroupSize << std::endl;

    //Kernel and parameter creation
    cl::Kernel kernel(program, "key_hash");

    // Will hold the result of the hash on OpenCL
    //##########################################//
    //TODO: Return only the last two 32bit words//
    //##########################################//
    std::vector<uint[2]> outResult(NUM_OF_HASHES);

    auto resultSize = sizeof(uint) * 2 * outResult.size();

    int err;

    cl::Buffer buf_finalBlock(context, CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR, sizeof(uint) * 16, finalBlock, &err);
    if (err != 0) opencl_handle_error(err);

    cl::Buffer buf_currentHash(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(uint) * 5, currentHash, &err);
    if (err != 0) opencl_handle_error(err);
    
    cl::Buffer buf_out_result(context, CL_MEM_WRITE_ONLY | CL_MEM_HOST_READ_ONLY, resultSize);

    kernel.setArg(0, buf_finalBlock);
    kernel.setArg(1, buf_currentHash);
    kernel.setArg(2, buf_out_result);

    // Creates the command queue
    cl::CommandQueue queue(context, device);

    // queue.enqueueNDRangeKernel(
    //     kernel, 
    //     cl::NullRange, 
    //     cl::NDRange(outResult.size())
    // );

    queue.enqueueNDRangeKernel(
        kernel, 
        cl::NullRange, 
        cl::NDRange(outResult.size())
    );

    clock_t tStart = clock();
    queue.enqueueReadBuffer(buf_out_result, CL_TRUE, 0, resultSize, outResult.data());
    auto tEnd = (double)(clock() - tStart)/CLOCKS_PER_SEC;
    auto hashPerSecond = NUM_OF_HASHES / tEnd;

    printf("[*] Time taken: %.2fs\n", tEnd);
    printf("[*] %.2f MH/s\n", hashPerSecond / 1000000);

    for(size_t i = 0; i < 10; i++)
    {
        print_hash(outResult[i], 2);
    }
    // print_hash(outResult[0], 2);
}

/*
    This method will be run on the CPU to generate work for OpenCL
*/
void create_work()
{
    // Creates PGP fingerprint packet
    auto PGP_v4_packet = create_PGP_fingerprint_packet();

    //DEBUG
    // PGP_v4_packet = "99010b045cd04d5a010800C95EEE4E44FB0609429D59D6197EE3F4E86DCEB2CD2BA09748A44D6DB8B8E4557D87AC335B8E7D8939D689E154C052E07BE6CD393A8FBCB657FFDFE7402D17F418DF21ED1847C1506E624265F12D2DEE08A77B422FD97C95F5451E963B2055910E571CE7157078EF6B6967C1A94EC094F314ABA9E1ABCDD8C68EE0FD3ABCBE1D50F5532EF099E3559BD3B738336D51319AE3CDD36CAEF1AF87C6A72FCACB428AB8D2F20A4E859D5C22ADC9C9A1A9DC99DBE9091BECA725C065A8B4996D5515F3FCD740E4A71B623C67DBC17444326F1E7140A0691255548422ABBF0D404512BE43DE59BBD02B8E3419AE22E17C201D7379B0AD70A309F05F8D70765A07BF422D000203";
    //

    // Pads and splits it blocks
    std::string padded_v4 = pad_hex_string_for_sha1(PGP_v4_packet);
    auto hex_blocks = split_hex_to_blocks(padded_v4, 64);

    if (PRINT_PGPv4_PACKET)
    {
        std::cout << "[*] PGP v4 packet: " << std::endl;
        std::cout << PGP_v4_packet << "\n\n";
    }

    if (PRINT_GPG_OUTPUT)
    {
       //## GPG output
        std::cout << "[*] GPG output: " << std::endl;
        //Runs it with a local python script
        std::string command = "python ../Misc/hex_pubkey.py ";
        command += PGP_v4_packet + "99";
        command += " | gpg --list-packets";

        std::system(command.c_str());
        std::cout << "\n\n"; 
    }

    //Hashes all but the last block
    uint digest[5];
    hash_blocks(hex_blocks, digest, hex_blocks.size() - 1);

    //Saves the final block
    uint finalBlock[16]; 
    hex_block_to_words(finalBlock, hex_blocks[hex_blocks.size() - 1]);
    
    // Adds the word to the vector
    KernelWork work(finalBlock, digest);
    kernel_work.push_back(work);
    
    // Local hash
    uint digest_test[5];
    hash_blocks(hex_blocks, digest_test, hex_blocks.size());
    std::cout << "[!] PGPv4 local hash result: \n";
    print_hash(digest_test, 5);
    std::cout << "\n";

    compute(finalBlock, digest);
}

int main()
{
    if (PRINT_SHA1_TEST) sha1_test();
    create_work();
    // compute();
}