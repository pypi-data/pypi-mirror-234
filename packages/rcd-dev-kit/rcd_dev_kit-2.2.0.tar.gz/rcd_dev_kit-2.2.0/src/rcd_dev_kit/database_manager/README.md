# Database Manager
Database Manager is a Python module for manipulating data with different databases.

## Set up
Set up .env as follow:
```python
#elasticsearch
ELASTICSEARCH_SCHEME=x
ELASTICSEARCH_PORT=x
ELASTICSEARCH_HOST=x
ELASTICSEARCH_USER=x
ELASTICSEARCH_PASSWORD=x

#redshift
REDSHIFT_HOST=x
REDSHIFT_USER=x
REDSHIFT_PASSWORD=x
REDSHIFT_DB=x

#S3
S3_BUCKET_DEV=x
S3_BUCKET_RAW=x
S3_BUCKET_DATAMART=x
AWS_ACCESS_KEY_ID=x
AWS_SECRET_ACCESS_KEY=x
AWS_DEFAULT_REGION=x

#Gcloud
GOOGLE_APPLICATION_CREDENTIALS=x
OPEN_DATA_SOURCE_BUCKET=x
GCLOUD_PROJECT=x
```

## Usage
### Elasticsearch
* index_json_bulk_parallel
    ```python
    import pandas as pd
    from rcd_dev_kit import database_manager
    # bulk indexing data to elasticsearch
    database_manager.index_json_bulk_parallel(index_name="my_index_name", method="json", json_path='my_json_path', keyword="") # with json file
    database_manager.index_json_bulk_parallel(index_name="my_index_name", method="dataframe", df=my_dataframe) # with pandas dataframe, pass your dataframe by pd_dataframe
    ```

* index_json_bulk
    ```python
    database_manager.index_json_bulk(json_path="my_json_path", index_name="my_index_name", keyword="") # bulk indexing data to elasticsearch
    ```

* index_json
    ```python
    database_manager.index_json(json_path="my_json_path", index_name="my_index_name", keyword="") # indexing data to elasticsearch
    ```

### Redshift
* send_to_redshift
    ```python
    import pandas as pd
    database_manager.send_to_redshift(database="my_database", schema="test_schema", table="my_table_name", df=my_dataframe) # fast way to send data to redshift&s3 without checking consistency
    database_manager.send_to_redshift(database="my_database", schema="test_schema", table="my_table_name", df=my_dataframe, check=True) # slow way to send data to redshift&s3 but will table structure
    database_manager.send_to_redshift(database="my_database", schema="test_schema", table="my_table_name", df=my_dataframe, send_metadata=True) # To send the metadata(Table and Column Descriptions within the table.)
    ```
    To include the metadata when sending the table to Redshift, we must have to set `send_metadata` to True and fill the `.json` file following the [`table_metadata.example.json`](../../../table_metadata.example.json) template. The file can be filled with either a single table or a list of all tables.

    You can choose how you want to send data to redshift :
  * mode = "merge_replace":
      ```python
      import pandas as pd
      # Table content in redshift
        id    col1   col2
        1      foo   foo2
        2      bar   bar2

      df1 = pd.DataFrame({'id': [2,3],
                    'col1': ['bar_changed','baz'],
                    'col2': [None,'baz2']})
      database_manager.send_to_redshift(database="my_database", schema="my_schema", table="my_table", df=df1, mode="merge_replace", column_pivot=["id"])
      # Table content in redshift
      id    col1           col2
      1      foo           foo2
      2      bar_changed   None
      3      baz           baz2
      ```
    It overwrites rows that match with columns defined in `column_pivot` and insert new rows 
  * mode = "merge_update":
      ```python
      import pandas as pd
      # Table content in redshift
        id    col1   col2
        1      foo   foo2
        2      bar   bar2

      df1 = pd.DataFrame({'id': [2,3],
                    'col1': ['bar_changed','baz'],
                    'col2': [None,'baz2']})
      database_manager.send_to_redshift(database="my_database", schema="my_schema", table="my_table", df=df1, mode="merge_update", column_pivot=["id"])
      # Table content in redshift
      id    col1           col2
      1      foo           foo2
      2      bar_changed   bar2
      3      baz           baz2
    
      df2 = pd.DataFrame({'id': [1,2,3,4],
                    'col2': ['foo_changed','bar_changed','baz_changed', 'foo2_changed']})
      database_manager.send_to_redshift(database="my_database", schema="my_schema", table="my_table", df=df2, mode="merge_update", column_pivot=["id"])
      # Table content in redshift
      id    col1           col2
      1      foo           foo_changed
      2      bar_changed   bar_changed
      3      baz           baz_changed
      4      None          foo2_changed
    
      df3 = pd.DataFrame({'id': [1,2,3,4],
                    'col3': ['content3','content3','content3', 'content3']})
      database_manager.send_to_redshift(database="my_database", schema="my_schema", table="my_table", df=df3, mode="merge_update", column_pivot=["id"])
      # Table content in redshift
      id    col1           col2              col3
      1      foo           foo_changed       content3
      2      bar_changed   bar_changed       content3
      3      baz           baz_changed       content3
      4      None          foo2_changed      content3
      ```
    It replaces non-null data in rows that match with columns defined in `column_pivot` and insert new rows.

    This mode can add new columns and/or replace non-null values without modifying the rest 
 
  * mode = "append":
      ```python
      import pandas as pd
      # Table content in redshift
        id    col1   col2
        1      foo   foo2
        2      bar   bar2

      df4 = pd.DataFrame({'id': [4,5],
                    'col1': ['foo','baz'],
                    'col2': [foo2,'baz2']})
      database_manager.send_to_redshift(database="my_database", schema="my_schema", table="my_table", df=df4, mode="append")
      # Table content in redshift
      id    col1           col2
      1      foo           foo2
      2      bar           bar2
      4      foo           foo2
      5      baz           baz2
      ```
    It adds new rows. Becareful, there is no check for duplicates with this method.

* read_from_redshift
    ```python
    database_manager.read_from_redshift(database="my_database", method="auto", schema="my_schema", table="my_table_name", debug=True) # reading data from redshift with auto mode
    database_manager.read_from_redshift(database="my_database", method="sql", sql_query='SELECT * FROM reference.jp__gender_dictionary__mhlw', debug=False) # reading data from redshift with sql query
    ```

### S3
* upload_raw_s3
    ```python
    database_manager.upload_raw_s3(local_folder_path="my_folder", uuid="my_uuid")
    ```

* download_raw_s3
    ```python
    database_manager.download_raw_s3(local_folder_path="my_folder", uuid="my_uuid")
    ```

## Gcloud storage
* upload_to_gcloud
    ```python
    database_manager.upload_to_gcloud(local_folder_path="my_folder", uuid="my_uuid")
    ```
    
* download_from_gcloud
    ```python
    database_manager.download_from_gcloud(local_folder_path="my_folder", uuid="my_uuid")
    ```

## Roadmap
* Redshift: Find package for calculating significant digits of precision.
* Redshift: Dynamically adding or deleting columns.
* Redshift: Transfer sqlalchemy core to sqlalchemy orm.


## Feedback
Any questions or suggestions?
Please contact package maintainer **yu.levern@realconsultingdata.com**
