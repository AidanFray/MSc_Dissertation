

#include <CL/cl.hpp>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string.h>
#include <sstream>
#include <cstdlib>
#include <array>
#include <time.h>
#include <stack> 
#include <thread>
#include <chrono>

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

static std::stack<KernelWork> kernel_work;

int KEY_LENGTH = 2048;
int MAX_EXPONENT = 16777215;
int EXPONENT = 0x01000001;

int NUM_OF_HASHES = MAX_EXPONENT;

// Print vars
bool PRINT_PGPv4_PACKET = false;
bool PRINT_GPG_OUTPUT = false;
bool PRINT_SHA1_TEST = false;

bool running = true;


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



void key_from_exponent_and_base_packet(std::string basePacket, std::string exponent)
{
    std::string keyPacket = basePacket.substr(0, basePacket.length() - 8);

    //Pads exponent
    while (exponent.length() < 8) exponent = "0" + exponent;

    std::string newPacket = keyPacket + exponent;

    std::cout << newPacket << std::endl;
}


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
void compute()
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
    //std::cout << "[*] Work Group size set to: " << workGroupSize << std::endl;
    cl::Kernel kernel(program, "key_hash");
    cl::CommandQueue queue(context, device);

    while (true)
    {
        clock_t tStart = clock();
        KernelWork work;

        //TODO: wait if there is no work
        if (kernel_work.size() == 0)
        {
            //std::cout << "[!] Not enough work!" << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
        else
        {
            work = kernel_work.top();
            kernel_work.pop();

            // Will hold the result of the hash on OpenCL
            // is size of the hash plus the success value (0x12345678) and exponent used
            uint outResult[7];
            auto resultSize = sizeof(uint) * 7;

            int err;
            cl::Buffer buf_finalBlock(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(uint) * 16, work.FinalBlock, &err);
            if (err != 0) opencl_handle_error(err);

            cl::Buffer buf_currentHash(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(uint) * 5, work.CurrentHash, &err);
            if (err != 0) opencl_handle_error(err);
            
            cl::Buffer buf_out_result(context, CL_MEM_WRITE_ONLY | CL_MEM_HOST_READ_ONLY, resultSize);

            kernel.setArg(0, buf_finalBlock);
            kernel.setArg(1, buf_currentHash);
            kernel.setArg(2, buf_out_result);

            //TODO: What does this call do?
            queue.enqueueNDRangeKernel(
                kernel, 
                cl::NullRange, 
                NUM_OF_HASHES
            );

            queue.enqueueReadBuffer(buf_out_result, CL_TRUE, 0, resultSize, outResult);

            auto tEnd = (double)(clock() - tStart)/CLOCKS_PER_SEC;
            auto hashPerSecond = (int)(NUM_OF_HASHES) / tEnd;

            std::cout << "[*] Current Rate: " << (int)(hashPerSecond / 1000000) << " MH/s\r" << std::flush;

            //Looks for the positive result value
            if (outResult[0] == (uint)0x12345678)
            {   
                std::string exponent = integer_to_hex(outResult[1]);

                std::cout << "\nWe've got one" << std::endl;
                std::cout << "Exponent: " << exponent << std::endl;

                key_from_exponent_and_base_packet(work.PGP_Packet, exponent);

                break;
            }
        }
    }
}

/*
    This method will be run on the CPU to generate work for OpenCL
*/
void create_work()
{
    while (running)
    {
        // Creates PGP fingerprint packet
        auto PGP_v4_packet = create_PGP_fingerprint_packet();

        // //DEBUG
        // PGP_v4_packet = "99010e045cd1909c010800D19AC0765A452C3FF2BF055EA1BB69A6EB8B77BE93BFF56340564DE9F85F41E36CFF97FFC2381CE9507C9B44DC050A5F31EB2E5E3E28D09AA027D8C24E7E95E2E3641AC501FC6D6D702F3A652791B8701D32E7A85BF345A2CBAB4DA0FF3B53C437EE7905D21AA58CCB74375F2796728F3C26C836D583E87F9ED8EB120EE7E86F3C4EBAE34A21C1A3D0ACAAE2D0CF7F97AA94395A71F4B79C398B58006EB3EAE9C9CF7698BF75048F963071FC81D84F8CEDB2427539E23C7BE0FB519D525DF3DBBF0898DFEF6D32B417F9E21766CF29C89EE4F082A619D01DE684305DC6E4169B19177528CE2690F910B9BE3213430FDAC6867BE87B2A7966F5CAC88202A4DFF9001901000001";
        
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
        
        // // Local hash
        // uint digest_test[5];
        // hash_blocks(hex_blocks, digest_test, hex_blocks.size());
        // std::cout << "[!] PGPv4 local hash result: \n";
        // print_hash(digest_test, 5);
        // std::cout << "\n";

        //Adds the work
        KernelWork work(finalBlock, digest, PGP_v4_packet); 
        kernel_work.push(work);
    }
}

int main()
{
    if (PRINT_SHA1_TEST) sha1_test();
    std::thread createWorkThread1(create_work);
    std::thread createWorkThread2(create_work);
    std::thread createWorkThread3(create_work);
    std::thread createWorkThread4(create_work);
    
    compute();

    //Stops the threads
    running = false;
    createWorkThread1.join();
    createWorkThread2.join();
    createWorkThread3.join();
    createWorkThread4.join();
}