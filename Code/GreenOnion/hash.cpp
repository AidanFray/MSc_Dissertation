

#include <CL/cl.hpp>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>

#include <openssl/rsa.h>
#include <openssl/rand.h>
#include <openssl/pem.h>

#include "Crypto/sha1.hpp"
#include "OpenCLHelper.cpp"

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

    //Local string
    const std::string testStr = "Hello world!";

    LocalSHA1 checksum;
    checksum.update(testStr);
    const std::string localHash = checksum.final();

    std::cout << "Local:  " << localHash << std::endl << std::endl;
}

/*
Converts an RSA key to PGP fingerprint packet defined in RFC 4880
*/
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

/*
This method will be run on the CPU to generate work for OpenCL
*/
void create_work()
{
    // Generate Key
    RSA *r = RSA_generate_key(1024, 3, NULL, NULL);

    BIO *bio = BIO_new(BIO_s_mem());
    PEM_write_bio_RSAPublicKey(bio, r);

    int pem_pkey_size = BIO_pending(bio);
    char *pem_pkey = (char*) calloc((pem_pkey_size)+1, 1);
    BIO_read(bio, pem_pkey, pem_pkey_size);

    std::cout << pem_pkey << std::endl;

    const BIGNUM *n, *e, *d;
    
    RSA_get0_key(r, &n, &e, &d);

    std::string str_n = BN_bn2hex(n);
    std::string str_e = BN_bn2hex(e);

    //Creates the PGP v4 fingerprint packet
    std::string PGP_v4_packet = rsa_key_to_pgp(str_n, str_e);

    // Just here as an example
    if (RSA_check_key(r))
    {
        std::cout << "KEY VALID" << std::endl;
    }

    //TODO: Find a way to convert RSA to PGP key???

    //TODO: Hash all but the last block? Better way to do this?

    //TODO: Upload the values to OpenCL

    //TODO: Strech the key out using timestamp and exponent

    //TODO: Add inputs to the kernel
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