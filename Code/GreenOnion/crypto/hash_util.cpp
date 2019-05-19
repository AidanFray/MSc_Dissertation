#include <stddef.h>  // for size_t
#include <stdint.h>  // for uint32_t
#include <sstream>   // for stringstream, hex, basic_ostream, basic_ostream<...
#include <string>    // for string, operator+, operator<<
#include <vector>    // for vector
#include "sha1.hpp"  // for transform


/*
    Adds SHA-1 padding to a hex string
*/
std::string pad_hex_string_for_sha1(std::string hexString)
{
    //Size it bits
    size_t orig_size = hexString.size()* 4;

    hexString += "80";

    // Division by 2 due to hex
    while ((hexString.size() / 2) % 64 < 56) hexString += "00";

    // Length to hex
    std::stringstream stream;
    stream << std::hex << orig_size;
    std::string hexLength(stream.str());

    while (hexLength.length() != 16) 
    {
        hexLength = "0" + hexLength;
    }

    hexString += hexLength;

    return hexString;
}


/*
    Converts a hex string in a number of blocks
*/
std::vector<std::string> split_hex_to_blocks(std::string hexString, int blockSizeInBytes)
{
    //Needed because of hex
    blockSizeInBytes *= 2;

    std::vector<std::string> blocks;

    for(size_t i = 0; i < hexString.length(); i += blockSizeInBytes)
    {
        blocks.push_back(hexString.substr(i, blockSizeInBytes));
    }

    return blocks;
}


/*
    512 bit block to 16 x 32bit words
*/
void hex_block_to_words(uint32_t* W, std::string hexString)
{
    auto hexWords = split_hex_to_blocks(hexString, 4);

    for(size_t i = 0; i < 16; ++i)
    {
        //Converts hex to integer
        std::stringstream ss;
        ss << std::hex << hexWords[i];
        ss >> W[i];
    }
}

/*
    Function used to SHA-1 hash a number of blocks. 

    num_of_blocks
        This variable can be used to specify how many blocks are hashed. This can be 
        used to obtain an intermediate hash

    hex_blocks
        512 bit blocks that require hashing

    digest
        The result of the SHA-1 hash at any stage
*/
void hash_blocks(std::vector<std::string> hex_blocks, uint32_t* digest, int num_of_blocks)
{
    digest[0] = 0x67452301;
    digest[1] = 0xEFCDAB89;
    digest[2] = 0x98BADCFE;
    digest[3] = 0x10325476;
    digest[4] = 0xC3D2E1F0;
    // Full hash
    for(int i = 0; i < num_of_blocks; ++i)
    {
        uint32_t W[16];
        hex_block_to_words(W, hex_blocks[i]);
        transform(digest, W);
    }
}

void hash_string(std::string input, uint32_t* digest)
{
    std::string paddedInput = pad_hex_string_for_sha1(input);
    auto hex_blocks = split_hex_to_blocks(paddedInput, 64);
    hash_blocks(hex_blocks, digest, hex_blocks.size());
}