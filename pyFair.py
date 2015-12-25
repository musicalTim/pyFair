#!/usr/bin/python3
#
###############################################################################
###############################################################################
#
# PYFAIR
# pyFair.py
#
# Timothy Wood
# 22 December 2015
#
# Encodes and Decodes alpha strings using the Playfair (or 
#     Wheatstone-Playfair) cipher
#
###############################################################################
###############################################################################

import string # for string.ascii_uppercase

DEBUGGING = True

###############################################################################
# Global Variables
###############################################################################
TEST_KEY = "DIFFERENT"

LETTER_A = ord('A')
HEIGHT = 5
WIDTH = 5 # Table is a 5x5 grid
TABLE = []
SKIP_LETTER = 'Q' # Default: table created skipping Q (Q's converted to X's)
                  # Alternative: skip J (J's converted to I's)

###############################################################################
# Encode
###############################################################################

# def encode(message):

###############################################################################
# Decode
###############################################################################



###############################################################################
# Helper Functions
###############################################################################

def createTable(keyIn):
    # Add letters of key to list of letters for key table
    tableLetters = ""
    for char in keyIn:
        if char.isalpha():
            if not char in tableLetters:
                tableLetters = tableLetters + char

    # Add the remainder of the alphabet, in order, to the list
    for letter in string.ascii_uppercase: # iterate over the alphabet
        if letter not in tableLetters and letter != SKIP_LETTER:
            # skip if letter already used (in key)
            # or if letter is (Q or J depending on option)
            tableLetters = tableLetters + letter

    # Create a two-dimensional list - five rows
    letterIndex = 0 #iterate over tableLetters to fill in key table
    for i in range(0, HEIGHT): # create five rows in table
        newRow = [] 
        for j in range(0, WIDTH):
            newRow.append(tableLetters[letterIndex])
            letterIndex += 1
        TABLE.append(newRow)
    # end for i in range

def printTable():
    for row in TABLE:
        print(row)

###############################################################################
# Testing
###############################################################################

print("LETTER_A is ", LETTER_A)
createTable(TEST_KEY)
print("Printing Rows")
for row in TABLE:
    print(row)
#printTable()


