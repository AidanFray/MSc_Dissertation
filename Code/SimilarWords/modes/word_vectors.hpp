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

class WordVectors
{
    private:
        std::map<std::string, std::vector<float>> wordVectors;
        std::map<std::string, std::vector<float>> load_word_vectors();

        float distance(std::string word1, std::string word2);

    public:
        WordVectors() {};
        bool word_is_available(std::string word1);
        bool similar(std::string word1, std::string word2, float similarity);
        void load() {load_word_vectors();}
};