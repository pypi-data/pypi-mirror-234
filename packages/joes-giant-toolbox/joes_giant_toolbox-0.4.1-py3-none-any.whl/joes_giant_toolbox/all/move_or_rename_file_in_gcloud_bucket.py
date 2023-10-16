import google.cloud.storage


def move_or_rename_file_in_gcloud_bucket(
    source_bucket_name: str,
    source_filename: str,
    destination_bucket_name: str,
    destination_filename: str,
    verbose: bool = True,
) -> None:
    """Move or rename a file which is in a google cloud bucket (which includes moving it to a different bucket)

    Notes
    -----
    This code is stolen from the google cloud documentation (https://cloud.google.com/storage/docs/copying-renaming-moving-objects#storage-move-object-python)
    The copy/rename will not work if the destination filename already exists, raising a "PreconditionFailed: 412 POST" error

    Parameters
    ----------
    source_bucket_name: str
        Bucket name that file is currently in
    source_filename: str,
        Current name of the file in the source bucket
    destination_bucket_name: str
        Name of bucket that you want to move file to (can be the same as [source_bucket_name])
    destination_filename: str
        Desired name of the file in the destination bucket
    verbose: bool (default: True)
        Print process information to standard out during running of the function

    Example Usage
    -------------
    >>> move_or_rename_file_in_gcloud_bucket(
    ...     source_bucket_name="bucket1",
    ...     source_filename="folder5/sixty9.json",
    ...     destination_bucket_name="bucket2",
    ...     destination_filename="folder5/sixty9.json",
    ... )
    File (blob) 'folder5/sixty9.json' in bucket 'bucket1' moved to file (blob) 'folder5/sixty9.json' in bucket 'bucket2'
    """
    storage_client = google.cloud.storage.Client()
    source_bucket = storage_client.bucket(source_bucket_name)
    source_blob = source_bucket.blob(source_filename)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    destination_generation_match_precondition = 0

    blob_copy = source_bucket.copy_blob(
        source_blob,
        destination_bucket,
        destination_filename,
        if_generation_match=destination_generation_match_precondition,
    )

    source_bucket.delete_blob(source_filename)

    if verbose:
        print(
            f"File (blob) '{source_blob.name}' in bucket '{source_bucket.name}' moved to file (blob) '{blob_copy.name}' in bucket '{destination_bucket.name}'"
        )
