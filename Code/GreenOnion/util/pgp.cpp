#include <openssl/ossl_typ.h>                       // for BIGNUM, BN_CTX, RSA
#include <openssl/rsa.h>                            // for RSA_generate_key
#include <openssl/bn.h>                             // for BN_bn2hex, BN_CTX...
#include <sys/types.h>                              // for uint
#include <iostream>                                 // for endl, operator<<
#include <cstdlib>                                  // for system, NULL
#include <bitset>                                   // for bitset
#include <string>                                   // for string, allocator
#include <vector>                                   // for vector

#include "../cppcodec/cppcodec/base64_rfc4648.hpp"  // for base64_rfc4648
#include "../cppcodec/cppcodec/hex_upper.hpp"       // for hex_upper
#include "../crypto/hash_util.hpp"                  // for hash_blocks, hex_...
#include "kernel_work.hpp"                          // for KernelWork
#include "conversion.hpp"                           // for hex_string_to_mpi
#include "functions.hpp"                            // for pad, split_string...

using base64 = cppcodec::base64_rfc4648;
using hex = cppcodec::hex_upper;

//NOTE:
// Keys can be imported using
//
//      cat public .key | gpg --import --allow-non-selfsigned-uid


//Hex for "John Doe <change_me@email.com>"
static std::string ID_PACKET_STRING = "4a6f686e20446f65203c6368616e67655f6d6540656d61696c2e636f6d3e";

/*
    TODO
*/
std::string wrap_in_pgp_header(int tagNumber, std::string packetContent)
{
    // string representation of binary
    std::string header = "";

    // CTB indicator bit
    header += "1";

    // New packet format
    header += "0";

    // Packet tag
    header += std::bitset<4>(tagNumber).to_string();

    header += "01";

    auto header_integer = std::bitset<8>(header);
    auto header_hex = integer_to_hex((int)header_integer.to_ulong());
    pad(header_hex, 2, '0');

    // +1 is for the 04 about to be added to the header
    auto packet_len_hex = integer_to_hex(packetContent.length() / 2);

    pad(packet_len_hex, 4, '0');
    header_hex += packet_len_hex;

    //Wraps the header around the content
    header_hex += packetContent;

    return header_hex;
}

/*
    TODO
*/
std::string create_pgp_secret_key_checksum(std::string hexString)
{
    //TODO: Checksums are not being validated properly
    //
    // The RFC states:
    //
    //         "The two-octet checksum that follows the algorithm-specific portion is
    //          the algebraic sum, mod 65536, of the plaintext of all the algorithm-
    //          specific octets (including MPI prefix and data)."


    long total = 0;

    total += sum_all_bytes_in_a_hex_string(hexString);

    int total_int = (int)(total % 65536);

    auto checksum_hex = integer_to_hex(total_int);
    pad(checksum_hex, 4, '0');

    return checksum_hex;
}

/*
    Converts an RSA key to PGP public key packet defined in RFC 4880
*/
std::string create_pgp_v4_fingerprint_packet(std::string n, std::string e, int timestamp)
{   
    // ############################################################################ //
    //  Start   Length   Version  Timestamp   Algo(RSA)    MPI(n)    MPI(e)                                 
    //  0x99     XX       0x04      XXXX        0x01         X         X
    // ############################################################################ //

    // How many characters the packet length is
    int PACKET_LENGTH_CHARS = 4; 
    int TIMESTAMP_LENGTH_CHARS = 8;

    std::string result = "";

    //Version number
    result += "04";

    //Pads to 4 bytes
    std::string timestamp_string = integer_to_hex(timestamp);
    pad(timestamp_string, TIMESTAMP_LENGTH_CHARS, '0');

    result += timestamp_string;

    // Algo number
    result += "01";

    //MPI (N)
    result += hex_string_to_mpi(n);

    //MPI (e)
    result += hex_string_to_mpi(e);

    std::string public_packet_len = integer_to_hex(result.length() / 2);
    pad(public_packet_len, 4, '0');

    result = "99" + public_packet_len + result;

    return result;
}

/*
    TODO
*/
std::string create_pgp_secret_key_packet(std::string publicKeyPacket, std::string d, std::string p, std::string q, std::string u)
{
    std::string secret_key_packet = "";

    secret_key_packet += "04";

    // Adds the public key packet without the header
    secret_key_packet += publicKeyPacket.substr(8, publicKeyPacket.length());

    // No encryption
    secret_key_packet += "00";

    // MPI (d)
    auto mpi_d = hex_string_to_mpi(d);
    secret_key_packet += mpi_d;

    // MPI (p)
    auto mpi_p = hex_string_to_mpi(p);
    secret_key_packet += mpi_p;

    // MPI (q)
    auto mpi_q = hex_string_to_mpi(q);
    secret_key_packet += mpi_q;

    // MPI (u) [Multiplicative inverse of p, mod q]
    auto mpi_u = hex_string_to_mpi(u);
    secret_key_packet += mpi_u;

    //TODO : checksum - needs to be a sum of the algorithm specific bytes mod 65537
    std::string checksum_string = mpi_d + mpi_p + mpi_q + mpi_u;
    secret_key_packet += create_pgp_secret_key_checksum(checksum_string);

    //Finishes off the private key packet
    secret_key_packet = wrap_in_pgp_header(5, secret_key_packet);

    return secret_key_packet;
}

