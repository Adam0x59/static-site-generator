"""Module for processing inline markdown into TextNode objects."""

from htmlnode import *
from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Split text nodes into formatted types based on a given delimiter.

    Args:
        old_nodes (list): List of TextNode objects to be processed.
        delimiter (str): Delimiter string to split the text.
                         Valid values: "`" for CODE, "**" for BOLD, "_" for ITALIC.
        text_type (TextType): The TextType to assign to the split content.

    Returns:
        list: List of TextNode objects with appropriate text types.
    """
    # List to store new nodes
    new_nodes = []
    # Iterate through items(old_node) in old_nodes list
    for old_node in old_nodes:
        # If old_node is not object of type TextType.TEXT add to new node list as is.
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # Buffer list for split nodes
        split_nodes = []
        # Split the text of old_nodes into a list, splitting on the delimiters
        sections = old_node.text.split(delimiter)
        # Raise an error if sections lenght is an even number (indicates that it contains a non-closed delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        # Iterate through each item in the sections list
        for i in range(len(sections)):
            # If item is an empty string, ignore it and move onto the next
            if sections[i] == "":
                continue
            # If item has an even index number add to split_nodes as a text item.
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            # If item has an odd index number add to split_nodes as an item of type "text_type"
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        # When done iterating through sections list, extend new_nodes list with split_nodes list.
        #print(f"\n{new_nodes}")
        new_nodes.extend(split_nodes)
    # When done iterating through old_nodes list, return new_nodes
    #print(f"\n{new_nodes}")
    return new_nodes

def extract_markdown_images(text):
    """Extract markdown image syntax from a string.

    Matches patterns like ![alt text](url) and handles URLs with parentheses.

    Args:
        text (str): Input text string.

    Returns:
        list of tuple: List of (alt_text, url) tuples for each image found.

    Note:
        Does not handle nested parentheses in the URL.
    """
    found_links = re.findall(r"!\[([^\[\]]*)\]\(((?:[^()]+|\([^()]*\))+)\)",text)
    return found_links

def extract_markdown_links(text):
    """Extract markdown link syntax from a string.

    Matches patterns like [anchor text](url) and handles URLs with parentheses.

    Args:
        text (str): Input text string.

    Returns:
        list of tuple: List of (anchor_text, url) tuples for each link found.

    Note:
        Does not handle nested parentheses in the URL.
    """
    found_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(((?:[^()]+|\([^()]*\))+)\)",text)
    return found_links

def split_nodes_image(old_nodes):
    """Split TextNode objects with markdown image syntax into TEXT and IMAGE types.

    Args:
        old_nodes (list): List of TextNode objects.

    Returns:
        list: List of TextNode objects split by image markdown.
    """
    # List to hold the resulting TextNode objects after splitting
    new_nodes = []

    # Iterate through each input node
    for old_node in old_nodes:
        # If the node is not of type TEXT, pass it through unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Extract any markdown-style image links from the text
        images = extract_markdown_images(old_node.text)

        # If no images are found, add the node as-is
        if not images:
            new_nodes.append(old_node)
            continue

        # Start with the full text of the node to be split
        to_split = old_node.text

        # For each image found, split the text at the image markdown
        for alt_text, url in images:
            # Split the text at the first occurrence of the image markdown
            parts = to_split.split(f"![{alt_text}]({url})", 1)
            # Update the remaining text to be processed
            to_split = parts[1]

            if parts[0] == "":
                # No text before the image — just add the image node
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                continue

            # Add both the preceding text and the image as separate nodes
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

        # After all images are processed, add any remaining text
        if to_split:
            new_nodes.append(TextNode(to_split, TextType.TEXT))

    # Return the list of new nodes, now split into text and image parts
    return new_nodes

def split_nodes_link(old_nodes):
    """Split TextNode objects with markdown link syntax into TEXT and LINK types.

    Args:
        old_nodes (list): List of TextNode objects.

    Returns:
        list: List of TextNode objects split by link markdown.
    """
    # List to hold the resulting TextNode objects after splitting
    new_nodes = []

    # Iterate through each input node
    for old_node in old_nodes:
        # If the node is not of type TEXT, pass it through unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Extract any markdown-style links from the text
        links = extract_markdown_links(old_node.text)

        # If no links are found, add the node as-is
        if not links:
            new_nodes.append(old_node)
            continue

        # Start with the full text of the node to be split
        to_split = old_node.text

        # For each link found, split the text at the link markdown
        for anchor_text, url in links:
            # Split the text at the first occurrence of the link markdown
            parts = to_split.split(f"[{anchor_text}]({url})", 1)
            # Update the remaining text to be processed
            to_split = parts[1]

            if parts[0] == "":
                # No text before the link — just add the image node
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                continue

            # Add both the preceding text and the link as separate nodes
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

        # After all links are processed, add any remaining text
        if to_split:
            new_nodes.append(TextNode(to_split, TextType.TEXT))

    # Return the list of new nodes, now split into text and link parts
    return new_nodes
    
def text_to_textnodes(text):
    """Convert a markdown-formatted string to a list of TextNode objects.
    Applies processing for code, bold, italic, image, and link syntax.

    Args:
        text (str): Markdown-formatted text.

    Returns:
        list: List of TextNode objects with appropriate types.
    """
    output = []
    node = TextNode(text, TextType.TEXT)
    code_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    bold_nodes = split_nodes_delimiter(code_nodes, "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    image_nodes = split_nodes_image(italic_nodes)
    output = split_nodes_link(image_nodes)
  
    return output