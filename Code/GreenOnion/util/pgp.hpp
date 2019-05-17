#include <string>

#include "kernel_work.hpp"

void generate_rsa_key(
                        std::string &str_n,
                        std::string &str_e, 
                        std::string &str_d, 
                        std::string &str_p, 
                        std::string &str_q, 
                        std::string &str_u,  
                        int key_length, 
                        int exponent
                     );

std::string create_pgp_v4_fingerprint_packet(std::string n, std::string e, int timestamp);
std::string create_pgp_secret_key_packet(std::string publicKeyPacket, std::string d, std::string p, std::string q, std::string u);

std::string create_pgp_header(int tagNumber, int packetLength);

std::string get_private_key_pgp_armor(std::string secretKeyPacket);
std::string get_public_key_pgp_armor(std::string v4fingerprintPacket);

void sha1_hash_all_but_final_block_of_pgp_packet(uint *finalBlock, uint *digest, std::string PGP_v4_packet);

void print_found_key(KernelWork work, std::string exponent);