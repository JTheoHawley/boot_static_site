


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
                return ""
        prop = ""
        for key, value in self.props.items():
            prop += f' {key}="{value}"'
        return prop
    
    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError ("no value present")
        if self.tag == None:
            return (f"{self.value}")
        else:
            html_prop = self.props_to_html()
            return (f"<{self.tag}{html_prop}>{self.value}</{self.tag}>")
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError ("no tag present")
        if self.children == None:
            raise ValueError ("no children present")
        else:
            html_string = ""
            for child in self.children:
                html_string += child.to_html()
            return (f"<{self.tag}>{html_string}</{self.tag}>")