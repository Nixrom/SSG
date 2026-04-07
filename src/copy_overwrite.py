import os
import shutil
import re

def replace_with_copy(source, destination, delete=False):
    if delete == True:
        shutil.rmtree(destination)
        os.mkdir(destination)
    for entity in os.listdir(source):
        ent = os.path.join(source, entity)
        if os.path.isfile(ent) and not re.findall(r".+.md(?!.)", entity):
            shutil.copy(ent, destination)
        if os.path.isdir(ent):
            copy_ent = os.path.join(destination, entity)
            os.mkdir(copy_ent)
            replace_with_copy(ent, copy_ent)
