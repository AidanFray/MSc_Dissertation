#!/usr/bin/env gnuplot
reset
n=100 #number of intervals
max=20. #max value
min=0. #min value
width=(max-min)/n #interval width

#function used to map a value to the intervals
hist(x,width)   = width * floor(x/width)+width/2.0

sum = 0
s(x)            = ((sum = sum + 1), 0)

set term png #output terminal and file
set output "histogram.png"
set xrange [min:max]
set yrange [0:]
set offset graph 0.05,0.05,0.05,0.0
set xtics min,(max-min)/5,max
set boxwidth width*0.9
set style fill solid 0.5 #fillstyle
set tics out nomirror
set xlabel "x"
set ylabel "Frequency"

plot "pgp_even_data/values.dat" u (hist($1,width)):(1.0) smooth freq lc rgb"red" notitle, \
    "dictionary_popular/values.dat" u (hist($1,width)):(1.0) smooth freq lc rgb"purple" notitle, \
    "pgp_odd_data/values.dat" u (hist($1,width)):(1.0) smooth freq lc rgb"blue" notitle, \
    "peerio/values.dat" u (hist($1,width)):(1.0) smooth freq lc rgb"orange" notitle
