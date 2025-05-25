import unittest
from markdown_to_html import *

class TestMarkdownToHTML(unittest.TestCase):
    
    def test_markdown_to_html_debug(self):
       text = ("""
# This is a heading
               
               

     
This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
               
```
This is a code block
containing some code
```              
  
- This is the first list item in a list block
- This is a list item
- This is another list item
       """)
       markdown_to_html(text)