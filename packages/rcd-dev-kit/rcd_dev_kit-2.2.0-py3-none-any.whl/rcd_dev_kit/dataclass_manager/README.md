# Dataclass Manager
Dataclass Manager is a Python module for organise different type of dataclass.
## Set up
Set up .env as follow:
```python
#mysql
MYSQL_HOST=x
MYSQL_DB=x
MYSQL_PORT=x
MYSQL_USER=x
MYSQL_PASSWORD=x
```
## Usage
### RawDataFile object
* RawDataFile
    ```python
    from rcd_dev_kit.dataclass_manager import RawDataFile
    class MyRawData(RawDataFile):
        source_name = "xxx"
        source_url = "xxx"
        source_uuid = "xxx"
        file_name = "xxx"
        file_folder = "xxx"

        def __init__(self):
            super().__init__(base_path=os.environ.get("MY_BASE_PATH"))
            # my attribute necessary
            self.xx = xx
            self.yy = yy

        def download(self):
            # my method to download raw data file

        def read(self):
            # my mehod to read RAW data of list of RAW data

        # other method necessary
    ```
* Dictionary
    ```python
    from rcd_dev_kit.dataclass_manager import Dictionary
  import pandas as pd
    df1 = pd.DataFrame({ "country_id":["fr","us"],
  "gender_id":[1,2]
  })
    gender_dict = Dictionary(database=my_database, table_name="ww__gender__oip_dictionary")
    df_join = gender_dict.join(df=df1, how='left', on=["gender_id"], select=["gender_label_fr"])
    
  >>> df_join 
    countryid    gender_id   gender_label_fr
        fr              1               Male
        uk              2            Femelle
    
    ```
## Roadmap


## Feedback
Any questions or suggestions?
Please contact package maintainer **yu.levern@realconsultingdata.com**
