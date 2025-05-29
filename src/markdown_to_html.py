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

    # Convert markdown into blocks
    markdown_blocks = markdown_to_blocks(markdown)

    # Convert list into list of tuples [(BlockType, markdown Block), ...]
    markdown_block_tuples = []
    for block in markdown_blocks:
        block_joined = "\n".join(block)
        markdown_block_tuples.append((block_to_block_type(block_joined), block))
    print("\n************\nOuter-Block Identification:")
    for block in markdown_block_tuples:
        print(f"\n{block}")

    # Convert any code-blocks into LeafNodes
    code = []
    for block in markdown_block_tuples:
        code.append(block_to_text_node(block))
    print("\n************\nHeadings and code converted:")
    for block in code:
        print(f"\n{repr(f"{block}")}")

    # Convert any paragraphs into list of TextNodes
    c_paragraphs = []
    for block in code:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            c_paragraphs.append(block)
            continue
        if block[0] == BlockType.PARAGRAPH:
            c_paragraphs.append(ParentNode("p", block_text_to_leaf_nodes(block)))
            continue
        c_paragraphs.append(block)
    print("\n************\nParagraphs Split:")
    for block in c_paragraphs:
        print(f"\n{repr(f"{block}")}")

    cp_headings = []
    for block in c_paragraphs:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            cp_headings.append(block)
            continue
        if block[0] == BlockType.HEADING:
            print(block[0])
            heading_num = len(re.findall(r"^#{1,6}", "".join(block[1]))[0])
            #print(heading_num)
            #heading_val = len(heading_num)
            cp_headings.append(ParentNode(f"h{heading_num}", block_text_to_leaf_nodes(block)))
            continue
        cp_headings.append(block)
    print("\n************\nHeadings Split:")
    for block in cp_headings:
        print(f"\n{repr(f"{block}")}")
            
    
def block_text_to_leaf_nodes(block):
    block_text_nodes = text_to_textnodes("\n".join(block[1]))
    block_leaf_nodes = []
    for node in block_text_nodes:
        block_leaf_nodes.append(text_node_to_html_node(node))
    return block_leaf_nodes
    
    '''
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

