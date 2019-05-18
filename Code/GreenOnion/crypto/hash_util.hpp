#include <stdint.h>  // for uint32_t
#include <string>    // for string
#include <vector>    // for vector

std::string pad_hex_string_for_sha1(std::string hexString);
std::vector<std::string> split_hex_to_blocks(std::string hexString, int blockSizeInBytes);
void hex_block_to_words(uint32_t* W, std::string hexString);
void hash_blocks(std::vector<std::string> hex_blocks, uint32_t* digest, int num_of_blocks);
void hash_string(std::string input, uint32_t* digest);