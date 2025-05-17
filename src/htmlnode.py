
class HTMLnode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        # The HTML tag (e.g., 'p', 'div', 'span'). Can be None for text-only nodes.
        self.tag = tag
        # The text content of the node. Used for text nodes or elements with inner text.
        self.value = value
        # A list of child HTMLnode objects. Defaults to an empty list if not provided.
        self.children = children or []
        # A dictionary of HTML attributes (e.g., {"href": "example.com", "class": "link"}).
        self.props = props or {}

    def to_html(self):
        # This method should generate HTML output for the node.
        # Not implemented yet; subclasses or later extensions will define it.
        raise NotImplementedError
    
    # Convert the node's props dictionary into a string of HTML attributes.
    # Returns a string in the format: ' key1="value1" key2="value2"'
    def props_to_html(self):
        return ''.join(f" {key}=\"{value}\"" for key, value in self.props.items())

    # Return a readable string representation of the TextNode instance,
	# useful for debugging and logging.
    def __repr__(self):
        return f"HTML-node({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLnode):
    # By not setting a default for tag or value these are REQUIRED variables
    def __init__(self, tag, value, props=None):
        # passing an empty dict to the HTMLnode constructor declares 'no children'
        super().__init__(tag, value, {}, props)

    # Method to return a html LeafNode object formatted as html.
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node has no value!")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    # Return a readable string representation of the TextNode instance,
	# useful for debugging and logging.
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLnode):
    # Set up class default/required values
    def __init__(Self, tag, children, props=None):
        # Passing None to the HTML node constructor declares 'no value"
        super().__init__(tag, None, children, props)

    #Method to return a html ParentNode object formatted as html.
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node have no tag")
        if self.children is None:
            raise ValueError("Parent has no children")
        # Recursive child tree walk, when list item is None return to main path
        child_string_list = [item.to_html() for item in self.children if item is not None]
        # Print recursion result as a joined list.
        return f"<{self.tag}{self.props_to_html()}>{"".join(child_string_list)}</{self.tag}>"