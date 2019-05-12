#include <iostream>
#include <stdlib.h>
#include <map>
#include <vector>
#include <sstream>
#include <fstream>

int DIFFERENCE_TOLERANCE = 1;

std::string inputFileName = "";
std::string outputFileName = "";
std::map<std::string, std::vector<std::string>> similarWords;

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
    Compares each word using it's levistien distance
*/
void find_similar_words(std::vector<std::string> words)
{
    int loop = 0;
    for (std::string word_y : words)
    {
        std::string word_x;
        for (size_t i = 0; i < words.size(); i++)
        {
            word_x = words[i];

             // Makes sure the same words aren't checked
            if (word_y != word_x)
            {
                int diff = lev_distance(word_y, word_x);

                if (diff <= DIFFERENCE_TOLERANCE)
                {
                    // Not found in dictionary
                    if (similarWords.count(word_y) == 0)
                    {

                        std::vector<std::string> sim_words;
                        sim_words.push_back(word_x);

                        similarWords.insert(
                            std::pair
                            <
                                std::string, 
                                std::vector<std::string>
                            >
                            (word_y, sim_words));
                    }
                    // Found in dictionary
                    else
                    {   
                        similarWords[word_y].push_back(word_x);
                    }
                }
            }
        }
        std::cout << "[*] Line: " << loop << "/" << words.size() << "\r" << std::flush;
        loop++;
    }
}

/*
    Saves the similar words to a specified file
*/
void save_similar_words_to_file()
{
    std::ofstream outFile (outputFileName);

    for (std::pair<std::string, std::vector<std::string>> wordPair : similarWords)
    {
        auto word = wordPair.first;
        auto simWords = wordPair.second;

        outFile << word << ",";

        for (std::string simWord : simWords)
        {
            outFile << simWord << ",";
        }
        outFile << "\n";
    }

    outFile.close(); 
}

/*
    Loads a CSV file and splits values
*/
std::vector<std::string> load_CSV(std::string filePath)
{

    std::ifstream input(filePath);

    std::string line;
    std::vector<std::string> words;
    for( std::string line; getline(input, line); )
    {
        words.push_back(line);
    }

    return words;
}

int main(int argc, char *argv[])
{
    if ( argc != 3)
    {
        std::cout << "Usage: ./a.out <IN_WORDLIST_PATH> <OUT_WORDLIST_PATH>" << std::endl;
        exit(0);
    }

    // Sets the args
    inputFileName = argv[1];
    outputFileName = argv[2];

    int loop = 0;
    auto words = load_CSV(inputFileName);

    if (words.empty())
    {
        std::cout << "[!] No words loaded!" << std::endl;
        exit(0);
    }

    find_similar_words(words);
    save_similar_words_to_file();
}