"""
This class is calculatable with sympy.
"""
import sympy as sp


# ==================================================
class SymList(list):

    # ==================================================
    def __init__(self, *args):
        """
        initialize list.
        """
        super().__init__(args)

    # ==================================================
    def __getitem__(self, i):
        """
        default value is sp.zero
        """
        try:
            return list.__getitem__(self, i)
        except KeyError:
            return sp.S(0)

    # ==================================================
    def __iadd__(self, other):
        """ += other """
        if isinstance(other, list):
            for i, v in enumerate(other):
                self[i] += v
            return self
        elif isinstance(other, (int, float, complex, sp.Basic)):
            for i in range(len(self)):
                self[i] += other
            return self

    # ==================================================
    def __isub__(self, other):
        """ -= other """
        if isinstance(other, list):
            for i, v in enumerate(other):
                self[i] -= v
            return self
        elif isinstance(other, (int, float, complex, sp.Basic)):
            for i in range(len(self)):
                self[i] -= other
            return self

    # ==================================================
    def __imul__(self, other):
        """ *= other """
        if isinstance(other, list):
            return [a * b for b in other for a in self]
        elif isinstance(other, (int, float, complex, sp.Basic)):
            return [a * other for a in self]

    # ==================================================
    def __itruediv__(self, other):
        """ /= other """
        if isinstance(other, (int, float, complex, sp.Basic)):
            for i in range(len(self)):
                self[i] /= other
            return self

    # ==================================================
    def __ipow__(self, other):
        """ **= other """
        if isinstance(other, (int, float, complex, sp.Basic)):
            for i in range(len(self)):
                self[i] **= other
            return self

    # ==================================================
    def __add__(self, other):
        """ self + other """
        lst = self
        lst += other
        return lst

    # ==================================================
    def __radd__(self, other):
        """ other + self """
        lst = self
        lst += other
        return lst

    # ==================================================
    def __sub__(self, other):
        """ self - other """
        lst = self
        lst -= other
        return lst

    # ==================================================
    def __rsub__(self, other):
        """ other - self """
        lst = self
        lst *= -1
        lst += other
        return lst

    # ==================================================
    def __mul__(self, other):
        """ self * other """
        lst = self
        lst *= other
        return lst

    # ==================================================
    def __rmul__(self, other):
        """ other * self """
        lst = self
        lst *= other
        return lst

    # ==================================================
    def __truediv__(self, other):
        """ self / other """
        lst = self
        lst /= other
        return lst

    # ==================================================
    def __rtruediv__(self, other):
        """ other / self """
        lst = self
        lst **= -1
        lst *= other
        return lst

    # ==================================================
    def __pow__(self, other):
        """ self ** other """
        lst = self
        lst **= other
        return lst

    # ==================================================
    def simplify(self, type="factor"):
        """
        simplify list values.

        Args:
            type (str, optional): type of simplification, ``factor/expand/cancel/simplify``
        """
        t = {
            "factor": sp.factor,
            "expand": sp.expand,
            "cancel": sp.cancel,
            "simplify": sp.simplify,
        }

        for i, v in enumerate(self):
            self[i] = t[type](v)
