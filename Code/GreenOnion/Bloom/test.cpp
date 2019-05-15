#include "BloomFilter.cpp"

int main()
{
    BloomFilter bf(100, 1);

    long x = 0xffffffffffffffff;
    auto l = hash(x);

    return 0;
}