from enum import Enum

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