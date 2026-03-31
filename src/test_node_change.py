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
        self.assertEqual(new_nodes, [TextNode("code block", TextType.CODE), TextNode(" This is text with two ", TextType.TEXT),TextNode("code block", TextType.CODE), TextNode(" words", TextType.TEXT)])
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://i.imgur.com/zjjcJKZ.png), sorry, [more than one link.](Test link)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("more than one link.", "Test link")], matches)
    def test_extract_empty(self):
        matches = extract_markdown_images("This is an imageless string.")
        self.assertListEqual([], matches)
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
