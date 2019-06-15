#include <string>
#include <boost/algorithm/string.hpp>

#define cc         *i
#define nc         *(i + 1)
#define nnc        *(i + 2)
#define pc          lastChar
#define NULLCHAR    (char)NULL

bool is(std::string x, char c);
char at(std::string x, int i);

std::string metaphone(std::string x);
bool metaphone_similar(std::string word1_metaphone, std::string word2);

