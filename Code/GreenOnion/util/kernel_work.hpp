#include <iostream>

#ifndef KernelWork_H
#define KernelWork_H

/*
    Struct that is used to hold to work for OpenCL
*/
class KernelWork
{
    public:
        uint FinalBlock[16];
        uint CurrentHash[5];
        std::string m_fingerprintPacket;

        // RSA key elements
        std::string m_n;
        std::string m_d;
        std::string m_p;
        std::string m_q;
        std::string m_u;

    KernelWork(uint[16], uint[5], std::string, std::string, std::string, std::string, std::string, std::string);
    KernelWork();
};

#endif