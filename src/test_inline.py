import unittest
from src.inline import *

class TestInline(unittest.TestCase):

    ''' # This is a debugging test - Not a valid unit test
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code` block, Here's `another` one! And `another`", TextType.TEXT)
        node2 = TextNode("`This is` text with a **bold** block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        new_nodes_bold = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
    '''

    # Test split_nodes_delim: String with one bold word.
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    # Test split_nodes_delim: String wit two bold words, string ends with delim.
    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    # Test split_nodes_delim: String with multi word bold section and single bold word, string ends with delim.
    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    # Test split_nodes_delim: String with italic word.
    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    # Test split_nodes_delim: String with bold and italic words, Look for bold first, pass result straight into italic lookup.
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    # Test split_nodes_delim: String with code block.
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    '''
    def test_debug_extract_md_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        print(extract_markdown_images(text))

    def test_debug_extract_md_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        print(extract_markdown_links(text))
    '''
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_broken_format(self):
        broken = extract_markdown_images(
            "Here is some text and a ![broken(https://image.link), which should not match"
        )
        self.assertNotEqual([("broken", "https://image.link")], broken)

    def test_extract_markdown_link_broken_format(self):
        broken = extract_markdown_images(
            "Here is some text and a [broken(https://link.link), which should not match"
        )
        self.assertNotEqual([("broken", "https://link.link")], broken)

    def test_extract_markdown_link_incorrect_format(self):
        incorrect = extract_markdown_links(
            "Here is some text with a ![incorrect](https://link-pretending-to-be-an.image), which should not match"
        )
        self.assertNotEqual([("incorrect", "https://link-pretending-to-be-an.image")], incorrect)

    def test_extract_markdown_image_incorrect_format(self):
        incorrect = extract_markdown_links(
            "Here is some text with a [incorrect](https://image-pretending-to-be-an.link), which should not match"
        )
        self.assertNotEqual([("incorrect", "https://link-pretending-to-be-an.image")], incorrect)
    
    def test_extract_markdown_image_multi(self):
        find_both = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)" \
            "and This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], find_both)
    
    def test_extract_markdown_link_multi(self):
        find_both = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)" \
            "and This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], find_both)

    def test_extract_markdown_chained_image_link(self):
        find_links = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)" \
            "and This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        find_images = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)" \
            "and This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        find_images.extend(find_links)
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"), ("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], find_images)

    def test_extract_markdown_image_no_alt_text(self):
        incorrect = extract_markdown_images(
            "Here is some text with a ![](https://image.empty-alt-text), which should match"
        )
        self.assertEqual([("", "https://image.empty-alt-text")], incorrect)

    def test_extract_markdown_link_no_anchor_text(self):
        incorrect = extract_markdown_links(
            "Here is some text with a [](https://link.empty-anchor-text), which should match"
        )
        self.assertEqual([("", "https://link.empty-anchor-text")], incorrect)

    
if __name__ == "__main__":
    unittest.main()