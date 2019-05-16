#include <array>
#include <math.h> 

#include "BloomFilter.h"
#include "MurmurHash3.cpp"

BloomFilter::BloomFilter(unsigned long size, short numHashes): m_numHashes(numHashes) 
{
    m_bits = new bool[size] {false};
    m_size = size;
}

std::array<uint, 2> hash(unsigned long value) 
{
  uint leftSide = value >> 32;
  uint rightSide = (uint)value;

  std::array<uint, 2> hashValues;
  hashValues[0] = MurmurHash3_x86_32(&leftSide, sizeof(leftSide), 0);
  hashValues[1] = MurmurHash3_x86_32(&rightSide, sizeof(leftSide), 0);

  return hashValues;
}

long nthHash(uint8_t n, uint hashA, uint hashB, unsigned long filterSize) 
{
    return (hashA + n * hashB) % filterSize;
}

void calculate_bloom_size(long num_of_elements)
{
  //TODO : this can be altered
  float probability = 1/1000000000;

  auto top = ((num_of_elements * log(probability))) / (log(2) * log(2));
}


void BloomFilter::add(unsigned long value) 
{
  auto hashValues = hash(value);

  for (int n = 0; n < m_numHashes; n++) {

      auto pos = nthHash(n, hashValues[0], hashValues[1], m_size);
      m_bits[pos] = true;
  }
}

bool BloomFilter::possiblyContains(unsigned long value) const 
{
  auto hashValues = hash(value);

  for (int n = 0; n < m_numHashes; n++) {

      auto d = nthHash(n, hashValues[0], hashValues[1], m_size);

      if (!m_bits[d]) {
          return false;
      }
  }

  return true;
}