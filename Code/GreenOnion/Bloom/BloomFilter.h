#include <vector>
#include <cstdint> 

class BloomFilter {
public:
  BloomFilter(unsigned long size, short numHashes);

  void add(unsigned long value);
  bool possiblyContains(unsigned long value) const;

  uint8_t m_numHashes;
  bool *m_bits;
  unsigned long m_size;
};