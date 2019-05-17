#include <string>

// Hex
std::string unsigned_integer_to_hex(uint integer);
std::string integer_to_hex(int integer);
uint hex_to_integer(std::string hexString);
unsigned long hex_to_64bit_integer(std::string hexString);
std::string hex_to_binary(std::string hexString);
std::string binary_strip_left_zeros(std::string binaryString);
std::string hex_string_to_mpi(std::string hexString);

std::string sha_digest_to_string(uint *digest, int len);