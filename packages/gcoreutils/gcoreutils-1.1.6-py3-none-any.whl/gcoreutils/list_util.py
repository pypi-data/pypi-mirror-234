"""
utility for list.
"""
import math


# ==================================================
def regularize_table(lst2d, padding=None):
    """
    regularize an irregular table.

    Args:
        lst2d (list): 2d list with different number of columns
        padding (any, optional): padding value

    Returns:
        list: regularized 2d list
    """
    if type(lst2d) != list:
        raise KeyError(f"non list type ({type(lst2d)}) is given.")

    col = max(map(len, lst2d))
    tbl = []
    for r in lst2d:
        p = [padding] * col
        p[: len(r)] = r
        tbl.append(p)
    return tbl


# ==================================================
def list_to_table(lst1d, col, p=None):
    """
    convert from list to table

    Args:
        lst1d (list): 1d list
        col (int): number of columns
        p (any, optional): padding value (no padding for None)

    Returns:
        list: 2d list
    """
    if type(lst1d) != list:
        raise KeyError(f"non list type ({type(lst1d)}) is given.")

    n = len(lst1d)
    row = int(math.ceil(n / col))
    tbl = []
    for i in range(row):
        tbl.append(lst1d[col * i : col * (i + 1)])
    d = row * col - n
    if p is not None and d != 0:
        tbl[-1].extend([p] * d)

    return tbl


# ==================================================
def flatten(lst):
    """
    flatten abitrary shape of list.

    Args:
        lst (Any): list to flatten.

    Returns:
        list: flattened list.
    """

    def _flatten(lst):
        for el in lst:
            if isinstance(el, list):
                yield from _flatten(el)
            else:
                yield el

    if isinstance(lst, list):
        return list(_flatten(lst))
    else:
        return lst
