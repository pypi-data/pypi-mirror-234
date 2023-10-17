from databricks import sql

class DatabricksSQLClient:
    """
    Databricks remote SQL client for executing SQL statements on a Databricks cluster.

    This class provides a convenient way to connect to a Databricks cluster and execute SQL statements.

    Args:
        server_hostname (str): The hostname of the Databricks server.
        http_path (str): The HTTP path for the Databricks server.
        access_token (str): The access token for authentication.
    """
    def __init__(self, server_hostname: str, http_path: str, access_token: str):
        self._server_hostname = server_hostname
        self._http_path = http_path
        self._token = access_token

    def execute_statement(self, statement: str):
        """
        Execute an SQL statement on the Databricks cluster.

        Args:
            statement (str): The SQL statement to execute.

        Returns:
            ArrowTable: The result of the SQL query as an Arrow table.
        """
        with sql.connect(server_hostname=self._server_hostname,
                         http_path=self._http_path,
                         access_token=self._token) as connection:

            with connection.cursor() as cursor:
                cursor.execute(statement)
                return cursor.fetchall_arrow()