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
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
        if self.tag == "b":
            return f"<b>{self.value}</b>"
        if self.tag == "i":
            return f"<i>{self.value}</i>"
        if self.tag == "p":
            return f"<p>{self.value}</p>"
        if self.tag == "code":
            return f"<code>{self.value}</code>"
        if self.tag == "a":
            return f"<a href=\"{self.props["href"]}\">{self.value}</a>"
        if self.tag == "img":
            return f"<img src=\"{self.props["src"]}\" alt=\"{self.value}\" />"
    def __repr__(self):
        return(f"tag={self.tag}, value={self.value},  props={self.props_to_html()}")
