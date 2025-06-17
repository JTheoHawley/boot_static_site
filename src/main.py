from textnode import TextNode, TextType
import os
import shutil


def main():
    public_set_up()
    copy_static("static", "public")
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
main()