import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_full(self):
        print(HTMLNode("<Test>", "Test Value", [], {"Test1.11":"Test1.12", "Test1.21":"Test1.22"}))
    def test_direct(self):
        print(HTMLNode(props={"Test2.11":"Test2.12", "Test2.21":"Test2.22"}))
    def test_empty(self):
        print(HTMLNode())
    def test_children(self):
        child=HTMLNode("<Test>", "Test Value", [], {"Test4.11":"Test4.12", "Test4.21":"Test4.22"})
        print(HTMLNode("<Test>", "Test Value", [child], {"Test4.31":"Test4.32", "Test4.31":"Test4.32"}))
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_empty(self):
        node = LeafNode(None, "World, Hello!")
        self.assertEqual(node.to_html(), "World, Hello!")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Link Text", {"href":"Link Source"})
        self.assertEqual(node.to_html(), "<a href=\"Link Source\">Link Text</a>")
    def test_leaf_to_html_img(self):
        node = LeafNode("img", "Image Description", {"src":"Image Link Source", "href":"Link Source"})
        self.assertEqual(node.to_html(), "<img src=\"Image Link Source\" alt=\"Image Description\" />")
        print(node.to_html())

if __name__ == "__main__":
    unittest.main()
