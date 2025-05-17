from enum import Enum
from htmlnode import *

# Enum representing different types of text formatting.
# Each member maps to a Markdown-style representation.
class TextType(Enum):
	TEXT = "normal text"
	BOLD = "**bold**"
	ITALIC = "_italic_"
	CODE = "`code`"
	LINK = "[anchor text](URL)"
	IMAGE = "[alt text](URL)"

# A class representing a segment of formatted text, possibly with a link or image URL.
class TextNode:
	def __init__(self, text, text_type, url=None):
		# Plaintext content of text node
		self.text = text
		# Formatting type, types defined in TextType enum
		self.text_type = text_type
		# Optional URL for links or images; None for other types.
		self.url = url


	# Define equality between two TextNode instances.
	# Two nodes are equal if their text, type, and URL are all equal.
	def __eq__(self, other):
		return(
			self.text == other.text and
			self.text_type == other.text_type and
			self.url == other.url
		)
	
	# Return a readable string representation of the TextNode instance,
	# useful for debugging and logging.
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
	if text_node.text_type == TextType.TEXT:
		return LeafNode(None, text_node.text)
	elif text_node.text_type == TextType.BOLD:
		return LeafNode("b", text_node.text)
	elif text_node.text_type == TextType.ITALIC:
		return LeafNode("i", text_node.text)
	elif text_node.text_type == TextType.CODE:
		return LeafNode("code", text_node.text)
	elif text_node.text_type == TextType.LINK:
		return LeafNode("a", text_node.text, {"href":text_node.url})
	elif text_node.text_type == TextType.IMAGE:
		return LeafNode("img", "",{"src":text_node.url, "alt":text_node.text})
	else:
		raise ValueError("Not a valid type")