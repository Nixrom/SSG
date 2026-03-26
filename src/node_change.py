from textnode import *
from htmlnode import *

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
        if i.text.count(delimiter) < 2:
            raise Exception("Invalid markdown text: too few delimiters")
        if i.text.count(delimiter) % 2:
            raise Exception("Invalid markdown text: odd number of delimiters")
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
