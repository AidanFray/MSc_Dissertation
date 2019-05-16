#include <math.h> 
#include <iostream>

int main()
{
    auto num_of_elements = 5000000;

    //TODO : this can be altered
    // Currently: 1 in a trillion
    double probability = 1e-10;

    auto top = ((num_of_elements * log(probability)));
    auto bottom = (log(2) * log(2));

    auto m = top / bottom;

    std::cout << (unsigned long)abs(m) << std::endl;
}