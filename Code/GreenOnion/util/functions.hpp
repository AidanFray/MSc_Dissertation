#include <string>
#include <vector>

void pad(std::string &inputString, int minimumLength, char paddingChar);
void sleep(int milliseconds);
void split(std::vector<std::string> &result, std::string str, char delim);
std::string key_from_exponent_and_base_packet(std::string basePacket, std::string exponent);
void print_hash(uint* hash, int blockLength);