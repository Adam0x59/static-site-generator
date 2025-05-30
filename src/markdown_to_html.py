"""This file is for code related to converting html to markdown"""

from inline import *
from htmlnode import *
from block_markdown import *
from textnode import *
import inspect

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
    for block in markdown_blocks:
        print(block)
    # Identify outer block types, convert into list of tuples 
    # [(BlockType, markdown Block), ...]
    markdown_block_tuples = identify_outer_block_types(markdown_blocks, "-d")
    # Convert any code blocks into leaf nodes
    code = convert_code_blocks(markdown_block_tuples, "-d")
    # Convert any paragraphs into LeafNodes wrapped in a HTMLnode
    c_paragraphs = convert_paragraphs(code, "-d")
    # Convert any headings into LeafNodes wrapped in a HTMLnode
    cp_headings = convert_headings(c_paragraphs, "-d")
    # Convert quote blocks into LeafNodes wrapped in a HTMLnode
    cph_quotes = convert_quotes(cp_headings, "-d")
    # Convert list blocks into LeafNodes wrapped in HTMLnodes
    cphq_lists = convert_lists(cph_quotes, "-d")

    for parent_node in cphq_lists:
        if isinstance(parent_node, ParentNode):
            print(ParentNode.to_html(parent_node))


def block_text_to_leaf_nodes(block):
    '''Converts a block of Markdown text into a list of LeafNode objects.

    Args:
        block (tuple): A tuple of (block_type, lines), where lines is a list of strings representing the block content.

    Returns:
        list: A list of LeafNode objects representing inline content.
    '''
    block_text_nodes = text_to_textnodes("\n".join(block[1]))
    block_leaf_nodes = []
    for node in block_text_nodes:
        block_leaf_nodes.append(text_node_to_html_node(node))
    return block_leaf_nodes

def text_to_leaf_nodes(text):
    '''Converts a string of Markdown text into a list of LeafNode objects

    Args:
        text (str): A raw string representation of the Markdown content.

    Returns:
        list: A list of LeafNode objects representing inline content
    '''
    text_nodes = text_to_textnodes(text)
    text_leaf_nodes = []
    for node in text_nodes:
        text_leaf_nodes.append(text_node_to_html_node(node))
    return text_leaf_nodes

def identify_outer_block_types(blocks, debug=None):
    '''Identifies the outer block type for each block in a list of Markdown blocks.

    Args:
        blocks (list): A list of blocks, where each block is a list of strings representing lines of Markdown.
        debug (str, optional): If set to "-d", debug output is printed to the console. Default is None.

    Returns:
        list: A list of tuples in the format (BlockType, block), where `BlockType` is an enum indicating the type of block, 
              and `block` is the original list of lines.
    '''
    markdown_block_tuples = []
    for block in blocks:
        block_joined = "\n".join(block)
        markdown_block_tuples.append((block_to_block_type(block_joined), block))
    debug_output(markdown_block_tuples, debug)
    return markdown_block_tuples

def convert_code_blocks(blocks, debug=None):
    '''Converts any code blocks found in a list of blocks into LeafNode objects.

    Args:
        blocks (list): A list of tuples, each tuple is (block_type, lines),
            where `block_type` is an enum or identifier,
            and `lines` is a list of strings representing lines of Markdown.
        debug (str, optional): If set to "-d", debug output is printed to the console. Default is None.

    Returns:
        list: A list containing LeafNode objects converted from code blocks.
              Each tuple from the input list is processed; code blocks are replaced by their corresponding LeafNode objects,
              while other block are added to the list without modification.
    '''
    code = []
    for block in blocks:
        code.append(code_block_to_leaf_node(block))
    debug_output(code, debug)
    return code

def convert_paragraphs(blocks, debug=None):
    '''Converts paragraph blocks into ParentNode objects containing LeafNode children representing inline Markdown.

    Args:
        blocks (list): A list containing either HTMLnode objects or tuples of the form (block_type, lines),
            where `block_type` is an enum or identifier,
            and `lines` is a list of strings representing lines of Markdown.
        debug (str, optional): If set to "-d", debug output is printed to the console. Default is None.

    Returns:
        list: A list of HTMLnode objects where paragraph tuples are replaced by ParentNode("p", [...LeafNodes...]),
              and all other blocks or nodes are included unchanged.
    '''
    c_paragraphs = []
    for block in blocks:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            c_paragraphs.append(block)
            continue
        if block[0] == BlockType.PARAGRAPH:
            c_paragraphs.append(ParentNode("p", block_text_to_leaf_nodes(block)))
            continue
        c_paragraphs.append(block)
    debug_output(c_paragraphs, debug)
    return c_paragraphs

def convert_headings(blocks, debug=None):
    '''Converts Markdown heading blocks into ParentNode objects containing LeafNode children.

    Args:
        blocks (list): A list of elements, each either:
            - an HTMLnode (LeafNode or ParentNode), or
            - a tuple of the form (block_type, lines), where `block_type` is an enum identifier 
              and `lines` is a list of strings representing a Markdown block.
        debug (str, optional): If set to "-d", debug output is printed to the console. Default is None.

    Returns:
        list: A list of HTMLnode objects. Any heading blocks (i.e., lines starting with 1–6 '#' symbols)
              are converted to ParentNode("hX", [...LeafNodes...]), where X is the heading level.
              All other blocks are passed through unchanged.
    '''
    cp_headings = []
    for block in blocks:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            cp_headings.append(block)
            continue
        if block[0] == BlockType.HEADING:
            heading_num = len(re.findall(r"^#{1,6}", "".join(block[1]))[0])
            cp_headings.append(ParentNode(f"h{heading_num}", block_text_to_leaf_nodes(block)))
            continue
        cp_headings.append(block)
    debug_output(cp_headings, debug)
    return cp_headings

