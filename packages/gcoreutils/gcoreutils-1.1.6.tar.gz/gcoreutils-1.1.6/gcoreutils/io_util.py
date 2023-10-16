"""
utility for input and ouput.
"""
import json
import re
import ast


# ==================================================
def read_jsonc(filename):
    """
    read JSON(C) file.

    Args:
        filename (str): file name.

    Returns:
        dict: dictionary from JSON.
    """
    with open(filename, mode="r", encoding="utf-8") as f:
        s = f.read()
    s = re.sub(r"/\*[\s\S]*?\*/|//.*", "", s)
    d = json.loads(s)
    return d


# ==================================================
def write_jsonc(filename, dic, header=None):
    """
    write JSON(C) file.

    Args:
        filename (str): filename.
        dic (dict): dictionary to write.
        header (str, optional): header comment at the top of file.
    """
    text = ""
    if header is not None:
        text += "/*\n" + header + "\n*/\n"
    text += json.dumps(dic, indent=2)
    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(text)


# ==================================================
def read_dict(filename):
    """
    read dict text file.

    Args:
        filename (str): file name.

    Returns:
        dict: dictionary from dict text.
    """
    with open(filename, mode="r", encoding="utf-8") as f:
        s = f.read()

    if s[: s.find("{")].count("=") > 0:
        s = s.split("=")[-1].strip(" ")

    c = ast.get_docstring(ast.parse(s))
    if c is not None:
        s = s.replace(c, "").replace('"""', "")
    d = ast.literal_eval(s)
    return d


# ==================================================
def write_dict(filename, dic, header=None, var=None):
    """
    write dict text file.

    Args:
        filename (str): filename.
        dic (dict): dictionary to write.
        header (str, optional): header comment at the top of file.
        var (str, optional): varialbe of dict.
    """
    with open(filename, mode="w", encoding="utf-8") as f:
        if header is not None:
            print('"""' + header + '"""', file=f)
        if var is None:
            print(dic, file=f)
        else:
            print(f"{var} =", dic, file=f)
