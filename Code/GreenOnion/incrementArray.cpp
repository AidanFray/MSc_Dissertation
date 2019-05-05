// Note: If program stats that <CL/cl.hpp> is missing you need to install 'opencl-headers'

// AMD
//  - opencl-mesa

// Intel
//  - intel-opencl-runtime

#include <CL/cl.hpp>
#include <iostream>
#include <fstream>
#include "OpenCLHelper.cpp"

int main()
{
    auto platform = GetPlatform();
    auto devices = GetAllDevices(platform, false);
    auto device = devices.front();

    cl::Context context(devices);

    auto program = BuildProgram("./OpenCL/ProcessArray.cl", context);

    std::vector<int> vec(1000);

    cl::Buffer inBuf(
        context, 
        CL_MEM_READ_ONLY | CL_MEM_HOST_NO_ACCESS | CL_MEM_COPY_HOST_PTR, 
        sizeof(int) * vec.size(),
        vec.data()
    );

    cl::Buffer outBuf(
        context,
        CL_MEM_WRITE_ONLY | CL_MEM_HOST_READ_ONLY,
        sizeof(int) * vec.size()
    );

    cl::Kernel kernel(program, "ProcessArray");
    kernel.setArg(0, inBuf);
    kernel.setArg(1, outBuf);

    cl::CommandQueue queue(context, device);

    queue.enqueueReadBuffer(outBuf, CL_FALSE, 0, sizeof(int) * vec.size(), vec.data());

    std::cout << "Output: " <<vec[100] << std::endl;
}

