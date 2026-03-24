class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def __repr__(self):
        return(f"tag={self.tag}, value={self.value}, children={self.children}, props={self.props_to_html()}")
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        rep_str = []
        if self.props != None:
            for i in self.props:
                if i != None:
                    rep_str.append(f" {i}=\"{self.props[i]}\"")
        return("".join(rep_str))

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value == None:
            raise ValueError("No Value")
        if self.tag == None:
            return f"{self.value}"
        if self.tag == "a":
            return f"<a href=\"{self.props["href"]}\">{self.value}</a>"
        if self.tag == "img":
            return f"<img src=\"{self.props["src"]}\" alt=\"{self.value}\" />"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    def __repr__(self):
        return(f"tag={self.tag}, value={self.value},  props={self.props_to_html()}")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("No Tag")
        if self.children == None:
            raise ValueError("No Children")
        der_children =""
        for i in self.children:
            der_children += i.to_html()
        return f"<{self.tag}>{der_children}</{self.tag}>"
