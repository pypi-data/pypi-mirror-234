import pandas as pd

class QDBConnector:
    """
    Base class for database connectors.

    Provides common methods for working with a database table.
    """

    def selectObj(self, columns, condition):
        """
        Select data from the table.

        Args:
            columns (str or list): The columns to select. Pass "*" to select all columns.
            condition (str): The condition for the selection.

        Returns:
            pd.DataFrame, pyspark DataFrame: The selected data.

        Note:
            - If condition is a list, it will be joined with "&" as the condition.
            - If columns is "*", all columns are selected.
        """
        pass

    def deleteObj(self, idx):
        """
        Delete data from the table based on the provided index.

        Args:
            idx: The index of the data to be deleted.

        Note:
            This method should be implemented in derived classes.
        """
        pass

    def insertObj(self, new_data):
        """
        Insert new data into the table.

        Args:
            new_data (dict): A dictionary containing the data to be inserted.

        Note:
            This method should be implemented in derived classes.
        """
        pass

    def updateObj(self, new_data, index=None):
        """
        Update data in the table.

        Args:
            new_data (dict): A dictionary containing the new data.
            index: The index or condition to specify which data to update.

        Note:
            This method should be implemented in derived classes.
        """
        pass


class QPDConnector(QDBConnector):
    """
    Connector for Pandas DataFrames.

    Provides methods for working with Pandas DataFrames as a database table.
    """

    def __init__(self, table):
        self.table = table

    def selectObj(self, columns, condition):
        if isinstance(condition, list):
            condition = " & ".join(condition)
        return self.table.query(condition)[self.table.columns if columns == "*" else columns].copy()

    def deleteObj(self, idx):
        self.table.drop(idx, inplace=True)

    def insertObj(self, new_data):
        new_data = pd.DataFrame([new_data])
        self.table = pd.concat([self.table, new_data], ignore_index=True)

    def updateObj(self, new_data, index=None):
        if isinstance(new_data, dict):
            new_data = pd.DataFrame(new_data, index=index)
        self.table.update(new_data)

    def columns(self):
        return self.table.columns


class QHiveConnector(QDBConnector):
    """
    Connector for Hive tables.

    Provides methods for working with Hive tables.
    """

    def __init__(self, table, connector, to_pandas=True):
        self._table = table
        self._connector = connector
        self._columns = self._get_columns(self._connector(f"select * from {self._table} limit 1"))

    def _get_columns(self, row):
        if type(row).__name__ == 'Table':
            row = row.to_pandas()
        return row.columns

    def selectObj(self, columns="*", condition=None):
        print(f"select {columns} from {self._table} {'where ' + condition if condition else ''}")
        return self._connector(f"select {columns} from {self._table} {'where ' + condition if condition else ''}")

    def deleteObj(self, condition):
        print(f"delete from {self._table} where {condition}")
        self._connector(f"delete from {self._table} where {condition}")

    def insertObj(self, new_data):
        keys = new_data.keys()
        values = [qstr(x) for x in new_data.values()]
        print(f"insert into {self._table} ({','.join(keys)}) VALUES ({','.join(values)})")
        self._connector(f"insert into table {self._table} ({','.join(keys)}) VALUES ({','.join(values)})")

    def executeQuery(self, query):
        return self._connector(query)

    @property
    def columns(self):
        return self._columns

    @property
    def table(self):
        return self._table
