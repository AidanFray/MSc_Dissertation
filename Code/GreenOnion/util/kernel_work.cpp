#include <iostream>

#include "kernel_work.hpp"

KernelWork::KernelWork (uint finalBlock[16], uint currentHash[5], std::string packet, std::string privateKey)
{
    //Better way to do this?
    for(int i=0; i<5; ++i)
        CurrentHash[i] = currentHash[i];

    for(int i=0; i<16; ++i)
        FinalBlock[i] = finalBlock[i];

    PGP_Packet = packet;
    Private_Key = privateKey;
}

KernelWork::KernelWork() {}