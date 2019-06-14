#include <algorithm>
#include <functional>
#include <string>
#include <cctype>
#include <iostream>

using namespace std;

char f_transform(char c);
string soundex(const string &s);

bool soundex_similar(std::string word1, std::string word2);