#include <sstream>
#include <vector>

/*
    Adds SHA-1 padding to a hex string
*/
std::string pad_hex_string_for_sha1(std::string hexString)
{
    size_t orig_size = hexString.size();

    hexString += "80";

    // Division by 2 because 2 character make a byte
    // in the hex string
    while ((hexString.size() / 2) % 64 < 56)
    {
        hexString += "00";
    }

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

    for(size_t i = 0; i < 16; i++)
    {
        //Converts hex to integer
        std::stringstream ss;
        ss << std::hex << hexWords[i];
        ss >> W[i];
    }
}