/*
    TODO
*/
std::string get_private_key_pgp_armor(std::string secretKeyPacket)
{
    auto bytes = hex::decode(secretKeyPacket);
    auto base64_PGP_packet = base64::encode(bytes);

    std::string public_key = ""; 

    public_key += "-----BEGIN PGP PRIVATE KEY BLOCK-----\n\n";
    public_key += split_string_with_newline_sep(base64_PGP_packet, 64);
    public_key += "=\n"; //Adds a dud Cyclic Redundancy Check
    public_key += "-----END PGP PRIVATE KEY BLOCK-----\n";

    return public_key;
}

/*
    Prints the key in ascii PGP armour format
*/
std::string get_public_key_pgp_armor(std::string v4fingerprintPacket)
{
    auto bytes = hex::decode(v4fingerprintPacket);
    std::string base64_PGP_packet = base64::encode(bytes);

    std::string public_key = ""; 

    public_key += "-----BEGIN PGP PUBLIC KEY BLOCK-----\n\n";
    public_key += split_string_with_newline_sep(base64_PGP_packet, 64);
    public_key += "=\n"; //Adds a dud Cyclic Redundancy Check
    public_key += "-----END PGP PUBLIC KEY BLOCK-----";

    return public_key;
}

/*
    TODO
*/
std::string get_user_id_packet()
{
    return wrap_in_pgp_header(13, ID_PACKET_STRING);
}

/*
    Generates an RSA key to be sent to the GPU
*/
void generate_rsa_key(
                        std::string &str_n, 
                        std::string &str_e, 
                        std::string &str_d, 
                        std::string &str_p, 
                        std::string &str_q, 
                        std::string &str_u,
                        int key_length, 
                        int exponent
                     )
{
    // Generate Key
    RSA *r = RSA_generate_key(key_length, exponent, NULL, NULL);
    
    const BIGNUM *n, *e, *d, *p, *q;
    BIGNUM *u = BN_new();

    RSA_get0_key(r, &n, &e, &d);
    RSA_get0_factors(r, &p, &q);

    BN_CTX *ctx = BN_CTX_new();
    BN_mod_inverse(u, p, q, ctx);

    //Converts public key sections to hex
    str_n = BN_bn2hex(n);
    str_e = BN_bn2hex(e);
    str_d = BN_bn2hex(d);
    str_p = BN_bn2hex(p);
    str_q = BN_bn2hex(q);
    str_u = BN_bn2hex(u);
}

/*
    Hashes all but the last block of the PGP packet
*/
void sha1_hash_all_but_final_block_of_pgp_packet(uint *finalBlock, uint *digest, std::string PGP_v4_packet)
{
    // Pads and splits it blocks
    std::string padded_v4 = pad_hex_string_for_sha1(PGP_v4_packet);
    auto hex_blocks = split_hex_to_blocks(padded_v4, 64);

    //Hashes all but the last block
    hash_blocks(hex_blocks, digest, hex_blocks.size() - 1);

    //Saves the final block
    hex_block_to_words(finalBlock, hex_blocks[hex_blocks.size() - 1]);
}

/*
    TODO
*/
void gpg_command_line(std::string publicArmorKey)
{
    //Runs it through gpg
    std::string command = "echo \"" + publicArmorKey + "\" | gpg --list-packets";
    std::system(command.c_str());
}

/*
    Prints important parts of the key when a match is found
*/
void print_found_key(KernelWork work, std::string exponent)
{
    std::cout << "\nWe've got one!!" << std::endl;

    // Public key
    std::string v4_fingerprint_packet = key_from_exponent_and_base_packet(work.m_fingerprintPacket, exponent);
    std::string v4_fingerprint_packet_with_user_id = v4_fingerprint_packet + get_user_id_packet();
    std::string public_armour_key = get_public_key_pgp_armor(v4_fingerprint_packet_with_user_id);

    // Private key
    std::string secret_key_packet = create_pgp_secret_key_packet(v4_fingerprint_packet, work.m_d, work.m_p, work.m_q, work.m_u);
    secret_key_packet += get_user_id_packet();
    std::string private_armor_key = get_private_key_pgp_armor(secret_key_packet);

    std::cout << "\n\n";
    // std::cout << public_armour_key                                        << std::endl;
    std::cout << private_armor_key                                        << std::endl;
    gpg_command_line(private_armor_key);
    std::cout                                                             << std::endl;
}