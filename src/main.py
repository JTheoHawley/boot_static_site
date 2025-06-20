from textnode import TextNode, TextType
from blockline import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import os
import shutil
import sys


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    public_set_up()
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    


def public_set_up():
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")

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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    full_html = full_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    dest_name = os.path.dirname(dest_path)
    os.makedirs(dest_name, exist_ok=True)
    with open(dest_path, "w") as d:
        d.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        if os.path.isfile(content_path) and item.endswith(".md"):
            rel_path = os.path.relpath(content_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, rel_path)
            dest_dir = dest_path.replace(".md", ".html")
            generate_page(content_path, template_path, dest_dir, basepath)
        elif os.path.isdir(content_path):
            dest_path = os.path.join(dest_dir_path, item)
            os.mkdir(dest_path)
            generate_pages_recursive(content_path, template_path, dest_path, basepath)

            
main()