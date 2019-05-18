#include <chrono>  // for duration_cast, operator-, duration, system_clock::...
#include "timer.hpp"

Timer::Timer() : beg_(clock_::now()) \
{

}

void Timer::reset() 
{
        beg_ = clock_::now(); 
}

double Timer::elapsed() const 
{ 
    return std::chrono::duration_cast<second_>(clock_::now() - beg_).count(); 
}