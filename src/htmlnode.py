
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
