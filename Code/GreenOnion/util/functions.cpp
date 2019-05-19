#include <math.h>                                   // for ceil
#include <string.h>                                 // for size_t
#include <sys/types.h>                              // for uint
#include <chrono>                                   // for milliseconds
#include <iostream>                                 // for basic_istream, cout
#include <string>                                   // for string, operator+
#include <thread>                                   // for sleep_for
#include <vector>                                   // for vector
#include <sstream>                                  // for sstream
#include "../cppcodec/cppcodec/base64_rfc4648.hpp"  // for base64_rfc4648
#include "../cppcodec/cppcodec/hex_upper.hpp"       // for hex_upper
#include "conversion.hpp"                           // for hex_to_integer

using base64 = cppcodec::base64_rfc4648;
using hex = cppcodec::hex_upper;

/*
    Pads a string to a certain length
*/
void pad(std::string &inputString, size_t minimumLength, char paddingChar)
{
    while (inputString.length() < minimumLength)
    {
        inputString = paddingChar + inputString;
    }
}

/*
    Encapsulation for this_thread::sleep_for
*/
void sleep(int milliseconds)
{
    std::this_thread::sleep_for(std::chrono::milliseconds(milliseconds));
}

/*
    Splits a string with a certain delimiter
*/
void split(std::vector<std::string> &result, std::string str, char delim)
{
    std::stringstream ss(str);
    std::string token;
    while (std::getline(ss, token, delim)) {
        result.push_back(token);
    }
}

/*
    Method used to recreate the fingerprint packet of a hashed key
*/
std::string key_from_exponent_and_base_packet(std::string basePacket, std::string exponent)
{
    std::string keyPacket = basePacket.substr(0, basePacket.length() - 8);

    //Pads exponent
    pad(exponent, 8, '0');

    std::string newPacket = keyPacket + exponent;

    return newPacket;
}

/*
    Function used to print arrays containing hashes
*/
void print_hash(uint* hash, int blockLength)
{
    for(size_t i = 0; i < blockLength; ++i)
    {
        std::string hexString = integer_to_hex(hash[i]);

        //Pads the string
        pad(hexString, 8, '0');
        std::cout << hexString;
    }
    std::cout << std::endl;
}

/*
    TODO
*/
std::string split_string_with_newline_sep(std::string inputString, int lineLength)
{
    std::string outputString = "";

    for (size_t i = 0; i < ceil(inputString.length() / 64) + 1; i++)
    {
        int start_pos = i * lineLength;
        int end_pos = start_pos + lineLength;

        // Caps the value
        if (end_pos >= inputString.length())
        {
            end_pos = inputString.length();
        }

        outputString += inputString.substr(start_pos, (end_pos - start_pos));
        outputString += "\n";
    }
    
    return outputString;
}

/*
    TODO
*/
long sum_all_bytes_in_a_hex_string(std::string hexString)
{
    long total = 0;
    for (size_t i = 0; i < hexString.length(); i += 2)
    {
        total += hex_to_integer(hexString.substr(i, 2));
    }
    return total;
}