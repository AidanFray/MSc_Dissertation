#include <string.h>
#include <sstream>
#include <bitset>
#include <vector>
#include <chrono>
#include <thread>


#include "conversion.cpp"
#include "kernel_work.cpp"

#include "../cppcodec/cppcodec/base64_rfc4648.hpp"
#include "../cppcodec/cppcodec/hex_upper.hpp"

using base64 = cppcodec::base64_rfc4648;
using hex = cppcodec::hex_upper;

/*
    Pads a string to a certain length
*/
void pad(std::string &inputString, int minimumLength, char paddingChar, bool leftPad = true)
{
    while (inputString.length() < minimumLength)
    {
        if (leftPad)    inputString = paddingChar + inputString;
        else            inputString = inputString + paddingChar;
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
    Prints the key in ascii PGP armour format
*/
std::string get_public_armour_pgp_key(std::string PGP_packet)
{
    auto bytes = hex::decode(PGP_packet);
    auto base64_PGP_packet = base64::encode(bytes);

    std::string public_key = ""; 

    public_key += "-----BEGIN PGP PUBLIC KEY BLOCK-----\n\n";
    public_key += base64_PGP_packet + "\n";
    public_key += "=\n"; //Adds a dud Cyclic Redundancy Check
    public_key += "-----END PGP PUBLIC KEY BLOCK-----\n";

    return public_key;
}

/*
    Prints important parts of the key when a match is found
*/
void print_found_key(KernelWork work, std::string exponent)
{
    std::cout << "\nWe've got one!!" << std::endl;
    std::string PGP_packet = key_from_exponent_and_base_packet(work.PGP_Packet, exponent);
    std::string armour_key = get_public_armour_pgp_key(PGP_packet);

    std::cout << "##################################################### " << std::endl;
    std::cout << "Public Key                                            " << std::endl;
    std::cout << armour_key <<std::endl;
    std::cout << "Private Key                                           " << std::endl;
    std::cout << work.Private_Key + "\n"                                  << std::endl;
    //Runs it through gpg
    std::string command = "echo \"" + armour_key + "\" | gpg --list-packets -v";
    std::system(command.c_str());
    std::cout << std::endl;
    std::cout << "##################################################### " << "\n\n";
}