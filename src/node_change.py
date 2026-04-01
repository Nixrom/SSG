from textnode import *
from htmlnode import *
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

