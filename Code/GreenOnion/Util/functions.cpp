#include <string.h>
#include <sstream>

/*
    Method that converts a int32 to a hex string
*/
std::string integer_to_hex(int input)
{
    std::ostringstream streamHex;
    streamHex << std::hex << input;
    std::string hexValue = streamHex.str();

    return hexValue;
}

