#include <bitset>       // for bitset
#include <sstream>      // for hex, ostringstream, stringstream, basic_ostream
#include <string>       // for string, operator+, operator<<, basic_string

/*
    UInt32 --> Hex
*/
std::string unsigned_integer_to_hex(uint integer)
{
    std::ostringstream streamHex;
    streamHex << std::hex << integer;
    std::string hexValue = streamHex.str();

    return hexValue;
}

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
    Converts a hex string to an 32-bit integer
*/
uint hex_to_integer(std::string hexString)
{
    std::stringstream ss;
    ss << std::hex << hexString;

    uint n;
    ss >> n;

    return n;
}

/*
    TODO
*/
unsigned long hex_to_64bit_integer(std::string hexString)
{
    std::stringstream ss;
    ss << std::hex << hexString;

    unsigned long n;
    ss >> n;

    return n;
}


/*
    Hex --> Binary
*/
std::string hex_to_binary(std::string hexString)
{
    
    int n = hex_to_integer(hexString);
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
    TODO
*/
std::string hex_strip_left_zeros(std::string hexString)
{
    while (hexString[0] == '0')
    {
        hexString = hexString.substr(1, hexString.length());
    }

    return hexString;
}


/*
    Hex to multiprecision integer (MPI - RFC 4880)
*/
std::string hex_string_to_mpi(std::string hexString)
{


    // This method converts all but the most significant byte into binary and adds that to
    // the size of all hex char * 4
    //
    // This is because the MSB may have leading zeros when converted to binary

    auto msb = hex_to_binary(hexString.substr(0, 2));
    auto msb_stripped = binary_strip_left_zeros(msb);

    int binary_len = ((hexString.length() - 2) * 4) + msb_stripped.length();

    auto binary_string_len = integer_to_hex(binary_len);

    //Pads to 2 bytes
    while (binary_string_len.length() < 4) binary_string_len = "0" + binary_string_len;

    std::string output = binary_string_len + hexString;
    return output;
}

/*
    TODO
*/
std::string sha_digest_to_string(uint *digest, int len)
{
    std::string result;
    for (int i = 0; i < len; i++)
    {
        result += unsigned_integer_to_hex(digest[i]);
    }
    
    return result;
}
