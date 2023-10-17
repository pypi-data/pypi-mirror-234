import os
import re
from typing import List, Optional
from google.cloud import storage
from ..decorator_manager import timeit
from ..file_manager import detect_all_files, detect_path, read_file_as_bytes_array


def list_gcloud_objects(
        prefix: str,
        bucket: str = os.environ.get("OPEN_DATA_SOURCE_BUCKET")
):
    """
    List all objects in a Google Cloud Storage prefix.

    Parameters:
          prefix (str): The full path to the file inside Google Storage.
          bucket (str): default env var "OPEN_DATA_SOURCE_BUCKET"): The bucket on gcloud to access data.
    """
    gcs = GcloudOperator(bucket=bucket)
    return [blob.name for blob in gcs.list_blob(prefix=prefix)]


@timeit(program_name="Upload data folder to gcloud")
def upload_to_gcloud(
        local_folder_path: str,
        uuid: str,
        bucket: str = os.environ.get("OPEN_DATA_SOURCE_BUCKET"),
):
    """
    Function upload_to_gcloud.
    Upload raw data folder to gcloud.

    Parameters:
          local_folder_path (str): The path of local folder which contains files.
          uuid (str): The uuid for the source.
          bucket (str): default env var "OPEN_DATA_SOURCE_BUCKET"): The bucket on gcloud to access data.

    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.upload_to_gcloud(local_folder_path="my_folder", uuid="my_uuid")
    """
    os.path.isdir(local_folder_path)
    uuid_path = os.path.join(local_folder_path.split(uuid)[0], uuid)
    sub_folder_path = local_folder_path.split(uuid)[1]

    gcs = GcloudOperator(bucket=bucket)

    # List of files available in Google Storage
    lst_blob = [
        path
        for blob in gcs.list_blob(prefix=f"{uuid}{sub_folder_path}")
        if (path := blob.name.removeprefix(f"{uuid}/")) != ""
    ]
    print(f"💧{len(lst_blob)} blob from `{bucket}/{uuid}{sub_folder_path}` detected.")

    # List of local files candidate to be uploaded into Google Storage
    lst_local_file = [
        file_path.removeprefix(f"{uuid_path}{os.path.sep}")
        for file_path in detect_all_files(local_folder_path, full_path=True)
        if not os.path.split(file_path)[-1].startswith(".")
    ]
    print(f"📑{len(lst_local_file)} local files from `{local_folder_path}` detected.")

    # All the new files available locally but not yet in Google Storage. So they must be sent.
    lst_upload = sorted(
        [file_path for file_path in set(lst_local_file) - set(lst_blob)]
    )
    print(f"📤{len(lst_upload)} local file need to be uploaded as gcloud blob.")

    # All the files available both locally and in the cloud. We must verify if any of the already existing files has
    # changed so we can overwrite the new version in Google Storage.
    lst_verify_content_update = sorted(
        [file_path for file_path in list(set(lst_local_file) & set(lst_blob))]
    )

    # Dictionary containing the name of each local file and its content value in bytes.
    dct_file_as_bytes = {}
    for path in lst_verify_content_update:
        dct_file_as_bytes[path] = read_file_as_bytes_array(os.path.join(uuid_path, path))

    # We search for which of the files present both locally and in the cloud have its content changed. So we retrieve
    # the file content in bytes locally and in the cloud and compare them. Those which have changed must be updated.
    lst_update = [
        path
        for path in lst_verify_content_update
        if dct_file_as_bytes[path] != gcs.download_as_byte_blob(blob_path=os.path.join(uuid, path))
    ]
    print(f"📤{len(lst_update)} local file had their content changed and need to be updated into gcloud.")

    for file_path in (lst_upload + lst_update):
        gcs.upload_blob(
            local_file_path=os.path.join(uuid_path, file_path),
            blob_path=os.path.join(uuid, file_path),
        )


