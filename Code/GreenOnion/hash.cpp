#include <CL/cl.hpp>
#include <fstream>
#include <iostream>
#include <iomanip>

#include "OpenCLHelper.cpp"

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

    // Prints out the hash
    std::cout << std::hex << hash[0];
    std::cout << std::hex << hash[1];
    std::cout << std::hex << hash[2];
    std::cout << std::hex << hash[3];
    std::cout << std::hex << hash[4];
    std::cout << std::endl;
}

int main()
{
    sha1_test();
}