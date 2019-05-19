#include <CL/cl.hpp>                    // for Buffer, Kernel, CommandQueue, Context
#include <CL/cl.h>                      // for CL_MEM_COPY_HOST_PTR, CL_MEM_READ_ONLY

#include <openssl/sha.h>                // for SHA1
#include <sys/types.h>                  // for uint
#include <string.h>                     // for strlen
#include <iostream>                     // for operator<<, basic_ostream, cout
#include <stdio.h>                      // for printf
#include <fstream>                      // for ifstream
#include <csignal>                      // for signal, SIGINT
#include <cstdlib>                      // for exit, size_t
#include <iomanip>                      // for setprecision
#include <chrono>                       // for milliseconds
#include <string>                       // for string, getline, operator<<, to_string
#include <thread>                       // for thread, sleep_for
#include <vector>                       // for vector
#include <math.h>                       // for pow, round
#include <ctime>                        // for time
#include <mutex>                        // for mutex, lock_guard
#include <queue>                        // for queue
#include <map>                          // for map

#include "bloom/BloomFilter.hpp"        // for BloomFilter, calculate_bloom_size
#include "util/OpenCLHelper.hpp"        // for opencl_handle_error, BuildProgram
#include "util/kernel_work.hpp"         // for KernelWork
#include "crypto/hash_util.hpp"         // for hash_string
#include "util/terminal_colors.hpp"     // for INFO, WARNING, OUTPUT
#include "util/conversion.hpp"          // for hex_to_64bit_integer, integer_to_hex
#include "util/functions.hpp"           // for sleep, pad, key_from_exponent_and_b...
#include "util/timer.hpp"               // for Timer
#include "util/pgp.hpp"                 // for create_pgp_v4_fingerprint_packet

//########################################################//
//                     ISSUES                             //
//########################################################//
// BUG: Program is having an error where when the first FP
//       is introduced the number starts rapidly climbing??
//
//########################################################//
// TODO: Dynamically sized bloom filter functionality
//
// TODO: pass in 'target_keys.txt' as a parameter to the
//       script
//
// TODO: Saving found keys to file
//
// TODO: Benchmark mode
//
// TODO: Have the script only print when a key is pressed
//       this is similar to the way HashCat works
//########################################################//
static std::queue<KernelWork> kernel_work;
static std::mutex kernel_work_lock;

// TODO: Make these script arguments
bool PRINT_SHA1_TEST = true;
bool END_ON_KEY_FOUND = true;

// RSA key params
int KEY_LENGTH = 2048;
int EXPONENT = 0x01000001;

// Bloom filter params
uint BLOOM_NUMBER_OF_HASHES_STATIC  = 5;    //Set to 0 for dynamic size
long BLOOM_SIZE_STATIC              = 0;    //Set to 0 for dynamic size

// Threading params
bool running = true;
size_t numberOfThreads = 1;
std::vector<std::thread> workThreads;

size_t NUM_OF_HASHES = 16777215;            // The amount of hashes per loop
size_t MAX_WORK_SIZE = 1000;                //Set to 0 for no cap

//DEBUG
// std::string target_keys_file_path = "/home/main_user/GitHub/Cyber-Security-Individual-Project/Code/GreenOnion/target_keys.txt";
// std::string kernel_file_path = "/home/main_user/GitHub/Cyber-Security-Individual-Project/Code/GreenOnion/opencl/SHA1.cl";

std::string target_keys_file_path = "./target_keys.txt";
std::string kernel_file_path = "./opencl/SHA1.cl";

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

    auto program = BuildProgram(kernel_file_path, context);

    // 160 bit digest
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
    Loads the keys hashes the program should be searching for. 
    It's loaded into a bloom filter and a hash table (required for checking false positives)
*/
void load_filters(BloomFilter &bf, std::map<std::string, bool> &hash_table, std::string filePath)
{
    std::cout << OUTPUT << " Creating bloom filter....." << std::endl;
    std::string line;
    std::ifstream infile(filePath);
    while (std::getline(infile, line))
    {
        auto integer = hex_to_64bit_integer(line);

        // Adds the value to the bloom bit array
        bf.add(integer);

        // Adds the value to the hash table
        // this is for checking the false positives of the bloom later
        hash_table[line] = true;
    }
    std::cout << OUTPUT << " Bloom filter creation complete!" << std::endl;
}

