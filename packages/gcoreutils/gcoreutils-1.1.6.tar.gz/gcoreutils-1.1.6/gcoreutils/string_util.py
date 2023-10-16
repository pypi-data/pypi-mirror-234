"""
utility for string.
"""
import numpy as np
import re
from fractions import Fraction


# ==================================================
def remove_space(s):
    """
    remove space, tab, and newline.

    Args:
        s (str): string

    Returns:
        str: removed string
    """
    if type(s) != str:
        raise KeyError(f"invalid type ({type(s)}) is given.")

    s = s.replace(" ", "").replace("\t", "").replace("\n", "")
    return s


# ==================================================
def wrap_string(a, left="", right=""):
    """
    wrap array elementwise with left and right strings.

    Args:
        a (array-like): array
        left (str, optional): left string to wrap
        right (str, optional): right string to wrap

    Returns:
        array-like: wrapped array
    """
    return np.frompyfunc(lambda i: left + i + right, 1, 1)(np.array(a, dtype=str))


# ==================================================
def table_to_str(tbl, sep=", ", endl="\n"):
    """
    convert from table to string.

    Args:
        tbl (array-like): table of strings
        sep (str, optional): separator string
        endl (str, optional): newline string

    Returns:
        str: string
    """
    t = np.array(tbl, dtype=str, ndmin=2)
    if t.ndim > 2:
        raise KeyError("invalid array dimension.")
    return endl.join(map(sep.join, t.tolist()))


# ==================================================
def circle_number(c):
    """
    get a LaTeX code for a letter with circle.

    Args:
        c (any): letter (convertable to string)

    Returns:
        str: LaTeX code
    """
    pre = r"{\ooalign{\hfil\resizebox{.8\width}{\height}{"
    post = r"}\hfil\crcr\raise.1ex\hbox{\large$\bigcirc$}}}"
    return pre + str(c) + post


# ==================================================
# https://note.nkmk.me/python-fractions-usage/
# https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
def convert_to_fraction(s):
    """
    convert float number in string to fractional one.

    Args:
        s (str or [str]): a (list of) string containing float expressions

    Returns:
        str or [str]: a (list of) converted string
    """
    tp = type(s)
    if tp != str and tp != list:
        return s

    def conv(s):
        float_ptn = "[-+]?(\d*\.\d*|\.\d+)([eE][-+]?\d+)?"
        rx = re.compile(float_ptn)

        lst = rx.findall(s)
        lst = set([i[0] for i in lst])
        for r in lst:
            s = s.replace(r, str(Fraction(r).limit_denominator()))
        return s

    return conv(s) if tp == str else [conv(s1) for s1 in s]


# ==================================================
def class_name(cls):
    """
    get class name from type.

    Returns:
        str: class name.
    """
    f = str(cls)
    name = f[f.rfind(".") + 1 : f.rfind("'")]
    return name
