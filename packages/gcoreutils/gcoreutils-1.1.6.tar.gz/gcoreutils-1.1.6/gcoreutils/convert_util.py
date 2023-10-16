"""
utility for conversion.
"""
import re
import ast
import numpy as np
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication, rationalize
from sympy import SympifyError, latex
from gcoreutils.basic_util import apply, get_variable
from gcoreutils.list_util import flatten


# ==================================================
def text_to_list(text):
    """
    convert single text to list.

    Args:
        text (str): text to convert.

    Returns:
        list or str: converted list.

    Notes:
        - if format error occurs, return None.
    """
    if not isinstance(text, str):
        return None

    lb = text.count("[")
    rb = text.count("]")
    if lb != rb:
        return None
    elif lb == 0 and rb == 0:
        return text

    text = re.sub(r"\s*\[\s*", "[", text)
    text = re.sub(r"\s*\]\s*", "]", text)

    text = text.replace("[", "['").replace("]", "']").replace(",", "','").replace("'[", "[").replace("]'", "]")
    try:
        lst = ast.literal_eval(text)
    except (SyntaxError, ValueError):
        return None

    return lst


# ==================================================
def text_to_sympy(text, local=None, check_var=None, rational=True):
    """
    convert single text to sympy list.

    Args:
        text (str): text to convert.
        local (dict, optional): variables to replace.
        check_var (set, optional): set of variables to accept.
        rational (bool, optional): replace floating number with rational one ?

    Returns:
        list or sympy: converted list.

    Notes:
        - if format error occurs, return None.
        - if an element cannot be converted to sympy, it becomes None.
    """
    lst = text_to_list(text)
    if lst is None:
        return None

    if check_var is None:
        check_var = []
    check_var = set(check_var)

    transformations = standard_transformations + (implicit_multiplication,)
    if rational:
        transformations += (rationalize,)

    def to_sympy(t):  # converter for each element.
        try:
            expression = parse_expr(t, transformations=transformations, local_dict=local)
        except (SympifyError, SyntaxError, TypeError):
            return None
        var = set(get_variable(expression))
        if len(check_var) != 0 and not (var <= check_var):
            return None

        return expression

    s = apply(to_sympy, lst)

    return s


# ==================================================
def is_valid_sympy(text, check_var=None):
    """
    check whether text is valid as sympy expression.

    Args:
        text (str): text to check.
        check_var (list, optional): acceptable variable strings. if None is given, do not check.

    Returns:
        bool: return True if valid.
    """
    try:
        lst = text_to_sympy(text, check_var=check_var)
    except Exception:
        return False
    lst = flatten(lst)
    if lst is None or (type(lst) == list and lst.count(None) > 0):
        return False
    else:
        return True


# ==================================================
def sympy_to_str(lst):
    """
    convert list to str list.

    Args:
        lst (list or ndarray or sympy): list to convert.

    Returns:
        list or str: converted list.

    Notes:
        - if an element cannot be converted to float, it becomes None.
    """
    if isinstance(lst, np.ndarray):
        lst = lst.tolist()

    def to_str(t):  # converter for each element.
        try:
            t = str(t)
        except TypeError:
            return None
        return t

    s = apply(to_str, lst)
    return s


# ==================================================
def sympy_to_float(lst):
    """
    convert list to float list.

    Args:
        lst (list or ndarray or sympy): list to convert.

    Returns:
        list or float: converted list.

    Notes:
        - if an element cannot be converted to float, it becomes None.
    """
    if isinstance(lst, np.ndarray):
        lst = lst.tolist()

    def to_float(t):  # converter for each element.
        try:
            t = float(t)
        except TypeError:
            return None
        return t

    s = apply(to_float, lst)
    return s


# ==================================================
def sympy_to_complex(lst):
    """
    convert list to complex list.

    Args:
        lst (list or ndarray or sympy): list to convert.

    Returns:
        list or complex: converted list.

    Notes:
        - if an element cannot be converted to complex, it becomes None.
    """
    if isinstance(lst, np.ndarray):
        lst = lst.tolist()

    def to_complex(t):  # converter for each element.
        try:
            t = complex(t)
        except TypeError:
            return None
        return t

    s = apply(to_complex, lst)
    return s


# ==================================================
def sympy_to_latex(lst):
    """
    convert list to latex list.

    Args:
        lst (list or ndarray or sympy): list to convert.

    Returns:
        list or str: converted list.

    Notes:
        - if an element cannot be converted to complex, it becomes None.
    """
    if isinstance(lst, np.ndarray):
        lst = lst.tolist()

    def to_latex(t):  # converter for each element.
        try:
            if t is not None:
                t = latex(t)
        except TypeError:
            return None
        return t

    s = apply(to_latex, lst)
    return s


# ==================================================
def sympy_to_mathematica(lst):
    """
    convert sympy to Mathematica. (simple version)

    Args:
        lst (list or ndarray or sympy): list to convert.

    Returns:
        list or str: converted list.

    Notes:
        - if an element cannot be converted to complex, it becomes None.
    """
    key_list = [  # (sympy, mathematica)
        ("sqrt", "Sqrt"),
        ("sin", "Sin"),
        ("cos", "Cos"),
        ("tan", "Tan"),
        ("exp", "Exp"),
        ("log", "Log"),
        ("pi", "Pi"),
        ("None", ""),
        ("[", "{"),
        ("]", "}"),
        ("(", "["),
        (")", "]"),
    ]

    if isinstance(lst, np.ndarray):
        lst = lst.tolist()

    def to_str(t):  # converter for each element.
        try:
            t = str(t)
        except TypeError:
            return None
        return t

    s = apply(to_str, lst)
    s = str(s).replace("'", "")

    for x in key_list:
        s = s.replace(*x)

    return s
