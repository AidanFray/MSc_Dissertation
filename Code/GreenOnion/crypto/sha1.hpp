#include <stddef.h>  // for size_t
#include <stdint.h>  // for uint32_t, uint64_t
#include <string>    // for string

#ifndef SHA1_H
#define SHA1_H

void reset(uint32_t digest[], std::string &buffer, uint64_t &transforms);
uint32_t rol(const uint32_t value, const size_t bits);
uint32_t blk(const uint32_t block[16], const size_t i);
void Round0(const uint32_t block[16], const uint32_t v, uint32_t &w, const uint32_t x, const uint32_t y, uint32_t &z, const size_t i);
void Round1(uint32_t block[16], const uint32_t v, uint32_t &w, const uint32_t x, const uint32_t y, uint32_t &z, const size_t i);
void Round2(uint32_t block[16], const uint32_t v, uint32_t &w, const uint32_t x, const uint32_t y, uint32_t &z, const size_t i);
void Round3(uint32_t block[16], const uint32_t v, uint32_t &w, const uint32_t x, const uint32_t y, uint32_t &z, const size_t i);
void Round4(uint32_t block[16], const uint32_t v, uint32_t &w, const uint32_t x, const uint32_t y, uint32_t &z, const size_t i);
void transform(uint32_t digest[5], uint32_t block[16]);

#endif
