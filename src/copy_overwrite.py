import os
import shutil

def replace_with_copy(source, destination, delete=False):
    src = os.path.abspath(source)
    dst = os.path.abspath(destination)
    if delete == True:
        shutil.rmtree(destination)
        os.mkdir(destination)
    for entity in os.listdir(source):
        ent = os.path.join(source, entity)
        if os.path.isfile(ent):
            shutil.copy(ent, destination)
        if os.path.isdir(ent):
            copy_ent = os.path.join(destination, entity)
            os.mkdir(copy_ent)
            replace_with_copy(ent, copy_ent)
