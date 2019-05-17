#include <string>

#include "kernel_work.hpp"

std::string rsa_key_to_pgp(std::string n, std::string e, int timestamp);
void print_found_key(KernelWork work, std::string exponent);

std::string get_private_key_pgp_armor();
std::string get_public_key_pgp_armor(std::string PGP_packet);