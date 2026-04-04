import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "#"
    CODE = "`"
    QUOTE = ">"
    UNORDERED_LIST = "-"
    ORDERED_LIST = "N. "

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    end_blocks = []
    for i in blocks:
        hold = i.strip()
        if hold != "":
            end_blocks.append(hold)
    return end_blocks

def block_to_block_type(text):
    lines = text.split("\n")
    if re.findall(r"(?<!.)(#{1,6} ).+(?!\n)", text) and len(lines) == 1:
        return BlockType.HEADING
    if re.findall(r"(?<!.)(```\n(.|\n)*\n```)", text):
        return BlockType.CODE
    if len(lines) == len(re.findall(r"(?<!.)(>)", text)):
        return BlockType.QUOTE
    if len(lines) == len(re.findall(r"(?<!.)(- )", text)):
        return BlockType.UNORDERED_LIST
    start_numbers = re.findall(r"(?<!.)(\d. )", text)
    if start_numbers:
        if start_numbers[0] == "1. " and len(start_numbers) == len(lines) and start_numbers == sorted(start_numbers):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
