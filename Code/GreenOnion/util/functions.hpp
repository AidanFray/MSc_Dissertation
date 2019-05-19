#include <sys/types.h>  // for uint
#include <string>       // for string
#include <vector>       // for vector

void pad(std::string &inputString, size_t minimumLength, char paddingChar);
void sleep(int milliseconds);
void split(std::vector<std::string> &result, std::string str, char delim);
std::string key_from_exponent_and_base_packet(std::string basePacket, std::string exponent);
void print_hash(uint* hash, int blockLength);
std::string split_string_with_newline_sep(std::string inputString, int lineLength);
long sum_all_bytes_in_a_hex_string(std::string hexString);