/*
    Gets the number of target keys being loaded into the program
*/
uint get_and_check_target_key_length(std::string filePath)
{
    int number_of_lines = 0;
    std::string line;
    std::ifstream myfile(filePath);

    while (std::getline(myfile, line))
        ++number_of_lines;

    if (number_of_lines == 0)
    {
        std::cout << WARNING <<" Error: No target keys have been loaded. Please check the target_keys.txt file" << std::endl;
        exit(0);
    }
    std::cout << INFO <<" Number of target keys loaded: " << number_of_lines << std::endl;

    return number_of_lines;
}

/*
    Calculates the potential run time required to find a match
*/
std::string calculate_run_time(double hashRate, long numberOfKeys)
{
    std::string units[5] = {"Seconds", "Minutes", "Hours", "Days", "Years"};
    int lengthChars = 16; // 4 words

    std::string current_unit = units[0];

    long double top = (pow(2, (4 * lengthChars)));
    double time_value = top / hashRate / numberOfKeys;

    // Conversions to minutes
    if(time_value > 60.0)
    {
        current_unit = units[1];
        time_value /= 60;
    }

    // Conversions to hours
    if(time_value > 60.0)
    {
        current_unit = units[2];
        time_value /= 60;
    }

    // Conversions to days
    if(time_value > 24.0)
    {
        current_unit = units[3];
        time_value /= 24;
    }

    // Conversions to years
    if(time_value > 365.0)
    {
        current_unit = units[4];
        time_value /= 365;
    }

    return std::to_string((uint)time_value) + " " + current_unit;
}

