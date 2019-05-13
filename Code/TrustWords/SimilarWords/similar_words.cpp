#include <iostream>
#include <stdlib.h>
#include <map>
#include <vector>
#include <sstream>
#include <fstream>

#include "soundex.cpp"

int DIFFERENCE_TOLERANCE = 1;

std::string inputFileName = "";
std::string outputFileName = "";


// TODO: pass these as parameters
static bool LEV_DISTANCE = false;
static bool SOUNDEX = false;

std::string SOUNDEX_CLI_TAG = "-s";
std::string LEV_CLI_TAG = "-l";

/*
    Saves the similar words to a specified file
*/
void save_similar_words_to_file(ofstream &outFile, std::vector<std::string> sim_words)
{
    for (std::string word : sim_words)
    {
        outFile << word << ",";
    }

    outFile << "\n";
    outFile << std::flush;
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
    // ## Note ##
    // The format of saving to file after every word alongside a refresh of the vector is 
    // to solve the issue of the vector getting too large and causing my Linux OS to freeze
    // the I/O slows down the operation but now I'm not guessing if the input will be too big 

    std::vector<std::string> sim_words;
    std::ofstream outFile (outputFileName);

    int loop = 0;
    for (std::string word_y : words)
    {
        // Recreates the vector for this word_y
        sim_words.clear();
        sim_words.push_back(word_y);

        std::string wordY_soundex = soundex(word_y);
        
        for (std::string word_x : words)
        {
             // Makes sure the same words aren't checked
            if (word_y != word_x)
            {
                bool add_word = false;

                if (LEV_DISTANCE)
                {
                    int diff = lev_distance(word_y, word_x);
                    add_word = diff <= DIFFERENCE_TOLERANCE;
                        
                }
                else if (SOUNDEX)
                {
                    std::string wordX_soundex = soundex(word_x);
                    add_word = wordX_soundex == wordY_soundex;
                }

                // Adds the word to the dictionary  
                if (add_word)
                {
                    sim_words.push_back(word_x);
                    add_word = false;
                }
    
            }
        }
        std::cout << "[*] Line: " << loop << "/" << words.size() << "\r" << std::flush;
        loop++;

        // Saves the word to file
        save_similar_words_to_file(outFile, sim_words);
    }
    outFile.close();
}

/*
    Prints the usage for the script
*/
void usage()
{
    std::cout << "Usage: ./a.out <IN_WORDLIST_PATH> <OUT_WORDLIST_PATH> <MODE> [-s|-l]" << std::endl;
    exit(0);
}

/*
    TODO
*/
void parse_program_mode(std::string commandInput)
{
    if (commandInput == SOUNDEX_CLI_TAG)
    {
        SOUNDEX = true;
    }
    else if (commandInput == LEV_CLI_TAG)
    {
        LEV_DISTANCE = true;
    }
    else
    {
        std::cout << "[!] Error: Please select a mode!" << std::endl;
        usage();
    }
}

int main(int argc, char *argv[])
{
    if ( argc != 4)
    {
        usage();
    }

    // Sets the args
    inputFileName = argv[1];
    outputFileName = argv[2];
    std::string mode = argv[3];

    parse_program_mode(mode);

    int loop = 0;
    auto words = load_CSV(inputFileName);

    if (words.empty())
    {
        std::cout << "[!] No words loaded!" << std::endl;
        exit(0);
    }

    find_similar_words(words);
    // save_similar_words_to_file();
}