

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
#include <map>

#include <openssl/rsa.h>
#include <openssl/rand.h>
#include <openssl/pem.h>
#include <openssl/sha.h>
#include <bits/stdc++.h> 

#include "Crypto/sha1.cpp"
#include "Crypto/hash_util.cpp"

#include "Util/functions.cpp"
#include "Util/OpenCLHelper.cpp"
#include "Util/timer.cpp"

#include "Bloom/BloomFilter.cpp"

//########################################################//
//                     ISSUES                             //
//########################################################//
// TODO:    If there is more than one match per OpenCL loop
//          it will overwrite the previous match.
//          The solution for this will be the implement a 
//          way to return multiple matches for each run
//########################################################//

static std::queue<KernelWork> kernel_work;
static std::mutex kernel_work_lock;
std::condition_variable condition;

int KEY_LENGTH = 2048;
int EXPONENT = 0x01000001;

// 0x01FFFFFF - 0x01000001
int NUM_OF_HASHES = 16777215;

// Print vars
bool PRINT_SHA1_TEST = true;

//Set to 0 for no cap
int MAX_WORK_SIZE = 1000;

// Threading vars
bool running = true;
int numberOfThreads = 1;
std::vector<std::thread> workThreads;

//DEBUG
// std::string target_keys_file_path = "/home/user/Github/Cyber-Security-Individual-Project/Code/GreenOnion/target_keys.txt";
// std::string kernel_file_path = "/home/user/Github/Cyber-Security-Individual-Project/Code/GreenOnion/OpenCL/SHA1.cl";

std::string target_keys_file_path = "./target_keys.txt";
std::string kernel_file_path = "./OpenCL/SHA1.cl";

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
    Hashes all but the last block of the PGP packet
*/
void hash_packet(uint *finalBlock, uint *digest, std::string PGP_v4_packet)
{
    // Pads and splits it blocks
    std::string padded_v4 = pad_hex_string_for_sha1(PGP_v4_packet);
    auto hex_blocks = split_hex_to_blocks(padded_v4, 64);

    //Hashes all but the last block
    hash_blocks(hex_blocks, digest, hex_blocks.size() - 1);

    //Saves the final block
    hex_block_to_words(finalBlock, hex_blocks[hex_blocks.size() - 1]);
}

/*
    Converts an RSA key to PGP public key packet defined in RFC 4880
*/
std::string rsa_key_to_pgp(std::string n, std::string e, int timestamp)
{   
    //Structure 2024 key:
    // ############################################################################ //
    //  Start   Length   Version  Timestamp   Algo(RSA)    MPI(n)    MPI(e)                                 
    //  0x99     XX       0x04      XXXX        0x01         X         X
    // ############################################################################ //

    // How many characters the packet length is
    int PACKET_LENGTH_CHARS = 4; 
    int TIMESTAMP_LENGTH_CHARS = 8;

    std::string result = "";

    //Version number
    result += "04";

    //Pads to 4 bytes
    std::string timestamp_string = integer_to_hex(timestamp);
    pad(timestamp_string, TIMESTAMP_LENGTH_CHARS, '0');

    result += timestamp_string;

    // Algo number
    result += "01";

    //MPI (N)
    result += "0800";
    result += n;

    //MPI (e)
    result += hex_string_to_mpi(e);

    //Encapsulates in a fingerprint packet
    std::string public_packet_len = integer_to_hex(result.length() / 2);
    pad(public_packet_len, 4, '0');

    result = "99" + public_packet_len + result;

    return result;
}

/*
    Generates an RSA key to be sent to the GPU
*/
void generate_RSA_key(std::string &str_n, std::string &str_e, std::string &str_d)
{
    // Generate Key
    RSA *r = RSA_generate_key(KEY_LENGTH, EXPONENT, NULL, NULL);
    
    const BIGNUM *n, *e, *d;
    RSA_get0_key(r, &n, &e, &d);

    //Converts public key sections to hex
    str_n = BN_bn2hex(n);
    str_e = BN_bn2hex(e);
    str_d = BN_bn2hex(d);
}

