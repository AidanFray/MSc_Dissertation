#include <iostream>
#include <stdlib.h>
#include <map>
#include <vector>
#include <fstream>
#include <sstream>

// ########################################## //
//                  TODO                      //
// ########################################## //
// TODO For some godly reason some words are
//      repeated in the word set, these will 
//      need to be cleaned 
// ########################################## //

int DIFFERENCE_TOLERANCE = 1;

std::string inputFileName = "./en_unique.csv";
std::string outputFileName = "similar.csv";
std::map<std::string, std::vector<std::string>> similarWords;

/*
    TODO
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
    TODO
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
    TODO
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
    https://stackoverflow.com/questions/1120140/how-can-i-read-and-parse-csv-files-in-c
*/
std::vector<std::string> get_next_line_and_split_into_tokens(std::istream& str)
{
    std::vector<std::string>   result;
    std::string                line;
    std::getline(str,line);

    std::stringstream          lineStream(line);
    std::string                cell;

    while(std::getline(lineStream,cell, ','))
    {
        result.push_back(cell);
    }
    // This checks for a trailing comma with no data after it.
    if (!lineStream && cell.empty())
    {
        // If there was a trailing comma then add an empty element.
        result.push_back("");
    }
    return result;
}

/*
    Loads a CSV file and splits values
*/
std::vector<std::string> load_CSV(std::string filePath)
{
    std::ifstream infile(filePath);
    std::vector<std::string> words;
    std::vector<std::string> line;

    while (true) 
    {
        line = get_next_line_and_split_into_tokens(infile);

        if (line[0] == "en")
        {
            words.push_back(line[2]);
        }
        else break;
    } 

    return words;
}

int main()
{
    int loop = 0;
    auto words = load_CSV(inputFileName);

    // For VSCode debugging
    if (words.empty())
    {
        words = load_CSV("/home/user/Github/Cyber-Security-Individual-Project/Code/TrustWords/en.csv");
    }

    find_similar_words(words);
    save_similar_words_to_file();
}