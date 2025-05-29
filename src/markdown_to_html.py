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
    # Break markdown blocks up into top level HTMLnodes
    # *****************************************************

    # Convert markdown into blocks
    markdown_blocks = markdown_to_blocks(markdown)
    # Identify outer block types, convert into list of tuples 
    # [(BlockType, markdown Block), ...]
    markdown_block_tuples = identify_outer_block_types(markdown_blocks)
    # Convert any code blocks into leaf nodes
    code = convert_code_blocks(markdown_block_tuples)
    # Convert any paragraphs into LeafNodes wrapped in a HTMLnode
    c_paragraphs = convert_paragraphs(code)
    # Convert any headings into LeafNodes wrapped in a HTMLnode
    cp_headings = convert_headings(c_paragraphs)
    # Convert quote blocks into LeafNodes wrapped in a HTMLnode
    cph_quotes = convert_quotes(cp_headings)
    # Convert list blocks into LeafNodes wrapped in HTMLnodes
    cphq_lists = convert_lists(cph_quotes)

def block_text_to_leaf_nodes(block):
    block_text_nodes = text_to_textnodes("\n".join(block[1]))
    block_leaf_nodes = []
    for node in block_text_nodes:
        block_leaf_nodes.append(text_node_to_html_node(node))
    return block_leaf_nodes

def text_to_leaf_nodes(text):
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        text_leaf_nodes = text_node_to_html_node(node)
    return text_leaf_nodes

def identify_outer_block_types(list):
    markdown_block_tuples = []
    for block in list:
        block_joined = "\n".join(block)
        markdown_block_tuples.append((block_to_block_type(block_joined), block))
    print("\n************\nOuter-Block Identification:")
    for block in markdown_block_tuples:
        print(f"\n{block}")
    return markdown_block_tuples

def convert_code_blocks(list):
    code = []
    for block in list:
        code.append(code_block_to_leaf_node(block))
    print("\n************\ncode converted:")
    for block in code:
        print(f"\n{repr(f"{block}")}")
    return code

def convert_paragraphs(list):
    c_paragraphs = []
    for block in list:
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
    return c_paragraphs

def convert_headings(list):
    cp_headings = []
    for block in list:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            cp_headings.append(block)
            continue
        if block[0] == BlockType.HEADING:
            #print(block[0])
            heading_num = len(re.findall(r"^#{1,6}", "".join(block[1]))[0])
            cp_headings.append(ParentNode(f"h{heading_num}", block_text_to_leaf_nodes(block)))
            continue
        cp_headings.append(block)
    print("\n************\nHeadings Split:")
    for block in cp_headings:
        print(f"\n{repr(f"{block}")}")
    return cp_headings

def convert_quotes(list):
    cph_quotes = []
    quote_lines_stripped = []
    for block in list:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            cph_quotes.append(block)
            continue
        if block[0] == BlockType.QUOTE:
            #quote_lines_stripped = []
            for item in block[1]:
                quote_lines_stripped.append(item[2:] if item.startswith('> ') else item)
            block = (BlockType.QUOTE, quote_lines_stripped)
            cph_quotes.append(ParentNode("blockquote", block_text_to_leaf_nodes(block)))
            continue
        cph_quotes.append(block)
    print("\n************\nQuotes Split:")
    for block in cph_quotes:
        print(f"\n{repr(f"{block}")}")
    return cph_quotes

def convert_lists(list):
    cphq_lists = []
    indentation_index = []
    for block in list:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            cphq_lists.append(block)
            continue
        if block[0] in (BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST):
            indentation_buffer = []
            for item in block[1]:
                indentation_num = len(re.findall(r"^\s*", item)[0])
                indentation_buffer.append((indentation_num, item.strip()))
            indetation_buffer_to_HTMLnodes(indentation_buffer)
            #indentation_index.append(indentation_buffer)
        #print(indentation_index)


'''
def indetation_buffer_to_HTMLnodes(list):
    nodes = [(0,[])]
    previous_indent = 0
    current_indent = 0
    current_node_index = 0

    for item in list:
        # set current indent to item[0]
        current_indent = item[0]
        # if current_indent is equal to previous_indent add item leaf nodes to current node.
        if current_indent == previous_indent:
            nodes[current_node_index][1].append(text_to_leaf_nodes(item[1]))
        if current_indent > previous_indent:
            current_node_index += 1
            if (len(nodes)-1) < current_node_index:
                nodes.append((current_node_index, []))
                print(nodes)
            nodes[current_node_index][1].append(text_to_leaf_nodes(item[1]))
        if current_indent < previous_indent:
            current_node_index -= 1
            nodes[current_node_index][1].append(text_to_leaf_nodes(item[1]))
        previous_indent = current_indent
    print(nodes)
    pass
'''
    # *****************************************************
    # Re-assemble HTMLnodes into output file and return
    # *****************************************************

