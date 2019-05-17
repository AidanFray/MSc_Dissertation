#include <string>

#include "kernel_work.hpp"

void generate_rsa_key(std::string &str_n, std::string &str_e, std::string &str_d, int key_length, int exponent);

std::string rsa_key_to_pgp(std::string n, std::string e, int timestamp);
std::string get_private_key_pgp_armor();
std::string get_public_key_pgp_armor(std::string PGP_packet);

void sha1_hash_all_but_final_block_of_pgp_packet(uint *finalBlock, uint *digest, std::string PGP_v4_packet);

void print_found_key(KernelWork work, std::string exponent);