def convert_quotes(blocks, debug=None):
    '''Converts Markdown blockquote blocks into ParentNode("blockquote") objects with inline LeafNode children.

    Args:
        blocks (list): A list of elements, each either:
            - an HTMLnode (LeafNode or ParentNode), or
            - a tuple of the form (block_type, lines), where `block_type` is an enum identifier
              and `lines` is a list of strings representing a block of Markdown text.

        debug (str, optional): If set to "-d", debug output is printed to the console. Default is None.

    Returns:
        list: A list of HTMLnode objects. Blocks with block type QUOTE are transformed into 
              ParentNode("blockquote", [...LeafNodes...]), with the Markdown quote prefix (`> `) stripped.
              All other blocks are returned unchanged.
    '''
    cph_quotes = []
    for block in blocks:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            cph_quotes.append(block)
            continue
        if block[0] == BlockType.QUOTE:
            quote_lines_stripped = []
            for item in block[1]:
                quote_lines_stripped.append(item[2:] if item.startswith('> ') else item)
            stripped_block = (BlockType.QUOTE, quote_lines_stripped)
            cph_quotes.append(ParentNode("blockquote", block_text_to_leaf_nodes(stripped_block)))
            continue
        cph_quotes.append(block)
    debug_output(cph_quotes, debug)
    return cph_quotes

def convert_lists(blocks, debug=None ):
    '''Converts Markdown list blocks into structured HTMLnode list representations.

    Args:
        blocks (list): A list of elements, where each element is either:
            - an HTMLnode (LeafNode or ParentNode), or
            - a tuple of the form (block_type, lines), where `block_type` is an enum 
              indicating the type of Markdown block, and `lines` is a list of strings.

        debug (str, optional): If set to "-d", debug output is printed to the console. Default is None.

    Returns:
        list: A list of HTMLnode objects. Blocks with type ORDERED_LIST or UNORDERED_LIST are converted 
              using indentation logic into nested list structures (via `list_indentation_nodes`).
              All other blocks are returned unchanged.
    '''
    cphq_lists = []
    for block in blocks:
        if isinstance(block, (LeafNode, ParentNode, HTMLnode)):
            cphq_lists.append(block)
            continue
        if block[0] in (BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST):
            indentation_buffer = []
            for item in block[1]:
                indentation_num = len(re.findall(r"^\s*", item)[0])
                indentation_buffer.append((indentation_num, item.strip()))
            cphq_lists.append(list_indentation_nodes(indentation_buffer, debug))
            continue
        cphq_lists.append(block)
        raise Exception("Un-processed list items remaining, may require debugging.")
    debug_output(cphq_lists, debug)
    return cphq_lists

def list_indentation_nodes(blocks, debug=None):
    '''Converts a flat list of (indentation_level, line) tuples into a nested ParentNode structure.

    This function is used by `convert_lists()` to process indented Markdown list items
    (e.g., bullet points or numbered lists) and convert them into a tree of HTMLnode elements
    reflecting proper nesting based on indentation.

    Args:
        blocks (list): A list of tuples where each tuple is (indentation_level, line), with:
            - `indentation_level` (int): The number of leading spaces indicating nesting depth.
            - `line` (str): A stripped Markdown line representing a list item.
        debug (str, optional): If set to "-d", prints debug information about the nesting tree.

    Returns:
        ParentNode: A root-level ParentNode whose children represent the nested list structure,
                    composed of ParentNode and LeafNode objects according to indentation.
    '''
    nodes = [ParentNode(None, None, None)]
    nesting_stack = [0]
    for item in blocks:
        if nesting_stack[-1] == item[0]:
            if nodes[-1].tag is None:    
                nodes[-1].tag = repr(line_to_block_type(item[1]))
            children_text = text_to_textnodes(item[1])
            children_nodes = []
            for text in children_text:
                children_nodes.append(text_node_to_html_node(text))
            nodes[-1].children.extend(children_nodes)
            continue

        if item[0] > nesting_stack[-1]:
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
                if nodes[-1].tag is None:    
                    nodes[-1].tag = repr(line_to_block_type(item[1]))
                children_text = text_to_textnodes(item[1])
                children_nodes = []
                for text in children_text:
                    children_nodes.append(text_node_to_html_node(text))
                nodes[-1].children.extend(children_nodes)
            continue
    if debug == "-d": 
        print("\n************\nList Split:")
        print(nesting_stack)
        for node in nodes:
            print_tree(node)
    return nodes[0]

def print_tree(node, indent=0):
    '''Recursively prints the structure of a tree rooted at a ParentNode.

    Args:
        node (ParentNode or LeafNode): The current node to print.
        indent (int): The current depth level, used to format visual indentation.
    
    Returns:
        None: This is a debugging utility that prints directly to the console.
    '''
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

    
def debug_output(data, debug=None, label=None):
    '''Helper function for debugging - prints items in a list line by line.

    Args:
        data (list): The list of items to print to the console.
        debug (str, optional): Debug flag — if set to "-d", output is printed.
        label (str, optional): Custom label for the debug section header. If not provided, the caller's function name is used.

    Returns:
        None: This is a debugging utility that prints directly to the console 
    '''
    if debug == "-d":
        caller = inspect.stack()[1].function
        name = label or caller
        print(f"\n************\n{name}:")
        for item in data:
            print(f"\n{item}")

