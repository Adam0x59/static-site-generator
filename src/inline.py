from htmlnode import *
from textnode import *
import re

'''
***********************************************************
This function splits a text string into a list of nodes
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

def extract_markdown_images(text):
    found_links = re.findall(r"!\[([^\[\]]*)\]\(((?:[^()]+|\([^()]*\))+)\)",text)
    return found_links

def extract_markdown_links(text):
    found_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(((?:[^()]+|\([^()]*\))+)\)",text)
    return found_links

def split_nodes_image(old_nodes):
    # Create a list to store new nodes found
    new_nodes = []
    # Iterate through old nodes
    for old_node in old_nodes:
        # Create an empty list to store found images
        images = []
        # Search current old node for image links, add any found to end of images list.
        images.extend(extract_markdown_images(old_node.text))
        # if no images are found append current old node to end of new nodes list. 
        if images == []:
            new_nodes.append(old_node)
            # Return to outer for-loop - move on to next iteration
            continue
        # Copy text from current old node into to_split variable
        to_split = old_node.text
        # Iterate through any image links in images list
        for i in range(len(images)):
            # Use buffer list to store current split. 
            buffer_list = to_split.split(f"![{images[i][0]}]({images[i][1]})", 1)
            # Update to_split to value of second string in buffer list
            to_split = buffer_list.pop(1)
            # If first item in buffer list is zero append current image object to new_nodes
            # as there is no text preceeding it.
            if buffer_list[0] == "":
                new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                # Return to outer for-loop - move on to next iteration
                continue
            # If first item in buffer is not an empty string, extend new_nodes.
            new_nodes.extend([
                # First add the preceding string as a text object
                TextNode(buffer_list[0], TextType.TEXT),
                # Next add current image object
                TextNode(images[i][0], TextType.IMAGE, images[i][1])
                ])
            # If we are on the final iteration
            if i == len(images) - 1:
                # Check that to_split is not empty.
                if to_split != "":
                    # If not empty we need to append it's contents to new_nodes as a text object
                    new_nodes.append(TextNode(to_split, TextType.TEXT))
                else:
                    # If empty - Return to outer for-loop - move on to next iteration
                    continue
    # When done iterating, return new_nodes
    return new_nodes
    
def split_nodes_link(old_nodes):
    # Create a list to store new nodes found
    new_nodes = []
    # Iterate through old nodes
    for old_node in old_nodes:
        # Create an empty list to store found images
        links = []
        # Search current old node for image links add any found to end of images list
        links.extend(extract_markdown_links(old_node.text))
        #print(extract_markdown_links(old_node.text))
        # if no images are found append current old node to end of new nodes list. 
        if links == []:
            new_nodes.append(old_node)
            # Return to outer for-loop - move on to next iteration
            continue
        # Copy text from current old node into to_split variable
        to_split = old_node.text
        # Iterate through any image links in images list
        for i in range(len(links)):
            # Use buffer list to store current split. 
            buffer_list = to_split.split(f"[{links[i][0]}]({links[i][1]})", 1)
            # Update to_split to value of second string in buffer list
            to_split = buffer_list.pop(1)
            # If first item in buffer list is zero append current image object to new_nodes
            # as there is no text preceeding it.
            if buffer_list[0] == "":
                new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                # Return to outer for-loop - move on to next iteration
                continue
            # If first item in buffer is not an empty string, extend new_nodes.
            new_nodes.extend([
                # First add the preceding string as a text object
                TextNode(buffer_list[0], TextType.TEXT),
                # Next add current image object
                TextNode(links[i][0], TextType.LINK, links[i][1])
                ])
            # If we are on the final iteration
            if i == len(links) - 1:
                # Check that to_split is not empty.
                if to_split != "":
                    # If not empty we need to append it's contents to new_nodes as a text object
                    new_nodes.append(TextNode(to_split, TextType.TEXT))
                else:
                    # If empty - Return to outer for-loop - move on to next iteration
                    continue
    # When done iterating, return new_nodes
    return new_nodes
    
def text_to_nodes(text):
    
    pass