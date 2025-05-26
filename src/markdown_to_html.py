"""This file is for code related to converting html to markdown"""

from inline import *
from htmlnode import *
from block_markdown import *
from textnode import *

def markdown_to_html(markdown):
    """Converts a full Markdown document into a single Parent HTMLNode
    containing child HTMLNode objects that represent nested HTML elements.

    Args:
        markdown (str): A complete raw Markdown document.

    Returns:
        HTMLNode: A parent HTMLNode object representing the top-level HTML
        element, containing child HTMLNode objects representing nested HTML blocks.
    """

    # *****************************************************
    # Break markdown blocks up into top level HTMLnodes by
    # *****************************************************
    
    # Convert markdown file into a list of markdown blocks
    markdown_blocks = markdown_to_blocks(markdown)
    # Convert list into list of tuples [(BlockType, markdown Block), ...]
    markdown_block_tuples = []
    for block in markdown_blocks:
        block_joined = "\n".join(block)
        markdown_block_tuples.append((block_to_block_type(block_joined), block))
    print("\nOuter-Block Identification:\n")
    for block in markdown_block_tuples:
        print(f"\n{block}")
'''
    # Convert any headings or code blocks into LeafNodes
    mdbt_headings_code = []
    for block in markdown_block_tuples:
        mdbt_headings_code.append(block_to_text_node(block))

    # Convert any un-ordered lists into a parent HTMLnode containing
    # list items as TextNodes
    for block in mdbt_headings_code:
        #print(block)
        if type(block) != LeafNode:
            #print(block)
            pass

    #print("\n")
    for node in mdbt_headings_code:
        #print(node)
        pass
''' 
    # *****************************************************
    # Re-assemble HTMLnodes into output file and return
    # *****************************************************

