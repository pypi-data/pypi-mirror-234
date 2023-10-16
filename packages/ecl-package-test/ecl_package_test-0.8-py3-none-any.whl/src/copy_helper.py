import shutil


def copy_dir(src, dist):
    shutil.copytree(src, dist)
