from block_functions import *
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_block_type_basic(self):
        matches = [block_to_block_type("### header"), block_to_block_type("```\ncode block\n```"), block_to_block_type("Hello World")]
        self.assertEqual(matches, [BlockType.HEADING, BlockType.CODE, BlockType.PARAGRAPH])
    def test_block_type_quote_and_lists(self):
        matches = [block_to_block_type("> quote\n>test>\n>one"), block_to_block_type("- unordered\n- list\n- testing\n- one."), block_to_block_type("1. ordered list\n2. testing.")]
        self.assertEqual(matches, [BlockType.QUOTE, BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST])
    def test_block_type_various_paragraphs(self):
        matches = [block_to_block_type("1. not ordered\n3. ordered list\n2. testing"), block_to_block_type(">Mixed\n## signals\n3. paragraph\n```\nblock")]
        self.assertEqual(matches, [BlockType.PARAGRAPH, BlockType.PARAGRAPH])
