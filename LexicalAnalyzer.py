# Created in Python 3.6
import re
import collections

def checkToken(line):   # Checks the line for tokens, adding the line number to the tokens dictionary for the appropriate category if a token is found

    for t in tokens: # Iterate through each token category
        p = re.findall(tokens[t][0], line) # Generates a list containing each instance of the current token category found based on the regular expression present at the beginning of the list        
        if(p and not doubleOperator(p)):
            line = re.sub(tokens[t][0], t + "\xA9", line) # Substitutes the instances of tokens we already counted for in the line with the category, adds a copyright sign as a delimiter between tokens

            for item in p: # Iterate through all tokens matched
                if type(item) == tuple:
                    item = str([i for i in item if i != ''][0]) # for some reason some matches will include an empty string, want to remove that
                if(item in symbols):
                    symbols[str(item)].append(numline)
                else:
                    symbols[str(item)] = [numline]

    line = line.rstrip(',') # strip off the last comma

    if errorCheck(line):
        print("Error! Unidentified symbol found on line " + str(numline) + ".\n")
    else:
        print(str(numline) + ": " + re.sub(r'\xA9',', ',line).strip(', '))
        print()
        
def doubleOperator(token): # Checks given token input for any double operators, if double operators are found returns true.
    if any(item == "=="  or item == "++" or item == "--" or item == "**" or item == "//" for item in token): # check each item passed to us to see if there's a double operator
            return True

def errorCheck(line):
    result = line.split("\xA9") # split by copyright symbol
    result = [s for s in result if s != ''] # remove empty cells using list comprehension
    result = [r.strip(' ') for r in result] # do the same to strip whitespace away from elements

    if not all(s in tokens for s in result): # short circuits on the first false, so if there are any strings in result that aren't in the keys of tokens then it will return true
        return True

    return False

def symbolTable():
    with open("output.txt", 'w') as of:
        of.write("SYMBOL TABLE:\n")
        for keys in sorted(symbols): # write the keys and their values to the output file sorted by the keys 
            of.write(keys + ': ' + str(symbols[keys]))
            of.write("\n")

tokens = { # tokens dictionary with category names and lists containing the regular expressions to be used as the first element. the line numbers shall be added to this same dictionary
    "IDENT": [r'[a-zA-Z]\w*'],
    "ASSIGNOP": [r'=+|\+=|\-=|\*=|/='], # added + to the end of operator regex's to capture double or more operators, such as ==
    "INT": [r'\d+'],
    "MULTOP": [r'(\*)+|(/)+'],
    "ADDOP": [r'(\+)+|(\-)+'],
    "TERM": [r'\;']
}

symbols = {}

numline = 1

fname = input("Please enter an input file name: ")
with open(fname) as f:
    for line in f:
        line = line.rstrip() # remove newline
        checkToken(line) # pass the line to checkToken, which will parse it and populate the tokens dictionary
        numline = numline + 1

symbolTable() # produce a symbol table with the modified tokens dictionary
print("Symbol table produced in output.txt")