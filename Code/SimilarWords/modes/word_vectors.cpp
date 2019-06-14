#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>

#include <iterator>
#include <algorithm>
#include <functional>
#include <math.h>
#include <cmath>
#include <numeric> 

#include "word_vectors.hpp"

/*
    Splits a string into a vector by a defined delminiter
 */
std::vector<std::string> split(std::string strToSplit, char delimeter)
{
    std::stringstream ss(strToSplit);
    std::string item;
    std::vector<std::string> splittedStrings;
    while (std::getline(ss, item, delimeter))
    {
    splittedStrings.push_back(item);
    }
    return splittedStrings;
}

/*
    Method to load the Word vectors for the .dat file
*/
std::map<std::string, std::vector<float>> WordVectors::load_word_vectors()
{
    //TODO: Sort out file path
    auto path = "data/word_vectors.dat";

    std::string line;
    std::ifstream myfile(path);
    while (getline(myfile, line) )
    {
        auto parts = split(line, ' ');

        // Separates all string values
        auto word = parts[0];
        auto vector_values_str = std::vector<std::string>(&parts[2], &parts[parts.size()]);

        std::vector<float> vector_values;

        // Converts all values to float
        for(std::string value_str : vector_values_str)
        {
            vector_values.push_back(atof(value_str.c_str()));
        }
        
        wordVectors[word] = vector_values;

    }
    myfile.close();

    if(wordVectors.size() == 0)
    {
        std::cout << "[!] No wordvectors loaded!" << std::endl;
        exit(0);
    }
}

/*
    Checks if a word is in the dictionary
 */
bool WordVectors::word_is_available(std::string word1)
{
    if (wordVectors.find(word1) == wordVectors.end() ) {
        return false;
    } else {
        return true;
    }
}


/*
    Computes the euclidian distance between two float vectors
 */
float WordVectors::distance(std::string word1, std::string word2)
{
    auto a = wordVectors[word1];
    auto b = wordVectors[word2];

    std::vector<double>	auxiliary;

    std::transform (a.begin(), a.end(), b.begin(), std::back_inserter(auxiliary),//
    [](float element1, float element2) {return pow((element1-element2),2);});

    return std::sqrt(std::accumulate(auxiliary.begin(), auxiliary.end(), 0.0));
} 

/*
    Calculates if two words are deemed as "similar"
 */
bool WordVectors::similar(std::string word1, std::string word2, float similarity)
{
    std::transform(word1.begin(), word1.end(), word1.begin(), ::toupper);
    std::transform(word2.begin(), word2.end(), word2.begin(), ::toupper);

    if (!word_is_available(word1) || !word_is_available(word2)) return false;

    //TODO: SEG_FAULT occuring here???
    auto dist = distance(word1, word2);
    if (dist < similarity) return true;

    return false;
}