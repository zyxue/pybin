#!/bin/bash

# data must be in the first and second columns

gnuplot -e "set term dumb; plot '$1' using 1:2"