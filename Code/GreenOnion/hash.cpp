

#include <CL/cl.hpp>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string.h>
#include <sstream>
#include <cstdlib>
#include <array>
#include <time.h>
#include <queue> 
#include <thread>
#include <mutex>
#include <csignal>
#include <condition_variable>

#include <openssl/rsa.h>
#include <openssl/rand.h>
#include <openssl/pem.h>
#include <openssl/sha.h>

#include "Crypto/sha1.cpp"
#include "Crypto/hash_util.cpp"

#include "Util/functions.cpp"
#include "Util/OpenCLHelper.cpp"
#include "Util/timer.cpp"


//########################################################//
//                     ISSUES                             //
//########################################################//
// TODO:    More accurate representation of hashing speed
//          needed
//
// TODO:    Look into a better way to multi-thread the
//          work production. ATM I think it's just
//          running the work on the same thread
//
// TODO:    Add RegEx support to the OpenCL program
//
// TODO:    The program is being bottle necked by work
//          generation, is there a faster way to get 
//          more work for OpenCL??
//
// TODO:    Format output public key into a PGP public key
//          packet
//########################################################//

static std::queue<KernelWork> kernel_work;
static std::mutex kernel_work_lock;
std::condition_variable condition;

int KEY_LENGTH = 2048;
int EXPONENT = 0x01000001;

// 0x01FFFFFF - 0x01000001
int NUM_OF_HASHES = 16777215;

// Print vars
bool PRINT_PGPv4_PACKET = false;
bool PRINT_GPG_OUTPUT = false;
bool PRINT_SHA1_TEST = true;

// Threading vars
bool running = true;
int numberOfThreads = 5;
std::vector<std::thread> workThreads;

/*
    Used to test that OpenCL is producing the correct result
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
    print_hash(openclHash, 5);

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
std::string rsa_key_to_pgp(std::string n, std::string e, std::string d)
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

    return result + "#" + d;
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
    std::string str_d = BN_bn2hex(d);

    //Creates the PGP v4 fingerprint packet
    return rsa_key_to_pgp(str_n, str_e, str_d);
}

/*
    Communicates with OpenCL and proccess results
*/
int loops = 0;
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
        Timer tmr;

        KernelWork work;

        while (kernel_work.empty())
        {
            //Sleeps if there is no work
            //std::cout << "[!] Not enough work! Sleeping!" << "\r";
            // std::this_thread::sleep_for(std::chrono::milliseconds(250));
        }
        
        {
            std::lock_guard<std::mutex> lock(kernel_work_lock);
            work = kernel_work.front();
            kernel_work.pop();
        }

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

        auto totalTime = tmr.elapsed();
        tmr.reset();
        auto hashPerSecond = (long)(NUM_OF_HASHES / totalTime);

        // std::cout << "[*] Current Rate: " << (uint)(hashPerSecond / 1000000) << " MH/s\r" << std::flush;
        std::cout 
        << "[*] " 
        << "Current Rate: " <<  hashPerSecond / 1000000 << " MH/s\r" 
        << std::flush;

        //Looks for the positive result value
        if (outResult[0] == (uint)0x12345678)
        {   
            std::string exponent = integer_to_hex(outResult[1]);
            print_found_key(work, exponent);
            break;
        }
        loops++;
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
        auto PGP_v4_packet_with_private_key = create_PGP_fingerprint_packet();

        //PGPv4 fingerprint packet and private key (d) are separated with a "#"
        std::vector<std::string> result;
        split(result, PGP_v4_packet_with_private_key, '#');

        std::string PGP_v4_packet = result[0];
        std::string private_key = result[1];

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
        
        //Adds the work to the stack object
        {
            std::lock_guard<std::mutex> lock(kernel_work_lock);
            KernelWork work(finalBlock, digest, PGP_v4_packet, private_key); 
            kernel_work.push(work);
        }
    }
}


void signalHandler(int signum) {
    std::cout << "\n[*] Interrupt signal received.\n";

    //Stops the threads
    running = false;
    sleep(1000);

    exit(signum);  
}

int main()
{
    signal(SIGINT, signalHandler);  

    if (PRINT_SHA1_TEST) sha1_test();

    //Creates threads
    for (size_t i = 0; i < numberOfThreads; i++)
    {
        std::thread t(create_work);
        t.detach();
    }
    
    //Lets the work populate
    sleep(5000);

    std::cout << "[*] Setup complete!" << std::endl;
    std::cout << "[D] " << kernel_work.size() << std::endl;

    compute();
    running = false;
    sleep(1000);
}