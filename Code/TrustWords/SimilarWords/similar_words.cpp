#include <iostream>
#include <stdlib.h>
#include <map>
#include <vector>
#include <sstream>
#include <fstream>

#include "./modes/soundex.hpp"
#include "./modes/levenshtien.hpp"
#include "./modes/double_metaphone.hpp"

std::string inputFileName = "";
std::string outputFileName = "";

static bool LEV_DISTANCE = false;
static bool SOUNDEX = false;
static bool METAPHONE = false;

std::string SOUNDEX_CLI_TAG = "-s";
std::string LEV_CLI_TAG = "-l";
std::string METAPHONE_CLI_TAG = "-m";

/*
    Saves the similar words to a specified file
*/
void save__CSV(ofstream &outFile, std::vector<std::string> sim_words)
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
        // Refreshes the vector for each word_y
        sim_words.clear();
        sim_words.push_back(word_y);


        // ########## PRE-COMP ########## //
        std::string pre_word_y;
        if      (METAPHONE)  pre_word_y = DoubleMetaphone(word_y);
        else if (SOUNDEX)    pre_word_y = soundex(word_y);

        // ############################## //
        for (std::string word_x : words)
        {
             // Makes sure the same words aren't checked
            if (word_y != word_x)
            {
                bool add_word = false;

                if      (LEV_DISTANCE)      add_word = levenshtein_similar(word_y, word_x);
                else if (SOUNDEX)           add_word = soundex_similar(pre_word_y, word_x);
                else if (METAPHONE)         add_word = metaphone_similar(pre_word_y, word_x);
                {
                    /* code */
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
        save__CSV(outFile, sim_words);
    }
    outFile.close();
}

/*
    Prints the usage for the script
*/
void usage()
{
    std::cout << "Usage: ./a.out <IN_WORDLIST_PATH> <OUT_WORDLIST_PATH> <MODE> [-s|-l|-m]" << std::endl;
    exit(0);
}

/*
    TODO
*/
void parse_program_mode(std::string commandInput)
{
    if      (commandInput == SOUNDEX_CLI_TAG)       SOUNDEX = true;
    else if (commandInput == LEV_CLI_TAG)           LEV_DISTANCE = true;
    else if (commandInput == METAPHONE_CLI_TAG)     METAPHONE = true;
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

    auto words = load_CSV(inputFileName);

    if (words.empty())
    {
        std::cout << "[!] No words loaded!" << std::endl;
        exit(0);
    }

    find_similar_words(words);
    // save__CSV();
}