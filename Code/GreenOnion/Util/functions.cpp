#include <string.h>
#include <sstream>
#include <bitset>

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

/*
TODO
*/
std::string hex_to_binary(std::string hex_value)
{
    std::stringstream ss;
    ss << std::hex << hex_value;

    int n;
    ss >> n;
    std::bitset<32> b(n);

    return b.to_string();
}

/*
TODO
*/
std::string binary_strip_left_zeros(std::string binary_string)
{
    //Strips left zeros
    std::string output;
    int endIndex = 0;

    for(size_t i = 0; i < binary_string.length(); i++)
    {
        // 0x31 == "1" in ASCII hex
        if (binary_string[i] == 0x31) {

            //Takes the values after the leading zeros
            output = binary_string.substr(endIndex, binary_string.length() - endIndex);
            break;
        }

        endIndex++;
    }

    return output;
}
