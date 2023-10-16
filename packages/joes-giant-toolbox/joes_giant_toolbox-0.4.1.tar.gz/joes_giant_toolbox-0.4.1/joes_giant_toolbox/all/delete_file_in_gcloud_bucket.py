import google.cloud.storage


def delete_file_in_gcloud_bucket(
    bucket_name: str, file_name: str, verbose: bool = True
) -> None:
    """Delete a file which is in a google cloud bucket

    Notes
    -----
    This code is mostly taken from the Google Cloud documentation https://cloud.google.com/storage/docs/deleting-objects#client-libraries

    Parameters
    ----------
    bucket_name: str
        The name of the bucket containing the file
    file_name: str
        The name of the file to be deleted
    verbose: bool, optional (default=True)
        Whether to print status messages about the process

    Example Usage
    -------------
    >>>delete_file_in_gcloud_bucket(bucket_name="output_bucket", file_name="users.json")
    Deleted file from google cloud bucket gs://output_bucket/users.json
    >>>delete_file_in_gcloud_bucket(bucket_name="output_bucket", file_name="2023/01/users.json")
    Deleted file from google cloud bucket gs://output_bucket/2023/01/users.json
    """
    storage_client = google.cloud.storage.Client()
    bucket_obj = storage_client.bucket(bucket_name)
    file_blob = bucket_obj.blob(file_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to delete is aborted if the object's
    # generation number does not match your precondition.
    generation_match_precondition = None
    file_blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
    generation_match_precondition = file_blob.generation
    file_blob.delete(if_generation_match=generation_match_precondition)
    if verbose:
        print(f"Deleted file from google cloud bucket gs://{bucket_name}/{file_name}")
