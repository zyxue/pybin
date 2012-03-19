#!/bin/bash

# data must be in the first and second columns

# $1 is the xvg file
# $2, $3 specify the column number to be plotted

gnuplot -e "set term dumb; plot '$1' using $2:$3"