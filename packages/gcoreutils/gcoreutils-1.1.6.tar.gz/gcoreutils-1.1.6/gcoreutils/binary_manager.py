"""
This class manages binary data.
"""
import os
import sys
import pickle
import glob
from gcoreutils.string_util import class_name


# ==================================================
class BinaryManager(dict):  # { str: class }
    """
    binary data manager.
    """

    # Attributes:
    #    __bin_directory (str): binary data folder
    #    __verbose (bool): show info. ?
    #
    # ==================================================
    def __init__(self, bin_dir="", verbose=False):
        """
        initialize the class.

        Args:
            bin_dir (str, optional): directory for binary files.
            verbose (bool, optional): write message ?
        """
        bin_dir = os.path.dirname(bin_dir)
        if bin_dir == "":
            bin_dir = "."
        self.__bin_directory = bin_dir + "/"
        self.__verbose = verbose

    # ==================================================
    def _dprint(self, *s):
        if self.__verbose:
            print(*s, file=sys.stderr)

    # ==================================================
    def __getitem__(self, cls):
        """
        get binary class data.

        Args:
            cls (Any): a class that is created by cls().

        Returns:
            cls: class data. if it does not exist, binary file is created, otherwise it is read from saved file.
        """
        name = class_name(cls)

        p = self._file_name(name)
        if os.path.exists(p):
            if name in self.keys():
                return self.get(name)
            else:
                with open(p, "rb") as f:
                    data = pickle.load(f)
                self._dprint("read", p)
                self.setdefault(name, data)
                return data
        else:
            data = cls()
            with open(p, "wb") as f:
                pickle.dump(data, f)
            self._dprint("wrote", p)
            self.setdefault(name, data)
            return data

    # ==================================================
    def _file_name(self, tag):
        """
        full path file name for given name of data.

        Args:
            tag (str): name of data

        Returns:
            path: full path file name.
        """
        f = self.__bin_directory + tag + ".pkl"
        f = os.path.normpath(f)
        return f

    # ==================================================
    def load(self):
        """
        load all binary data in bin_dir.
        """
        fn = self._file_name("*")
        files = glob.glob(fn)

        for p in files:
            with open(p, "rb") as f:
                data = pickle.load(f)
            self._dprint("read", p)
            name = os.path.splitext(os.path.basename(p))[0]
            self.setdefault(name, data)
