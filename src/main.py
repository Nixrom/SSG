from textnode import TextNode
from copy_overwrite import replace_with_copy
from generate_page import generate_pages_recursive
import os

src = os.path.abspath("static")
src_2 = os.path.abspath("content")
dst = os.path.abspath("public")
gn_tmpl = os.path.abspath("template.html")

def main():
    replace_with_copy(src, dst, True)
    replace_with_copy(src_2, dst)
    generate_pages_recursive(src_2, gn_tmpl, dst)


main()