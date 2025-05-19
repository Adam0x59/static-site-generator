from htmlnode import *
from textnode import *
import re

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

def extract_markdown_images(text):
    found_links = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return found_links

def extract_markdown_links(text):
    found_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return found_links