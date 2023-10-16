"""
This class is calculatable with sympy.
"""
import sympy as sp
import copy


# ==================================================
class SymDict(dict):

    # ==================================================
    def __init__(self, dic=None, **kwargs):
        """
        initialize dict.

        Args:
            dic (dict, optional): dictionary.
            kwargs (dict, optional): keywords to initialize the dictionary.
        """
        super().__init__(**kwargs)

        if dic is not None:
            self.update(dic)

    # ==================================================
    def __getitem__(self, key):
        """
        default value is sp.zero
        """
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return sp.S(0)

    # ==================================================
    def __iadd__(self, other):
        """ += other """
        if isinstance(other, dict):
            self.update({k: self[k] + v for k, v in other.items()})
        elif isinstance(other, (int, float, complex, sp.Basic)):
            self.update({k: v + other for k, v in self.items()})

        return self

    # ==================================================
    def __isub__(self, other):
        """ -= other """
        if isinstance(other, dict):
            self.update({k: self[k] - v for k, v in other.items()})
        elif isinstance(other, (int, float, complex, sp.Basic)):
            self.update({k: v - other for k, v in self.items()})

        return self

    # ==================================================
    def __imul__(self, other):
        """ *= other """
        if isinstance(other, dict):
            self.update({k: self[k] * v for k, v in other.items()})
        elif isinstance(other, (int, float, complex, sp.Basic)):
            self.update({k: v * other for k, v in self.items()})

        return self

    # ==================================================
    def __itruediv__(self, other):
        """ /= other """
        if isinstance(other, (int, float, complex, sp.Basic)):
            self.update({k: v / other for k, v in self.items()})
            return self

    # ==================================================
    def __ipow__(self, other):
        """ **= other """
        if isinstance(other, (int, float, complex, sp.Basic)):
            self.update({k: v ** other for k, v in self.items()})
            return self

    # ==================================================
    def __add__(self, other):
        """ self + other """
        dic = copy.copy(self)
        dic += other
        return dic

    # ==================================================
    def __radd__(self, other):
        """ other + self """
        dic = copy.copy(self)
        dic += other
        return dic

    # ==================================================
    def __sub__(self, other):
        """ self - other """
        dic = copy.copy(self)
        dic -= other
        return dic

    # ==================================================
    def __rsub__(self, other):
        """ other - self """
        dic = copy.copy(self)
        dic *= -1
        dic += other
        return dic

    # ==================================================
    def __mul__(self, other):
        """ self * other """
        dic = copy.copy(self)
        dic *= other
        return dic

    # ==================================================
    def __rmul__(self, other):
        """ other * self """
        dic = copy.copy(self)
        dic *= other
        return dic

    # ==================================================
    def __truediv__(self, other):
        """ self / other """
        dic = copy.copy(self)
        dic /= other
        return dic

    # ==================================================
    def __rtruediv__(self, other):
        """ other / self """
        dic = copy.copy(self)
        dic **= -1
        dic *= other
        return dic

    # ==================================================
    def __pow__(self, other):
        """ self ** other """
        dic = copy.copy(self)
        dic **= other
        return dic

    # ==================================================
    def simplify(self, type="factor"):
        """
        simplify dict values.

        Args:
            type (str, optional): type of simplification, ``factor/expand/cancel/simplify``
        """
        t = {
            "factor": sp.factor,
            "expand": sp.expand,
            "cancel": sp.cancel,
            "simplify": sp.simplify,
        }
        simp = t[type]

        for k, v in self.items():
            self[k] = simp(v)

    # ==================================================
    def remove_zero(self):
        """
        remove zero values from dict.
        """
        zero_key = [k for k, v in self.items() if v == sp.S(0)]
        for k in zero_key:
            del self[k]
