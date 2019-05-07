#include <iostream>

/*
    Struct that is used to hold to work for OpenCL
*/
class KernelWork
{
    public:
        uint FinalBlock[16];
        uint CurrentHash[5];
        std::string PGP_Packet;

    KernelWork(uint[16], uint[5], std::string);
    KernelWork();
};

KernelWork::KernelWork (uint finalBlock[16], uint currentHash[5], std::string packet)
{
    //Better way to do this?
    for(int i=0; i<5; ++i)
        CurrentHash[i] = currentHash[i];

    for(int i=0; i<16; ++i)
        FinalBlock[i] = finalBlock[i];

    PGP_Packet = packet;
}

KernelWork::KernelWork() {}