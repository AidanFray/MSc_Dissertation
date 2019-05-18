#include <CL/cl.hpp>  // for Context (ptr only), Device (ptr only), Platform
#include <string>     // for string
#include <vector>     // for vector

const char *getErrorString(int error); 
void opencl_handle_error(int error, std::string name="");
std::vector<cl::Device> GetAllDevices(cl::Platform platform, bool printInfo);
cl::Platform GetPlatform();
cl::Program BuildProgram(const std::string& fileName, cl::Context context);