import re


def replace_code(path, prefix, replacement):
    with open(path, "r") as f:
        file_str = f.read()
    replace_str = re.sub(f"##{prefix} BLOCK[\s\S]*##END", replacement, file_str)
    with open(path, "w") as f:
        f.write(replace_str)


def add_import(path, line):
    with open(path, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)
