from .db_client import *
from .external_api import *


def insertValsToHive(data):
    """
    Convert data to a list of SQL values for insertion into Hive.

    Args:
        data (dict): Data to be inserted.

    Returns:
        list: List of SQL values.
    """
    vals=[]
    for k,v in data.items():
        if k in ('other','year'): continue
        vals.append(f"\'{v}\'") if v else vals.append(f"NULL")
    return vals

class VinDecoder:
    """
    VIN decoding and data management class.

    Provides methods for decoding VINs, looking up VIN information, and exporting data to Excel.
    """
    def __init__(self, connector):
        self._db_connector =  QHiveConnector("qirevin.out_db", connector)
        self._vin_parser = VinInfo()
        self._vin_external_api=[VinNHTSA()]

    def _spark2pandas(self, df):
        """
        Convert a Spark DataFrame to a Pandas DataFrame.

        Args:
            df: Spark DataFrame.

        Returns:
            pd.DataFrame: Pandas DataFrame.
        """
        return df.to_pandas() if type(df).__name__ == 'Table' else df.toPandas()
    
    def _decomposeVin(self, vin, only_keys=False):
        """
        Decompose a VIN into its components.

        Args:
            vin (str): The VIN to decompose.
            only_keys (bool): If True, return only keys.

        Returns:
            dict: Decomposed VIN information.
        """
        decomposition=self._vin_parser.lookup_vin(vin)
        return {'wmi':decomposition['wmi'], 'vds':decomposition['vds'], 'vis':decomposition['vis']} if only_keys else decomposition
    
    def _queryData(self, vin):
        """
        Query data from the database for the given VINs.

        Args:
            vin (list): List of VINs to query.

        Returns:
            pd.DataFrame: Resulting data.
        """
        lookup_request=''
        for v in vin:
            vin_decoded=self._decomposeVin(v, only_keys=True)
            conditions=f"(vds = '{vin_decoded['vds']}' and wmi = '{vin_decoded['wmi']}' and vis = '{vin_decoded['vis']}')"
            lookup_request = lookup_request + " or " + conditions if lookup_request else conditions
        return self._spark2pandas(self._db_connector.selectObj("*", lookup_request))
        
    def lookup_vin(self, vin, query=None):
        """
        Look up VIN information in the database or through external APIs.

        Args:
            vin (str, list): The VIN(s) to look up.
            query (str): An optional SQL query to filter data from the database.

        Returns:
            pd.DataFrame or None: The decoded VIN information.
        """
        if all([vin,query]) or not any([vin,query]): Exception('ValueError. Use either vin or query')
        if query: return self._spark2pandas(self._db_connector.selectObj("*", query))
        if isinstance(vin, str): vin=[vin]
        result=[self._queryData(vin[i:i+50]) for i in range(0, len(vin), 50)]
        merged_df = pd.concat(result).merge(pd.DataFrame([{**self._decomposeVin(v, only_keys=True), "vin":v} for v in vin]), on=['wmi', 'vds', 'vis'], how='right', indicator=True)
        vin = merged_df[merged_df['_merge'] == 'right_only'].drop(columns=['_merge'])['vin'].values
        for v in vin:
            try:
                decoded_vin = self._parse_vin(v)
                if decoded_vin is not None: result.append(decoded_vin)
            except Exception as e: 
                print(e)
                continue
        if len(result)==0: return None
        elif len(result)==1: return result[0]
        return pd.concat(result)

    def _parse_vin(self, v):
        """
        Parse VIN information and insert it into the database.

        Args:
            v (str): The VIN to parse.

        Returns:
            pd.DataFrame or None: The parsed VIN information.
        """
        vin_info=self._decomposeVin(v)
        if not all([vin_info['vds'],vin_info['wmi'],vin_info['vis']]): return None
        conditions=f"vds = '{vin_info['vds']}' and wmi = '{vin_info['wmi']}' and vis = '{vin_info['vis']}'"
        external_api_res = {}
        for api in self._vin_external_api:
            try: external_api_res.update(api.lookup_vin(v))
            except: continue
        insert_data={**vin_info, **external_api_res, "other": {**vin_info.get("other", {}), **external_api_res.get("other", {})}} if all([external_api_res['vds'],external_api_res['wmi'],external_api_res['vis']]) else vin_info
        self._insert({k:v for k,v in insert_data.items() if v is not None}, self._db_connector)
        return self._spark2pandas(self._db_connector.selectObj("*", conditions))
    
    def export_excel(self, vin, query=None, hierarchical=False, fname="output.xlsx"):
        """
        Export VIN information to an Excel file.

        Args:
            vin (str, list): The VIN(s) to export.
            query (str): An optional SQL query to filter data from the database.
            fname (str): The output file name.
        """
        response = self.lookup_vin(vin=vin, query=query, hierarchical=hierarchical)
        if isinstance(response, pd.DataFrame): 
            response['date_created'] = response['date_created'].dt.tz_localize(None)
            response.to_excel(fname)
        else: Exception('ValueError. No data to write')

    def _distinct(self, table, columns):
        """
        Get distinct values from a database table.

        Args:
            table: The database table to query.
            columns (str, list): The columns for which to get distinct values.

        Returns:
            np.ndarray: Array of distinct values.
        """
        if isinstance(columns, str): columns=[columns]
        q = f"select distinct {','.join(columns)} from {table.table}"
        return self._spark2pandas(self._db_connector.executeQuery(q)).values[:, 0]

    def _insert(self, data,table):
        data={**{k:None for k in table.columns if k != "date_created"}, **data}
        vals=','.join(insertValsToHive(data))
        q=f"""insert into table {table.table} ({','.join([x for x in data.keys() if x not in ('other', 'year', 'date_created')])},other,year,date_created) VALUES ({vals}, '{json.dumps(data.get('other', {}))}', {data.get("year", None)},current_timestamp())"""
        print(q)
        self._db_connector.executeQuery(q)