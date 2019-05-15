#include <array>

#include "BloomFilter.h"
#include "MurmurHash3.cpp"

BloomFilter::BloomFilter(uint64_t size, uint8_t numHashes): m_bits(size), m_numHashes(numHashes) 
{}

std::array<uint64_t, 2> hash(long value) 
{
  std::array<uint64_t, 2> hashValue;
  MurmurHash3_x86_128(&value, sizeof(value), 0, hashValue.data());

  return hashValue;
}

inline uint64_t nthHash(uint8_t n, uint64_t hashA, uint64_t hashB, uint64_t filterSize) 
{
    return (hashA + n * hashB) % filterSize;
}

void BloomFilter::add(long value) 
{
  auto hashValues = hash(value);

  for (int n = 0; n < m_numHashes; n++) {
      m_bits[nthHash(n, hashValues[0], hashValues[1], m_bits.size())] = true;
  }
}

bool BloomFilter::possiblyContains(long value) const 
{
  auto hashValues = hash(value);

  for (int n = 0; n < m_numHashes; n++) {
      if (!m_bits[nthHash(n, hashValues[0], hashValues[1], m_bits.size())]) {
          return false;
      }
  }

  return true;
}