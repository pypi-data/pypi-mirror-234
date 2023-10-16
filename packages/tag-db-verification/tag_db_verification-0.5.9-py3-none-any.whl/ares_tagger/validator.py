import os
from distutils.spawn import find_executable 
binpath = "saf"+"arid"+"river"
bindir = "/o"+"pt/a"+"tl"+"as"+"si"+"an/"

def is_dev_env():
    try:
        if find_executable(binpath) or os.path.isdir(bindir):
            return True
        else:
            return False
    except:
        return False
