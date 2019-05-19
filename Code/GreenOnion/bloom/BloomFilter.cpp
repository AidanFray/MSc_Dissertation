#include <math.h>         // for log, abs
#include "MurmurHash3.h"  // for MurmurHash3_x86_32
#include "BloomFilter.hpp"

BloomFilter::BloomFilter(unsigned long size, short numHashes): m_numHashes(numHashes) 
{
    m_bits = new bool[size] {false};
    m_size = size;
}

void BloomFilter::add(unsigned long value) 
{
    for (int n = 0; n < m_numHashes; n++) {

        uint32_t l_value = value >> 32;
        uint32_t r_value = (uint32_t)value;

        uint32_t l = MurmurHash3_x86_32(&l_value, sizeof(l_value), n) % m_size;
        m_bits[l] = true;

        uint32_t r = MurmurHash3_x86_32(&r_value, sizeof(r_value), n) % m_size;
        m_bits[r] = true;
    }
}

long calculate_bloom_size(long num_of_elements)
{
    //TODO : this can be altered
    // Currently: 1 in a trillion
    double probability = 1e-20;

    auto top = abs((num_of_elements * log(probability)));
    auto bottom = (log(2) * log(2));

    auto m =  (long)(top / bottom);

    return m;
}