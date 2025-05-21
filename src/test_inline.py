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

    '''
    def test_split_nodes_image_debug(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        node2 = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        split_nodes_image([node, node2])
    '''

    def test_split_nodes_imade_not_textnode_bold(self):
        node = split_nodes_image([TextNode("Some Bold Text", TextType.BOLD)])
        self.assertEqual([TextNode("Some Bold Text", TextType.BOLD)], node)

    def test_split_nodes_imade_not_textnode_italic(self):
        node = split_nodes_image([TextNode("Some italic text", TextType.ITALIC)])
        self.assertEqual([TextNode("Some italic text", TextType.ITALIC)], node)

    def test_split_nodes_imade_not_textnode_code(self):
        node = split_nodes_image([TextNode("Some code", TextType.CODE)])
        self.assertEqual([TextNode("Some code", TextType.CODE)], node)

    def test_split_nodes_image_no_links(self):
        node = split_nodes_image([
            TextNode(
            "Here is a string containing no links",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Here is a string containing no links", TextType.TEXT)
        ], node)

    def test_split_nodes_image_tl_no_il(self):
        node = split_nodes_image([
            TextNode(
            "Here is a string containing a text link but no image [Text Link](https://This-is-a-text.link)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Here is a string containing a text link but no image [Text Link](https://This-is-a-text.link)", TextType.TEXT)
        ], node)

    def test_split_nodes_image_empty_string(self):
        node = split_nodes_image([
            TextNode(
            "",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("", TextType.TEXT)
        ], node)

    def test_split_nodes_image_empty_old_nodes_list(self):
        node = split_nodes_image([
            #This is an empty list
        ])
        self.assertEqual([
            # Expecting an empty list
        ], node)
    
    def test_split_nodes_just__one_image_link(self):
        node = split_nodes_image([
            TextNode(
            "![Image](https://This-is-a-image.link)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Image", TextType.IMAGE, "https://This-is-a-image.link")
        ], node)

    def test_split_nodes_image_just_image_links(self):
        node = split_nodes_image([
            TextNode(
            "![Image](https://This-is-a-image.link)![Image-2](https://This-is-image-2.link)![Image Three](https://This-is-image_three.link)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Image", TextType.IMAGE, "https://This-is-a-image.link"),
            TextNode("Image-2", TextType.IMAGE, "https://This-is-image-2.link"),
            TextNode("Image Three", TextType.IMAGE, "https://This-is-image_three.link")
        ], node)

    def test_split_nodes_image_image_links_and_text_links(self):
        node = split_nodes_image([
            TextNode(
            "![Image](https://This-is-a-image.link)[Text Link](https://This-is-a-text.link)![Image-2](https://This-is-image-2.link)[Text Link](https://This-is-a-text.link)![Image Three](https://This-is-image_three.link)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Image", TextType.IMAGE, "https://This-is-a-image.link"),
            TextNode("[Text Link](https://This-is-a-text.link)", TextType.TEXT),
            TextNode("Image-2", TextType.IMAGE, "https://This-is-image-2.link"),
            TextNode("[Text Link](https://This-is-a-text.link)", TextType.TEXT),
            TextNode("Image Three", TextType.IMAGE, "https://This-is-image_three.link")
        ], node)

    def test_split_nodes_images_surrounded_text(self):
        node = split_nodes_image([
            TextNode(
            "Here is an image link: ![Image](https://This-is-a-image.link) Here is one more! ![Image-2](https://This-is-image-2.link) ![Go on have a third!] ![Image Three](https://This-is-image_three.link), (Some text to close off.)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Here is an image link: ", TextType.TEXT),
            TextNode("Image", TextType.IMAGE, "https://This-is-a-image.link"),
            TextNode(" Here is one more! ", TextType.TEXT),
            TextNode("Image-2", TextType.IMAGE, "https://This-is-image-2.link"),
            TextNode(" ![Go on have a third!] ", TextType.TEXT),
            TextNode("Image Three", TextType.IMAGE, "https://This-is-image_three.link"),
            TextNode(", (Some text to close off.)", TextType.TEXT)
        ], node)

    def test_split_nodes_images_text_open_close_with_images(self):
        node = split_nodes_image([
            TextNode(
            "![Image](https://This-is-a-image.link) Here is one more! ![Image-2](https://This-is-image-2.link) ![Go on have a third!] ![Image Three](https://This-is-image_three.link)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Image", TextType.IMAGE, "https://This-is-a-image.link"),
            TextNode(" Here is one more! ", TextType.TEXT),
            TextNode("Image-2", TextType.IMAGE, "https://This-is-image-2.link"),
            TextNode(" ![Go on have a third!] ", TextType.TEXT),
            TextNode("Image Three", TextType.IMAGE, "https://This-is-image_three.link"),
        ], node)

    def test_split_nodes_image_duplicate_links(self):
        node = split_nodes_image([
            TextNode(
            "![Image](https://link.com) and again ![Image](https://link.com)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Image", TextType.IMAGE, "https://link.com"),
            TextNode(" and again ", TextType.TEXT),
            TextNode("Image", TextType.IMAGE, "https://link.com")
        ], node)

    def test_split_nodes_image_empty_alt_text(self):
        node = split_nodes_image([
            TextNode(
            "![](https://empty-alt.com)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("", TextType.IMAGE, "https://empty-alt.com")
        ], node)

    def test_split_nodes_image_broken_syntax(self):
        node = split_nodes_image([
            TextNode(
            "![Broken(image.com)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("![Broken(image.com)", TextType.TEXT)
        ], node)
     
    def test_split_nodes_image_fake_image_link(self):
        node = split_nodes_image([
            TextNode(
            "Look at this: ![Fake](not a real link",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Look at this: ![Fake](not a real link", TextType.TEXT)
        ], node)

    def test_split_nodes_image_existing_image_node(self):
        node = split_nodes_image([
            TextNode("Image", TextType.IMAGE, "https://image.com")
        ])
        self.assertEqual([
            TextNode("Image", TextType.IMAGE, "https://image.com")
        ], node)

    def test_split_nodes_image_inline_image_in_sentence(self):
        node = split_nodes_image([
            TextNode(
            "Here's an ![inline](https://image.com) image.",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Here's an ", TextType.TEXT),
            TextNode("inline", TextType.IMAGE, "https://image.com"),
            TextNode(" image.", TextType.TEXT)
        ], node)

    def test_split_nodes_image_trailing_image(self):
        node = split_nodes_image([
            TextNode(
            "This is a test ![img](https://img.com)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("This is a test ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://img.com")
        ], node)

    
    def test_split_nodes_image_url_with_parentheses(self):
        node = split_nodes_image([
            TextNode(
            "![Alt](https://example.com/image_(1).png)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Alt", TextType.IMAGE, "https://example.com/image_(1).png")
        ], node)
    
    '''
    def test_split_nodes_links_just_links(self):
        node = split_nodes_link([
            TextNode(
            "[Image](https://This-is-a-image.link)[Image-2](https://This-is-image-2.link)[Image Three](https://This-is-image_three.link)",
            TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Image", TextType.LINK, "https://This-is-a-image.link"),
            TextNode("Image-2", TextType.LINK, "https://This-is-image-2.link"),
            TextNode("Image Three", TextType.LINK, "https://This-is-image_three.link")
        ], node)
    '''
    def test_split_nodes_links_not_textnode_bold(self):
        node = split_nodes_link([TextNode("Some Bold Text", TextType.BOLD)])
        self.assertEqual([TextNode("Some Bold Text", TextType.BOLD)], node)

    def test_split_nodes_links_not_textnode_italic(self):
        node = split_nodes_link([TextNode("Some italic text", TextType.ITALIC)])
        self.assertEqual([TextNode("Some italic text", TextType.ITALIC)], node)

    def test_split_nodes_links_not_textnode_code(self):
        node = split_nodes_link([TextNode("Some code", TextType.CODE)])
        self.assertEqual([TextNode("Some code", TextType.CODE)], node)

    def test_split_nodes_links_no_links(self):
        node = split_nodes_link([
            TextNode(
                "Here is a string containing no links",
                TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Here is a string containing no links", TextType.TEXT)
        ], node)

    def test_split_nodes_links_tl_no_il(self):
        node = split_nodes_link([
            TextNode(
                "Here is a string containing a text link but no image [Text Link](https://This-is-a-text.link)",
                TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Here is a string containing a text link but no image ", TextType.TEXT),
            TextNode("Text Link", TextType.LINK, "https://This-is-a-text.link")
        ], node)

    def test_split_nodes_links_empty_string(self):
        node = split_nodes_link([
            TextNode(
                "",
                TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("", TextType.TEXT)
        ], node)

    def test_split_nodes_links_empty_old_nodes_list(self):
        node = split_nodes_link([
            # This is an empty list
        ])
        self.assertEqual([
            # Expecting an empty list
        ], node)

    def test_split_nodes_links_just_one_link(self):
        node = split_nodes_link([
            TextNode(
                "[Link](https://example.com)",
                TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Link", TextType.LINK, "https://example.com")
        ], node)

    def test_split_nodes_links_just_links(self):
        node = split_nodes_link([
            TextNode(
                "[Link1](https://example.com/1)[Link2](https://example.com/2)[Link3](https://example.com/3)",
                TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Link1", TextType.LINK, "https://example.com/1"),
            TextNode("Link2", TextType.LINK, "https://example.com/2"),
            TextNode("Link3", TextType.LINK, "https://example.com/3")
        ], node)

    def test_split_nodes_links_text_and_links(self):
        node = split_nodes_link([
            TextNode(
                "Start [Link1](https://example.com/1) middle [Link2](https://example.com/2) end.",
                TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Start ", TextType.TEXT),
            TextNode("Link1", TextType.LINK, "https://example.com/1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("Link2", TextType.LINK, "https://example.com/2"),
            TextNode(" end.", TextType.TEXT)
        ], node)

    
    def test_split_nodes_links_with_parentheses_in_url(self):
        node = split_nodes_link([
            TextNode(
                "[Alt](https://example.com/image_(1).pdf)",
                TextType.TEXT
            ),
            TextNode(
                "[Alt](https://example.com/image_(2)(3)(16).pdf)",
                TextType.TEXT
            )
        ])
        self.assertEqual([
            TextNode("Alt", TextType.LINK, "https://example.com/image_(1).pdf"),
            TextNode("Alt", TextType.LINK, "https://example.com/image_(2)(3)(16).pdf")
        ], node)
    

if __name__ == "__main__":
    unittest.main()