"""
PARSING
*******
takes the parameters file and block with quotes
then, reads and parses the file in a manner that:
- all the characters are lowered by lower()
- all the lines are splitted into a list by splitlines()
- all the items of the list are also splitted into lists 
        by split(' = ') if they have ' = ' sign in them 
        
DICTIONARY
*******
checks if the function is called for substrate or slider
due to result, creates a dictionary so that
all the parameters are ordered starting 
from block name till '/' sign by parms.index
--------------------------------------------------
(!) only returns the parameters of the specified block
--------------------------------------------------
"""

def parse(file, block):
    with open(file, 'r') as f:
        parms = [parm.split(' = ') for parm in f.read().lower().splitlines()]
        if block == '&substrate':
            parms = dict(parms[parms.index(['&substrate'])+1:parms.index(['/'])])
        elif block == '&slider':
            parms = dict(parms[parms.index(['&slider'])+1:parms.index(['/'], 9)])
    return parms
