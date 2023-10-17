import multiprocessing
import os
import io
import requests
import zipfile
import csv
from contextlib import closing
from datetime import datetime
import re
import warnings


class FileDownloader:
    """
    FileDownloader, download data from valid url and save into download path.

    Args:
        download_path (str): The location to save data.

    Attributes:
        _new_name (dictionary): The dictionary with download url as key, new saving name as value.

    Examples:
        >>> from rcd_dev_kit.file_manager import FileDownloader
        >>> be_download = FileDownloader(download_path="be/download")
        Initialize 💻download path as "be/download".
    """

    def __init__(self, download_path):
        """
        The constructor for FileDownloader.

        Parameters:
           download_path (str): The location to save data.

        Examples:
            >>> from rcd_dev_kit.file_manager import FileDownloader
            >>> be_download = FileDownloader(download_path="be/download")
            Initialize 💻download path as "be/download".
        """
        print(f"Initialize 💻download path as \"{download_path}\".")
        self.download_path = download_path
        self._keyword = ""
        self._suffix = ""
        self._delimiter = ""
        self._new_name = ""

    def check_download_path(self):
        """
        The function to check if download path exist and create path is it doesn't exist.

        Examples:
            >>> be_download.check_download_path()
            ✓Path "be/download" exists.
            >>> be_download.check_download_path()
            Path "be/download_data" does not exist, creating...
        """
        if os.path.isdir(self.download_path):
            print(f"✓Path \"{self.download_path}\" exists.")
        else:
            print(f"Path \"{self.download_path}\" does not exist, creating...")
            os.makedirs(self.download_path)

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, value):
        print(f"Setting keyword to {value}")
        self._keyword = value

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        print(f"Setting suffix to {value}")
        self._suffix = value

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        print(f"Setting delimiter to {value}")
        self._delimiter = value

    @property
    def new_name(self):
        return self._new_name

    @new_name.setter
    def new_name(self, value):
        print(f"Setting new_name to {value}")
        self._new_name = value

    def download_excel(self, url_valid):
        """
        The function to download excel.

        Parameters:
            url_valid (str): An valid url with response code 200.
        Examples:
            >>> be_download.download_excel("https://www.inami.fgov.be/SiteCollectionDocuments/liste-specialites-20200601.xlsx")
            📥Downloading from https://www.inami.fgov.be/SiteCollectionDocuments/liste-specialites-20200601.xlsx...
            XLSX will save as 2020-06-01---liste-specialites.xlsx in be/download.
            ✓Download completed.
        """
        print(f"📥Downloading from {url_valid}...")
        file_name = self._new_name or url_valid.split("/")[-1]
        # if not re.match(r"^[0-9]+(-[0-9]+)+___[0-9]+(-[0-9]+)*___[A-Za-z\-\_]+.[a-z]+", file_name):
        #     warnings.warn('Be careful, the name of your downloaded file should have this format : {datetime.now().date()}---{period}---{file_name}')
        print(f"Excel will save as {file_name} in {self.download_path}.")

        response = requests.get(url_valid)
        with open(os.path.join(self.download_path, file_name), "wb") as output:
            output.write(response.content)
        print("✓Download completed.")

    def download_csv(self, url_valid):
        """
        The function to download csv with user defined delimiter.

        Parameters:
            url_valid (str): An valid url with response code 200.
        Examples:
            >>> it_download = FileDownloader(download_path="it/download")
            >>> it_download.set_delimiter(delimiter=";")
            >>> it_download.download_csv(url_valid="https://www.aifa.gov.it/documents/20142/825643/Lista_farmaci_equivalenti.csv")
            📥Downloading from "https://www.aifa.gov.it/documents/20142/825643/Lista_farmaci_equivalenti.csv"...
            CSV will save as "Lista_farmaci_equivalenti.csv" in "it/download".
            Detecting encoding...
            Encoding found: ISO-8859-1.
            There are 7334 lines in csv.
            ✓Download completed.
        """
        print(f"📥Downloading from \"{url_valid}\"...")
        file_name = self._new_name or url_valid.split("/")[-1]
        # if not re.match(r"^[0-9]+(-[0-9]+)+___[0-9]+(-[0-9]+)*___[A-Za-z\-\_]+.[a-z]+", file_name):
        #     warnings.warn('Be careful, the name of your downloaded file should have this format : {datetime.now().date()}---{period}---{file_name}')
        print(f"CSV will save as \"{file_name}\" in \"{self.download_path}\".")

        with requests.Session() as s:
            response = requests.get(url_valid)
            print(f"Detecting encoding...")
            encoding = response.encoding
            print(f"Encoding found: {encoding}.")
            decoded_content = response.content.decode(encoding)
            cr = csv.reader(decoded_content.splitlines(), delimiter=self.delimiter)
            my_list = list(cr)
            print(f"There are {len(my_list)} lines in csv.")
            with open(os.path.join(self.download_path, file_name), 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=self.delimiter)
                writer.writerows(my_list)
        print(f"✓Download completed.")

    def download_zip(self, url_valid):
        """
        The function to download file from zip with suffix.

        Parameters:
            url_valid (str): An valid url with response code 200.
        Examples:
            >>> ch_download = FileDownloader(download_path="ch/download")
            >>> ch_download.download_zip(url_valid="http://www.spezialitaetenliste.ch/BAG_xls_2020.zip")
            📥Downloading from "http://www.spezialitaetenliste.ch/BAG_xls_2020.zip"...
            ✓Download completed.
        """
        print(f"📥Downloading from \"{url_valid}\"...")
        response = requests.get(url_valid)
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        with closing(zip_file) as zfile:
            for info in zfile.infolist():
                if info.filename.endswith(self.suffix) and self.keyword in info.filename:
                    # info.filename = do_something_to(info.filename)
                    info.filename = self._new_name or info.filename
                    zfile.extract(info, self.download_path)
        print(f"✓Download completed.")

    def download_pdf(self, url_valid):
        print(f"📥Downloading from {url_valid}...")
        file_name = self._new_name or url_valid.split("/")[-1]
        # if not re.match(r"^[0-9]+(-[0-9]+)+___[0-9]+(-[0-9]+)*___[A-Za-z\-\_]+.[a-z]+", file_name):
        #     warnings.warn('Be careful, the name of your downloaded file should have this format : {datetime.now().date()}---{period}---{file_name}')
        print(f"PDF will save as {file_name} in {self.download_path}.")

        response = requests.get(url_valid)
        with open(os.path.join(self.download_path, file_name), "wb") as output:
            output.write(response.content)
        print("✓Download completed.")


def multiprocessing_download(lst_url, work_func):
    """
    The function to download data with multiprocessing.

    Parameters:
       lst_url (list): A list of urls for downloading.
       work_func (any): A function for downloading.
    Examples:
        >>> from rcd_dev_kit.file_manager import multiprocessing_download
        >>> multiprocessing_download(lst_url=["http://www.spezialitaetenliste.ch/BAG_xls_2020.zip", "http://www.spezialitaetenliste.ch/BAG_xls_2019.zip"], work_func=ch_download.download_zip)
        📥Downloading from "http://www.spezialitaetenliste.ch/BAG_xls_2020.zip"...
        ✓Download completed.
        📥Downloading from "http://www.spezialitaetenliste.ch/BAG_xls_2019.zip"...
        ✓Download completed.
        Data Downloaded in 0:00:33.098939s.⏰
    """
    start = datetime.now()
    nb_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(nb_processes)
    chunk_size = 5
    async_result = pool.map_async(func=work_func, iterable=lst_url, chunksize=chunk_size)
    async_result.wait()
    async_result.get()
    pool.close()
    print(f"Data Downloaded in {datetime.now() - start}s.⏰")
