# Import all classes and functions from textnode and htmlnode modules.
from textnode import *
from htmlnode import *

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
    pass # Placeholder to indicate intentional no-op

# Only run the main function if this file is executed directly.
if __name__ == "__main__":
    main()