from htmlnode import *
from textnode import *
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_img(self):
        node = TextNode("This is an image node", TextType.IMAGE, "Image URL")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"Image URL", "alt":"This is an image node"})
