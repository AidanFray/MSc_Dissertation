#include <array>

#include "BloomFilter.h"
#include "MurmurHash3.cpp"

BloomFilter::BloomFilter(unsigned long size, short numHashes): m_bits(size), m_numHashes(numHashes) 
{}

std::array<uint, 2> hash(unsigned long value) 
{
  uint leftSide = value >> 32;
  uint rightSide = (uint)value;

  std::array<uint, 2> hashValues;
  hashValues[0] = MurmurHash3_x86_32(&leftSide, sizeof(leftSide), 0);
  hashValues[1] = MurmurHash3_x86_32(&rightSide, sizeof(leftSide), 0);

  return hashValues;
}

long nthHash(uint8_t n, uint hashA, uint hashB, long filterSize) 
{
    return (hashA + n * hashB) % filterSize;
}

void BloomFilter::add(unsigned long value) 
{
  auto hashValues = hash(value);

  for (int n = 0; n < m_numHashes; n++) {

      auto pos = nthHash(n, hashValues[0], hashValues[1], m_bits.size());
      m_bits[pos] = true;
  }
}

bool BloomFilter::possiblyContains(unsigned long value) const 
{
  auto hashValues = hash(value);

  for (int n = 0; n < m_numHashes; n++) {

      auto d = nthHash(n, hashValues[0], hashValues[1], m_bits.size());

      if (!m_bits[d]) {
          return false;
      }
  }

  return true;
}