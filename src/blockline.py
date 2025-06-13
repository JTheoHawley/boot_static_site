from enum import Enum
from textnode import TextNode, TextType
from node_delimiter import text_to_textnodes, split_nodes_delimiter, split_nodes_image, split_nodes_link
from text_to_html import text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    md_split = markdown.split('\n\n')
    for block in md_split:
        strip_block = block.strip()
        if strip_block == "":
            continue
        blocks.append(strip_block)
    return blocks

def block_to_block_type(md_block):
    if md_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE
    if md_block.startswith(">"):
        for line in md_block.split("\n"):
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if md_block.startswith("- "):
        for line in md_block.split("\n"):
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if md_block.startswith("1. "):
        i = 1
        for line in md_block.split("\n"):
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(paragraph_to_html_node(block))
        if block_type == BlockType.HEADING:
            html_nodes.append(heading_to_html_node(block))
        if block_type == BlockType.QUOTE:
            html_nodes.append(quote_to_html_node(block))
        if block_type == BlockType.CODE:
            html_nodes.append(code_to_html_node(block))
    return ParentNode("div", html_nodes)


def paragraph_to_html_node(block_text):
    text_nodes = text_to_textnodes(block_text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return ParentNode("p", children)

def heading_to_html_node(block_text):
    children = []
    tag = None
    if block_text.startswith("# "):
        tag = "h1"
        heading_text = block_text[2:]
        text_nodes = text_to_textnodes(heading_text)
        for node in text_nodes:
            children.append(text_node_to_html_node(node))
    elif block_text.startswith("## "):
        tag = "h2"
        heading_text = block_text[3:]
        text_nodes = text_to_textnodes(heading_text)
        for node in text_nodes:
            children.append(text_node_to_html_node(node))
    elif block_text.startswith("### "):
        tag = "h3"
        heading_text = block_text[4:]
        text_nodes = text_to_textnodes(heading_text)
        for node in text_nodes:
            children.append(text_node_to_html_node(node))
    elif block_text.startswith("#### "):
        tag = "h4"
        heading_text = block_text[5:]
        text_nodes = text_to_textnodes(heading_text)
        for node in text_nodes:
            children.append(text_node_to_html_node(node))
    elif block_text.startswith("##### "):
        tag = "h5"
        heading_text = block_text[6:]
        text_nodes = text_to_textnodes(heading_text)
        for node in text_nodes:
            children.append(text_node_to_html_node(node))
    elif block_text.startswith("###### "):
        tag = "h6"
        heading_text = block_text[7:]
        text_nodes = text_to_textnodes(heading_text)
        for node in text_nodes:
            children.append(text_node_to_html_node(node))
    return ParentNode(tag, children)

def quote_to_html_node(block_text):
    lines = block_text.split("\n")
    clean_lines = []
    for line in lines:
        if line.startswith("> "):
            clean_lines.append(line[2:])
        elif line.startswith(">"):
            clean_lines.append(line[1:])
        else:
            clean_lines.append(line)
    cleaned_text = "\n".join(clean_lines)
    text_nodes = text_to_textnodes(cleaned_text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return ParentNode("blockquote", children)

def code_to_html_node(block_text):
    lines = block_text.split("\n")
    code_lines = lines[1:-1]
    code_content = "\n".join(code_lines) + "\n"
    code_leaf = LeafNode("code", code_content)
    return ParentNode("pre", [code_leaf])