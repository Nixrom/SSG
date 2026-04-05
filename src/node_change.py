from textnode import *
from htmlnode import *
from block_functions import *
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case TextType.PARAGRAPH:
            return LeafNode("p", text_node.text)
        case _:
            raise Exception("Not a text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    end_list = []
    for i in old_nodes:
        if i.text_type != TextType.TEXT:
            end_list.append(i)
            continue
        if i.text.count(delimiter) % 2 and i.text.count(delimiter) > 1:
            raise Exception(f"Invalid markdown text: odd number of {delimiter} delimiters")
        if i.text.count(delimiter) == 0:
            end_list.append(i)
            continue
        split_text = i.text.split(delimiter)
        if i.text.find(delimiter) == 0:
            count = 0
            for j in split_text:
                if j == "":
                    count+=1
                    continue
                if not count % 2:
                    end_list.append(TextNode(j, TextType.TEXT))
                else:
                    end_list.append(TextNode(j, text_type))
                count+=1
        else:
            count = 0
            for j in split_text:
                if j == "":
                    count+=1
                    continue
                if not count % 2:
                    end_list.append(TextNode(j, TextType.TEXT))
                else:
                    end_list.append(TextNode(j, text_type))
                count+=1
    return end_list

def extract_markdown_images(text):
    return re.findall(r"!\[(.+?)\]\((.+?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.+?)\]\((.+?)\)", text)

def split_nodes_image(old_nodes):
    final_nodes = []
    for o_node in old_nodes:
        delim = extract_markdown_images(o_node.text)
        o_node_text = o_node.text
        if len(delim) == 0:
            final_nodes.append(o_node)
            continue
        for i in range(0, len(delim)):
            o_node_text = o_node_text.split(f"![{delim[i][0]}]({delim[i][1]})", 1)
            if o_node_text[0] == "":
                final_nodes.append(TextNode(delim[i][0], TextType.IMAGE, delim[i][1]))
            else:
                final_nodes.append(TextNode(o_node_text[0], TextType.TEXT))
                final_nodes.append(TextNode(delim[i][0], TextType.IMAGE, delim[i][1]))
            o_node_text = o_node_text[1]
            if i+1 == len(delim) and o_node_text != "":
                final_nodes.append(TextNode(o_node_text, TextType.TEXT))
    return final_nodes

def split_nodes_link(old_nodes):
    final_nodes = []
    for o_node in old_nodes:
        delim = extract_markdown_links(o_node.text)
        o_node_text = o_node.text
        if len(delim) == 0:
            final_nodes.append(o_node)
            continue
        for i in range(0, len(delim)):
            o_node_text = o_node_text.split(f"[{delim[i][0]}]({delim[i][1]})", 1)
            if o_node_text[0] == "":
                final_nodes.append(TextNode(delim[i][0], TextType.LINK, delim[i][1]))
            else:
                final_nodes.append(TextNode(o_node_text[0], TextType.TEXT))
                final_nodes.append(TextNode(delim[i][0], TextType.LINK, delim[i][1]))
            o_node_text = o_node_text[1]
            if i+1 == len(delim) and o_node_text != "":
                final_nodes.append(TextNode(o_node_text, TextType.TEXT))
    return final_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    for i in [["**", TextType.BOLD], ["_", TextType.ITALIC], ["`", TextType.CODE]]:
        nodes = split_nodes_delimiter(nodes, i[0], i[1])
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_title(markdown):
    if not re.findall(r"(?<!.)#{1}[^#](.+)", markdown):
        raise Exception("No Header")
    return (re.findall(r"(?<!.)#{1}[^#](.+)", markdown)[0].strip())