@timeit(program_name="download data folder from gcloud")
def download_from_gcloud(
        local_folder_path: str,
        uuid: str,
        starts_with: Optional[str] = None,
        ends_with: Optional[str] = None,
        regex: Optional[str] = None,
        bucket: str = os.environ.get("OPEN_DATA_SOURCE_BUCKET"),
):
    """
    Function download_from_gcloud.
    Download raw data folder from gcloud.

    Parameters:
          local_folder_path (str): The path of local folder which contains files.
          uuid (str): The uuid for the source.
          bucket (str): default env var "OPEN_DATA_SOURCE_BUCKET"): The bucket on gcloud to access data.
          starts_with (str): The beginning pattern of files to be downloaded.
          ends_with (str): The ending pattern of files to be downloaded.
          regex (str): Regex to filter the tables you want to download

    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.download_from_gcloud(local_folder_path="my_folder", uuid="my_uuid")
    """
    detect_path(local_folder_path)
    uuid_path = os.path.join(local_folder_path.split(uuid)[0], uuid)
    sub_folder_path = local_folder_path.split(uuid)[1]

    gcs = GcloudOperator(bucket=bucket)
    lst_blob = [
        path
        for blob in gcs.list_blob(prefix=f"{uuid}{sub_folder_path}")
        if (path := blob.name.removeprefix(f"{uuid}/")) != ""
    ]
    if starts_with:
        lst_blob = [path for path in lst_blob if path.startswith(starts_with)]
    if ends_with:
        lst_blob = [path for path in lst_blob if path.endswith(ends_with)]
    if regex:
        pattern = re.compile(regex)
        lst_blob = [path for path in lst_blob if pattern.match(path)]
    print(f"💧{len(lst_blob)} blob from `{bucket}/{uuid}{sub_folder_path}` detected.")

    lst_local_file = [
        file_path.removeprefix(f"{uuid_path}{os.path.sep}")
        for file_path in detect_all_files(local_folder_path, full_path=True)
        if not os.path.split(file_path)[-1].startswith(".")
    ]

    print(f"📑{len(lst_local_file)} local files from `{local_folder_path}` detected.")
    lst_download = sorted(
        [file_path for file_path in set(lst_blob) - set(lst_local_file)]
    )
    print(f"📥{len(lst_download)} gcloud blob need to be downloaded as local file.")

    for file_path in lst_download:
        gcs.download_blob(
            local_file_path=os.path.join(uuid_path, file_path),
            blob_path=os.path.join(uuid, file_path),
        )


class GcloudOperator:
    def __init__(self, bucket: str = os.environ.get("OPEN_DATA_SOURCE_BUCKET")) -> None:
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(bucket)
        print(f"☑️Bucket is set to: {self.bucket}")

    def list_blob(self, prefix: str) -> List:
        """
        It will give you the list of object in the Google Cloud Storage given a prefix.

        Parameters:
              prefix(str): The full path to the file inside Google Storage.
        """
        return [blob for blob in self.bucket.list_blobs(prefix=prefix)]

    def download_blob(self, local_file_path: str, blob_path: str) -> None:
        """
        It will download the object from Google Cloud Storage.

        Parameters:
              local_file_path(str): The relative path to the file locally.
              blob_path(str): The full path to the file inside Google Storage.
              checksum(str): Method of verification. Default is 'md5'.
        """
        blob = self.bucket.get_blob(blob_path)

        # Create the sub-folders when downloading file from GCloud.
        dir_to_make = "/".join(local_file_path.split("/")[:-1])
        if not os.path.exists(dir_to_make):
            os.makedirs(dir_to_make)

        with open(local_file_path, "wb") as file_obj:
            blob.download_to_file(file_obj)

    def download_as_byte_blob(self, blob_path: str, checksum: str = "md5") -> None:
        """
        It will download the object from Google Cloud Storage as a bytes array of its content. It can be useful to
        check if the content has changed between a local and cloud file, or to verify if a file was corrupted or not
        during the upload.

        Parameters:
              blob_path(str): The full path to the file inside Google Storage.
              checksum(str): Method of verification. Default is 'md5'.
        """
        blob = self.bucket.get_blob(blob_path)
        file_as_byte = blob.download_as_bytes(checksum=checksum)
        return file_as_byte

    def upload_blob(self, local_file_path: str, blob_path: str, checksum: Optional[str] = None) -> None:
        """
        It will upload a file into Google Cloud Storage.

        Parameters:
              local_file_path(str): The relative path to the file locally.
              blob_path(str): The full path to the file inside Google Storage.
              checksum(str): Method of verification. Default is None.
        """
        blob = self.bucket.blob(blob_path)
        blob.upload_from_filename(filename=local_file_path, checksum=checksum)
