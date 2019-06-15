#include <string>

// General util
bool charIsIn(std::string str, char c);
bool isVowel(char c);
bool replace(std::string& str, const std::string& from, const std::string& to);

// Match Rating Util
std::string removeDoubleConst(std::string word);
std::string reduce_code(std::string word);
int calculate_minimum_rating(int combined_len);

std::string match_rating_encode(std::string word);
bool match_rating_similar(std::string word1, std::string word2);

