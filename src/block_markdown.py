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

def line_to_block_type(line):
    """Takes a line of text and returns BlockType object.
    
    Accepts:
        line (str): A line of markdown text

    Returns:
        BlockType object: containing value of current line.
    """
    # Check if first or last characters of a line are code
    if re.match(r"^```.*|.*```$", line, flags=re.DOTALL):
        return BlockType.CODE

    # Check if line starts with a >
    if re.match(r"^>.*", line):
        return BlockType.QUOTE

    # Check if line is an unordered-list 
    if re.match(r"^\s*(?:[-*+]\s+)", line):
        return BlockType.UNORDERED_LIST
    
    if re.match(r"^\s*\d+\.\s+"):
        return BlockType.ORDERED_LIST
    
    # Check if block starts with 1 to 6 # charachters
    # If not block must be a paragraph
    if re.match(r"^#{1,6}\s+.*", line):
        return BlockType.HEADING
    return BlockType.PARAGRAPH

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

def block_to_text_node(block):
    """Takes in markdown block and it's type, converts to TextType.
    Only converts vaiable blocks which need no further processing:
        - Heading
        - Code 
    Invalid Blocks returned as is

    Args:
        block (tuple) - (block_type, block_val):
            block_val (str): A block of markdown
            block_type (BlockType): Type of markdown block
    
    Returns:
        text_node (TextNode): If converted text node returned
        (block_type, block): If passed, returns tuple
    """
    if block[0] == BlockType.HEADING:
        hash_found_list = re.findall(r"#{1}", block[1])
        #print(hash_found_list)
        heading_number = len(hash_found_list)
        #print(heading_number)
        #print(LeafNode(f"<h{heading_number}>", block[1]))
        return LeafNode(f"<h{heading_number}>", block[1])
    
    if block[0] == BlockType.CODE:
        return LeafNode("<code>", block[1])
    
    return block

def list_formatter(block):
    """Converts list content into list nodes
    
    Args:
        block (tuple):
            block_val (str): Text content of markdown block
            block_type (BlockType): Type of markdown block

    Returns:
        node (ParentNode): Parent node to contain list
            inner_nodes (leaf node)
    """
    pass