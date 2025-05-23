"""This file contains code related to block markdown"""

from htmlnode import *
from textnode import *
from enum import Enum
import re

# Class to store block types
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    """Converts a raw markdown STRING into a LIST of "block" STRINGS
    
    Markdown string represents a full document

    Args:
        A single STRING of raw markdown

    Returns:
        A LIST of STRINGS, each string is a block of markdown,
        list order same as order found in input string.
    """
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
    
    #print(split)  # Optional: print blocks for debugging
    return split  # Return the list of clean, meaningful blocks

def block_to_block_type(block):
    """Returns a value for the block-type of a given STRING.

    Args: A "block" of text which is a single text STRING with
    no \n\n breaks and stripped of whitespace - the output
    from markdown_to_blocks()
    
    Returns: a BlockType object denoting the type of block
    passed in. 
    
    Notes:
        This operates on the outer block only nested or
        inline blocks should be handled seperately using 
        inline functions
    """
    
    # Check if first and last characters of a block are ```
    if re.match(r"^```.*```$", block, flags=re.DOTALL):
        return BlockType.CODE
    
    # Split block into individual lines for later processing
    lines = block.split("\n")

    # Check if each line starts with a >
    if all(re.match(r"^>.*", line) for line in lines):
        return BlockType.QUOTE

    # Check if each line starts with a -   
    if all(re.match(r"^-\s+", line) for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check if each line starts with a ordered list identifier
    # 1. Item 1
    # 2. Item 2
    # And so on... Also makes sure numbers start at 1 and increment sequentially.
    for i, line in enumerate(lines):
        line_number = re.findall(r"^(\d+)\.",line)
        if not line_number or int(line_number[0]) != i+1:
            break
    else:
        return BlockType.ORDERED_LIST
    
    # Check if block starts with 1 to 6 # charachters
    # If not block must be a paragraph
    if re.match(r"^#{1,6}\s+.*", block):
        return BlockType.HEADING
    return BlockType.PARAGRAPH

