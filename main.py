# ========================================================================
# Assignment 4
# Alan Torres
# CSCE 4553: Information Retrieval
# Purpose: The objective of this assignment is to build a command line retrieval engine on top of our pre-made fixed-length inverted file. 
# Input: Queries which are lists of words
# Output: Top 10-ranking documents on the terminal based on the weights of the words given on the command line.
# ========================================================================
import sys
import os
from HTMLLexer import HTMLLexer

# Get number of total arguments and make one big string full of the queries
number_of_arguments = len(sys.argv)
all_words = ""
for i in range(1, number_of_arguments):
	all_words += (sys.argv[i] + " ")

# write all query words to temp.txt file
with open("temp.txt", 'w') as f:
	f.write(all_words)

# read queries from 'temp.txt' file and tokenize
m = HTMLLexer()
m.build()
m.tokenizeFile("temp.txt")