/*
    Converts the keys to check to two 32-bit integers
*/
void convert_target_keys_to_opencl_param(std::vector<std::array<uint, 2>> targetKeys, uint* target_key_values)
{
    for (size_t i = 0; i < targetKeys.size(); i++)
    {
        auto key_values = targetKeys[i];

        for (size_t x = 0; x < 2; x++)
        {
            target_key_values[(i * 2) + x] = key_values[x];
        }
    }
}

/*
    Loads the keys hashes the program should be searching for
*/
void load_filters(BloomFilter &bf, std::map<std::string, bool> &hash_table, std::string filePath)
{
    std::string line;
    std::ifstream infile(filePath);
    while (getline(infile, line))
    {
        auto integer = hex_to_64bit_integer(line);

        // Adds the value to the bloom bit array
        bf.add(integer);

        // Adds the value to the hash table
        // this is for checking the false positives of the bloom later
        hash_table[line] = true;
    }
}

/*
    TODO
*/
uint get_target_key_length(std::string filePath)
{
    int number_of_lines = 0;
    std::string line;
    std::ifstream myfile(filePath);

    while (std::getline(myfile, line))
        ++number_of_lines;

    return number_of_lines;
}


/*
    Communicates with OpenCL and proccess results
*/
void compute()
{
    int loops = 1;
    int false_positives = 0;

    int workSize = 0;
    int workGroupSize = 0;
    int createWorkThreads = 0;

    //Inits OpenCL devices
    auto platform = GetPlatform();
    auto devices = GetAllDevices(platform, false);
    auto device = devices.front();
    cl::Context context(devices);
    auto program = BuildProgram(kernel_file_path, context);
    workGroupSize = device.getInfo<CL_DEVICE_MAX_WORK_GROUP_SIZE>();
    //std::cout << "[*] Work Group size set to: " << workGroupSize << std::endl;
    cl::Kernel kernel(program, "key_hash");
    cl::CommandQueue queue(context, device);


    //################################  FILTERS ## #######################################//
    //TODO : refactor
    std::map<std::string, bool> target_keys_hash_table;

    //TODO: Move these to a better location
    //      These will also require passing to the OpenCL kernel
    auto number_of_target_keys = get_target_key_length(target_keys_file_path);

    if (number_of_target_keys == 0)
    {
        std::cout << "[!] Error: No target keys have been loaded. Please check the target_keys.txt file" << std::endl;
        exit(0);
    }
    std::cout << "[*] Number of target keys loaded: " << number_of_target_keys << std::endl;

    auto BLOOM_SIZE = calculate_bloom_size(number_of_target_keys);

    //DEBUG
    BLOOM_SIZE = 1700000;
    
    auto NUMBER_OF_HASHES = 2;

    std::cout << "[*] Creating bloom filter....." << std::endl;

    BloomFilter bf(BLOOM_SIZE, NUMBER_OF_HASHES);
    load_filters(bf, target_keys_hash_table, target_keys_file_path);

    long bloom_bit_vector_size[1] = {BLOOM_SIZE};

    std::cout << "[*] Bloom filter complete!" << std::endl;
    //#####################################################################################//

    while (true)
    {
        Timer tmr;

        KernelWork work;

        if (kernel_work.empty())
        {
            //Sleeps if there is no work
            std::cout << "[!] Not enough work! Sleeping!" << "\n";
            std::this_thread::sleep_for(std::chrono::milliseconds(250));
        }
        else
        {
            {
                std::lock_guard<std::mutex> lock(kernel_work_lock);
                work = kernel_work.front();
                kernel_work.pop();
            }

            // Will hold the result of the hash on OpenCL
            // is size of the hash plus the success value (0x12345678) and exponent used
            uint outResult[2];
            auto resultSize = sizeof(uint) * 2;

            int err;
            cl::Buffer buf_finalBlock(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(uint) * 16, work.FinalBlock, &err);
            if (err != 0) opencl_handle_error(err, "final_block");

            cl::Buffer buf_currentHash(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(uint) * 5, work.CurrentHash, &err);
            if (err != 0) opencl_handle_error(err, "current_hash");

            cl::Buffer buf_bitVector(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, (sizeof(bool) * BLOOM_SIZE), bf.m_bits, &err);
            if (err != 0) opencl_handle_error(err, "bit_vector");

            cl::Buffer buf_bitVectorSize(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(long), bloom_bit_vector_size, &err);
            if (err != 0) opencl_handle_error(err, "bit_vector_size");
            
            cl::Buffer buf_out_result(context, CL_MEM_WRITE_ONLY | CL_MEM_HOST_READ_ONLY, resultSize);

            kernel.setArg(0, buf_finalBlock);
            kernel.setArg(1, buf_currentHash);
            kernel.setArg(2, buf_bitVector);
            kernel.setArg(3, buf_bitVectorSize);
            kernel.setArg(4, buf_out_result);

            queue.enqueueNDRangeKernel(
                kernel, 
                cl::NullRange, 
                cl::NDRange(NUM_OF_HASHES, 1)
            );

            queue.enqueueReadBuffer(buf_out_result, CL_TRUE, 0, resultSize, outResult);

            auto totalTime = tmr.elapsed();
            tmr.reset();
            auto hashPerSecond = (long)(NUM_OF_HASHES / totalTime);

            // std::cout << "[*] Current Rate: " << (uint)(hashPerSecond / 1000000) << " MH/s\r" << std::flush;

            auto HPS = std::to_string(hashPerSecond / 1000000);
            pad(HPS, 4, '0');

            double fp_percentage = ((double)false_positives / (double)loops) * 100;

            std::cout 
            << "[*]" 
            << " -- Current Rate:  "       << HPS << " MH/s" 
            << " -- Loops: "               << loops 
            << " -- FP: "                  << false_positives
            << " -- FP Percentage: "       << fp_percentage << "%"
            << "\r"
            << std::flush;

            //Looks for the positive result value
            if (outResult[0] == (uint)0x12345678)
            {   
                std::string exponent = integer_to_hex(outResult[1]);

                //Recreates the key
                auto x = key_from_exponent_and_base_packet(work.PGP_Packet, exponent);
                
                //Obtains the hash of the key
                uint digest[5];
                hash_string(x, digest);
                auto hex_digest = sha_digest_to_sting(digest, 2);

                // If true an actual key is found
                if(target_keys_hash_table.count(hex_digest))
                {
                    print_found_key(work, exponent);
                    break;
                }
                else
                {
                    false_positives++;
                    outResult[0] = 0xffffffff;
                }
            }
            loops++;
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
        //Stops the program from working too hard by capping the max work size
        if (kernel_work.size() < MAX_WORK_SIZE || MAX_WORK_SIZE == 0)
        {
            std::string n, e, d;
            generate_RSA_key(n, e, d);

            // Creates PGP fingerprint packet
            int timestamp = (int)std::time(nullptr);

            // Stretches out the key using the time stamp 
            for (size_t i = 0; i < 1000; i++)
            {
                auto PGP_v4_packet = rsa_key_to_pgp(n, e, timestamp + i);

                //DEBUG
                // PGP_v4_packet = "99010e045cdd5d39010800A963BD6AF2ED6CD5DAE0CCDF363F649A8850D3476715E9F3540EF5DA47A761AFC129ACE0004D2E7A0B33CD6760175F3BE7315DBA4300A6C4480FD250474164AB15C32207DBEE8340FE8D2D394F52FE4B3C51B9D217C245B41433DBB631F8B85601BCB133345EF769DA33D98DF8C98D04B6D958F324C4C329E5AD29BEB267863E70024434D1E7D42FD92D67FD1BFE7037C708A94F09C7481A6CEDC51A010005ABF9F7E36EFF31C6BD039C17EED160ECD788716ED7638EF176F435049CFF31CB014F9348A8C29185ECBAF65F63D73C963174F17DC6F1CA33F49C442DDF8389EA67C9E5A89DCDD2A645C1B00839268BF4558A43BBD7BD3CA6111831334AFA16EBE3001901000001";

                uint finalBlock[16]; 
                uint intermediate_digest[5];
                hash_packet(finalBlock, intermediate_digest, PGP_v4_packet);
                
                //Adds the work to the stack object
                {
                    std::lock_guard<std::mutex> lock(kernel_work_lock);
                    KernelWork work(finalBlock, intermediate_digest, PGP_v4_packet, d); 
                    kernel_work.push(work);
                }
            }
        }
        else
        {
            sleep(500);
        }
    }
}


void signalHandler(int signum) 
{
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
    
    compute();
    running = false;
    sleep(1000);
}