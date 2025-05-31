import unittest
from markdown_to_html import *

class TestMarkdownToHTML(unittest.TestCase):
    '''
    def test_markdown_to_html_debug(self):
        text = ("""
# This is a heading with some **bold**, and _Italic_
               
###### This ia a H6 # title

     
This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
               
```
This is a code block
containing some code
```              
  
- This is the first list **item** in a list block
- This is a list item
- This is another list item
This is a paragraph
                
### This is a heading H3
                
- List item 1
- List item 2
    - Indented list item 1
        - Second indented list item 1
            1. ol-item 1
            2. ol-item 2
            3. ol-item 3
    - Indented list item 2
- List item 3

Paragrah after a list block
               
1. Ordered List 1
2. Ordered List 2
3. Ordered List 3
                
3. New ordered list
    - With Nesting
        - And more
            1. Some more OL
            2. More OL
4. New ordered list
            - orphan Tag
               
```
# This is a code block

This is a paragraph in a code block
- List item 1
- List item 2

> Quote inside code block
```
               
3. OL out of order 1
7. OL out of order 2
5. OL out of order 3

Paragraph after a code block.

> This is a quote block
> with **bold text** and _italic text_
> Another line in a quote block
> And another

Paragraph after a quote block  
       """)
        markdown_to_html(text)
    '''

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
       
        node = markdown_to_html(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
"""
        node = markdown_to_html(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        )

    def test_unordered_list(self):
        md = """
- Item one with _italic_
- Item two with **bold**
- Item three with `code`
"""
        node = markdown_to_html(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><ul><li>Item one with <i>italic</i></li><li>Item two with <b>bold</b></li><li>Item three with <code>code</code></li></ul></div>"
        )

    def test_ordered_nested_list(self):
        md = """
1. First item
2. Second item
    - Nested item one
    - Nested item two
3. Third item
"""
        node = markdown_to_html(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item<ul><li>Nested item one</li><li>Nested item two</li></ul></li><li>Third item</li></ol></div>"
        )

    def test_blockquote(self):
        md = """
> This is a quote with **bold**
> and _italic_ on the next line
"""
        node = markdown_to_html(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b><br>and <i>italic</i> on the next line<br></blockquote></div>"
        )

    def test_mixed_content(self):
        md = """
# Title

This is a paragraph with `code`.

- List item 1
- List item 2

Another paragraph here.
"""
        node = markdown_to_html(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>This is a paragraph with <code>code</code>.</p><ul><li>List item 1</li><li>List item 2</li></ul><p>Another paragraph here.</p></div>"
        )