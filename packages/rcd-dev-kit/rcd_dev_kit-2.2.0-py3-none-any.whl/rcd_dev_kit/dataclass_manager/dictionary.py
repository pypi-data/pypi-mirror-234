from rcd_dev_kit.database_manager import send_to_redshift, RedshiftOperator, read_from_redshift
from rcd_dev_kit.decorator_manager import timeit
from typing import Optional
import pandas as pd
from abc import ABC
import os


class Dictionary(ABC):
    """
    Class Dictionary. One class = One dictionary table
    Use this class to create or read dictionary table
    """
    def __init__(self,
                 database=None,
                 schema_name=None,
                 table_name=None):
        self.database = (
            "staging"
            if database is None
            else database.lower()
        )
        self.schema_name = (
            "reference"
            if schema_name is None
            else schema_name.lower()
        )
        self.table_name = table_name

        self.ro = RedshiftOperator(database=self.database)
        self.ro.schema = self.schema_name
        self.ro.table = self.table_name

        self.df_final = pd.DataFrame()

    @timeit(program_name=f"🗂Upload dictionary to redshift")
    def upload_to_redshift(self, df = pd.DataFrame(),
                           json_path: str = "table_metadata.json",
                           mode: str = 'merge_update',
                           column_pivot: list = [],
                           drop: bool = False, check: bool = False, pk: list = [],
                           first_data: Optional[str] = None,
                           last_data: Optional[str] = None):
        """
        Function upload_to_redshift
        Use this function to send data to s3 bucket and redshift.

        Args:
            df(pd.Dataframe): Dataframe to send to redshift
            json_path(str): Path where to find the metadata JSON file
            mode(str): {'overwrite', 'merge_replace', 'merge_update', 'append'}. 'merge_update' by default
                    Define how data will be send to redshift.
                    overwrite : Replace the entire table.
                    merge_replace : Replace all values if rows exist in table and insert new rows.
                    merge_update : Update only non-null value if row exist in table and insert new rows.
                    append : insert rows to the existing table
            column_pivot(list) : List of columns names to merge on. Column names must be found in both side.
                            Mandatory if mode in {'merge_replace', 'merge_update'}.
            drop(bool): (Avoid to use!) False by default. If True, allow to drop columns.
            check(bool): False by default. If True, check the column type and length is consistent as current table in
                     redshift.
            pk(list): List of columns names to set as primary keys.
            first_data(str): The most ancient date present regarded by your data.
            last_data(str): The most recent date present regarded by your data.

        """
        current_pk = self.ro.get_primary_keys()
        if len(column_pivot) == 0 and mode != "overwrite" and len(current_pk) > 0:
            print('Search for primary key ...')
            column_pivot = current_pk
            print('column_pivot = ', column_pivot)
        send_to_redshift(database=self.database, schema=self.schema_name, table=self.table_name,
                         df=df,
                         json_path=json_path,
                         mode=mode, column_pivot=column_pivot,
                         drop=drop,
                         check=check,
                         first_data=first_data,
                         last_data=last_data
                         )
        if pk:
            self.set_primary_keys(pk)

    def set_primary_keys(self, lst_pk: list = [], drop: bool = False):
        self.ro.set_primary_key(columns=lst_pk, drop=drop)

    def get(self):
        if self.ro.detect_table():
            self.df_final = read_from_redshift(database=self.database, method='auto',
                                               schema=self.schema_name, table=self.table_name)
        else:
            print(f"❌ Table {self.schema_name}.{self.table_name} does not exist")
            pass

    def join(self, df_to_merge: pd.DataFrame, how: str, on: list, select: list = []) -> pd.DataFrame:
        if len(self.df_final.index) == 0:
            self.get()

        df_to_merge[on] = df_to_merge[on].astype(str)
        if select:
            select.extend(on)
            df_select = self.df_final[select]
            return df_to_merge.merge(df_select, how=how, on=on)
        else:
            return df_to_merge.merge(self.df_final, how=how, on=on)

