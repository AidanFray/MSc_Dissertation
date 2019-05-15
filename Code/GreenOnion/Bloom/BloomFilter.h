#include <vector>
#include <cstdint> 

class BloomFilter {
public:
  BloomFilter(uint64_t size, uint8_t numHashes);

  void add(long value);
  bool possiblyContains(long value) const;

  uint8_t m_numHashes;
  std::vector<bool> m_bits;
};