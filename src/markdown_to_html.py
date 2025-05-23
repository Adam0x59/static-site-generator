"""This file is for code related to converting html to markdown"""

from inline import *
from htmlnode import *
from block_markdown import *
from textnode import *

def markdown_to_html(markdown):
    """Converts a full Markdown document into a single Parent HTMLNode
    containing child HTMLNode objects that represent nested HTML elements.

    Args:
        markdown (str): A complete raw Markdown document.

    Returns:
        HTMLNode: A parent HTMLNode object representing the top-level HTML
        element, containing child HTMLNode objects representing nested HTML blocks.
    """
    markdown_blocks = markdown_blocks(markdown)
    pass
