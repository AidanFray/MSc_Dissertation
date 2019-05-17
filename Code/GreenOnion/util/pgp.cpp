#include <string>

#include "conversion.hpp"
#include "functions.hpp"
#include "kernel_work.hpp"

#include "../cppcodec/cppcodec/base64_rfc4648.hpp"
#include "../cppcodec/cppcodec/hex_upper.hpp"

using base64 = cppcodec::base64_rfc4648;
using hex = cppcodec::hex_upper;

/*
    Converts an RSA key to PGP public key packet defined in RFC 4880
*/
std::string rsa_key_to_pgp(std::string n, std::string e, int timestamp)
{   
    //Structure 2024 key:
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
    result += "0800";
    result += n;

    //MPI (e)
    result += hex_string_to_mpi(e);

    //Encapsulates in a fingerprint packet
    std::string public_packet_len = integer_to_hex(result.length() / 2);
    pad(public_packet_len, 4, '0');

    result = "99" + public_packet_len + result;

    return result;
}

/*
    TODO
*/
void get_private_key_pgp_armor()
{
    // Public key packet

    // 0x00 (no encryption)

    // checksum

    // MPI (d)

    // MPI (p)

    // MPI (q)

    // MPI (u) [Multiplicative inverse of p, mod q]
}

/*
    Prints the key in ascii PGP armour format
*/
std::string get_public_key_pgp_armor(std::string PGP_packet)
{
    auto bytes = hex::decode(PGP_packet);
    auto base64_PGP_packet = base64::encode(bytes);

    std::string public_key = ""; 

    public_key += "-----BEGIN PGP PUBLIC KEY BLOCK-----\n\n";
    public_key += base64_PGP_packet + "\n";
    public_key += "=\n"; //Adds a dud Cyclic Redundancy Check
    public_key += "-----END PGP PUBLIC KEY BLOCK-----\n";

    return public_key;
}

/*
    Prints important parts of the key when a match is found
*/
void print_found_key(KernelWork work, std::string exponent)
{
    std::cout << "\nWe've got one!!" << std::endl;
    std::string PGP_packet = key_from_exponent_and_base_packet(work.PGP_Packet, exponent);
    std::string armour_key = get_public_key_pgp_armor(PGP_packet);

    std::cout << "##################################################### " << std::endl;
    std::cout << "Public Key                                            " << std::endl;
    std::cout << armour_key <<std::endl;
    std::cout << "Private Key                                           " << std::endl;
    std::cout << work.Private_Key + "\n"                                  << std::endl;
    //Runs it through gpg
    std::string command = "echo \"" + armour_key + "\" | gpg --list-packets -v";
    std::system(command.c_str());
    std::cout << std::endl;
    std::cout << "##################################################### " << "\n\n";
}