/*
    Communicates with OpenCL and proccess results
*/
void compute()
{
    int loops = 1;
    int false_positives = 0;

    // ### OpenCL INIT ###
    auto platform = GetPlatform();
    auto devices = GetAllDevices(platform, false);
    auto device = devices.front();
    cl::Context context(devices);
    auto program = BuildProgram(kernel_file_path, context);
    // int workGroupSize = device.getInfo<CL_DEVICE_MAX_WORK_GROUP_SIZE>();
    //std::cout << OUTPUT << " Work Group size set to: " << workGroupSize << std::endl;
    cl::Kernel kernel(program, "key_hash");
    cl::CommandQueue queue(context, device);

    // ### FILTER INIT ###
    auto number_of_target_keys = get_and_check_target_key_length(target_keys_file_path);

    long BLOOM_SIZE = 0;
    if (BLOOM_SIZE_STATIC != 0) 
    {
        BLOOM_SIZE = BLOOM_SIZE_STATIC;
    }
    else
    {
        BLOOM_SIZE = calculate_bloom_size(number_of_target_keys);
    }

    uint BLOOM_NUMBER_OF_HASHES = 0;
    if (BLOOM_NUMBER_OF_HASHES_STATIC != 0) 
    {
        BLOOM_NUMBER_OF_HASHES = BLOOM_NUMBER_OF_HASHES_STATIC;
    }
    else 
    {
        BLOOM_NUMBER_OF_HASHES = calculate_number_of_hashes(number_of_target_keys, BLOOM_SIZE);
    }

    std::cout << INFO << " Bloom filter size: " << BLOOM_SIZE << std::endl;
    std::cout << INFO << " Number of bloom filter hash cycles: " << BLOOM_NUMBER_OF_HASHES << std::endl;
    std::cout << std::endl;

    // Filter objects    
    std::map<std::string, bool> target_keys_hash_table;
    BloomFilter bf(BLOOM_SIZE, BLOOM_NUMBER_OF_HASHES);
    load_filters(bf, target_keys_hash_table, target_keys_file_path);

    while (true)
    {
        Timer tmr;
        KernelWork work;

        if (kernel_work.empty())
        {
            //Sleeps if there is no work
            std::cout << WARNING << " Not enough work! Sleeping!" << "\n";
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

            cl::Buffer buf_bitVectorSize(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(long), new long[1] {BLOOM_SIZE}, &err);
            if (err != 0) opencl_handle_error(err, "bit_vector_size");

            cl::Buffer buf_numberOfHashes(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(uint), new uint[1] {BLOOM_NUMBER_OF_HASHES}, &err);
            if (err != 0) opencl_handle_error(err, "number_of_hashes");
            
            cl::Buffer buf_out_result(context, CL_MEM_WRITE_ONLY | CL_MEM_HOST_READ_ONLY, resultSize);

            kernel.setArg(0, buf_finalBlock);
            kernel.setArg(1, buf_currentHash);
            kernel.setArg(2, buf_bitVector);
            kernel.setArg(3, buf_bitVectorSize);
            kernel.setArg(4, buf_numberOfHashes);
            kernel.setArg(5, buf_out_result);

            queue.enqueueNDRangeKernel(
                kernel, 
                cl::NullRange, 
                cl::NDRange(NUM_OF_HASHES, 1)
            );

            queue.enqueueReadBuffer(buf_out_result, CL_TRUE, 0, resultSize, outResult);

            auto totalTime = tmr.elapsed();
            tmr.reset();
            auto hashPerSecond = (long)(NUM_OF_HASHES / totalTime);

            // std::cout << OUTPUT << " Current Rate: " << (uint)(hashPerSecond / 1000000) << " MH/s\r" << std::flush;

            auto HPS = std::to_string(hashPerSecond / 1000000);
            pad(HPS, 4, '0');

            double fp_percentage = ((double)false_positives / (double)loops) * 100;

            std::cout << std::setprecision(2) << std::setiosflags(std::ios::fixed)
            << OUTPUT << "" 
            << " -- Current Rate:  "       << HPS << " MH/s" 
            << " -- Loops: "               << loops 
            << " -- FP: "                  << false_positives
            << " -- FP Percentage: "       << fp_percentage << "%"
            << " -- Runtime: "             << calculate_run_time(hashPerSecond, number_of_target_keys)
            << "\r"
            << std::flush;

            //Looks for the positive result value
            if (outResult[0] == (uint)0x12345678)
            {
                std::string exponent = integer_to_hex(outResult[1]);
                pad(exponent, 8, '0');

                //Recreates the key
                auto pgp_key = key_from_exponent_and_base_packet(work.m_fingerprintPacket, exponent);
                
                //Obtains the hash of the key
                uint digest[5];
                hash_string(pgp_key, digest);

                // Only takes the 2 left most 32-bit blocks
                auto hex_digest = sha_digest_to_string(digest, 2);

                // If true an actual key is found
                if(target_keys_hash_table.count(hex_digest))
                {
                    print_found_key(work, exponent);
                    if (END_ON_KEY_FOUND) break;
                }
                else
                {
                    //Resets
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
            std::string n, e, d, p, q, u;
            generate_rsa_key(n, e, d, p, q, u, KEY_LENGTH, EXPONENT);

            // Creates PGP fingerprint packet
            int timestamp = (int)std::time(nullptr);

            // Stretches out the key using the time stamp 
            for (size_t i = 0; i < 1000; i++)
            {
                auto PGP_v4_packet = create_pgp_v4_fingerprint_packet(n, e, timestamp + i);

                // DEBUG
                // PGP_v4_packet = "99010e045cdfe0dd010800D06223A61A67F848EC1F7C6739D8FE22BD6A0C6083E309149FC8BD081B99CCDA10A1182F8690402CCE679626B77157A039B543C7239D597534572F0A91BC1FA001355B45D1FC05CBC900F043E3A9C055DA3D35D3FBCDCFC1CF82D006A81943599E445B797489C496462F7AAB3BD1BB4E40D994E3A78F0E28149E242BBCF3661F07827E728B5C259FCF0A8EA3CA37822602620DA8C89C27F0DF226AE84EA7F1980F9CEE2373C707610C45536903B3E03B37B98D979ADA24B68748A2321EB51D986BF29048108F31592C1B11B7E34B34BE5185435BE0F0B6F9C11C9CA9FFEEB8060A63F7A594B1CC72A61E9E505EEE023FDA8D2B1356015E74D6513D20B228BC5F001901000001";

                uint finalBlock[16]; 
                uint intermediate_digest[5];
                sha1_hash_all_but_final_block_of_pgp_packet(finalBlock, intermediate_digest, PGP_v4_packet);
                
                //Adds the work to the stack object
                {
                    std::lock_guard<std::mutex> lock(kernel_work_lock);
                    KernelWork work(finalBlock, intermediate_digest, PGP_v4_packet, n, d, p, q, u); 
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
    std::cout << "\n" << OUTPUT << " Interrupt signal received.\n";

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