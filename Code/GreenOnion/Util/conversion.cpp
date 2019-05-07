#include <string>
#include <sstream>
#include <bitset>

/*
    Int32 --> Hex
*/
std::string integer_to_hex(int integer)
{
    std::ostringstream streamHex;
    streamHex << std::hex << integer;
    std::string hexValue = streamHex.str();

    return hexValue;
}

/*
    Hex --> Binary
*/
std::string hex_to_binary(std::string hexString)
{
    std::stringstream ss;
    ss << std::hex << hexString;

    int n;
    ss >> n;
    std::bitset<32> b(n);

    return b.to_string();
}

/*
    Strips the left most zeros from a binary value
*/
std::string binary_strip_left_zeros(std::string binaryString)
{
    //Strips left zeros
    std::string output;
    int endIndex = 0;

    for(size_t i = 0; i < binaryString.length(); ++i)
    {
        // 0x31 == "1" in ASCII hex
        if (binaryString[i] == 0x31) {

            //Takes the values after the leading zeros
            output = binaryString.substr(endIndex, binaryString.length() - endIndex);
            break;
        }

        endIndex++;
    }

    return output;
}

/*
    Hex to multiprecision integer (MPI - RFC 4880)
*/
std::string hex_string_to_mpi(std::string hexString)
{
    auto binary_string = hex_to_binary(hexString);
    auto stripped_binary_string = binary_strip_left_zeros(binary_string);
    auto binary_string_len = integer_to_hex(stripped_binary_string.length());

    //Pads to 2 bytes
    while (binary_string_len.length() < 4) binary_string_len = "0" + binary_string_len;

    std::string output = binary_string_len + hexString;
    return output;
}