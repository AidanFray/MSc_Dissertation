#include "kernel_work.hpp"

KernelWork::KernelWork (
                            uint finalBlock[16],
                            uint currentHash[5],
                            std::string v4fingerprintPacket,
                            std::string n,
                            std::string d,
                            std::string p,
                            std::string q,
                            std::string u
                        )
{
    //Better way to do this?
    for(int i=0; i<5; ++i)
        CurrentHash[i] = currentHash[i];

    for(int i=0; i<16; ++i)
        FinalBlock[i] = finalBlock[i];

    m_fingerprintPacket = v4fingerprintPacket;
    m_n = n;
    m_d = d;
    m_p = p;
    m_q = q;
    m_u = u;
}

KernelWork::KernelWork() {}