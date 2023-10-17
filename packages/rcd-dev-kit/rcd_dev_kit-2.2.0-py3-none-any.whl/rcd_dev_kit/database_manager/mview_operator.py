from abc import ABC
from .redshift_operator import RedshiftOperator  # Import necessary modules and classes
from sqlalchemy import inspect
from dotenv import load_dotenv, find_dotenv


class MvOperator(ABC):
    def __init__(self, database: str = 'staging', writer: str = 'cube_writer_prod'):
        """
        Initializes a Materialized Vue Object.

        Args:
            database (str): The name of the redshift database to connect to. Defaults to 'staging'.
            writer (str): The name of the writer. Defaults to 'cube_write_prod'.
        """
        load_dotenv(find_dotenv())  # Load environment variables from a .env file if available

        self.database = database
        self.writer = writer

        self._schema_name: str = None
        self._table_name: str = None

        self.ro = RedshiftOperator(database=self.database)  # Initialize a RedshiftOperator instance

        self.sql_mv_query = None  # Placeholder for the materialized view query

    def schema(self, name: str) -> 'MvOperator':
        """
        Set the schema name for the materialized view.

        Args:
            name (str): The name of the schema.

        Returns:
            MvOperator: The instance of the MvOperator class.
        """
        self._schema_name = name
        return self

    def table_name(self, name: str) -> 'MvOperator':
        """
        Set the table name for the materialized view.

        Args:
            name (str): The name of the table.

        Returns:
            MvOperator: The instance of the MvOperator class.
        """
        self._table_name = name
        return self

    @property
    def materialized_view_name(self) -> str:
        """
        Get the full name of the materialized view.

        Returns:
            str: The full name of the materialized view.
        """
        if self._schema_name is None or self._table_name is None:
            raise ValueError("Schema name and table name must be set.")
        return f"{self._schema_name}.{self._table_name}"

    def process_materialized_view(self) -> None:
        """
        Process the materialized view by creating or refreshing it.
        """
        inspect_engine = inspect(self.ro.engine)
        if not inspect_engine.has_table(schema=self._schema_name, table_name=self.table_name):
            print(f"Creating materialized_view {self.materialized_view_name}...")
            self.create_materialized_view()
            self.grant_select_materialized_view()
        else:
            print(f"Refreshing materialized_view {self.materialized_view_name}...")
            self.refresh_materialized_view()

    def create_materialized_view(self) -> None:
        """
        Create the materialized view.
        """
        self.ro.conn.execution_options(isolation_level="AUTOCOMMIT").execute(self.sql_mv_query)
        print("📌 Materialized view created")

    def grant_select_materialized_view(self) -> None:
        """
        Grant SELECT privileges on the materialized view to a specific writer.
        """
        grant_query = f"GRANT SELECT ON {self.materialized_view_name} TO {self.writer};"
        self.ro.conn.execution_options(isolation_level="AUTOCOMMIT").execute(grant_query)
        print(f"📌 Granted SELECT on {self.materialized_view_name} to {self.writer}")

    def drop_materialized_view(self) -> None:
        """
        Drop the materialized view if it exists.
        """
        delete_query = f"DROP MATERIALIZED VIEW IF EXISTS {self.materialized_view_name};"
        self.ro.conn.execution_options(isolation_level="AUTOCOMMIT").execute(delete_query)
        print(f"📌 {self.materialized_view_name} is dropped")

    def refresh_materialized_view(self) -> None:
        """
        Refresh the materialized view.
        """
        refresh_query = f"REFRESH MATERIALIZED VIEW {self.materialized_view_name};"
        self.ro.conn.execution_options(isolation_level="AUTOCOMMIT").execute(refresh_query)
        print(f"📌 {self.materialized_view_name} is refreshed")
