# File Manager
File Manager is a Python module for manipulating directory and files.

## Usage
### File detector
* detect_path
    ```python
    from rcd_dev_kit import file_manager
    file_manager.detect_path(path="my_path")
    ```
    >👉🏻Path "my_path" does not exist, creating...

    >🥂Path "my_path" exists.
* detect_all_files
    ```python
    from rcd_dev_kit import file_manager
    file_manager.detect_all_files(root_path="my_path")
    ```
    >['.DS_Store', '2021-10-13---bdmit__cip_ampp_list.json', 'test.xlsx', 'cip_ampp_code.csv']
    ```python
    file_manager.detect_all_files(root_path="my_path", full_path=True)
    ```
    >['tmp/.DS_Store', 'tmp/2021-10-13---bdmit__cip_ampp_list.json', 'tmp/test.xlsx', 'tmp/hello/cip_ampp_code.csv']

### File writer
    ```python
    from rcd_dev_kit import file_manager
    file_manager.write_df_to_json_parallel(df=my_dataframe, json_path="my_path")
    ```
    >✅'Parallel Writing pd.DataFrame to json' end in 0:00:00.008030 s.⏰

### File operator (in dev)
* FileOperator
    ```python
    from rcd_dev_kit import file_manager
    fo = file_manager.FileOperator("price_tracker/all/drug_cards")
    fo.remove_all()
    ```

>Initializing directory path as 'price_tracker/all/drug_cards'

>There are 84651 files under directory.

### File downloader
* FileDownloader class
  * download_excel()
  ```python
  from rcd_dev_kit import file_manager
  
  fd = file_manager.FileDownloader(download_path= "path/where/to/store/file" )
  fd.check_download_path()
  fd.new_name = "new_name.xlsx"
  fd.download_excel(url_valid="https://www.sampledocs.in/DownloadFiles/SampleFile?filename=sampledocs-50mb-xlsx-file.xlsx")
  ```
  * download_csv()
  ```python
  from rcd_dev_kit import file_manager
  
  fd = file_manager.FileDownloader(download_path= "path/where/to/store/file" )
  fd.check_download_path()
  fd.new_name = "new_name.csv"
  fd.delimiter=";"
  fd.download_csv(url_valid="https://sample-videos.com/csv/Sample-Spreadsheet-1000-rows.csv")
  ```
  * download_zip()
  ```python
  from rcd_dev_kit import file_manager
  
  fd = file_manager.FileDownloader(download_path= "path/where/to/store/file" )
  fd.check_download_path()
  fd.keyword = "Publication"
  fd.suffix = "xlsx"
  fd.download_zip(url_valid="http://www.spezialitaetenliste.ch/BAG_xls_2020.zip")
  ```
  `self.keyword`: it will return all files that contain the `self.keyword` in the filename.
  `self.suffix`: it will return all files that ends with `self.suffix`. If `null`, it returns all suffix
  
  * download_pdf()
  ```python
  from rcd_dev_kit import file_manager
  
  fd = file_manager.FileDownloader(download_path= "path/where/to/store/file" )
  fd.check_download_path()
  fd.new_name = "new_name.pdf"
  fd.download_pdf(url_valid="https://www.sampledocs.in/DownloadFiles/SampleFile?filename=sampledocs-100mb-pdf-file.pdf")
  ```
* multiprocessing_download()

This function purpose is to download data with multiprocessing. You need to pass a list of urls and also
a function for downloading.
```python
from rcd_dev_kit.file_manager import multiprocessing_download

multiprocessing_download(lst_url=["http://www.spezialitaetenliste.ch/BAG_xls_2020.zip", 
                                  "http://www.spezialitaetenliste.ch/BAG_xls_2019.zip"], 
                         work_func= download_function_to_define)
        
```

## Roadmap
* add detect file suffix
* add detect file size
* add rename file
* add docs

## Feedback
Any questions or suggestions?
Please contact package maintainer **yu.levern@realconsultingdata.com**
