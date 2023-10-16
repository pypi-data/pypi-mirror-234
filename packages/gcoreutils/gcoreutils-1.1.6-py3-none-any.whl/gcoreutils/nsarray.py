"""
This class manages sympy-numpy combined array.
"""
import numpy as np
import sympy as sp
from gcoreutils.basic_util import get_variable, set_variable
from gcoreutils.string_util import remove_space
from gcoreutils.convert_util import sympy_to_float, sympy_to_complex
from gcoreutils.detail.nsarray_util import (
    text_to_sympy_array,
    list_to_text,
    list_to_latex,
    list_to_str,
    bond_to_vector_center,
    bond_to_tail_head,
    bond_to_start_vector,
)


# ================================================== class
class NSArray(np.ndarray):
    """
    sympy-numpy combined array.

    Attributes:
        style (str): scalar/vector/matrix/bond/bond_th/bond_sv.
        var (dict): dict of variables { str: sympy }.
        lst (bool): a set of values ?
        fmt (str): sympy/value.
        is_real (bool): real array ?

    Notes: string / internal
        - scalar : s, {s}, {{s}}, ... / s, [s], [[s]], ...
        - vector : v = [s], {v} / [s], [[s]].
        - matrix : m = [[s]], {m} / [[s]], [[[s]]].
        - bond : b = vector,center/"vector@center", {b} / [[s],[s]], [[[s],[s]]].
        - bond_th : b = tail,head/"tail;head", {b} / [[s],[s]], [[[s],[s]]].
        - bond_sv : b = start,vector/"start:vector", {b} / [[s],[s]], [[[s],[s]]].
    """

    # ================================================== constructor
    def __new__(cls, data, style=None, fmt="sympy", real=True):
        """
        create array.

        Args:
            data (str or array-like): single text or array.
            style (str, optional): scalar/vector/matrix/bond/bond_th/bond_sv.
            fmt (str, optional): sympy/value.
            real (bool, optional): real array ?
        """
        # key check.
        if style not in [None, "scalar", "vector", "matrix", "bond", "bond_th", "bond_sv"]:
            raise KeyError(f"unknown style = {style} is given.")
        if fmt not in ["sympy", "value"]:
            raise KeyError(f"unknown format = {fmt} is given.")

        # set numpy array, style, is_list, is_real.
        if isinstance(data, (int, float, complex)):
            data = str(data)
        if type(data) == str:
            a, style1, is_list, is_real = text_to_sympy_array(data)
            if style is None:
                style = style1
            elif style1 != style:
                raise KeyError("invalid style is given for string data.")
        elif isinstance(data, (list, np.ndarray)):
            if style is None:
                raise KeyError("style must be specified for array-like data.")
            if type(data) == list:
                a = np.array(data)
            else:
                a = data
            is_list = NSArray._check_lst(a, style)
            is_real = a.dtype != np.complex128
        else:
            raise KeyError(f"unknown type, {type(data)}.")

        # size check.
        if style == "vector":
            if a.ndim != 1 and a.ndim != 2:
                raise KeyError("shape is invalid for vector.")
        elif style == "matrix":
            if a.ndim != 2 and a.ndim != 3:
                raise KeyError("shape is invalid for matrix.")
        elif style in ["bond", "bond_th", "bond_sv"]:
            if a.ndim != 2 and a.ndim != 3:
                raise KeyError("shape is invalid for bond.")

        # set variables.
        var = set_variable(get_variable(a.tolist()), real=real)
        is_real = is_real and real

        # convert format.
        if fmt == "value":
            if is_real:
                a = np.array(sympy_to_float(a))
            else:
                a = np.array(sympy_to_complex(a))

        # set attributes.
        obj = np.asarray(a).view(cls)
        obj.style = style
        obj.var = var
        obj.lst = is_list
        obj.fmt = fmt
        obj.is_real = is_real

        return obj

    # ==================================================
    def __array_finalize__(self, obj):
        """
        set properties.

        Args:
            obj (ndarray): parent object.
        """
        if obj is None:
            return
        self.style = getattr(obj, "style", None)
        self.var = getattr(obj, "var", None)
        self.lst = getattr(obj, "lst", None)
        self.fmt = getattr(obj, "fmt", None)
        self.is_real = getattr(obj, "is_real", None)

    # ==================================================
    def __reduce__(self):
        """
        for pickle.

        Notes:
            - https://jpcodeqa.com/q/37dee51c5c4ab536b27bf2ed15e6679d
            - https://stackoverflow.com/questions/54486021/how-to-pickle-numpy-ndarray-derived-class
            - https://qiita.com/s-wakaba/items/f15b4aa579c018880758
        """
        pickled_state = super().__reduce__()
        return pickled_state[0], pickled_state[1], (pickled_state[2], self.__dict__, super().shape)

    # ==================================================
    def __setstate__(self, state):
        """
        for pickle.
        """
        _state, dic, shape = state

        # set shape.
        _state = list(_state)
        _state[1] = shape
        _state = tuple(_state)

        # set dict.
        self.__dict__.update(dic)

        super().__setstate__(_state)

    # ==================================================
    def __getitem__(self, key):
        s = super().__getitem__(key)
        if type(key) == int and isinstance(s, NSArray):
            s.lst = False
        return s

    # ==================================================
    def __len__(self):
        if self.is_empty:
            return 0
        elif self.lst:
            return super().shape[0]
        else:
            return 1

    # ================================================== low-level
    def numpy(self):
        """
        convert to conventional numpy array.

        Returns:
            ndarray: numpy array.
        """
        return np.array(self.tolist())

    # ==================================================
    @classmethod
    def _check_lst(cls, a, style):
        return (
            (style == "scalar" and a.ndim > 0)
            or (style == "vector" and a.ndim == 2)
            or (style == "matrix" and a.ndim == 3)
            or (style in ["bond", "bond_th", "bond_sv"] and a.ndim == 3)
        )

    # ==================================================
    @classmethod
    def _elementwise(cls, f, a):
        """
        apply function to a with elementwise.

        Args:
            f (function): function to apply.
            a (NSArray): data.

        Returns:
            NSArray: applied array.
        """
        vf = np.vectorize(lambda i: f(i))
        s = vf(a)
        return s

    # ==================================================
    @classmethod
    def _apply(cls, f, a, style):
        """
        apply function to a with style.

        Args:
            f (function): function to apply.
            a (NSArray): data.
            style (str): style.

        Returns:
            ndarray: applied array.
        """
        if style == "scalar":
            s = NSArray._elementwise(f, a)
        else:
            lst = NSArray._check_lst(a, style)
            if lst:
                s = [f(i) for i in a.tolist()]
            else:
                s = f(a.tolist())

        s = np.array(s)

        return s

    # ==================================================
    def __str__(self):
        """
        convert array to a single string.

        Returns:
            str: array in string.
        """
        s = list_to_text(self, self.style, self.lst)
        return s

    # ==================================================
    def __repr__(self):
        """
        convert array to a detailed string.

        Returns:
            str: detailed string.
        """
        lst = "" if not self.lst or self.size == 0 else "list "
        shape = str(super().shape) + " "
        if self.ndim == 0:
            shape = ""
        s = f"{shape}{lst}{str(self)} style = {self.style}, fmt = {self.fmt}, var = {self.var}, real = {self.is_real}"
        return s

    # ================================================== info.
    @property
    def shape(self):
        """
        shape of scalar or shape of vector, matrix, and bond in list.

        Returns:
            tuple: shape of scalar/vector/matrix/bond.
        """

        s = super().shape
        if self.style == "scalar":
            return s
        elif self.style == "matrix":
            return s[-2:]
        else:
            return s[-1:]

    # ==================================================
    @property
    def is_empty(self):
        """
        empty array ?

        Returns:
            bool: empty array ?
        """
        return self.size == 0

    # ==================================================
    def variable(self):
        """
        used variables in array.

        Returns:
            list: a list of variables (str).
        """
        return list(self.var.keys())

    # ================================================== conversion
    def value(self, subs=None):
        """
        convert to value array.

        Returns:
            NSArray: value array.
        """
        s = self if subs is None else NSArray._elementwise(lambda i: i.subs(subs), self)
        return NSArray(str(s), fmt="value", real=self.is_real)

    # ==================================================
    def sympy(self, real=True):
        """
        convert to sympy array.

        Args:
            real (bool, optional): real array ?

        Returns:
            NSArray: sympy array.
        """
        return NSArray(str(self), fmt="sympy", real=real)

    # ==================================================
    def str(self):
        """
        convert to string array.

        Returns:
            list or str: string list.
        """
        return list_to_str(self, self.style, self.lst)

    # ==================================================
    def latex(self):
        """
        convert to latex array.

        Returns:
            list or str: latex list.
        """
        return list_to_latex(self, self.style, self.lst)

    # ================================================== utility
    def convert_bond(self, style):
        """
        convert bond to given style.

        Args:
            style (str): style to convert, "bond/bond_th/bond_sv".

        Returns:
            - NSArray: b1 (vector, tail, start).
            - NSArray: b2 (center, head, vector).
        """
        if style not in ["bond", "bond_th", "bond_sv"]:
            raise KeyError("it is valid only for bond.")
        if self.style not in ["bond", "bond_th", "bond_sv"]:
            raise KeyError("it is valid only for bond.")
        if style == "bond":
            b1, b2 = bond_to_vector_center(self, self.style)
        elif style == "bond_th":
            b1, b2 = bond_to_tail_head(self, self.style)
        else:
            b1, b2 = bond_to_start_vector(self, self.style)
        b1 = NSArray(b1, "vector", self.fmt, self.is_real)
        b2 = NSArray(b2, "vector", self.fmt, self.is_real)
        return b1, b2

    # ==================================================
    @classmethod
    def create_bond_from_pair(cls, b1, b2, style, real=True):
        """
        create bond with given style from a pair, (b1, b2).

        Args:
            b1 (NSArray): first vectors.
            b2 (NSArray): second vectors.
            style (str): style, "bond/bond_th/bond_sv".
            real (bool): real variable ?

        Returns:
            NSArray: bond array.
        """
        if style not in ["bond", "bond_th", "bond_sv"]:
            raise KeyError(f"unknown style, {style}.")
        if b1.style != "vector" or b2.style != "vector":
            raise KeyError("it is valid only for vector for b1 and b2.")
        if len(b1) != len(b2):
            raise KeyError("lengths are different.")
        if b1.shape != b2.shape:
            raise KeyError("shapes are different.")
        if b1.fmt != b2.fmt:
            raise KeyError("formats are different.")

        sz = len(b1)
        nc = b1.shape[0]
        if b1.lst:
            th = np.empty((sz, 2, nc), dtype=b1.dtype)
            th[:, 0] = b1
            th[:, 1] = b2
        else:
            th = np.empty((2, nc), dtype=b1.dtype)
            th[0] = b1
            th[1] = b2

        s = NSArray(th, style, b1.fmt, real)

        return s

    # ==================================================
    def regular_direction(self):
        """
        convert bond direction so that lower component in vector is positive.

        Returns:
            NSArray: converted array.
        """
        if self.style not in ["bond", "bond_th", "bond_sv"]:
            raise KeyError("it is valid only for bond.")
        if len(self.variable()) > 0:
            raise KeyError("cannot sort because of containing variables.")

        v, c = self.convert_bond("bond")
        if self.lst:
            for i, vi in enumerate(v):
                for vix in vi:
                    if vix > 0:
                        break
                    elif vix == 0:
                        continue
                    else:
                        v[i] = -v[i]
                        break
        else:
            for vix in v:
                if vix > 0:
                    break
                elif vix == 0:
                    continue
                else:
                    v = -v
                    break

        b1, b2 = NSArray.create_bond_from_pair(v, c, "bond").convert_bond(self.style)
        s = NSArray.create_bond_from_pair(b1, b2, self.style, self.is_real)

        return s

    # ==================================================
    def reverse_direction(self):
        """
        reverse bond direction.

        Returns:
            NSArray: reversed array.
        """
        if self.style not in ["bond", "bond_th", "bond_sv"]:
            raise KeyError("it is valid only for bond.")
        if self.style == "bond_th":
            t, h = self.convert_bond("bond_th")
            rb = NSArray.create_bond_from_pair(h, t, "bond_th", self.is_real)
        elif self.style == "bond":
            v, c = self.convert_bond("bond")
            rb = NSArray.create_bond_from_pair(-v, c, "bond", self.is_real)
        else:
            s, v = self.convert_bond("bond_sv")
            rb = NSArray.create_bond_from_pair(s + v, -v, "bond_sv", self.is_real)
        return rb

    # ==================================================
    def sort(self, reverse=False):
        """
        sort array (in ascending order).

        Args:
            reverse (bool): reverse sort ?

        Returns:
            NSArray: sorted array.
        """
        if len(self.variable()) > 0:
            raise ValueError("cannot sort because of containing variables.")

        if not self.lst:
            return self

        shape = super().shape
        if self.style in ["bond", "bond_th", "bond_sv"]:
            s = self.reshape(shape[0], shape[1] * shape[2])  # concatinate two vectors.
        else:
            s = self
        s = NSArray(
            np.array(sorted([tuple(i.ravel()) for i in s.numpy()], reverse=reverse)).reshape(shape),
            self.style,
            self.fmt,
            self.is_real,
        )

        return s

    # ==================================================
    def simplify(self):
        """
        simplify array.

        Returns:
            NSArray: simplified array.
        """
        if self.fmt != "sympy":
            raise KeyError("it is valid only for sympy format.")
        s = NSArray(NSArray._elementwise(lambda i: i.simplify(), self), self.style, self.fmt, self.is_real)
        return s

    # ==================================================
    def factor(self):
        """
        factor array.

        Returns:
            NSArray: factored array.
        """
        if self.fmt != "sympy":
            raise KeyError("it is valid only for sympy format.")
        s = NSArray(NSArray._elementwise(lambda i: i.factor(), self), self.style, self.fmt, self.is_real)
        return s

    # ==================================================
    def expand(self):
        """
        expand array.

        Returns:
            NSArray: expanded array.
        """
        if self.fmt != "sympy":
            raise KeyError("it is valid only for sympy format.")
        s = NSArray(NSArray._elementwise(lambda i: i.expand(), self), self.style, self.fmt, self.is_real)
        return s

    # ==================================================
    def cancel(self):
        """
        cancel array.

        Returns:
            NSArray: canceled array.
        """
        if self.fmt != "sympy":
            raise KeyError("it is valid only for sympy format.")
        s = NSArray(NSArray._elementwise(lambda i: i.cancel(), self), self.style, self.fmt, self.is_real)
        return s

    # ==================================================
    def evalf(self):
        """
        evaluate floating number array.

        Returns:
            NSArray: evaluated array.
        """
        if self.fmt != "sympy":
            raise KeyError("it is valid only for sympy format.")
        s = NSArray(NSArray._elementwise(lambda i: i.evalf(), self), self.style, self.fmt, self.is_real)
        return s

    # ==================================================
    def re(self):
        """
        real part of array.

        Returns:
            NSArray: real part of array.
        """
        if self.fmt == "sympy":
            s = NSArray(NSArray._elementwise(lambda i: sp.re(i), self), self.style, self.fmt, True)
        else:
            s = NSArray(NSArray._elementwise(lambda i: np.real(i), self), self.style, self.fmt, True)
        return s

    # ==================================================
    def im(self):
        """
        imaginary part of array.

        Returns:
            NSArray: imaginary part of array.
        """
        if self.fmt == "sympy":
            s = NSArray(NSArray._elementwise(lambda i: sp.im(i), self), self.style, self.fmt, True)
        else:
            s = NSArray(NSArray._elementwise(lambda i: np.imag(i), self), self.style, self.fmt, True)
        return s

    # ==================================================
    def semi_evalf(self, denom=49):
        """
        evaluate complex fractional into floating number.

        Args:
            denom (int, optional): denominator more than which evalf is performed.

        Returns:
            NSArray: evaluated array.
        """
        if self.fmt != "sympy":
            raise KeyError("it is valid only for sympy format.")
        s = NSArray(
            NSArray._elementwise(lambda i: i.evalf() if sp.denom(i) > denom else i, self), self.style, self.fmt, self.is_real
        )
        return s

    # ==================================================
    def radsimp(self):
        """
        radsimp array.

        Returns:
            NSArray: radsimped array.
        """
        if self.fmt != "sympy":
            raise KeyError("it is valid only for sympy format.")
        s = NSArray(NSArray._elementwise(lambda i: i.radsimp(), self), self.style, self.fmt, self.is_real)
        return s

    # ==================================================
    def subs(self, subs):
        """
        substitute variables in terms of dict.

        Args:
            subs (dict): dict for substitution.

        Returns:
            NSArray: substituted array.
        """
        if subs is not None:
            return NSArray(NSArray._elementwise(lambda i: i.subs(subs), self), self.style, self.fmt, self.is_real)
        else:
            return self

    # ==================================================
    def index(self, s):
        """
        find index.

        Args:
            s (str or NSArray): element to find (single value).

        Returns:
            int or tuple: index or indices for scalar.

        Notes:
            - if s is not in elements, return None.
        """
        if not self.lst:
            raise KeyError("it is valid only for list type.")
        if type(s) == str:
            s = NSArray(s, real=self.is_real)
        else:
            s = NSArray(s, self.style, real=self.is_real)
        if s.lst:
            raise KeyError("plural elements are given.")

        s1 = s.str()
        ss = self.str()
        if self.style == "scalar":
            ss = np.array(ss)
            idx = np.where(ss == s1)
            if ss[idx].size == 0:
                idx = None
        else:
            idx = ss.index(s1) if s1 in ss else None
        return idx

    # ==================================================
    def remove(self, idx=None, info=None):
        """
        remove given indexed and associated info.

        Args:
            idx (ndarray, optional): indices to remove (None = remove nul).
            info (NSArray, optional): associated info.

        Returns: tuple
            - NSArray: removed array.
            - NSArray: removed array for info. (optional).
        """
        if idx is None:
            if self.style == "scalar":
                idx = self[self != 0]
            else:
                idx = np.array([i for i, b in enumerate(self) if not (b == 0).all()])
        if info is not None and idx.shape != self.shape:
            raise KeyError("shape of info is diffrent.")

        s = self[idx]
        if info is not None:
            info = info[idx]
            return s, info
        else:
            return s

    # ==================================================
    def _pad(self):
        """
        pad for affine transformation.

        Returns:
            ndarray: padded vector/matrix.
        """
        zero = 0 if self.fmt == "value" else sp.S(0)
        one = 1 if self.fmt == "value" else sp.S(1)
        a = NSArray._apply(lambda i: np.pad(i, (0, 1), "constant", constant_values=(zero, zero)), self, self.style)
        if self.style == "vector":
            if self.lst:
                a[:, -1] = one
            else:
                a[-1] = one
        else:
            if self.lst:
                a[:, -1, -1] = one
            else:
                a[-1, -1] = one

        a = NSArray(a, self.style, self.fmt, self.is_real)

        return a

    # ==================================================
    def transform(self, A, Ai=None):
        """
        transform vector/matrix/bond as A.v or A.m.A^{-1}.

        Args:
            A (NSArray): transform matrix.
            Ai (NSArray, optional): inverse of A.

        Returns:
            NSArray: transformed vector/matrix/bond.

        Notes:
            - if dim(A)=dim(v/m/b)+1, affine transformation is performed.
        """
        if self.style not in ["vector", "matrix", "bond", "bond_th", "bond_sv"]:
            raise KeyError("it is valid only for vector or matrix or bond.")
        if A.style != "matrix" or A.lst:
            raise KeyError("A is invalid.")
        if Ai is not None and (Ai.style != "matrix" or Ai.lst):
            raise KeyError("inverse of A is invalid.")

        affine = False
        if self.style in ["vector", "matrix"]:
            d = self.shape[0]
            affine = A.shape[0] == d + 1

        if affine:
            x = self._pad()
        else:
            x = self

        if self.style == "vector":
            s = NSArray._apply(lambda i: A @ i, x, self.style)
            if affine:
                if self.lst:
                    s = s[:, :-1]
                else:
                    s = s[:-1]
        elif self.style == "matrix":
            if Ai is None:
                Ai = A.inverse()
            s = NSArray._apply(lambda i: A @ i @ Ai, x, self.style)
            if affine:
                if self.lst:
                    s = s[:, :-1, :-1]
                else:
                    s = s[:-1, :-1]
        else:  # bond
            t, h = self.convert_bond("bond_th")
            t = t.transform(A)
            h = h.transform(A)
            s = NSArray.create_bond_from_pair(t, h, "bond_th")
            b1, b2 = s.convert_bond(self.style)
            s = NSArray.create_bond_from_pair(b1, b2, self.style)

        s = NSArray(s, self.style, self.fmt, self.is_real)
        if s.fmt == "sympy":
            s = s.expand()
        return s

    # ==================================================
    def apply(self, v):
        """
        apply matrices to single vector/matrix/bond as A.v.

        Args:
            v (NSArray): array to be applied.

        Returns:
            NSArray: applied vector/matrix/bond.

        Notes:
            - if dim(self)=dim(v/m/b)+1, affine transformation is performed.
        """
        if self.style != "matrix":
            raise KeyError("it is valid only for matrices.")
        if v.style not in ["vector", "matrix", "bond", "bond_th", "bond_sv"]:
            raise KeyError("it is valid only for vector or matrix or bond.")
        if v.lst:
            raise KeyError("it is valid only for non-list array.")

        Av = "{" + ",".join([str(v.transform(i)) for i in self]) + "}"
        return NSArray(Av, fmt=v.fmt, real=v.is_real and self.is_real)

    # ==================================================
    @classmethod
    def concat(cls, arrays, real=True):
        """
        concatenate arrays.

        Args:
            arrays (list): list of NSArray.
            real (bool, optional): real array ?

        Returns:
            NSArray: concatenated array.
        """
        if type(arrays) != list:
            raise KeyError("it is valid only for list of NSArray.")
        if len(arrays) == 0:
            raise KeyError("empty list is given.")
        style = arrays[0].style
        fmt = arrays[0].fmt
        for s in arrays:
            if s.style != style:
                raise KeyError("style is different.")
            if s.fmt != fmt:
                raise KeyError("fmt is different.")

        a = []
        for s in arrays:
            if s.lst:
                st = str(s)[1:-1]
            else:
                st = str(s)
            if st != "":
                a.append(st)
        a = "{" + ",".join(a) + "}"
        a = NSArray(a, fmt=fmt, real=real)

        return a

    # ==================================================
    def inverse(self):
        """
        inverse of matrix.

        Returns:
            NSArray: inverse of matrix.
        """
        if self.style != "matrix":
            raise KeyError("it is valid only for matrix.")

        if self.fmt == "sympy":
            s = NSArray._apply(lambda i: np.array(sp.Matrix(i).inv().expand()), self, self.style)
        else:
            s = NSArray._apply(lambda i: np.linalg.inv(i), self, self.style)
        s = NSArray(s, self.style, self.fmt, self.is_real)

        return s

    # ==================================================
    def det(self):
        """
        determinant of matrix.

        Returns:
            NSArray: determinant of matrix.
        """
        if self.style not in ["scalar", "matrix"]:
            raise KeyError("it is valid only for scalar or matrix.")

        if self.fmt == "sympy" and self.style == "matrix":
            s = NSArray._apply(lambda i: np.array(sp.Matrix(i).det().expand()), self, self.style)
        elif self.fmt == "value":
            s = NSArray._apply(lambda i: np.linalg.det(i), self, self.style)
        else:
            s = self
        s = NSArray(s, "scalar", self.fmt, self.is_real)

        return s

    # ==================================================
    def shift(self, with_shift=False):
        """
        shift elements within range [0,1).

        Args:
            with_shift (bool): return shift ?

        Returns:
            - NSArray: shifted array.
            or
            - NSArray: shift, i.e., orginal = shifted + shift.
        """

        def get_shift(v):
            s = sp.S(0)
            while v - s < 0 or v - s >= 1:
                if v - s < 0:
                    s -= 1
                else:
                    s += 1
            return s

        subs = {i: sp.S(0) for i in self.var.keys()}
        s = self.subs(subs)  # put zero for all variables

        if self.style in ["bond", "bond_th", "bond_sv"]:
            s = s.convert_bond("bond")[1]

        sht = NSArray._elementwise(get_shift, s)
        if self.style in ["bond", "bond_th", "bond_sv"]:
            v, c = self.convert_bond("bond")
            c = c - sht
            shifted = NSArray.create_bond_from_pair(v, c, "bond")
            b1, b2 = shifted.convert_bond(self.style)
            shifted = NSArray.create_bond_from_pair(b1, b2, self.style)
            st = "vector"
        else:
            shifted = self - sht
            st = self.style

        if with_shift:
            sht = NSArray(sht, st, self.fmt, self.is_real)
            return shifted, sht
        else:
            return shifted

    # ==================================================
    def remove_duplicate(self, sort=False):
        """
        remove duplicate elements.

        Args:
            sort (bool, optional): sort ?

        Returns:
            NSArray: removed array.

        Notes:
            - for scalar, convert to 1d array.
        """
        if self.style != "scalar" and not self.lst:
            return self

        if self.style in ["vector", "matrix"]:
            s = list(set([tuple(i.ravel()) for i in self]))

        elif self.style in ["bond", "bond_th", "bond_sv"]:
            shape = super().shape
            s = self.reshape((shape[0], shape[1] * shape[2]))  # concatinate two vectors.
            s = np.array(list(set([tuple(i.ravel()) for i in s])))
            s = s.reshape((len(s), 2, shape[2])).tolist()
        else:
            s = list(set(self.ravel()))
        s = NSArray(np.array(s), self.style, self.fmt, self.is_real)

        if sort:
            s = s.sort()

        return s

    # ==================================================
    def clip(self, r1, r2):
        """
        clipping indices.

        Args:
            r1 (list): lower bound in each dimension.
            r2 (list): upper bound in each dimension.

        Returns:
            ndarray: clipping indices.
        """
        if self.style not in ["vector", "bond", "bond_th", "bond_sv"]:
            raise KeyError("it is valid only for vector or bond.")
        if len(r1) != len(r2):
            raise KeyError("size of r1 and r2 is different.")

        d = len(r1)

        if self.style == "vector":
            s = self
            if self.fmt != "value":
                s = s.value()

            if self.lst:
                cond = [f"(s[:,{i}]>r1[{i}])" for i in range(d)] + [f"(s[:,{i}]<r2[{i}])" for i in range(d)]
            else:
                cond = [f"(s[{i}]>r1[{i}])" for i in range(d)] + [f"(s[{i}]<r2[{i}])" for i in range(d)]
            cond = "np.where(" + " & ".join(cond) + ")"

            idx = eval(cond)
        else:
            t, h = self.convert_bond("bond_th")
            if self.fmt != "value":
                t = t.value()
                h = h.value()

            if self.lst:
                cond = (
                    [f"(t[:,{i}]>r1[{i}])" for i in range(d)]
                    + [f"(t[:,{i}]<r2[{i}])" for i in range(d)]
                    + [f"(h[:,{i}]>r1[{i}])" for i in range(d)]
                    + [f"(h[:,{i}]<r2[{i}])" for i in range(d)]
                )
            else:
                cond = (
                    [f"(t[{i}]>r1[{i}])" for i in range(d)]
                    + [f"(t[{i}]<r2[{i}])" for i in range(d)]
                    + [f"(h[{i}]>r1[{i}])" for i in range(d)]
                    + [f"(h[{i}]<r2[{i}])" for i in range(d)]
                )
            cond = "np.where(" + " & ".join(cond) + ")"

            idx = eval(cond)

        return idx[0]

    # ==================================================
    @classmethod
    def distance(cls, s1, s2, G=None, accuracy=4):
        """
        group of sites with the same distance (in increasing order).

        Args:
            s1 (NSArray): vector array.
            s2 (NSArray): vector array.
            G (NSArray, optional): metric matrix (None = unit matrix).
            accuracy (int, optional): accuracy of digit.

        Returns:
            dict : i, j are indices of positions (i<=j only for s1=s2), { distance(float): [(i(int),j(int))] }.
        """
        if s1.style != "vector":
            raise KeyError("it is valid only for vector.")
        if s2.style != "vector":
            raise KeyError("it is valid only for vector.")
        if s1.shape != s2.shape:
            raise KeyError("vector size is different.")
        if G is not None:
            if G.style != "matrix" or G.lst:
                raise KeyError("G is invalid.")
            if G.shape[0] != G.shape[1] or G.shape[0] != s1.shape[0]:
                raise KeyError("invalid shape of G.")

        if G is None:
            G = np.eye(s1.shape[0])
        diff = id(s1) != id(s2)
        if s1.fmt != "value":
            s1 = s1.value()
        if diff and s2.fmt != "value":
            s2 = s2.value()
        else:
            s2 = s1

        d = {0: []}
        for i, v1 in enumerate(s1):
            for j, v2 in enumerate(s2):
                if diff or i <= j:
                    r = v1 - v2
                    dist = round(float(np.sqrt(r @ G @ r)), accuracy)
                    d[dist] = d.get(dist, []) + [(i, j)]
        d = {i: j for i, j in sorted(d.items())}

        return d

    # ==================================================
    @classmethod
    def igrid(cls, N, offset=None):
        """
        create integer grid points.

        Args:
            N (list): number of points in each direction.
            offset (tuple, optional): offset in each direction. 0 is used for None.

        Returns:
            NSArray: grid points.

        Notes:
            - grid point: increase of indices from left to right.
            - x[i] = offset + i.
        """
        d = len(N)
        if offset is None:
            offset = [0] * d
        g = [np.arange(offset[i], offset[i] + N[i]) for i in range(d)]
        g = np.meshgrid(*g[::-1], indexing="ij")
        grid = np.stack([i.ravel() for i in g][::-1], axis=1)
        s = NSArray(grid, style="scalar")

        return s

    # ==================================================
    @classmethod
    def grid(cls, grid_min, grid_max, grid_n, endpoint=False):
        """
        create grid points.

        Args:
            grid_min (list): lower bounds in each direction.
            grid_max (list): upper bounds in each direction.
            grid_n (list): number of points in each direction.
            endpoint (bool, optional): include end point ?

        Returns:
            NSArray: grid points.

        Notes:
            - grid point: increase of indices from left to right.
            - x[i] = (max-min)*i/n for endpoint is False, otherwise (max-min)*i/(n-1).
        """
        d = len(grid_n)
        r = [np.linspace(grid_min[i], grid_max[i], grid_n[i], endpoint=endpoint) for i in range(d)]
        r = np.meshgrid(*r[::-1], indexing="ij")
        grid = np.stack([i.ravel() for i in r][::-1], axis=1)
        s = NSArray(grid, style="scalar", fmt="value")

        return s

    # ==================================================
    @classmethod
    def grid_path(cls, pts, gpath, N1=100, A=None):
        """
        grid points along path.

        Args:
            pts (dict): definitions of points, e.g., {"A":[1,2,3],"B":[3,4,5]}.
            gpath (str): path, e.g., "A-B|C-D-E".
            N1 (int, optional): number of divisions.
            A (NSArray, optional): conversion matrix.

        Returns:
            - NSArray: grid points.
            - NSArray: linear positions.
            - dict: {disconnected linear position:label}.
        """
        if A is None:
            d = np.array(list(pts.values())[0]).shape[0]
            A = np.eye(d)

        gpath = remove_space(gpath)
        glabel = gpath.split("-")
        gpath = gpath.split("|")
        gpath = [i.split("-") for i in gpath]
        gpath = [[(i1, i2) for i1, i2 in zip(i[:-1], i[1:])] for i in gpath]
        gpath = sum(gpath, [])

        grid = []
        glin = []
        gdis = [0]
        x = 0
        for s, e in gpath:
            s = np.array(pts[s])
            e = np.array(pts[e])
            dv = (e - s) / N1
            d = np.linalg.norm(dv @ A.T)
            for j in range(N1):
                glin.append(x)
                grid.append(s + j * dv)
                x += d
            grid.append(s + N1 * dv)
            glin.append(x)
            gdis.append(x)

        grid = NSArray(grid, "vector", fmt="value")
        glin = NSArray(glin, "scalar", fmt="value")
        gdis = dict(zip(gdis, glabel))

        return grid, glin, gdis

    # ==================================================
    @classmethod
    def vector3d(cls, head="Q", pre=None):
        """
        3d vector.

        Args:
            head (str, optional): type of vector, Q/G/T/M.
            pre (str, optional): head of symbol.

        Returns:
            NSArray: 3d vector.
        """
        d = {"Q": "[x,y,z]", "G": "[X,Y,Z]", "T": "[t_x,t_y,t_z]", "M": "[m_x,m_y,m_z]"}
        if head not in d.keys():
            raise KeyError("invalid head is given.")

        if pre is None:
            s = d[head]
        else:
            s = f"[{pre}_x,{pre}_y,{pre}_z]"
        s = NSArray(s, real=True)
        return s

    # ==================================================
    def lambdify(self):
        """
        lambda function of array.

        Returns:
            function: function that takes (a list of) params as argument.

        Notes:
            - returned function takes (a list of) params, ndarray and NSArray.
            - doc can be viewed by f.__doc__.
        """
        if self.fmt != "sympy":
            raise KeyError("it is valid only for sympy format.")

        args = self.var.values()
        f = sp.lambdify(args, self.tolist(), "numpy")

        def fv(*x):
            if type(x[0]) == NSArray:
                x = x[0].value().numpy()
            else:
                x = np.array(*x)

            if x.ndim == 0:
                fx = np.array(f(x))
            elif x.ndim == 1:
                if len(args) == 1:
                    fx = np.array([f(i) for i in x])
                else:
                    fx = np.array(f(*x))
            else:
                fx = np.apply_along_axis(lambda i: f(*i), 1, x)

            return NSArray(fx, self.style, fmt="value")

        vstr = str(self.variable())[1:-1]
        fv.__doc__ = remove_space(f"f({vstr})".replace("'", "")) + " = " + str(self)

        return fv

    # ==================================================
    def diagonalize_hermite(self, params=None, eigenvector=True):
        """
        diagonalize hermitian matrix.

        Args:
            params (list, np.array, NSArray, optional): parameter set in each row (None = numerical data).
            eigenvector (bool, optional): compute eigen vector ?

        Returns:
            - function: used function.
            - NSArray: eigen values (vectors).
            - NSArray: eigen vectors (matrices) eigen vecotr in each column (optional).
        """
        if params is None:
            if self.fmt != "value":
                raise KeyError("it is valid only for value format.")
            f = None
            ms = self.numpy()
        else:
            f = self.lambdify()
            ms = f(params)
        d = ms.shape[1]
        if eigenvector:
            vals = np.empty(shape=(0, d), dtype="float64")
            vecs = np.empty(shape=(d, d, 0), dtype="complex128")
            for val, vec in map(np.linalg.eigh, ms):
                vals = np.vstack([vals, val])
                vecs = np.dstack([vecs, vec])
            vals = NSArray(vals, "vector", fmt="value")
            vecs = vecs.transpose((2, 0, 1))
            vecs = NSArray(vecs, "matrix", fmt="value")
            return f, vals, vecs
        else:
            vals = np.array(list(map(np.linalg.eigvalsh, ms))).T
            vals = NSArray(vals.T, "vector", fmt="value")
            return f, vals

    # ================================================== arithmetic
    def sum(self):
        """
        sum of array.

        Returns:
            NSArray: summed array.
        """
        if self.style == "scalar":
            s = np.sum(self.numpy())
        else:
            if self.fmt == "sympy":
                s = np.full(self.shape, sp.S(0))
            else:
                s = np.zeros(self.shape)
            for i in self:
                s += i
        s = NSArray(np.array(s), self.style, self.fmt, self.is_real)
        return s

    # ==================================================
    def norm(self):
        """
        norm of array.

        Returns:
            NSArray: norm of array.

        Notes:
            - for bond, return bond lengths, and for scalar, return absolute values.
        """
        if self.style in ["vector", "matrix"]:
            s = NSArray._apply(lambda i: sp.sqrtdenest(sp.sqrt(sp.trace(sp.Matrix(i).H @ sp.Matrix(i)))), self, self.style)
        elif self.style in ["bond", "bond_th", "bond_sv"]:
            v = self.convert_bond("bond")[0]
            s = NSArray._apply(lambda i: sp.sqrtdenest(sp.sqrt(sp.trace(sp.Matrix(i).H @ sp.Matrix(i)))), v, v.style)
        else:
            s = NSArray._elementwise(lambda i: sp.sqrtdenest(sp.sqrt(i * i.conjugate())), self)
        s = NSArray(s, "scalar", fmt=self.fmt, real=self.is_real)
        return s

    # ==================================================
    def normalize(self, ret_norm=False):
        """
        normalize matrix and its normalization const.

        Args:
            ret_norm (bool, optional): return norm ?

        Returns:
            - NSArray: normalized matrix.
            - NSArray: normalization const. (optional).

        Notes:
            - original matrix = normalization const. * normalized matrix.
        """
        if self.style not in ["vector", "matrix"]:
            raise KeyError("it is valid only for vector or matrix.")
        norm = self.norm()
        if self.lst:
            if self.fmt == "sympy":
                s = [i if n == 0 else (i / n).expand() for i, n in zip(self, norm)]
            else:
                s = [i if n == 0 else (i / n) for i, n in zip(self, norm)]
        else:
            if self.fmt == "sympy":
                s = self if norm == 0 else (self / norm).expand()
            else:
                s = self if norm == 0 else (self / norm)

        s = NSArray(np.array(s), self.style, self.fmt, self.is_real)

        if ret_norm:
            return s, norm
        else:
            return s

    # ==================================================
    @classmethod
    def dot(cls, s1, s2):
        """
        inner product s1.s2 or Tr(s1^dagger.s2) or sum(s1*s2).

        Args:
            s1 (NSArray): array 1.
            s2 (NSArray): array 2.

        Returns:
            sympy or float or complex: inner product.
        """
        if type(s2) == NSArray:
            s2 = s2.numpy()
        if type(s1) == NSArray:
            s1 = s1.numpy()
        s1c = NSArray._elementwise(lambda i: i.conjugate(), s1)
        s = np.sum(s1c * s2).expand()
        return s

    # ==================================================
    @classmethod
    def orthogonalize(cls, v, nmax=None):
        """
        orthogonalize vector/matrix by Gram-Schmidt orthogonalization method.

        Args:
            v (NSArray): vector/matrix array to be orthogonalized.
            nmax (int, optional): max. number of nonzero basis.

        Returns:
            - NSArray: orthogonalized vector/matrix array.
            - ndarray: nonzero vector/matrix indexes.
        """
        if v.style not in ["vector", "matrix"]:
            raise KeyError("it is valid only for vector or matrix.")
        if not v.lst:
            raise KeyError("it is valid only for list type.")

        ev = []
        nulvec = np.full(v.shape, sp.S(0))

        cnt = 0
        for v0 in v:
            s = nulvec.copy()
            for evi in ev:
                s += NSArray.dot(evi, v0) * evi
            e = v0 - s
            d = e.norm()
            if d != 0:
                e = e / d
                e = e.radsimp()
                cnt += 1
            else:
                e = nulvec.copy()
            ev.append(e)
            if nmax is not None and cnt == nmax:
                break

        ev = NSArray(ev, v.style, v.fmt, v.is_real)
        idx = np.array([i for i, b in enumerate(ev) if not (b == 0).all()])

        return ev, idx

    # ==================================================
    @classmethod
    def from_str(cls, s_lst, fmt="sympy", real=True):
        """
        create array from list of string.

        Args:
            s_lst ([str]): list of string.
            fmt (str, optional): sympy/value.
            real (bool, optional): real array ?

        Returns:
            NSArray: array.
        """
        if not hasattr(s_lst, "__iter__"):
            raise KeyError("non list is given.")
        s = "{" + ",".join(s_lst) + "}"
        return NSArray(s, fmt=fmt, real=real)

    # ==================================================
    @classmethod
    def zeros(cls, shape, style, fmt="sympy"):
        """
        create zero array.

        Args:
            shape (int or tuple): shape of array.
            style (str): scalar/vector/matrix.
            fmt (str, optional): sympy/value.
        """
        # key check.
        if style not in [None, "scalar", "vector", "matrix"]:
            raise KeyError(f"unknown style = {style} is given.")
        if fmt not in ["sympy", "value"]:
            raise KeyError(f"unknown format = {fmt} is given.")

        if style is None:
            style = "scalar"

        if fmt == "sympy":
            z = np.full(shape, sp.S(0))
        else:
            z = np.full(shape, 0.0)

        a = NSArray(z, style, fmt)
        return a
