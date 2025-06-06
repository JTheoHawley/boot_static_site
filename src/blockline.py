


def markdown_to_blocks(markdown):
    blocks = []
    md_split = markdown.split('\n\n')
    for block in md_split:
        strip_block = block.strip()
        if strip_block == "":
            continue
        blocks.append(strip_block)
    return blocks