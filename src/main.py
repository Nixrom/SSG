from textnode import TextNode
from copy_overwrite import replace_with_copy
from generate_page import generate_page
import os

src = os.path.abspath("static")
dst = os.path.abspath("public")
gn_from = os.path.abspath("content/index.md")
gn_tmpl = os.path.abspath("template.html")
gn_to = "public/index.html"

def main():
    replace_with_copy(src, dst, True)
    generate_page(gn_from, gn_tmpl, gn_to)


main()