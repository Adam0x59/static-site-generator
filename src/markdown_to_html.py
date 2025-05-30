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
    cphq_lists = convert_lists(cph_quotes, "-d")

    for parent_node in cphq_lists:
        if isinstance(parent_node, ParentNode):
            print(ParentNode.to_html(parent_node))


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

def identify_outer_block_types(list, debug=None):
    markdown_block_tuples = []
    for block in list:
        block_joined = "\n".join(block)
        markdown_block_tuples.append((block_to_block_type(block_joined), block))
    if debug == "-d":
        print("\n************\nOuter-Block Identification:")
        for block in markdown_block_tuples:
            print(f"\n{block}")
    return markdown_block_tuples

def convert_code_blocks(list, debug=None):
    code = []
    for block in list:
        code.append(code_block_to_leaf_node(block))
    if debug == "-d":
        print("\n************\ncode converted:")
        for block in code:
            print(f"\n{repr(f"{block}")}")
    return code

def convert_paragraphs(list, debug=None):
    c_paragraphs = []
    for block in list:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            c_paragraphs.append(block)
            continue
        if block[0] == BlockType.PARAGRAPH:
            c_paragraphs.append(ParentNode("p", block_text_to_leaf_nodes(block)))
            continue
        c_paragraphs.append(block)
    if debug == "-d":
        print("\n************\nParagraphs Split:")
        for block in c_paragraphs:
            print(f"\n{repr(f"{block}")}")
    return c_paragraphs

def convert_headings(list, debug=None):
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
    if debug == "-d":
        print("\n************\nHeadings Split:")
        for block in cp_headings:
            print(f"\n{repr(f"{block}")}")
    return cp_headings

def convert_quotes(list, debug=None):
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
    if debug == "-d":
        print("\n************\nQuotes Split:")
        for block in cph_quotes:
            print(f"\n{repr(f"{block}")}")  
    return cph_quotes

def convert_lists(list, debug=None ):
    cphq_lists = []
    for block in list:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            cphq_lists.append(block)
            continue
        if block[0] in (BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST):
            indentation_buffer = []
            for item in block[1]:
                indentation_num = len(re.findall(r"^\s*", item)[0])
                indentation_buffer.append((indentation_num, item.strip()))
            cphq_lists.append(list_indentation_nodes(indentation_buffer, debug))
    if debug == "-d":
        print("\n************\nLists Split:")
        for block in cphq_lists:
            print(f"\n{repr(f"{block}")}")
    return cphq_lists

def list_indentation_nodes(list, debug):
    nodes = [ParentNode(None, None, None)]
    nesting_stack = [0]
    #current_index = 0
    for item in list:
        if nesting_stack[-1] == item[0]:
            # Check if current nesting index exists in nesting_dict as a key.
            # Add to dict if not present.
            #if item[0] != nesting_stack[-1]:
            #    nesting_stack.append(item[0])
            # Check if current ParentNode has a tag, if tag is None update tag.
            if nodes[-1].tag is None:    
                nodes[-1].tag = repr(line_to_block_type(item[1]))
            # Convert item text into list of text-nodes
            children_text = text_to_textnodes(item[1])
            children_nodes = []
            # Convert items in list of text-nodes into LeafNodes
            for text in children_text:
                children_nodes.append(text_node_to_html_node(text))
            # Append list of LeafNodes into current ParentNode's list of children
            nodes[-1].children.extend(children_nodes)
            continue

        if item[0] > nesting_stack[-1]:
            # Check if current nesting index exists in nesting_dict as a key.
            # Add to dict if not present
            if nesting_stack[-1] is not item[0]:
                nesting_stack.append(item[0])
            nodes[-1].children.append(ParentNode(None, None, None))
            nodes.append(nodes[-1].children[-1])
            nodes[-1].tag = repr(line_to_block_type(item[1]))
            children_text = text_to_textnodes(item[1])
            children_nodes = []
            for text in children_text:
                children_nodes.append(text_node_to_html_node(text))
            nodes[-1].children.extend(children_nodes)
            continue

        if item[0] < nesting_stack[-1]:
            while nesting_stack[-1] > item[0]:
                nesting_stack.pop()
                nodes.pop()
            if nesting_stack[-1] == item[0]:
                # Check if current nesting index exists in nesting_dict as a key.
                # Add to dict if not present.
                if item[0] != nesting_stack[-1]:
                    nesting_stack.append(item[0])
                # Check if current ParentNode has a tag, if tag is None update tag.
                if nodes[-1].tag is None:    
                    nodes[-1].tag = repr(line_to_block_type(item[1]))
                # Convert item text into list of text-nodes  
                children_text = text_to_textnodes(item[1])
                children_nodes = []
                # Convert items in list of text-nodes into LeafNodes
                #print(children_text)
                for text in children_text:
                    #print(children_text)
                    children_nodes.append(text_node_to_html_node(text))
                # Append list of LeafNodes into current ParentNode's list of children
                nodes[-1].children.extend(children_nodes)
            continue
    if debug == "-d": 
        print("\n************\nList Split:")
        print(nesting_stack)
        for node in nodes:
            print_tree(node)
    return nodes[0]

def print_tree(node, indent=0):
    pad = "  " * indent
    if isinstance(node, ParentNode):
        print(f"{pad}ParentNode({node.tag})")
        for child in node.children:
            if isinstance(child, list):
                for item in child:
                    print_tree(item, indent + 1)
            else:
                print_tree(child, indent + 1)
    elif isinstance(node, LeafNode):
        print(f"{pad}LeafNode({node.value})")

    # *****************************************************
    # Re-assemble HTMLnodes into output file and return
    # *****************************************************

