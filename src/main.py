# Import all classes and functions from textnode and htmlnode modules.
from textnode import *
from htmlnode import *
from markdown_to_html import *
import os
import shutil
import sys

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

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    
    generate_site("content", "docs", "template.html")
    #generate_site("basepath ")

    #content = extract_file_contents("test.md")
    #extract_title(content)
    pass 

def generate_site(basepath, dir_to, template_path):
    rebuild_fs(dir_to)
    for item in os.listdir(basepath):
        #print(item)
        src_path = os.path.join(basepath, item)
        #print(src_path)
        dst_path = os.path.join(dir_to, re.sub(r"\..*$", ".html", item))
        #print(dst_path)
        if os.path.isfile(src_path):
            generate_page(src_path, template_path, dst_path)
        else:
            generate_site(src_path, dst_path, template_path)
    
def generate_page(basepath, template_path, dest_path):
    md_file =extract_file_contents(basepath)
    template_file = extract_file_contents(template_path)
    md_file_html = markdown_to_html(md_file)
    file_html = md_file_html.to_html()
    md_file_title = extract_title(md_file)
    template_file_title_replaced = template_file.replace("{{ Title }}", md_file_title)
    template_file_content_replaced = template_file_title_replaced.replace("{{ Content }}", file_html)
    template_file_href_replace = template_file_content_replaced.replace("href\"/", "href\"{basepath}")
    template_file_src_replace = template_file_href_replace.replace("src\"/", "src\"{basepath}")
    if os.path.exists(os.path.dirname(dest_path)):
        with open(dest_path, "w") as f:
            f.write(template_file_href_replace)
    else:
        create_dir(os.path.dirname(dest_path))
        with open(dest_path, "w") as f:
            f.write(template_file_src_replace)
    

def create_dir(dest_path):
    #print(f"create_dir initial Dest-Path: {dest_path}")
    if os.path.exists(os.path.dirname(dest_path)):
        #print(f"Dest-Path: {dest_path}")
        #print(f"Dir {os.path.dirname(dest_path)} exists, creating {dest_path}")
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
    else:
        create_dir(os.path.dirname(dest_path))
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
    

def extract_file_contents(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def extract_title(markdown):
    html_node = markdown_to_html(markdown)
    heading = find_title(html_node)
    #print(f"heading_found: {heading}")
    #if isinstance(heading, ParentNode) and heading.value:
    if not heading:
        raise Exception("No title found in markdown")
    heading_text = "".join(child.value for child in heading.children)
    #else:
    #    raise Exception("No title found in markdown")
    #print(heading_text)
    return heading_text


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
    raise Exception("No title found in markdown")

            
    pass

def rebuild_fs(dir_to):
    if os.path.exists(dir_to):
        #print("path exists")
        shutil.rmtree(dir_to)
        #print("'public' dir removed!")
    os.mkdir(dir_to)
    #print(f"empty 'public' dir created\n\n'public' contains: {os.listdir('public')}")
    copy_one_dir_contents_to_another("static", dir_to)

def copy_one_dir_contents_to_another(dir_from, dir_to):
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
            copy_one_dir_contents_to_another(src_path, dst_path)
    

# Only run the main function if this file is executed directly.
if __name__ == "__main__":
    main()
