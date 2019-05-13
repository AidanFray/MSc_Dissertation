#include <algorithm>
#include <functional>
#include <string>
#include <cctype>
#include <iostream>

using namespace std;

//----------------------------------------------------------------------------
char f_transform(char c)
{
    string consonants[6] = {"BFPV", "CGJKQSXZ", "DT", "L", "MN", "R"};
    for (int i = 0; i < 6; i++)
        if (consonants[i].find(c) != string::npos)
            return (i + 1) + '0';
    return c;
}

//----------------------------------------------------------------------------
string soundex(const string &s)
{
    string result;

    // Validate s
    if (std::find_if(
            s.begin(),
            s.end(),
            std::not1(std::ptr_fun<int, int>(std::isalpha))) != s.end())
        return result;

    // result <-- uppercase( s )
    result.resize(s.length());
    std::transform(
        s.begin(),
        s.end(),
        result.begin(),
        std::ptr_fun<int, int>(std::toupper));

    // Convert Soundex letters to codes
    std::transform(
        result.begin() + 1,
        result.end(),
        result.begin() + 1,
        f_transform);

    // Collapse adjacent identical digits
    result.erase(
        std::unique(
            result.begin() + 1,
            result.end()),
        result.end());

    // Remove all non-digits following the first letter
    result.erase(
        std::remove_if(
            result.begin() + 1,
            result.end(),
            std::not1(std::ptr_fun<int, int>(std::isdigit))),
        result.end());

    result += "000";
    result.resize(4);

    return result;
}