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
TEST_MSG = "The next clue is hidden *under* the green tree."

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

# 1. Insert X between two same letters, add x at end of odd-length message
#    for each pair (digraph)
# 2. If same row, shift right (wrap if needed)
# 3. If same col, shift down (wrap if needed)
# 4. Otherwise, take "opposite corners" (char one's row first)

def encode(message):
    output = ""
    message = message.upper() # Convert to uppercase
    # Remove punctuation and insert necessary X's (1.)
    readyMessage = ""
    for char in message:
        if char.isalpha():
            #Check for two same letters first
            if len(readyMessage) > 0 and readyMessage[len(readyMessage) - 1] == char:
                readyMessage = readyMessage + 'X'
            readyMessage = readyMessage + char
    # end for char in message
    if len(readyMessage) % 2 > 0:
        readyMessage = readyMessage + 'X'
    print("ENCODE MESSAGE:", message)
    print("ENCODE READYMESSAGE:", readyMessage)

    #Perform the encoding
    indexOne = 0
    indexTwo = 1 # iterate over readyMessage two characters at a time
    while indexTwo <= len(readyMessage) - 1:
        charOne = readyMessage[indexOne]
        charTwo = readyMessage[indexTwo]
        rowOne = LOOKUP_ROWS[ord(charOne) - LETTER_A]
        colOne = LOOKUP_COLS[ord(charOne) - LETTER_A]
        rowTwo = LOOKUP_ROWS[ord(charTwo) - LETTER_A]
        colTwo = LOOKUP_COLS[ord(charTwo) - LETTER_A]

        #print("ENCODE charOne:", charOne, "row", rowOne, "col", colOne)
        #print("ENCODE charTwo:", charTwo, "row", rowTwo, "col", colTwo)

        outRowOne = 0
        outColOne = 0
        outRowTwo = 0
        outColTwo = 0 # initialize vars for printing (debugging) later

        outCharOne = ''
        outCharTwo = ''

        if rowOne == rowTwo: # Same row - shift right (wrap to same row)
            outRowOne = rowOne
            outColOne = colOne + 1
            if outColOne >= WIDTH:
                outColOne -= WIDTH
            
            outRowTwo = rowTwo # also = rowOne
            outColTwo = rowTwo + 1
            if outColTwo >= WIDTH:
                outColTwo -= WIDTH
        elif colOne == colTwo: # Same col - shift down (wrap to same col)
            outRowOne = rowOne + 1
            if outRowOne >= HEIGHT:
                outRowOne -= HEIGHT
            outColOne = colOne

            outRowTwo = rowTwo + 1
            if outRowTwo >= HEIGHT:
                outRowTwo -= HEIGHT
            outColTwo = colTwo
        else:
            outRowOne = rowOne
            outColOne = colTwo

            outRowTwo = rowTwo
            outColTwo = colOne

        outCharOne = TABLE[outRowOne][outColOne]
        outCharTwo = TABLE[outRowTwo][outColTwo]
        output = output + outCharOne + outCharTwo + " "
        
        indexOne += 2 # taking two letters at a time
        indexTwo += 2
    return output

###############################################################################
# Decode
###############################################################################

#    for each pair (digraph)
# 1. If same row, shift left (wrap if needed)
# 2. If same col, shift up (wrap if needed)
# 3. Otherwise, take "opposite corners" (char one's row first)
#    Leave X's in place (user must interpret X's in output from context)

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
#print("Printing Lookup Rows")
#printLookupRows()
#print("Printing Lookup Cols")
#printLookupCols()
print("Encoding test message")
encodeResult = encode(TEST_MSG)
print("Result:", encodeResult)


