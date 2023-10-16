"""
basic utility.
"""
from sympy import Symbol, Basic, symbols


# ==================================================
def apply(f, lst):
    """
    apply function to (nested) list.

    Args:
        f (function): function to apply to each element of list.
        lst (list or value): (nested) list to apply.

    Returns:
        list or value: applied list.
    """
    if isinstance(lst, list):
        return [apply(f, x) for x in lst]
    else:
        return f(lst)


# ==================================================
def get_variable(lst):
    """
    get variables from sympy expression.

    Args:
        lst (list or sympy): sympy expression (except for Matrix).

    Returns:
        list: set of variable strings (sorted).
    """

    def get_var(t, var):  # converter for each element.
        if isinstance(t, Basic):
            var.update(set(map(str, t.atoms(Symbol))))

    var = set()
    apply(lambda t: get_var(t, var), lst)
    var = sorted(var)

    return var


# ==================================================
def set_variable(lst, real=False):
    """
    set variable dict.

    Args:
        lst (list): list of variable string.
        real (bool, optional): real variable ?

    Returns:
        dict: { text: variable }.
    """
    v = symbols(lst, real=real)
    d = dict(zip(lst, v))
    return d
