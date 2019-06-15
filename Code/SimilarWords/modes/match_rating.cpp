#include <vector>
#include <string>
#include <iostream>
#include <algorithm>

auto VOWELS = {'A', 'E', 'I', 'O', 'U'};

/* 
  Reverses a string parameter
*/
void reverseStr(std::string& str) 
{ 
    int n = str.length(); 
  
    // Swap character starting from two 
    // corners 
    for (int i = 0; i < n / 2; i++) 
    {
        std::swap(str[i], str[n - i - 1]); 
    }
} 

/*
    TODO
 */
std::string removeCharAtIndex(std::string inputString, int index)
{
    return inputString.substr(0, index) + inputString.substr(index + 1, inputString.length() - index);
}


/*
    Returns true if a char exists in a string
 */
int indexOfChar(std::string str, char c)
{
    for (size_t i = 0; i < str.length(); i++)
    {
        if (c == str[i]) return i;
    }

    return -1;
}

/*
    Returns true if a passed character is a vowel
 */
bool isVowel(char c)
{
    for(char v : VOWELS)
    {
        if (v == c) return true;        
    }
    return false;
}

/*
    Replaces a substring present in a string variable
 */
// https://stackoverflow.com/questions/3418231/replace-part-of-a-string-with-another-string
bool replace(std::string& str, const std::string& from, const std::string& to) 
{
    size_t start_pos = str.find(from);
    if(start_pos == std::string::npos)
        return false;
    str.replace(start_pos, from.length(), to);
    return true;
}

/*
    Remove any occuring chars from a string regardless of position
 */
void remove_matching_chars(std::string &large, std::string &small)
{
    int i = 0;
    while (i < large.length())
    {
        bool found = false;

        auto pos = indexOfChar(small, large[i]);

        if (pos != -1)
        {
            small = removeCharAtIndex(small, pos);
            large = removeCharAtIndex(large, i);
            found = true;
        }

        if(!found) i++;
    }
}

/*
    Remove chars that line up with each other in positions in the string
 */
void remove_exactly_matching_chars(std::string &large, std::string &small)
{
    int i = 0;
    while (i < small.length())
    {
        bool found = false;
        if (small[i] == large[i])
        {
            large = removeCharAtIndex(large, i);
            small = removeCharAtIndex(small, i);
            found = true;
        }

        if (!found) i++;
    }
}


/*
    Reduces double consanants down to a single char
 */
std::string removeDoubleConst(std::string word)
{
    // A
    replace(word, "BB", "B");
    replace(word, "CC", "C");
    replace(word, "DD", "D");
    // E
    replace(word, "FF", "F");
    replace(word, "GG", "G");
    replace(word, "HH", "H");
    // I
    replace(word, "JJ", "J");
    replace(word, "KK", "K");
    replace(word, "LL", "L");
    replace(word, "MM", "M");
    replace(word, "NN", "N");
    // O
    replace(word, "PP", "P");
    replace(word, "QQ", "Q");
    replace(word, "RR", "R");
    replace(word, "SS", "S");
    replace(word, "TT", "T");
    // U
    replace(word, "VV", "V");
    replace(word, "WW", "W");
    replace(word, "XX", "X");
    replace(word, "YY", "Y");
    replace(word, "ZZ", "Z");

    return word;
}

/*
    Using match code rules, codes biggers then 6 chars are reduced down
    by taking 3 chars at the start and end
 */
std::string reduce_code(std::string word)
{
    return word.substr(0, 3) + word.substr(word.length() - 3, 3);;
}

/*
    Calculates the minimum of the code pair
 */
int calculate_minimum_rating(int combined_len)
{
    if (combined_len <= 4)  return 5;
    if (combined_len <= 7)  return 4;
    if (combined_len <= 11) return 3;
    if (combined_len == 12) return 2;

    throw "Error: Invalid values passed to calculate_minimum_rating()";
}

/*
    Encodes a string using the Match Rating Algorithm
 */
std::string match_rating_encode(std::string word)
{
    std::transform(word.begin(), word.end(), word.begin(), ::toupper);

    // #1. Delete all vowels unless it starts the word
    std::string encoding = "";
    encoding += char(word[0]);
    for (size_t i = 1; i < word.size(); i++)
    {
        if (!isVowel(word[i])) encoding += word[i];        
    }
    
    // #2. Remove the second consonant of any double consonants present
    encoding = removeDoubleConst(encoding);

    // #3. Reduce codex to 6 letters by joining the first 3 and last 3 letters only 
    if (encoding.length() > 6)
    {
        encoding = reduce_code(encoding);
    }

    return encoding;
}

/*
    Determines if two words are similar
 */
bool match_rating_similar(std::string word1, std::string word2)
{
    auto code1 = match_rating_encode(word1);
    auto code2 = match_rating_encode(word2);

    // 1. If the length difference between the encoded strings is 3 or 
    // greater, then no similarity comparison is done.
    auto length_diff = abs(code1.length() - code2.length());
    if (length_diff >= 3) return false;

    // 2. Obtain the minimum rating value by calculating the length sum of the 
    // encoded strings and using below given Minimum Rating Table
    auto length_sum = code1.length() + code2.length();
    auto min_rating = calculate_minimum_rating(length_sum);

    // 3. Process the encoded strings from left to right and remove any identical 
    // characters found from both strings respectively.
    std::string large = code1;
    std::string small = code2;
    if (code1.length() < code2.length()) 
    {
        large = code2;
        small = code1;
    }
    // remove_matching_chars(large, small);
    remove_exactly_matching_chars(large, small);
    
    // 4. Process the unmatched characters from right to left and remove 
    // any identical characters found from both names respectively.
    reverseStr(large);
    reverseStr(small);
    // remove_matching_chars(large, small);
    remove_exactly_matching_chars(large, small);

    // 5. Subtract the number of unmatched characters from 6 in the longer string. 
    // This is the similarity rating.
    int similarity;
    if(large.length() > small.length()) similarity = 6 - large.length();
    else                                similarity = 6 - small.length();

    // 6. If the similarity rating equal to or greater than the minimum rating 
    // then the match is considered good.
    return similarity >= min_rating;
}