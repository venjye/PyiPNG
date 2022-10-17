import pyipng
import os


file_path = os.path.join(os.getcwd(),'cgbi_image.png')
with open(file_path,'rb') as f:
    bytes = f.read()
    fix_bytes = pyipng.convert(bytes)
    with open("fix_cgbi_image.png",'wb') as f:
        f.write(fix_bytes)