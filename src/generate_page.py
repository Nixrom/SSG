import os
from node_change import markdown_to_html_node
from node_change import extract_title

def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}.")
    markdown_from = open(from_path).read()
    html_template = open(template_path).read()
    html_from = markdown_to_html_node(markdown_from).to_html()
    title = extract_title(markdown_from)
    html_filled = html_template.replace("{{ Title }}", title)
    html_filled = html_filled.replace("{{ Content }}", html_from)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    open(dest_path, mode="x")
    open(dest_path, mode="w").write(html_filled)
