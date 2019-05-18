#include <cstdint>  // for uint8_t

#ifndef BloomFilter_H
#define BloomFilter_H

class BloomFilter {
public:
  BloomFilter(unsigned long size, short numHashes);

  void add(unsigned long value);

  uint8_t m_numHashes;
  unsigned long m_size;

  // Bloom filter bit vector
  bool *m_bits;
};

#endif

long calculate_bloom_size(long num_of_elements);