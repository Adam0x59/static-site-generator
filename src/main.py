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
    generate_site("content", "public", "template.html")

    #content = extract_file_contents("test.md")
    #extract_title(content)
    pass 

def generate_site(dir_from, dir_to, template_path):
    for item in os.listdir(dir_from):
        print(item)
        src_path = os.path.join(dir_from, item)
        print(src_path)
        dst_path = os.path.join(dir_to, re.sub(r"\..*$", ".html", item))
        print(dst_path)
        if os.path.isfile(src_path):
            #print(f"file found: {item}")
            generate_page(src_path, template_path, dst_path)
            #print(f"Added {item} to '{dir_to}'\n\n'{dir_to}' now contains: {os.listdir(f'{dir_to}')}")
        else:
            #print(f"Not a file, must be a dir: {item}")
            #dir_to_make = dst_path 
            #os.mkdir(dst_path)
            generate_site(src_path, dst_path, template_path)

'''
def generate_site(content_root_dir_path, template_path, dest_path):
    # Loop through all files
    for item in os.listdir(content_root_dir_path, dest_path):
        src_path = os.path.join(content_root_dir_path, item)
        dst_path = os.path.join(dest_path, item)
        if os.path.isfile(src_path):
            #print(f"file found: {item}")
            print(f"{src_path}")
            generate_page(src_path, template_path, dest_path)
            #print(f"Added {item} to '{dir_to}'\n\n'{dir_to}' now contains: {os.listdir(f'{dir_to}')}")
        else:
            #print(f"Not a file, must be a dir: {item}")
            os.mkdir(dst_path)
            copy_one_dir_contents_to_another(src_path, dst_path) 
    pass
'''
    
def generate_page(from_path, template_path, dest_path):
    print(f"\nGenerating page from {from_path} to {dest_path}, using {template_path}")
    print(os.path.dirname(dest_path))
    md_file =extract_file_contents(from_path)
    #print(f"\n{md_file}")
    template_file = extract_file_contents(template_path)
    #print(f"\n{template_file}")
    md_file_html = markdown_to_html(md_file)
    file_html = md_file_html.to_html()
    md_file_title = extract_title(md_file)
    template_file_title_replaced = template_file.replace("{{ Title }}", md_file_title)
    template_file_content_replaced = template_file_title_replaced.replace("{{ Content }}", file_html)
    #filepath = 
    print(f"Dest-Path: {dest_path}")
    print(f"os.path.dirname: {os.path.dirname(dest_path)}")
    if os.path.exists(os.path.dirname(dest_path)):
        with open(dest_path, "w") as f:
            f.write(template_file_content_replaced)
    else:
        create_dir(os.path.dirname(dest_path))
        with open(dest_path, "w") as f:
            f.write(template_file_content_replaced)
        
    print("\n***Page Generation Success***")

def create_dir(dest_path):
    print(f"create_dir initial Dest-Path: {dest_path}")
    if os.path.exists(os.path.dirname(dest_path)):
        print(f"Dest-Path: {dest_path}")
        print(f"Dir {os.path.dirname(dest_path)} exists, creating {dest_path}")
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
    print(f"heading_found: {heading}")
    #if isinstance(heading, ParentNode) and heading.value:
    if not heading:
        raise Exception("No title found in markdown")
    heading_text = "".join(child.value for child in heading.children)
    #else:
    #    raise Exception("No title found in markdown")
    print(heading_text)
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

def rebuild_public_fs():
    if os.path.exists("public"):
        #print("path exists")
        shutil.rmtree("public")
        #print("'public' dir removed!")
    os.mkdir("public")
    #print(f"empty 'public' dir created\n\n'public' contains: {os.listdir('public')}")
    copy_one_dir_contents_to_another("static", "public")

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
