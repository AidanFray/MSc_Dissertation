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
        std::string PGP_Packet;
        std::string Private_Key;

    KernelWork(uint[16], uint[5], std::string, std::string);
    KernelWork();
};

#endif