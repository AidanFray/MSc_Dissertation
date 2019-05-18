#include <string>
#include <vector>

#ifndef DOUBLE_METAPHONE__H
#define DOUBLE_METAPHONE__H

void MakeUpper(std::string &s);
int IsVowel(std::string &s, unsigned int pos);
int SlavoGermanic(std::string &s);
char GetAt(std::string &s, unsigned int pos);
void SetAt(std::string &s, unsigned int pos, char c);
int StringAt(std::string &s, unsigned int start, unsigned int length, ...);

std::string DoubleMetaphone(const std::string &str);

bool metaphone_similar(std::string word1, std::string word2);

#endif /* DOUBLE_METAPHONE__H */
