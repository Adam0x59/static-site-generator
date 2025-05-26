"""This file contains code related to block markdown"""

from htmlnode import *
from textnode import *
from enum import Enum
import re

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
    if re.match(r"^\s{0,3}(?:```|~~~).*", line):
        return BlockType.CODE

    if re.match(r"^>.*", line):
        return BlockType.QUOTE

    if re.match(r"^\s*(?:[-*+]\s+)", line):
        return BlockType.UNORDERED_LIST
    
    if re.match(r"^\s*\d+\.\s+", line):
        return BlockType.ORDERED_LIST
    
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
    markdown_lines = markdown.split("\n")
    current_block = []
    blocks = []
    inside_code = False
    current_block_type = None

    for line in markdown_lines:
        stripped = line.strip()
        rstripped = line.rstrip()
        block_type = line_to_block_type(line)
        if not inside_code and block_type != current_block_type and current_block:
            if block_type not in (BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST):
                blocks.append(current_block)
                current_block = []

        if block_type == BlockType.CODE and inside_code == True:
            inside_code = False
            current_block.append(rstripped)
            blocks.append(current_block)
            current_block = [] 
            current_block_type = None
            continue

        if inside_code == True:
            current_block.append(rstripped)
            continue

        if line.strip() == "":
            if current_block:
                blocks.append(current_block)
                current_block = []
            current_block_type = None
            continue

        if block_type == BlockType.CODE:
            current_block_type = block_type
            inside_code = True
            current_block.append(rstripped)
            continue

        current_block_type = block_type
        if block_type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
            current_block.append(rstripped)
            continue

        if block_type == BlockType.QUOTE:
            current_block.append(stripped)
            continue

        if block_type == BlockType.HEADING:
            current_block.append(stripped)
            blocks.append(current_block)
            current_block = []
            continue

        if block_type == BlockType.PARAGRAPH:
            current_block.append(stripped)

    if current_block:
        blocks.append(current_block)

    return blocks

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
    if re.match(r"^```.*```$", block, flags=re.DOTALL):
        return BlockType.CODE
    
    lines = block.split("\n")

    if all(re.match(r"^>.*", line) for line in lines):
        return BlockType.QUOTE

    if re.match(r"^\s*-\s+", block):
        return BlockType.UNORDERED_LIST
    
    if re.match(r"^\s*\d+\.\s+", block):
        return BlockType.ORDERED_LIST
    
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
        hash_found_list = re.findall(r"#{1}", "\n".join(block[1]))
        #print(hash_found_list)
        heading_number = len(hash_found_list)
        #print(heading_number)
        #print(LeafNode(f"<h{heading_number}>", block[1]))
        return LeafNode(f"h{heading_number}", "\n".join(block[1]))
    
    if block[0] == BlockType.CODE:
        return LeafNode("code", "\n".join(block[1][1:-1]))

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