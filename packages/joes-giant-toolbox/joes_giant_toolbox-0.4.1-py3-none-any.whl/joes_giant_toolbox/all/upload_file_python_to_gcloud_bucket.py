"""
This script defines the function upload_file_python_to_gcloud_bucket()
"""

import google.cloud.storage  # pylint: disable=import-error,no-name-in-module


def upload_file_python_to_gcloud_bucket(
    contents_str: str, bucket_name: str, filename_on_bucket: str, file_type: str
) -> None:
    """Write an object in python memory to a file (blob) on a google cloud bucket

    Parameters
    ----------
    contents_str: str
        The file, represented as a string e.g. using "str(python_object)" or json.dumps(python_dict)
    bucket_name: str
        The name of the bucket to which the file should be written
    filename_on_bucket: str
        The desired name of the file on the bucket
    file_type: str
        The file type
        examples: {"text/csv", "text/json", "text/html"}

    Notes
    -----
    In order to preserve unicode symbols when uploading a string (e.g. when uploading html) use:
        contents_str = my_string.encode("raw_unicode_escape")


    Example usage
    -------------
    >>> import joes_giant_toolbox.google_cloud
    >>> joes_giant_toolbox.google_cloud.upload_file_python_to_gcloud_bucket(
    ...     contents_str = pd.DataFrame({"x":[1,2,3]}).to_csv(index=False),
    ...     bucket_name="my-bucket",
    ...     filename_on_bucket="pd_df.csv",
    ...     file_type="text/csv"
    ... )

    >>> joes_giant_toolbox.google_cloud.upload_file_python_to_gcloud_bucket(
    ...     contents_str = json.dumps( {"x":69, "y":[4,20]} ),
    ...     bucket_name="my-bucket",
    ...     filename_on_bucket="dict.json",
    ...     file_type="text/json"
    ... )
    """
    storage_client = google.cloud.storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.blob(filename_on_bucket).upload_from_string(contents_str, file_type)
