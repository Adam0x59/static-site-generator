import unittest
from block_markdown import *

class TestInline(unittest.TestCase):
    
    def test_markdown_to_blocks_debug(self):
       text = ("""
# This is a heading

               
               


This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
       """)
       print("\n")
       print(text)
       node = markdown_to_blocks(text)
       self.assertEqual([
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n"\
            "- This is a list item\n"\
            "- This is another list item"
            ], node)




if __name__ == "__main__":
    unittest.main()