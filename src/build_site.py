import os
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import LeafNode
from markdown_blocks import markdown_to_html_node 


def read_file(file_path):
    contents_file = open(file_path)
    contents = contents_file.read()
    contents_file.close()
    return contents

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if block.startswith('# '):
                return block.split('# ')[1]
    raise Exception ("h1 header not present")

def generate_page(from_path, template_path, dest_path):

    new_dest_path = dest_path.replace(".md", ".html")
    
    print(f"Generating page from {from_path} to {new_dest_path} using {template_path}")
    markdown = read_file(from_path)
    template_content = read_file(template_path)
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(markdown)
    update_title = template_content.replace('{{ Title }}', title)
    update_content = update_title.replace('{{ Content }}', html_string)

    if os.path.exists(os.path.dirname(new_dest_path)) == False:
        os.makedirs(os.path.dirname(new_dest_path))
    f = open(new_dest_path, "w")
    f.write(update_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        new_content_path = os.path.join(dir_path_content, filename)
        new_dest_dir_path = os.path.join(dest_dir_path, filename)
        if filename.endswith(".md"):
            print(f"\nfound md file: {new_content_path}")
            print(f"destination directory: {dest_dir_path}")
            generate_page(new_content_path, template_path, new_dest_dir_path)
            pass
        elif os.path.isdir(new_content_path):
            print(f"\nthis is a directory: {new_content_path}")
            print(f"this is our new destination directory: {new_dest_dir_path}")
            print(f"os.path.exists(new_dest_dir_path): {os.path.exists(new_dest_dir_path)}")

            if os.path.exists(new_dest_dir_path) == False:
                print(f"make new directory: {new_dest_dir_path}")
                os.makedirs(new_dest_dir_path)
            generate_pages_recursive(new_content_path, template_path, new_dest_dir_path)


def return_common_path(path1, path2):
    common_path = os.path.commonpath([path1, path2])
