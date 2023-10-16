"""
This class manages a set of data frames.
"""
import pandas as pd


# ==================================================
class DataSet(dict):
    """
    class to manage data frames.

    Attributes:
        self (dict): { name: [pd.DataFrame] }
    """

    # self._role (dict): { name: [role] }

    # ==================================================
    def __init__(self, data=None):
        """
        initialize the class.

        Args:
            data (dict, optional): { name: ( [column], [role], [[value]] ) }

        Notes:
            - value can be omitted.
            - if [role] is None, None is used, while if [role] is str, str is used for all columns.
            - if [[value]] is None, empty data frame is created.
        """
        if data is None:
            data = {}
        self._header = {}
        self._role = {}
        for name, data1 in data.items():
            if len(data1) < 1:
                raise ValueError("dataset is missing.")
            if len(data1) == 1:
                data1 = (*data1, None, None)
            elif len(data1) == 2:
                data1 = (*data1, None)
            self._create_dataset(name, *data1)

    # ==================================================
    def _create_dataset(self, name, col, role, val):
        """
        create data frames.

        Args:
            name (str): name of data frame
            col (list or str): list of column's names
            role (list or str): list of roles

        Raises:
            ValueError: raised when sizes of col and role are different.
        """
        self[name] = pd.DataFrame(index=[], columns=col)

        ncol = len(col)
        self._header[name] = col

        if role is None:
            role = [None] * ncol
        elif type(role) == str:
            role = [role] * ncol

        if len(role) != ncol:
            raise ValueError(f"the sizes of col and prop are different, ({ncol},{len(role)}).")

        self._role[name] = role

        if val is not None:
            for row in val:
                self.append(name, row)

    # ==================================================
    @property
    def role(self):
        """
        role of data frames.

        Returns:
            dict: { name: [role] }
        """
        return self._role

    # ==================================================
    @property
    def header(self):
        """
        header of data frames.

        Returns:
            dict: { name: [header] }
        """
        return self._header

    # ==================================================
    def set_header(self, name, col):
        """
        set header of data frames.

        Args:
            name (str): name of data frame
            col (list or str): list of column's names
        """
        self[name] = pd.DataFrame(index=[], columns=col)
        self._header[name] = col

    # ==================================================
    def set_role(self, name, role):
        """
        set role of data frame.

        Args:
            name (str): name of data frame
            role (list or str): list of roles. if None or str, None or str is used for all columns

        Raises:
            ValueError: raised when name cannot be found or sizes of columns and role are different.
        """
        if name not in self.keys():
            raise ValueError(f"cannot find {name}.")
        ncol = len(self._header[name])
        if type(role) == str:
            role = [role] * ncol
        if len(role) != ncol:
            raise ValueError(f"the sizes of col and prop are different, ({ncol},{len(role)}).")
        self._role[name] = role

    # ==================================================
    def load_csv(self, name, filename, role=None):
        """
        load CSV into named data frame.

        Args:
            name (str): name of data frame
            filename (str): file name of CSV (first line is used as column header)
            role (list or str, optional): list of roles. if None or str, None or str is used for all columns

        Raises:
            ValueError: raised when sizes of read columns and role are different.
        """
        df = pd.read_csv(filename, skipinitialspace=True)
        self._create_dataset(name, df.columns.tolist(), role, df.values.tolist())

    # ==================================================
    def save_csv(self, head, name=None):
        """
        save CSV.

        Args:
            head (str): head of filename
            name (str, optional): name of data frame. if None, save all data frames separately with "_name"

        Notes:
            - role is lost.
        """
        if name is None:
            for name, df in self.items():
                df.to_csv(head + "_" + name + ".csv", index=False)
        else:
            self[name].to_csv(head + ".csv", index=False)

    # ==================================================
    def append(self, name, row):
        """
        append row to specified data frame.

        Args:
            name (str): name of data frame
            row (list): list of values

        Raises:
            ValueError: raised when size of row is different from columns.
        """
        dataset = self[name]
        if len(row) != len(dataset.columns):
            ncol = len(dataset.columns)
            nrow = len(row)
            raise ValueError(f"the size of row is different from that of columns, ({nrow},{ncol}).")
        self[name] = pd.concat([dataset, pd.DataFrame([row], columns=dataset.columns)], ignore_index=True)

    # ==================================================
    def indexed(self, name, index, sort=True):
        """
        indexed and sorted by indices.

        Args:
            name (str): name of data frame
            index (str or list): index or indices
            sort (bool, optional): sort by indices if True

        Returns:
            pd.DataFrame: indexed (and sorted) data frame.
        """
        df = self[name].copy()
        df["id"] = list(range(len(self[name])))
        if sort:
            return df.set_index(index).sort_index()
        else:
            return df.set_index(index)

    # ==================================================
    def extract(self, name, cond, index=False):
        """
        extract rows that match the given condition.

        Args:
            name (str): name of data frame
            cond (str): query condition
            index (bool, optional): return indices if True, otherwise return extracted data frame

        Returns:
            list or pd.DataFrame: list of indices if index is True, otherwise extracted data frame (reindexed).
        """
        r = self[name].query(cond)
        if index:
            return r.index.tolist()
        else:
            return r.reset_index(drop=True)

    # ==================================================
    def remove(self, name, cond, inplace=False):
        """
        remove rows that match the given condition.

        Args:
            name (str): name of data frame
            cond (str): query condition
            inplace (bool, optional): remove inplace if True

        Returns:
            pd.DataFrame or None: removed data frame (reindexed) if inplace is False, otherwise remove rows inplace.
        """
        idx = self.extract(name, cond, index=True)
        if inplace:
            self[name].drop(idx, inplace=True)
            self[name].reset_index(inplace=True, drop=True)
        else:
            return self[name].drop(idx).reset_index(drop=True)

    # ==================================================
    def to_data(self):
        """
        convert to raw data.

        Returns:
            dict: raw data. { name: ( [column], [role], [[value]] ) }

        Notes:
            returned dictionary can be used to create dataset as DataSet(data).
        """
        data = {name: (df.columns.tolist(), self.role[name], df.values.tolist()) for name, df in self.items()}
        return data
