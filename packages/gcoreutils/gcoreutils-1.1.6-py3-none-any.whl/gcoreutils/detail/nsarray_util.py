"""
utility for NSArray.
"""
import numpy as np
from gcoreutils.basic_util import apply
from gcoreutils.convert_util import sympy_to_latex, sympy_to_str, text_to_sympy
from gcoreutils.string_util import remove_space


# ==================================================
def text_to_sympy_array(text):
    """
    convert single text to sympy array.

    Args:
        text (str): single text to convert.

    Returns: tuple:
        - ndarray: sympy array.
        - str: style.
        - bool: is_list.
        - bool: is_real.
    """
    # check complex.
    is_real = text.count("I") == 0

    # check list.
    lcb = text.count("{")
    rcb = text.count("}")
    if lcb != rcb:
        raise KeyError("parenthesis { or } is invalid in " + f"{text}.")
    is_list = lcb > 0

    # check style.
    lb = text.count("[")
    rb = text.count("]")
    if lb != rb:
        raise KeyError("parenthesis [ or ] is invalid in " + f"{text}.")

    bond = text.count("@")
    bond_th = text.count(";")
    bond_sv = text.count(":")
    chk1 = bond > 0 and (bond_th > 0 or bond_sv > 0)
    chk2 = bond_th > 0 and (bond > 0 or bond_sv > 0)
    chk3 = bond_sv > 0 and (bond_th > 0 or bond > 0)
    if chk1 or chk2 or chk3:
        raise KeyError(f"different bonds are mixed in {text}.")
    if bond > 0 or bond_th > 0 or bond_sv > 0:
        if lb < 2:
            raise KeyError(f"bond contains no vectors in {text}.")
        if lcb > 1:
            raise KeyError("parenthesis { or } is invalid with bond in " + f"{text}.")

    if bond > 0:
        style = "bond"
    elif bond_th > 0:
        style = "bond_th"
    elif bond_sv > 0:
        style = "bond_sv"
    else:
        t = remove_space(text)[:3].strip("{}")
        c = t.count("[")
        if c == 1:
            style = "vector"
        elif c == 2:
            style = "matrix"
        elif c > 2:
            raise KeyError("invalid style in" + f"{text}.")
        else:
            style = "scalar"

    # convert to sympy list.
    if not is_list and style in ["bond", "bond_th", "bond_sv"]:
        text = "[" + text + "]"

    text = text.replace("{", "[").replace("}", "]").replace("@", ",").replace(";", ",").replace(":", ",")
    s = text_to_sympy(text)

    if style in ["bond", "bond_th", "bond_sv"]:
        if is_list:
            s = [[i, j] for i, j in zip(s[0::2], s[1::2])]
        else:
            s = [s[0], s[1]]

    return np.array(s), style, is_list, is_real


# ==================================================
def list_to_text(lst, style, is_list):
    """
    convert list to single text.

    Args:
        lst (list or value): list or value to convert.
        style (str): style, "scalar/vector/matrix/bond/bond_th/bond_sv".
        is_list (bool): list style ?

    Returns:
        str: converted text.
    """

    def to_text(t):  # converter for each element.
        try:
            if t is not None:
                t = str(t)
            else:
                t = ""
        except TypeError:
            return ""
        return t

    bond_delim = {"bond": "@", "bond_th": ";", "bond_sv": ":"}
    opt_style = ["scalar", "vector", "matrix", "bond", "bond_th", "bond_sv"]

    if style not in opt_style:
        raise KeyError(f"{style} must be {opt_style}.")

    s = apply(to_text, lst.tolist())

    if style in ["bond", "bond_th", "bond_sv"]:
        c = bond_delim[style]
        if is_list:
            s = ", ".join([str(t1).replace("'", "") + c + str(t2).replace("'", "") for t1, t2 in s])
            s = "[" + s + "]"
        else:
            s = str(s[0]).replace("'", "") + c + str(s[1]).replace("'", "")
    else:  # scalar, vector, matrix
        s = str(s).replace("'", "")
        if style == "scalar":
            s = s.replace("[", "{").replace("]", "}")

    if is_list:
        s = "{" + s[1:-1] + "}"

    return s


