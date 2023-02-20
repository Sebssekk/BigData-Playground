#!/usr/bin/python3

import sys

# Input takes from standard input for myline in sys.stdin: 
for line in sys.stdin:
# Remove whitespace either side 
  line = line.strip() 

# Break the line into words 
  words = line.split() 

# Iterate the words list
  for word in words:
# Write the results to standard output 
    print (f'{word}\t{1}')
