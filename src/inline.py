from htmlnode import *
from textnode import *
import re


'''
***********************************************************
This function splits a text STRING into a list of TextNode objects
of the correct type as denoted by markdown syntax.
***********************************************************
old_nodes   - A LIST of TextNodes to be processed
-----------------------------------------------------------
delimiter   - A STRING used split the string into nodes
            - Valid values:
                - "`"   = Code
                - "**"  = Bold
                - "_"   = Italic
-----------------------------------------------------------
text_type   - A STRING denoting the text type
            - Valid values:
                - "TextType.CODE"   = Code
                - "TextType.BOLD"   = Bold
                - "TextType.ITALIC"  = Italic
***********************************************************
'''
def split_nodes_delimiter(old_nodes, delimiter, text_type):
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


'''
***********************************************************
Function to find markdown format images in a given string of text.
Returns a list of tuples in the format: [("alt text": "url")"]
-----------------------------------------------------------
Uses regex to match strings that fit the format ![alt text](url)
url can contain parentheses ie: ![alt text](https://example.com/image_(2)(3)(16).pdf)
-----------------------------------------------------------
- Does not handle nested parentheses ie: ![alt text](https://example.com/image_(2)(42(3))(16).pdf)
this will result in the return of an empty list []
*********************************************************** 
'''
def extract_markdown_images(text):
    found_links = re.findall(r"!\[([^\[\]]*)\]\(((?:[^()]+|\([^()]*\))+)\)",text)
    return found_links


'''
***********************************************************
Function to find markdown format links in a given STRING of text.
Returns a list of tuples in the format: [("anchor text": "url")]
-----------------------------------------------------------
Uses regex to match strings that fit the format [anchor text](url)
url can contain parentheses ie: [anchor text](https://example.com/some_stuff_(2)(3)(16))
-----------------------------------------------------------
- Does not handle nested parentheses ie: [anchor text](https://example.com/some_stuff_(2)(42(3))(16))
this will result in the return of an empty list []
*********************************************************** 
'''
def extract_markdown_links(text):
    found_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(((?:[^()]+|\([^()]*\))+)\)",text)
    return found_links


'''
***********************************************************
Function to split onjects of class TextNode, and of type TextType.TEXT
into objects of type TextType.TEXT and TextType.IMAGE, all split objects
are added to a single list to be returned. Uses extract_markdown_images()
to perform the search and split.
-----------------------------------------------------------
INPUT must be a LIST, or a LIST of LISTS, containing objects of type TextNode
-----------------------------------------------------------
RETURNS a single LIST of objects of class TextNode
***********************************************************
'''
def split_nodes_image(old_nodes):
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


'''
***********************************************************
Function to split onjects of class TextNode, and of type TextType.TEXT
into objects of type TextType.TEXT and TextType.LINK, all split objects
are added to a single list to be returned. Uses extract_markdown_links()
to perform the search and split for each object.
-----------------------------------------------------------
INPUT must be a LIST, or a LIST of LISTS, containing objects of type TextNode
-----------------------------------------------------------
RETURNS a single LIST of objects of class TextNode
***********************************************************
'''    
def split_nodes_link(old_nodes):
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
    output = []
    node = TextNode(text, TextType.TEXT)
    code_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    bold_nodes = split_nodes_delimiter(code_nodes, "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    image_nodes = split_nodes_image(italic_nodes)
    output = split_nodes_link(image_nodes)
  
    return output