#include <string>
#include <math.h>

int DIFFERENCE_TOLERANCE = 1;

/*
    Calculates the levistien distance of two words
*/
int lev_distance(std::string word1, std::string word2)
{
    int diff = 0;

    int len_diff = word1.length() - word2.length();
    len_diff = std::abs(len_diff);

    //Deals with different length strings
    int min_len = 0;
    std::string min_word, max_word;
    if (word1.length() > word2.length())
    {
        min_len = word2.length();
        min_word = word1;
        max_word = word2;
    }
    else
    {
        min_len = word1.length();
        min_word = word2;
        max_word = word1;
    }
        
    for (size_t i = 0; i < min_len; i++)
    {
        if (min_word[i] != max_word[i])
        {
            diff += 1;
        }
    }

    // Adds on the remaining letters
    diff += len_diff;
    return diff;
        
}

/*
    Returns true if the two entered words are deemed similar
*/
bool levenshtein_similar(std::string word1, std::string word2)
{
    int diff = lev_distance(word1, word2);
    return diff <= DIFFERENCE_TOLERANCE;
}