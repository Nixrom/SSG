from textnode import TextNode
import os
import shutil

def main():
    replace_with_copy("static", "public", True)

def replace_with_copy(source, destination, delete=False):
    src = os.path.abspath(source)
    dst = os.path.abspath(destination)
    if delete == True:
        shutil.rmtree(dst)
        os.mkdir(dst)
    for entity in os.listdir(src):
        ent = os.path.join(src, entity)
        if os.path.isfile(ent):
            shutil.copy(ent, dst)
        if os.path.isdir(ent):
            copy_ent = os.path.join(dst, entity)
            os.mkdir(copy_ent)
            replace_with_copy(ent, copy_ent)

main()