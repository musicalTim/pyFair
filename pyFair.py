#!/usr/bin/python3
#
###############################################################################
###############################################################################
#
# PYFAIR
# pyFair.py
#
# Timothy Wood
# December 2015
#
# Encodes and Decodes alpha strings using the Playfair (or 
#     Wheatstone-Playfair) cipher
#
###############################################################################
###############################################################################

import string # for string.ascii_uppercase
import argparse

###############################################################################
# Global Variables
###############################################################################
# Functional
HEIGHT = 5
WIDTH = 5 # Table is a 5x5 grid
LETTER_A = ord('A')
NOT_IN_TABLE = 200 # LOOKUP_ROWS/COLS entry for letter not in key table

# Program Data
TABLE = [] # key table (look up a letter given a row and col)
LOOKUP_ROWS = [] # Reverse: look up row or column given a letter
LOOKUP_COLS = []

# Options
SKIP_LETTER = 'Q' # Default: table created skipping Q (Q's converted to X's)
                  # Alternative: skip J (J's to I's) or X (to Z's)
SKIP_REPLACE_WITH = 'X' # Letter to replace SKIP_LETTER if found in the message
VERBOSE = False # Print verbose output (--verbose or -v command line flag)

###############################################################################
# Encode
###############################################################################

# 1. Insert X between two same letters, add x at end of odd-length message
#    for each pair
# 2. If same row, shift right (wrap if needed)
# 3. If same col, shift down (wrap if needed)
# 4. Otherwise, take "opposite corners" (char one's row first)

def encode(message):
    output = ""
    message = message.upper() # Convert to uppercase
    # Remove punctuation and insert necessary X's
    readyMessage = ""
    for char in message:
        if char.isalpha():
            #Check for two same letters first
            if len(readyMessage) > 0 and readyMessage[len(readyMessage) - 1] == char:
                readyMessage = readyMessage + 'X'
            # Check for SKIP_LETTER
            if char == SKIP_LETTER:
                char = SKIP_REPLACE_WITH
            readyMessage = readyMessage + char
    # end for char in message
    if len(readyMessage) % 2 > 0:
        readyMessage = readyMessage + 'X'

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

        outRowOne = 0
        outColOne = 0
        outRowTwo = 0
        outColTwo = 0 # initialize vars

        outCharOne = ''
        outCharTwo = ''

        if rowOne == rowTwo: # Same row - shift right (wrap to same row)
            outRowOne = rowOne
            outColOne = colOne + 1
            if outColOne >= WIDTH:
                outColOne -= WIDTH
            
            outRowTwo = rowTwo # also = rowOne
            outColTwo = colTwo + 1
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

def decode(message):
    output = ""
    message = message.upper() # Convert to uppercase
    # Remove punctuation
    readyMessage = ""
    for char in message:
        if char.isalpha():
            readyMessage = readyMessage + char

    #Perform the decoding
    indexOne = 0
    indexTwo = 1 # iterate over readyMessage two characters at a time
    while indexTwo <= len(readyMessage) - 1:
        charOne = readyMessage[indexOne]
        charTwo = readyMessage[indexTwo]
        rowOne = LOOKUP_ROWS[ord(charOne) - LETTER_A]
        colOne = LOOKUP_COLS[ord(charOne) - LETTER_A]
        rowTwo = LOOKUP_ROWS[ord(charTwo) - LETTER_A]
        colTwo = LOOKUP_COLS[ord(charTwo) - LETTER_A]

        outRowOne = 0
        outColOne = 0
        outRowTwo = 0
        outColTwo = 0 # initialize vars

        outCharOne = ''
        outCharTwo = ''

        if rowOne == rowTwo: # Same row - shift left
            outRowOne = rowOne
            outColOne = colOne - 1
            if outColOne < 0:
                outColOne += WIDTH
            
            outRowTwo = rowTwo # also = rowOne
            outColTwo = colTwo - 1
            if outColTwo < 0:
                outColTwo += WIDTH
        elif colOne == colTwo: # Same col - shift up
            outRowOne = rowOne - 1
            if outRowOne < 0:
                outRowOne += HEIGHT
            outColOne = colOne

            outRowTwo = rowTwo - 1
            if outRowTwo < 0:
                outRowTwo += HEIGHT
            outColTwo = colTwo
        else:
            outRowOne = rowOne
            outColOne = colTwo

            outRowTwo = rowTwo
            outColTwo = colOne

        outCharOne = TABLE[outRowOne][outColOne]
        outCharTwo = TABLE[outRowTwo][outColTwo]
        output = output + outCharOne + outCharTwo  #no space
        
        indexOne += 2 # taking two letters at a time
        indexTwo += 2
    return output

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
    print("Key Table")
    for row in TABLE:
        print(row)

def printLookupRows():
    for i in range(0, len(LOOKUP_ROWS) ):
        print(i, LOOKUP_ROWS[i])

def printLookupCols():
    for i in range(0, len(LOOKUP_COLS) ):
        print(i, LOOKUP_COLS[i])

def outputVerbose(stringOut):
    global VERBOSE
    if VERBOSE == True:
        print(stringOut)

def setSkipLetter(ltr):
    global SKIP_LETTER
    global SKIP_REPLACE_WITH
    if ltr == 'Q':
        SKIP_LETTER = ltr
        SKIP_REPLACE_WITH = 'X'
    elif ltr == 'J':
        SKIP_LETTER = ltr
        SKIP_REPLACE_WITH = 'I'
    elif ltr == 'X':
        SKIP_LETTER = ltr
        SKIP_REPLACE_WITH = 'Z'
    else:
        print("Error: invalid skip letter given")

###############################################################################
# Arg parsing and Main
###############################################################################

parser = argparse.ArgumentParser(description='''Encode or decode a message 
 using the Playfair cipher.''')
parser.add_argument('--verbose','-v', action='store_true',
    help='print verbose output (including key table)')
parser.add_argument('function', choices=['ENCODE','DECODE'],
    help='encode or decode the message')
parser.add_argument('--skip','-s', choices=['Q','J','X'],
     help='\'skip-letter\' replace: Q=X (default), J=I, or X=Z')
parser.add_argument('--key','-k', nargs=1,
    help='key to use in creating key table (default: blank key)')
parser.add_argument('message', help='string to encode or decode')
nsArgs = parser.parse_args()
arguments = vars(nsArgs)

# MAIN
result = ""

if arguments['verbose'] == True:
    VERBOSE = True
if arguments['skip'] != None:
    setSkipLetter(arguments['skip'])

if arguments['key'] != None:
    createTable(arguments['key'][0])
else:
    createTable("")

if arguments['function'] == 'ENCODE':
    result = encode(arguments['message'])
elif arguments['function'] == 'DECODE':
    result = decode(arguments['message'])
else:
    result = "Error: invalid function specified"
if VERBOSE == True:
    printTable()
    print("Function:", arguments['function'])
    print("Alphabet fit: replace", SKIP_LETTER, "with", SKIP_REPLACE_WITH)
    print("Message:")
    print(arguments['message'])
    print("Result:")
print(result)
#end 


