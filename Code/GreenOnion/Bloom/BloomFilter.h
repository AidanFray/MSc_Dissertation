#include <vector>
#include <cstdint> 

class BloomFilter {
public:
  BloomFilter(unsigned long size, short numHashes);

  void add(unsigned long value);
  bool possiblyContains(unsigned long value) const;

  uint8_t m_numHashes;
  std::vector<bool> m_bits;
};