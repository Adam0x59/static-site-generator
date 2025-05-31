"""
This module defines HTML node classes for constructing and rendering HTML trees.
Includes base HTMLnode, LeafNode (no children), and ParentNode (with children).
"""

class HTMLnode:
    """Base class for all HTML node types.

    Attributes:
        tag (str or None): The HTML tag (e.g., 'p', 'div'). None for text-only nodes.
        value (str or None): The text content of the node.
        children (list): List of child HTMLnode objects.
        props (dict): Dictionary of HTML attributes (e.g., {"class": "link"}).
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        """Generates the HTML representation of this node.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError
    
    def props_to_html(self):
        """Converts the props dictionary into a string of HTML attributes.

        Returns:
            str: A string of HTML attributes in the format ' key="value"'.
        """
        return ''.join(f" {key}=\"{value}\"" for key, value in self.props.items())

    def __repr__(self):
        """Returns a string representation of the node for debugging.

        Returns:
            str: A string showing the node's key properties.
        """
        return f"HTMLnode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLnode):
    """Represents a HTML element with no children 
    (e.g., text or simple inline elements).

    Attributes:
        tag (str): The HTML tag (e.g., 'p', 'span').
        value (str): The text content of the element.
        props (dict): Optional dictionary of HTML attributes, eg: {"href": "example.com"}
    """
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        """Generates HTML output for this leaf node.

        Returns:
            str: A string of HTML for this node.

        Raises:
            ValueError: If tag or value is missing.
        """
        if self.value is None:
            raise ValueError("Leaf node has no value!")
        if self.tag is None:
            return self.value
        if self.tag == "code":
            return f"<pre><code{self.props_to_html()}>{self.value}</code></pre>"
        if self.tag == "code-inline":
            return f"<code{self.props_to_html()}>{self.value}</code>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        """Returns a string representation of the LeafNode.

        Returns:
            str: A formatted string with node details.
        """
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLnode):
    """Represents an HTML element that contains child nodes.

    Attributes:
        tag (str): The HTML tag.
        children (list): A list of child HTMLnode objects.
        props (dict): Optional dictionary of HTML attributes.
    """
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        """Returns a string representation of the ParentNode.

        Returns:
            str: A formatted string with node details.
        """
        return f"ParentNode({self.tag}, {self.children}, {self.props})"


    def to_html(self):
        """Generates HTML output for the parent node and all its children.

        Returns:
            str: A complete HTML string for this node and its children.

        Raises:
            ValueError: If tag is missing or children is empty.
        """
        if self.tag is None:
            raise ValueError("Parent node has no tag")
        if not self.children:
            raise ValueError("Children list is empty or does not exist")
        # Recursively generate HTML for all non-None children.
        child_string_list = [item.to_html() for item in self.children if item is not None]
        # Return string, fill in centre with joined list from recursive function output
        return f"<{self.tag}{self.props_to_html()}>{"".join(child_string_list)}</{self.tag}>"