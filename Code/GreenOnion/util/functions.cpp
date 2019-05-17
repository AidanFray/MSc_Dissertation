#include <string.h>
#include <sstream>
#include <bitset>
#include <vector>
#include <chrono>
#include <thread>
#include <iostream>

#include "../cppcodec/cppcodec/base64_rfc4648.hpp"
#include "../cppcodec/cppcodec/hex_upper.hpp"
#include "conversion.hpp"

using base64 = cppcodec::base64_rfc4648;
using hex = cppcodec::hex_upper;

/*
    Pads a string to a certain length
*/
void pad(std::string &inputString, int minimumLength, char paddingChar)
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