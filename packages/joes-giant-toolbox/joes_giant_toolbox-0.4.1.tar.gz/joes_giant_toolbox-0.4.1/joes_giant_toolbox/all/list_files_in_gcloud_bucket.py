"""
This script defines the function list_files_in_gcloud_bucket
"""
from typing import List
import google.cloud.storage  # pylint: disable=import-error, no-name-in-module


def list_files_in_gcloud_bucket(
    bucket_name: str, prefix: str | None = None
) -> List[str]:
    """
    Returns a list of the files (filenames) present in a google cloud bucket

    Parameters
    ----------
    bucket_name: str
        The name of the google cloud bucket
    prefix: str, optional (default=None)
        If present, only returns files whose path starts with the given prefix

    Returns
    -------
    List[str]
        List of filenames in the google cloud bucket (file pathes)
    """
    # pylint: disable=c-extension-no-member
    storage_client = google.cloud.storage.Client()
    # pylint: enable=c-extension-no-member
    if prefix is not None:
        blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    else:
        blobs = storage_client.list_blobs(bucket_name)
    all_filenames = []
    for blob in blobs:
        all_filenames.append(blob.name)

    return all_filenames
