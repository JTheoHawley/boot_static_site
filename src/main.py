from textnode import TextNode, TextType
from blockline import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import os
import shutil


def main():
    public_set_up()
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    test_node = TextNode("This is a Test", TextType.TEXT)
    print(test_node)


def public_set_up():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")

def copy_static(source_dir, dest_dir):
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_dir)
        else:
            os.mkdir(dest_path)
            copy_static(source_path, dest_path)

def extract_title(markdown):
    md_split = markdown.split("\n")
    for line in md_split:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No Heading")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    dest_name = os.path.dirname(dest_path)
    os.makedirs(dest_name, exist_ok=True)
    with open(dest_path, "w") as d:
        d.write(full_html)

main()