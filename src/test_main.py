import unittest
from main import *

class TestMain(unittest.TestCase):

    def test_extract_title(self):
        md = "# This is a heading"
        node = extract_title(md)
        self.assertEqual(node, "This is a heading")

    def test_extract_title_inline_elements(self):
        md = "# This is a **heading** with _inline_ elements `and` such"
        node = extract_title(md)
        self.assertEqual(
            node,
            "This is a heading with inline elements and such"
        )

    def test_extract_title_not_at_top(self):
        md ="""
Here is a paragraph of text

- A list
- Of list like
    - Things

```
Some code
in a block like
fashion
```

## a heading 2

# Here's the title...

And another paragraph
"""
        node = extract_title(md)
        self.assertEqual(
            node,
            "Here's the title..."
        )

    def test_extract_title_spaces_before(self):
        md = "         # A title with preceeding spaces"

        node = extract_title(md)
        self.assertEqual(node, "A title with preceeding spaces")

    def test_extract_title_no_title(self):
        md = "There's no title to be found here..."
        self.assertRaises(Exception, extract_title, md)