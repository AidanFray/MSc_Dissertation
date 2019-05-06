#include <iostream>

/*
    Struct that is used to hold to work for OpenCL
*/
class KernelWork
{
    public:
        uint FinalBlock[32];
        uint CurrentHash[5];

    KernelWork(uint[32], uint[5]);
};

KernelWork::KernelWork (uint finalBlock[32], uint currentHash[5])
{
    //Better way to do this?
    for(int i=0; i<5; ++i)
        CurrentHash[i] = currentHash[i];

    for(int i=0; i<32; ++i)
        FinalBlock[i] = finalBlock[i];
}