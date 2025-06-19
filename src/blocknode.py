from enum import Enum
from text_to_html_node_conversion import markdown_to_blocks
from text_to_html_node_conversion import text_to_textnodes, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import textwrap
from textnode import TextNode, TextType

class BlockType(Enum): 
    PARAGRAPH_BLOCK = "paragraph"
    HEADING_BLOCK = "heading"
    CODE_BLOCK = "code"
    QUOTE_BLOCK = "quote"
    UNORDERED_LIST_BLOCK = "unordered_list"
    ORDERED_LIST_BLOCK = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING_BLOCK
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE_BLOCK
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH_BLOCK
        return BlockType.QUOTE_BLOCK
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH_BLOCK
        return BlockType.UNORDERED_LIST_BLOCK
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH_BLOCK
            i += 1
        return BlockType.ORDERED_LIST_BLOCK
    return BlockType.PARAGRAPH_BLOCK
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH_BLOCK:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING_BLOCK:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE_BLOCK:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST_BLOCK:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST_BLOCK:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE_BLOCK:
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
    raw_text_node = TextNode(text, TextType.NORMAL_TEXT, None)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
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