#include <CL/cl.hpp>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>

#include <openssl/rsa.h>
#include <openssl/rand.h>
#include <openssl/pem.h>

#include "OpenCLHelper.cpp"

void print_hash(uint* hash)
{
    // Prints out the hash
    std::cout << std::hex << hash[0];
    std::cout << std::hex << hash[1];
    std::cout << std::hex << hash[2];
    std::cout << std::hex << hash[3];
    std::cout << std::hex << hash[4];
    std::cout << std::endl;
}

void sha1_test()
{
    auto platform = GetPlatform();
    auto devices = GetAllDevices(platform);
    auto device = devices.front();

    cl::Context context(devices);

    auto program = BuildProgram("./OpenCL/SHA1.cl", context);

    // 160 bit
    uint hash[5];

    cl::Buffer valueBuf(context, CL_MEM_READ_WRITE | CL_MEM_HOST_READ_ONLY, sizeof(hash));

    cl::Kernel kernel(program, "shaTest");
    kernel.setArg(0, valueBuf);

    cl::CommandQueue queue(context, device);
    queue.enqueueTask(kernel);
    queue.enqueueReadBuffer(valueBuf, CL_TRUE, 0, sizeof(hash), hash);

    print_hash(hash);
}

void seed_prng()
{
      time_t rawtime;
      struct tm* timeinfo;

      time(&rawtime);
      timeinfo = localtime(&rawtime);
      RAND_seed(asctime(timeinfo), 4);
}

std::string rsa_key_to_pgp(std::string n, std::string e)
{
    //Why is the n for a 1024 key 100 characters long????
    int totalLen = n.size() + e.size();

    std::string result = "";

    // Magic byte
    result += "99";

    //Version number
    result += "04";

    //Timestamp, blank because it will be incremented later
    result += "00000000";

    std::ostringstream streamHex;
    streamHex << std::hex << totalLen;
    std::string hexLength = streamHex.str();

    //Pads values of length
    while (hexLength.length() != 4)
    {
        hexLength = "0" + hexLength;
    }

    //Adds the modulus and exponent key
    result += n + e;

    return result;
}

void create_work()
{
    // Generate Key
    seed_prng();
    RSA *r = RSA_generate_key(1024, 3, NULL, NULL);

    const BIGNUM *n, *e, *d;
    
    RSA_get0_key(r, &n, &e, &d);

    std::string str_n = BN_bn2hex(n);
    std::string str_e = BN_bn2hex(e);

    //Creates the PGP v4 fingerprint packet
    std::string PGP_v4_packet = rsa_key_to_pgp(str_n, str_e);
    std::cout << PGP_v4_packet << std::endl; 

    //TODO: Create PGPv4 signature packet

    //TODO: Hash all but the last block? Better way to do this?

    //TODO: Upload the values to OpenCL

    //TODO: Strech the key out using timestamp and exponent

    //TODO: Add inputs to the kernel
}

void compute()
{
    int workSize = 0;
    int workGroupSize = 0;
    int createWorkThreads = 0;

    //Inits OpenCL devices
    auto platform = GetPlatform();
    auto devices = GetAllDevices(platform);
    auto device = devices.front();

    cl::Context context(devices);

    auto program = BuildProgram("./OpenCL/SHA1.cl", context);

    workGroupSize = device.getInfo<CL_DEVICE_MAX_WORK_GROUP_SIZE>();
    std::cout << "[*] Work Group size set to: " << workGroupSize << std::endl;

    //Kernel and parameter creation
    cl::Kernel kernel(program, "optimized");

    int num_exps = 1;
    uint* LastWs = new uint[num_exps * 16];
    uint* Midstates = new uint[num_exps * 5];
    int* ExpIndexes = new int[num_exps];
    uint* Results = new uint[128];

    cl::Buffer bufLastWs(context, CL_MEM_READ_ONLY | CL_MEM_HOST_READ_ONLY, sizeof(LastWs));
    cl::Buffer bufMidstates(context, CL_MEM_READ_ONLY | CL_MEM_HOST_READ_ONLY, sizeof(Midstates));
    cl::Buffer bufExpIndexes(context, CL_MEM_READ_ONLY | CL_MEM_HOST_READ_ONLY, sizeof(ExpIndexes));
    cl::Buffer bufResults(context, CL_MEM_READ_WRITE | CL_MEM_HOST_READ_ONLY, sizeof(Results));

    //TODO: Create pattern buffers

    //TODO: Assign arguments to the kernel

    //TODO: Start create work threads

    //TODO: Loop around each result for OpenGL
}

int main()
{
    sha1_test();
    create_work();
    compute();
}