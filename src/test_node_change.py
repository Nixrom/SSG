from htmlnode import *
from textnode import *
from node_change import *
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
    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" word", TextType.TEXT)])
    def test_split_start(self):
        node = TextNode("`code block` This is text with two `code block` words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        for i in new_nodes:
            print(i)
        self.assertEqual(new_nodes, [TextNode("code block", TextType.CODE), TextNode(" This is text with two ", TextType.TEXT),TextNode("code block", TextType.CODE), TextNode(" words", TextType.TEXT)])
