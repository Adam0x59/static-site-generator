'''
***********************************************************
This file contains code related to block markdown
***********************************************************
'''
from htmlnode import *
from textnode import *
from enum import Enum

# Class to store block types
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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
    # Step 1: Split the markdown into individual lines
    remove_line_whitespace = markdown.split("\n")
    
    normalized_lines = []
    for line in remove_line_whitespace:
        if line.strip() == "":
            # If the line is empty or only whitespace, treat it as a blank line
            normalized_lines.append("")
        else:
            # Otherwise, preserve the line as-is (including indentation or formatting)
            normalized_lines.append(line)
    
    # Step 2: Rejoin the normalized lines into a string
    markdown_preformat = "\n".join(normalized_lines)
    
    # Step 3: Split the string into blocks separated by two or more newlines
    split_pre = markdown_preformat.split("\n\n")
    
    split = []
    for item in split_pre:
        item = item.strip()  # Remove leading/trailing whitespace from each block
        if item == '':
            continue  # Skip any resulting empty blocks
        split.append(item)  # Keep non-empty blocks
    
    print(split)  # Optional: print blocks for debugging
    return split  # Return the list of clean, meaningful blocks