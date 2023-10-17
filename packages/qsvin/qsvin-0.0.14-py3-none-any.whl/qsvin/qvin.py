import logging
from .vin_decoder import *
from .remote_client import DatabricksSQLClient

class QVin(VinDecoder):
    """
    VIN decoding and data management class with additional features.

    Provides methods for decoding VINs, looking up VIN information, and exporting data to Excel. Extends the VinDecoder class.
    """
    def __init__(self, credentials=None): 
        if credentials: 
            from databricks import sql
            logging.getLogger("databricks.sql").setLevel(logging.ERROR)
            connector = DatabricksSQLClient(**credentials).execute_statement
        else: 
            from pyspark.sql import SparkSession
            connector = SparkSession.builder.getOrCreate().sql
        super(QVin, self).__init__(connector)

    def lookup_vin(self, vin, query=None): 
        """
        Look up VIN information and replace NaN values with None.

        Args:
            vin (str, list): The VIN(s) to look up.
            query (str): An optional SQL query to filter data from the database.

        Returns:
            pd.DataFrame or None: The decoded VIN information with NaN values replaced by None.
        """
        response=super().lookup_vin(vin, query=query).replace(np.nan, None)
        return response
    
    def get_distinct(self, columns):
        """
        Get distinct values from the database for the specified columns.

        Args:
            columns (str, list): The columns for which to get distinct values.

        Returns:
            dict: A dictionary with columns as keys and arrays of distinct values as values.
        """
        if isinstance(columns, str): columns=[columns]
        return {c:self._distinct(self._db_connector, c) for c in columns}