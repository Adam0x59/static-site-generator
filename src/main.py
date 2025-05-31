# Import all classes and functions from textnode and htmlnode modules.
from textnode import *
from htmlnode import *
from markdown_to_html import *
import os
import shutil

# Sanity check - if required - Yes main runs.
# print("hello world")

# Main loop
def main ():
    # Example test for __eq__ in TextNode.
    # This is now covered by unit tests, so the code is commented out.
    '''
    text_node_test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    text_node_test2 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node_test)
    print(text_node_test == text_node_test2)
    '''
    rebuild_public_fs()
    content = extract_file_contents("test.md")
    extract_title(content)
    pass 

def extract_file_contents(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def extract_title(markdown):
    html_node = markdown_to_html(markdown)
    heading = find_title(html_node)
    print(f"heading_found: {heading}")
    heading_text = "".join(child.value for child in heading.children)
    print(heading_text)


def find_title(node):
    if isinstance(node, list):  # if a list, iterate over it
        for child in node:
            result = find_title(child)
            if result:
                return result
        return None

    if hasattr(node, "tag") and node.tag == "h1":
        return node

    if hasattr(node, "children"):
        return find_title(node.children)
    
    raise Exception

            
    pass

def rebuild_public_fs():
    if os.path.exists("public"):
        #print("path exists")
        shutil.rmtree("public")
        #print("'public' dir removed!")
    os.mkdir("public")
    #print(f"empty 'public' dir created\n\n'public' contains: {os.listdir('public')}")
    copy_static_contents_to_public("static", "public")

def copy_static_contents_to_public(dir_from, dir_to):
    for item in os.listdir(dir_from):
        src_path = os.path.join(dir_from, item)
        dst_path = os.path.join(dir_to, item)
        if os.path.isfile(src_path):
            #print(f"file found: {item}")
            shutil.copy(src_path, dst_path)
            #print(f"Added {item} to '{dir_to}'\n\n'{dir_to}' now contains: {os.listdir(f'{dir_to}')}")
        else:
            #print(f"Not a file, must be a dir: {item}")
            os.mkdir(dst_path)
            copy_static_contents_to_public(src_path, dst_path)
    

# Only run the main function if this file is executed directly.
if __name__ == "__main__":
    main()
