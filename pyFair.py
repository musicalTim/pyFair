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
NOT_IN_TABLE = 200 # LOOKUP_ROWS/COLS entry for letter not in key table
HEIGHT = 5
WIDTH = 5 # Table is a 5x5 grid
TABLE = [] # key table (look up a letter given a row and col)
LOOKUP_ROWS = [] # Reverse: look up row or column given a letter
LOOKUP_COLS = []
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
    # Add letters of key to list of letters used to fill key table
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

    # Initialize LOOKUP_ROWS and LOOKUP_COLS
    for i in range(0, 26):
        LOOKUP_ROWS.append(NOT_IN_TABLE) # Entries for all but skipped letter
        LOOKUP_COLS.append(NOT_IN_TABLE) #     will be replaced below

    # Create a two-dimensional list - five rows of five, and fill with letters
    letterIndex = 0 #iterate over tableLetters to fill in key table
    for i in range(0, HEIGHT): # create five rows in table
        newRow = [] 
        for j in range(0, WIDTH):
            char = tableLetters[letterIndex]
            newRow.append(char)

            # Add entries to LOOKUP_ROWS and LOOKUP_COLS
            lookupIndex = ord(char) - LETTER_A
            print("CREATE TABLE lookupIndex:", lookupIndex)
            LOOKUP_ROWS[lookupIndex] = i
            LOOKUP_COLS[lookupIndex] = j

            letterIndex += 1
        # end for j in range
        TABLE.append(newRow)
    # end for i in range

def printTable():
    for row in TABLE:
        print(row)

def printLookupRows():
    for i in range(0, len(LOOKUP_ROWS) ):
        print(i, LOOKUP_ROWS[i])

def printLookupCols():
    for i in range(0, len(LOOKUP_COLS) ):
        print(i, LOOKUP_COLS[i])

###############################################################################
# Testing
###############################################################################

print("Creating key table using key")
createTable(TEST_KEY)
print("Printing Table")
printTable()
print("Printing Lookup Rows")
printLookupRows()
print("Printing Lookup Cols")
printLookupCols()


