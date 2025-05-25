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
       #print("\n")
       #print(text)
       node = markdown_to_blocks(text)
       self.assertEqual([
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n"\
            "- This is a list item\n"\
            "- This is another list item"
            ], node)
       
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_code(self):
        block = block_to_block_type("```\n##     Heading 2\n Some code\n```")
        self.assertEqual(BlockType.CODE, block)

    def test_block_to_block_type_code_missing_end(self):
        block = block_to_block_type("```Here is some code missing an end value")
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_block_to_block_type_code_missing_start(self):
        block = block_to_block_type("Here is some code missing the start```")
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_block_to_block_type_code_wrong_numbers(self):
        block = block_to_block_type("``code block with wrong number of ticks``")
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_block_to_block_type_quote(self):
        block = block_to_block_type("> ```\n>##     Heading 2 \n> Some code\n> ```\n> Some quote")
        self.assertEqual(BlockType.QUOTE, block)
    
    def test_block_to_block_type_quote_missing_one(self):
        block = block_to_block_type(">This is a quote\n This line is missing a quote \n> back to quote")
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_block_to_block_type_uolist(self):
        block = block_to_block_type("- List item 1\n-   list item 2\n-     List item 3")
        self.assertEqual(BlockType.UNORDERED_LIST, block)

    def test_block_to_block_type_uolist_missing_one(self):
        block = block_to_block_type("- Item 1\n- item 2\n item 3")
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_block_to_block_type_olist(self):
        block = block_to_block_type("1. List item 1\n2. list item 2\n3.   List item 3\n4. List item 4")
        self.assertEqual(BlockType.ORDERED_LIST, block)

    def test_block_to_block_type_olist_incorrect_numbering(self):
        block = block_to_block_type("1. this is item 1\n2. this is item 2\n4. this is item 3")
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_block_to_block_type_olist_missing_number(self):
        block = block_to_block_type("1. this is item 1\n . Item 2\n3. item 3")
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_block_to_block_type_paragraph(self):
        block = block_to_block_type("This is a paragraph\n With multiple lines\nHere's a third")
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_block_to_block_type_heading(self):
        block = block_to_block_type("# This is a heading")
        self.assertEqual(BlockType.HEADING, block)

    def test_block_to_block_type_heading_three(self):
        block = block_to_block_type("### Heading 3")
        self.assertEqual(BlockType.HEADING, block)

    def test_block_to_block_type_heading_six(self):
        block = block_to_block_type("###### Heading 6")
        self.assertEqual(BlockType.HEADING, block)

    def test_block_to_block_type_heading_no_space(self):
        block = block_to_block_type("#Heading no space")
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_block_to_block_type_heading_too_many(self):
        block = block_to_block_type("############### Toooo Many")
        self.assertEqual(BlockType.PARAGRAPH, block)

    def test_block_to_block_type_all_the_headings(self):
        block = block_to_block_type("# All\n## The\n### Headings\n#### Thats enough")
        self.assertEqual(BlockType.HEADING,block)

    def test_block_to_block_type_order_of_ops(self):
        block = block_to_block_type(">```# This should be a quote block\n>-regardless of the content\n>1.even lists\n>2. like this")
        self.assertEqual(BlockType.QUOTE, block)

    def test_block_to_block_type_order_of_ops_code_inner_no_escape(self):
        block = block_to_block_type("```\nThis should be a code block```this should not```\n# this is a comment not heading\n- Listy\n- list\n1. Oh-list\n2. such list...\n```")
        self.assertEqual(BlockType.CODE, block)

    def test_block_to_block_type_lists_mixed(self):
        block = block_to_block_type("- This\n- be\n- a F'n\1. Mixed\n2. List!")
        self.assertEqual(BlockType.PARAGRAPH, block)
        #returns pgraph -list mix invalid

    def test_block_to_block_type_lists_mixed_reverse(self):
        block = block_to_block_type("1. This\n2. be\n3. a F'n\n- Mixed\n- List!")
        self.assertEqual(BlockType.PARAGRAPH, block)
        #returns pgraph -list mix invalid

    def test_block_to_text_node_debug(self):
        block = (BlockType.HEADING, "# Heading 1")
        block2 = (BlockType.HEADING, "## Heading 2")
        block6 = (BlockType.HEADING, "###### Heading 6")
        print(block_to_text_node(block))
        print(block_to_text_node(block2))
        print(block_to_text_node(block6))


if __name__ == "__main__":
    unittest.main()