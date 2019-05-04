#include <CL/cl.hpp>

std::vector<cl::Device> GetAllDevices(cl::Platform platform)
{
    std::vector<cl::Device> devices;
    platform.getDevices(CL_DEVICE_TYPE_ALL, &devices);

    //Prints out first device
    auto device = devices.front();
    std::cout << "Vendor: " << device.getInfo<CL_DEVICE_VENDOR>() << std::endl;

    return devices;
}

cl::Platform GetPlatform()
{
    // Creates an obtains the platform
    std::vector<cl::Platform> platforms;
    cl::Platform::get(&platforms);
    auto platform = platforms.front();
    return platform;
}

cl::Program BuildProgram(const std::string& fileName, cl::Context context)
{
    std::ifstream file(fileName);
    std::string src(std::istreambuf_iterator<char>(file), (std::istreambuf_iterator<char>()));

    cl::Program::Sources sources(1, std::make_pair(src.c_str(), src.length() + 1));

    cl::Program program(context, sources);

    program.build();

    return program;
}