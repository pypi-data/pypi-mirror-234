"""
utility for crystal.
"""
import numpy as np
from gcoreutils.nsarray import NSArray


CHOP = 1e-4


# ==================================================
def cell_transform_matrix(cell, crystal="", translation=True):
    """
    get cell transform matrix from lattice constants.

    Args:
        cell (dict): lattice parameters, a, b, c, alpha, beta, gamma, and origin.
        crystal (str, optional): crystal, "triclinic/monoclinic/orthorhombic/tetragonal/trigonal/hexagonal/cubic".
        translation (bool, optional): if False, return 3x3 matrix.

    Returns: tuple
        - cell (dict): a, b, c, alpha, beta, gamma (float).
        - volume (float): volume.
        - A (NSArray): 4x4 [3x3] matrix (each unit vector in each column, 4th column is zero).
        - G (NSArray): 4x4 [3x3] metric matrix.
        - A_norm (NSArray): list of normalized vectors.

    Notes:
        - unit length or 90 degree are used when lattice constants are omitted.
    """
    if type(cell) is not dict:
        cell = {"a": 1.0, "b": 1.0, "c": 1.0, "alpha": 90.0, "beta": 90.0, "gamma": 90.0}

    a = max(float(cell.get("a", 1.0)), CHOP)
    b = max(float(cell.get("b", 1.0)), CHOP)
    c = max(float(cell.get("c", 1.0)), CHOP)
    alpha = max(float(cell.get("alpha", 90.0)), CHOP)
    beta = max(float(cell.get("beta", 90.0)), CHOP)
    gamma = max(float(cell.get("gamma", 90.0)), CHOP)

    if crystal in ["trigonal", "hexagonal"]:
        alpha = 90.0
        beta = 90.0
        gamma = 120.0
        b = a
    elif crystal == "monoclinic":
        alpha = 90.0
        gamma = 90.0
    elif crystal == "orthorhombic":
        alpha = 90.0
        beta = 90.0
        gamma = 90.0
    elif crystal == "tetragonal":
        alpha = 90.0
        beta = 90.0
        gamma = 90.0
        b = a
    elif crystal == "cubic":
        alpha = 90.0
        beta = 90.0
        gamma = 90.0
        b = a
        c = a

    cell = {}
    cell["a"] = a
    cell["b"] = b
    cell["c"] = c
    cell["alpha"] = alpha
    cell["beta"] = beta
    cell["gamma"] = gamma

    ca = np.cos(alpha * np.pi / 180)
    cb = np.cos(beta * np.pi / 180)
    cc = np.cos(gamma * np.pi / 180)
    sc = np.sin(gamma * np.pi / 180)
    s = 1 - ca * ca - cb * cb - cc * cc + 2 * ca * cb * cc
    s = 0.0 if s < 0.0 else np.sqrt(s)
    vol = a * b * c * s

    A = np.eye(4)
    A[0, 0] = a
    A[0, 1] = b * cc
    A[1, 1] = b * sc
    A[0, 2] = c * cb
    A[1, 2] = c * (ca - cb * cc) / sc
    A[2, 2] = c * s / sc

    if not translation:
        A = A[0:3, 0:3]

    G = A.T @ A

    A = A.round(14)
    G = G.round(14)

    A = NSArray(A, "matrix", "value")
    G = NSArray(G, "matrix", "value")

    # A_norm = A[0:3, 0:3].T.convert_style("vector").normalize()
    A_norm = NSArray([A[0:3, 0].tolist(), A[0:3, 1].tolist(), A[0:3, 2].tolist()], "vector", "value").normalize()
    A_norm = NSArray(A_norm.round(14), "vector", "value")

    return cell, vol, A, G, A_norm
