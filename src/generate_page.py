import os
from node_change import markdown_to_html_node
from node_change import extract_title
import re

def generate_page(from_path, template_path, dest_path, basepath):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}.")
    markdown_from = open(from_path).read()
    html_template = open(template_path).read()
    html_from = markdown_to_html_node(markdown_from).to_html()
    title = extract_title(markdown_from)
    html_filled = html_template.replace("{{ Title }}", title)
    html_filled = html_filled.replace("{{ Content }}", html_from)
    html_filled = html_filled.replace("href=\"/", f"href=\"{basepath}")
    html_filled = html_filled.replace("src=\"/", f"src=\"{basepath}")
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    if not os.path.exists(dest_path):
        open(dest_path, mode="x")
    open(dest_path, mode="w").write(html_filled)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entity in os.listdir(dir_path_content):
        ent = os.path.join(dir_path_content, entity)
        dst_path = os.path.join(dest_dir_path, entity)
        if os.path.isfile(ent) and re.findall(r".+.md(?!.)", entity):
            dst_path = dst_path.replace(".md", ".html")
            generate_page(ent, template_path, dst_path, basepath)
        if os.path.isdir(ent):
            generate_pages_recursive(ent, template_path, dst_path, basepath)
