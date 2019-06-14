#include <iostream>
#include <stdlib.h>
#include <map>
#include <vector>
#include <sstream>
#include <fstream>

#include "./modes/soundex.hpp"
#include "./modes/levenshtien.hpp"
#include "./modes/double_metaphone.hpp"
#include "./modes/nysiis.hpp"
#include "./modes/word_vectors.hpp"

std::string inputFileName = "";
std::string outputFileName = "";

// Values for quantifying tolerance or the measurement of "difference"
static float COMBINED_TOLERANCE = 1;
static float WORDVEC_TOLERANCE = 3.0;

// Command line tags
std::string SOUNDEX_CLI_TAG     = "-s";
std::string LEV_CLI_TAG         = "-l";
std::string METAPHONE_CLI_TAG   = "-m";
std::string NYSIIS_CLI_TAG      = "-n";
std::string COMBINED_MODE_TAG   = "-c";
std::string WORD_VEC_CLI_TAG    = "-v";

// Mode booleans
static bool LEV_DISTANCE    = false;
static bool SOUNDEX         = false;
static bool METAPHONE       = false;
static bool NYSIIS          = false;
static bool WORD_VEC        = false;
static bool COMBINED_MODE   = false;

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
    TODO
*/
function<std::string(std::string)> algorithms[] = {soundex, metaphone, nysiis}; 
bool combined_mode(std::string word1, std::string word2)
{
    float total = 0.0;
    for(auto al : algorithms)
    {
        auto code1 = al(word1);
        auto code2 = al(word2);
        auto lev = lev_distance(code1, code2);
        
        //TODO: add weights
        auto subtotal = lev;
        total += subtotal;
    }

    //DEBUG
    // if (total <= COMBINED_TOLERANCE) std::cout << "[D] " << word1 << " -- " << word2 << std::endl;

    return total <= COMBINED_TOLERANCE;
}

/*
    Compares each word using it's levistien distance
*/
void find_similar_words(std::vector<std::string> words, bool combined=false)
{
    // ## Note ##
    // The format of saving to file after every word alongside a refresh of the vector is 
    // to solve the issue of the vector getting too large and causing my Linux OS to freeze
    // the I/O slows down the operation but now I'm not guessing if the input will be too big 

    std::vector<std::string> sim_words;
    std::ofstream outFile (outputFileName);

    WordVectors wordvec;
    if (WORD_VEC)
    {
        wordvec.load();
        std::cout << "[*] Word vectors loaded successfully!" << std::endl;
    }

    int loop = 0;
    for (std::string word_y : words)
    {
        // Refreshes the vector for each word_y
        sim_words.clear();
        sim_words.push_back(word_y);


        // ########## PRE-COMP ########## //
        std::string pre_word_y;
        if      (METAPHONE)  pre_word_y = metaphone(word_y);
        else if (SOUNDEX)    pre_word_y = soundex(word_y);
        // ############################## //

        for (std::string word_x : words)
        {
             // Makes sure the same words aren't checked
            if (word_y != word_x)
            {
                bool add_word = false;

                if (combined) add_word = combined_mode(word_y, word_x);
                else
                {
                    if      (LEV_DISTANCE)      add_word = levenshtein_similar(word_y, word_x);
                    else if (SOUNDEX)           add_word = soundex_similar(pre_word_y, word_x);
                    else if (METAPHONE)         add_word = metaphone_similar(pre_word_y, word_x);
                    else if (WORD_VEC)          add_word = wordvec.similar(word_y, word_x, WORDVEC_TOLERANCE);
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
    std::cout << "Usage: ./a.out <IN_WORDLIST_PATH> <OUT_WORDLIST_PATH> <MODE> [-s|-l|-m|-c|-v|-n]" << std::endl;
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
    else if (commandInput == COMBINED_MODE_TAG)     COMBINED_MODE = true;
    else if (commandInput == NYSIIS_CLI_TAG)        NYSIIS = true;
    else if (commandInput == WORD_VEC_CLI_TAG)      WORD_VEC = true;
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

    // //##### DEBUG #####
    // inputFileName = "/home/main_user/GitHub/Cyber-Security-Individual-Project/Wordlists/Dictionary/words_popular.txt";
    // outputFileName = "./test.txt";
    // std::string mode = "-v";

    parse_program_mode(mode);

    auto words = load_CSV(inputFileName);

    if (words.empty())
    {
        std::cout << "[!] No words loaded!" << std::endl;
        exit(0);
    }

    find_similar_words(words, COMBINED_MODE);
    // save__CSV();
}