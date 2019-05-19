#include <math.h>           // for log, abs, round
#include "MurmurHash3.h"    // for MurmurHash3_x86_32
#include "BloomFilter.hpp"

// The odds of occurrence that a match will appear
// this is to keep to to about one FP per 100 loops
static double p = 1e-10;

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

long calculate_bloom_size(long n)
{
    return ceil((n * log(p)) / log(1 / pow(2, log(2))));
}

uint calculate_number_of_hashes(long n, long m)
{
    // Division by 2 dues to the split nature of
    // the way the hash is added to the bloom filter
    return round((m / n) * log(2));  
}