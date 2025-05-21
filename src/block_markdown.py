'''
***********************************************************
This file contains code related to block markdown
***********************************************************
'''
from htmlnode import *
from textnode import *


'''
***********************************************************
A function to convert a raw markdown STRING (representing a 
full document) into a LIST of "block" STRINGS.
-----------------------------------------------------------
INPUT: A single STRING of raw markdown.
-----------------------------------------------------------
OUTPUT: A LIST of STRINGS, each string is a "block" of 
markdown from the input (List of blocks is ordered by block
location as in the input string).
***********************************************************
'''
def markdown_to_blocks(markdown):
    split_pre = markdown.split("\n\n")
    split = [] 
    for item in split_pre:
        item = item.strip()
        if item == '':
            continue
        split.append(item)
    print(split)
    return split