import unittest
from markdown_to_html import *

class TestMarkdownToHTML(unittest.TestCase):
    
    def test_markdown_to_html_debug(self):
       text = ("""
# This is a heading with some **bold**, and _Italic_
               
###### This ia a H6 # title

     
This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
               
```
This is a code block
containing some code
```              
  
- This is the first list item in a list block
- This is a list item
- This is another list item
This is a paragraph
                
### This is a heading H3
                
- List item 1
- List item 2
    - Indented list item 1
       - Second indented list item 1
              1. ol_item 1
              2. ol_item 2
              3. ol_item 3
    - Indented list item 2
- List item 3

Paragrah after a list block
                
```
# This is a code block

This is a paragraph in a code block
- List item 1
- List item 2

> Quote inside code block
```

Paragraph after a code block.

> This is a quote block
> Another line in a quote block
> And another

Paragraph after a quote block  
       """)
       markdown_to_html(text)