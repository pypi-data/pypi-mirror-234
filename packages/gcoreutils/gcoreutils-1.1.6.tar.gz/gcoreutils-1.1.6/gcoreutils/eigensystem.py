"""
solve eigenvalue problem for a set of parameters.
"""
import numpy as np


# ==================================================
def eigensystem(mat_func, params, eigenvector=True):
    """
    solve eigenvalue problem.

    Args:
        mat_func (function): a function to get a matrix for a given set of parameters
        params (np.array): a set of parameters in each row
        eigenvector (bool, optional): compute eigenvectors ?

    Returns:
        tuple:
            np.array: eigenvalues of a set of parameters in each column
            np.array, optional: eigenvector matrices in order of a set of parameters, eigenvector of a matrix in each column
    """
    if type(params) != np.ndarray:
        raise KeyError(f"invalid type of parameters ({type(params)}) is given.")
    if params.ndim != 2:
        raise KeyError("params must be 2d np.array.")

    mats = mat_func(params)
    mats = np.array(mats).transpose((2, 0, 1))
    d = mats.shape[1]
    if eigenvector:
        vals = np.empty(shape=(0, d), dtype="float64")
        vecs = np.empty(shape=(d, d, 0), dtype="float64")
        for val, vec in map(np.linalg.eigh, mats):
            vals = np.vstack([vals, val])
            vecs = np.dstack([vecs, vec])
        vals = vals.T
        vecs = vecs.transpose((2, 0, 1))
        return vals, vecs
    else:
        vals = np.array(list(map(np.linalg.eigvalsh, mats))).T
        return vals
