

#include <CL/cl.hpp>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string.h>
#include <sstream>
#include <cstdlib>
#include <array>

#include <openssl/rsa.h>
#include <openssl/rand.h>
#include <openssl/pem.h>
#include <openssl/sha.h>

#include "Crypto/sha1.cpp"
#include "Crypto/hash_util.cpp"

#include "OpenCLHelper.cpp"

int MAX_EXPONENT = 16777215;

/*
    Struct that is used to hold to work for OpenCL
*/
class KernelWork
{
    public:
        uint32_t FinalBlock[32];
        uint32_t CurrentHash[5];

    KernelWork(uint32_t[32], uint32_t[5]);
};

KernelWork::KernelWork (uint32_t finalBlock[32], uint32_t currentHash[5])
{
    //Better way to do this?
    for(int i=0; i<5; ++i)
        CurrentHash[i] = currentHash[i];

    for(int i=0; i<32; ++i)
        FinalBlock[i] = finalBlock[i];
}

static std::vector<KernelWork> kernel_work;

void print_hash(uint* hash)
{
    for(size_t i = 0; i < 5; i++)
    {
        std::cout << hash[i];
    }
    std::cout << std::endl;
}

/*
    Used to test that OpenCL is producing the correst result
*/
void sha1_test()
{
    std::cout << "[*] Testing hashing: " << std::endl;

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
    //Structure:
    // ############################################################################ //
    //  Start   Length   Version  Timestamp   Algo(RSA)    N len     N    Sep   E                                       
    //  0x99      XX      0x04      XXXX        0x01      0x0800   X..X  0011  XXX
    // ############################################################################ //

    // 13 includes all the other values aside from the key length
    int totalLen = 13 + (n.size() / 2);

    // Key length - is everything but start byte and length 
    std::ostringstream streamHex;
    streamHex << std::hex << totalLen;
    std::string hexLength = streamHex.str();

    //Pads values of length
    while (hexLength.length() != 4)  hexLength = "0" + hexLength;

     //Pads values of e
    while (e.size() != 6)  e = "0" + e;

    std::string result = "";

    // Magic byte
    result += "99";

    //Length of packet
    result += hexLength;

    //Version number
    result += "04";

    //Timestamp, blank because it will be incremented later
    result += "00000000";

    // Algo and key length
    result += "01";
    result += "0400";

    //Adds the modulus and exponent key
    result += n;

    //TODO: Check this is a split?
    result += "0011";

    result += e;

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
    RSA *r = RSA_generate_key(1024, 3, NULL, NULL);
    
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
    std::vector<uint[5]>  outResult(10);

    auto resultSize = sizeof(uint) * 5 * outResult.size();

    int err;

    cl::Buffer buf_finalBlock(context, CL_MEM_READ_ONLY  | CL_MEM_COPY_HOST_PTR, sizeof(uint) * 32, finalBlock, &err);
    cl::Buffer buf_currentHash(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(uint) * 5 , currentHash, &err);
    cl::Buffer buf_out_result(context, CL_MEM_WRITE_ONLY | CL_MEM_HOST_READ_ONLY, resultSize);

    kernel.setArg(0, buf_finalBlock);
    kernel.setArg(1, buf_currentHash);
    kernel.setArg(2, buf_out_result);

    // Creates the command queue
    cl::CommandQueue queue(context, device);

    // queue.enqueueNDRangeKernel(
    //     kernel, 
    //     cl::NullRange, 
    //     cl::NDRange(100)
    // );

    queue.enqueueTask(kernel);
    queue.enqueueReadBuffer(buf_out_result, CL_TRUE, 0, resultSize, outResult.data());

    for(size_t i = 0; i < outResult.size(); i++)
    {
        print_hash(outResult[i]);
    }

    // //DEBUG
    // std::cout << "Hashing complete" << std::endl;   
}


/*
    This method will be run on the CPU to generate work for OpenCL
*/
void create_work()
{
    // ############################ //
    // Creates PGP fingerprint packet
    // ############################ //

    auto PGP_v4_packet = create_PGP_fingerprint_packet();

    // Pads and splits it blocks
    std::string padded_v4 = pad_hex_string_for_sha1(PGP_v4_packet);
    auto hex_blocks = split_hex_to_blocks(padded_v4, 64);

    // ############################ //
    //Hashes all but the last block
    // ############################ //
    uint32_t digest[5];

    // Init the SHA state
    digest[0] = 0x67452301;
    digest[1] = 0xEFCDAB89;
    digest[2] = 0x98BADCFE;
    digest[3] = 0x10325476;
    digest[4] = 0xC3D2E1F0;

    for(size_t i = 0; i < hex_blocks.size() - 1; i++)
    {
        uint32_t W[16];
        hex_block_to_words(W, hex_blocks[i]);
        transform(digest, W);
    }

    //Saves the final block
    uint32_t finalBlock[16]; 
    hex_block_to_words(finalBlock, hex_blocks[hex_blocks.size() - 1]);
    
    // KernelWork work(finalBlock, digest);

    // kernel_work.push_back(work);

    //DEBUG
    compute(finalBlock, digest);
}

int main()
{
    sha1_test();
    create_work();
    // compute();
}