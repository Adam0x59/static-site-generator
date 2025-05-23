from enum import Enum
from htmlnode import *

# Enum class to store text formatting types.
class TextType(Enum):
	TEXT = "normal text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

# A class representing a segment of formatted text, possibly with a link or image URL.
class TextNode:
	"""Represents a segment of formatted text.

	Attributes:
		text (str): The plain text content of the node.
		text_type (TextType): The formatting type of the node.
		url (str, optional): A URL for links or images. Defaults to None.
	"""
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
		"""Checks equality between this TextNode and another.

		Args:
			other (TextNode): The other TextNode to compare with.

		Returns:
			bool: True if all fields are equal, False otherwise.
		"""
		return(
			self.text == other.text and
			self.text_type == other.text_type and
			self.url == other.url
		)
	
	# Return a readable string representation of the TextNode instance,
	# useful for debugging and logging.
	def __repr__(self):
		"""Returns a string representation of the TextNode.

        Returns:
            str: A formatted string with node details.
        """
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

# Function to convert TextNode to html, form of LeafNode.
def text_node_to_html_node(text_node):
	"""Converts a TextNode object into a LeafNode representing HTML.

	Args:
		text_node (TextNode): The text node to convert.

	Returns:
		LeafNode: An HTML-compatible node.

	Raises:
		ValueError: If the text_type is not a recognized TextType.
	"""
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