# ==================================================
def _list_to_format(lst, style, is_list, vec, mat, bond):
    """
    convert list to str list.

    Args:
        lst (list or value): list or value to convert.
        style (str): style, "scalar/vector/matrix/bond/bond_th/bond_sv".
        is_list (bool): list style ?
        vec (function): vector format.
        mat (function): matrix format.
        bond (function): bond format.

    Returns:
        list or str: converted text.
    """
    bond_delim = {"bond": "@", "bond_th": ";", "bond_sv": ":"}
    opt_style = ["scalar", "vector", "matrix", "bond", "bond_th", "bond_sv"]

    if style not in opt_style:
        raise KeyError(f"{style} must be {opt_style}.")

    if style == "vector":
        if is_list:
            s = [vec(i) for i in lst]
        else:
            s = vec(lst)
    elif style == "matrix":
        if is_list:
            s = [mat(i) for i in lst]
        else:
            s = mat(lst)
    elif style in ["bond", "bond_th", "bond_sv"]:
        c = bond_delim[style]
        if is_list:
            s = [bond(i, c) for i in lst]
        else:
            s = bond(lst, c)
    else:
        s = lst

    return s


# ==================================================
def list_to_str(lst, style, is_list):
    """
    convert list to str list.

    Args:
        lst (list or value): list or value to convert.
        style (str): style, "scalar/vector/matrix/bond/bond_th/bond_sv".
        is_list (bool): list style ?

    Returns:
        list or str: converted text.
    """

    def vec_str(m):
        s = "[" + ", ".join(m) + "]"
        return s

    def mat_str(m):
        s = "[" + ", ".join(["[" + ", ".join(row) + "]" for row in m]) + "]"
        return s

    def bond_str(m, c):
        s = vec_str(m[0]) + c + vec_str(m[1])
        return s

    lst = sympy_to_str(lst.tolist())
    s = _list_to_format(lst, style, is_list, vec_str, mat_str, bond_str)
    return s


# ==================================================
def list_to_latex(lst, style, is_list):
    """
    convert list to latex list.

    Args:
        lst (list or value): list or value to convert.
        style (str): style, "scalar/vector/matrix/bond/bond_th/bond_sv".
        is_list (bool): list style ?

    Returns:
        list or str: converted text.
    """

    def vec_latex(m):
        s = r"\begin{pmatrix} "
        s += " & ".join(m)
        s += r" \end{pmatrix}"
        return s

    def mat_latex(m):
        s = r"\begin{pmatrix} "
        s += r" \\ ".join([" & ".join(row) for row in m])
        s += r" \end{pmatrix}"
        return s

    def bond_latex(m, c):
        s = vec_latex(m[0]) + c + vec_latex(m[1])
        return s

    lst = sympy_to_latex(lst.tolist())
    s = _list_to_format(lst, style, is_list, vec_latex, mat_latex, bond_latex)
    return s


# ==================================================
def bond_to_vector_center(bond, style):
    """
    convert to vector, center from bond.

    Args:
        bond (ndarray): bond.
        style (str): original style, bond/bond_th/bond_sv.

    Returns: tuple
        - ndarray: vector of bond.
        - ndarray: center of bond.
    """
    if bond.ndim == 3:
        b1 = bond[:, 0].copy()
        b2 = bond[:, 1].copy()
    else:
        b1 = bond[0].copy()
        b2 = bond[1].copy()
    if style == "bond":
        vector = b1
        center = b2
    elif style == "bond_th":
        vector = b2 - b1
        center = (b1 + b2) / 2
    else:
        vector = b2
        center = b1 + b2 / 2
    return vector, center


# ==================================================
def bond_to_tail_head(bond, style):
    """
    convert to tail, head from bond.

    Args:
        bond (ndarray): bond.
        style (str): original style, bond/bond_th/bond_sv.

    Returns: tuple
        - ndarray: tail of bond.
        - ndarray: head of bond.
    """
    if bond.ndim == 3:
        b1 = bond[:, 0].copy()
        b2 = bond[:, 1].copy()
    else:
        b1 = bond[0].copy()
        b2 = bond[1].copy()
    if style == "bond":
        tail = b2 - b1 / 2
        head = b2 + b1 / 2
    elif style == "bond_th":
        tail = b1
        head = b2
    else:
        tail = b1
        head = b1 + b2
    return tail, head


# ==================================================
def bond_to_start_vector(bond, style):
    """
    convert to start, vector from bond.

    Args:
        bond (ndarray): bond.
        style (str): original style, bond/bond_th/bond_sv.

    Returns: tuple
        - ndarray: start of bond.
        - ndarray: vector of bond.
    """
    if bond.ndim == 3:
        b1 = bond[:, 0].copy()
        b2 = bond[:, 1].copy()
    else:
        b1 = bond[0].copy()
        b2 = bond[1].copy()
    if style == "bond":
        start = b2 - b1 / 2
        vector = b1
    elif style == "bond_th":
        start = b1
        vector = b2 - b1
    else:
        start = b1
        vector = b2
    return start, vector
