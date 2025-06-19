from textnode import TextNode, TextType 
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL_TEXT: 
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == TextType.BOLD_TEXT: 
        return LeafNode("b", text_node.text, None)
    elif text_node.text_type == TextType.ITALIC_TEXT: 
        return LeafNode("i", text_node.text, None)
    elif text_node.text_type == TextType.CODE_TEXT: 
        return LeafNode("code", text_node.text, None)
    elif text_node.text_type == TextType.LINK_FORMAT: 
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE_FORMAT: 
        return LeafNode("img",None, props={"src":text_node.url, "alt":text_node.text})
    else: 
        raise Exception("text node is empty")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # print(old_nodes)
    for node in old_nodes: 
        if node.text_type!= TextType.NORMAL_TEXT: 
           new_nodes.append(node)
           continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections)%2==0: 
            raise ValueError("invalid markdown, formstted seaction not closed")
        for i in range(len(sections)): 
            if sections[i] == "":
                continue
            elif i%2==0: 
                split_nodes.append(TextNode(sections[i], TextType.NORMAL_TEXT, None))
            else: 
                split_nodes.append(TextNode(sections[i], text_type, None))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text): 
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return matches

def extract_markdown_links(text): 
    matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_images(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"![{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT, None))
            new_nodes.append(TextNode(link[0], TextType.IMAGE_FORMAT, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT, None))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT, None))
            new_nodes.append(TextNode(link[0], TextType.LINK_FORMAT, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT, None))
    return new_nodes

def text_to_textnodes(text): 
    nodes = [TextNode(text, TextType.NORMAL_TEXT, None)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    return nodes

def markdown_to_blocks(markdown): 
    markdown_list = markdown.strip().split('\n\n')
    cleaned_markdown = [mark for mark in markdown_list if mark != " "]
    return cleaned_markdown