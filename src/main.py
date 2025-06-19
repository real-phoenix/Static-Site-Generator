from textnode import TextNode, TextType
import os
import shutil
from blocknode import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path): 
    for entry in os.listdir(dir_path_content): 
        content_entry_path = os.path.join(dir_path_content, entry)
        dest_entry_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(content_entry_path): 
            generate_pages_recursive(content_entry_path, template_path, dest_entry_path)
        elif content_entry_path.endswith(".md"): 
            os.makedirs(dest_dir_path, exist_ok=True)
            dest_file_name = os.path.splitext(entry)[0] + ".html"
            dest_file_path = os.path.join(dest_dir_path, dest_file_name)
            generate_page(content_entry_path, template_path, dest_file_path)

def copy_dir_rec(src, dst): 
    if os.path.exists(dst): 
        shutil.rmtree(dst)
        print(f"Deleted existing destination path {dst}")
    os.mkdir(dst)
    print(f"Created destination directory{dst}")
    for item in os.listdir(src): 
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path): 
            shutil.copy(src_path, dst_path)
            print(f"Copied files {src_path} -> {dst_path}")
        elif os.path.isdir(src_path): 
            copy_dir_rec(src_path, dst_path)

def extract_title(markdown): 
    lines = markdown.split('\n')
    for line in lines: 
        if line.startswith("# "): 
            return line[2:].strip()
    raise Exception("No H1 header found in markdown")
    
def generate_page(from_path, template_path, dest_path): 
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, "r") as f:
        from_content = f.read()
    
    with open(template_path, "r") as f: 
        template_content = f.read()

    html_node = markdown_to_html_node(from_content)
    html_content = html_node.to_html()

    title = extract_title(from_content)
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f: 
        f.write(final_html)

def main(): 
    copy_dir_rec("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__": 
    main()