from textnode import *
from htmlnode import *

print("hello world")

def main ():
    text_node_test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    text_node_test2 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node_test)
    print(text_node_test == text_node_test2)
    

if __name__ == "__main__":
    main()