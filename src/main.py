from textnode import TextNode
from copy_overwrite import replace_with_copy
from generate_page import generate_pages_recursive
import os
import sys

src = os.path.abspath("static")
src_2 = os.path.abspath("content")
dst = os.path.abspath("docs")
gn_tmpl = os.path.abspath("template.html")
basepath = "/"
#if sys.argv[1] != "":
#    basepath = sys.argv[1]

def main():
    replace_with_copy(src, dst, True)
    replace_with_copy(src_2, dst)
    generate_pages_recursive(src_2, gn_tmpl, dst, basepath)


main()