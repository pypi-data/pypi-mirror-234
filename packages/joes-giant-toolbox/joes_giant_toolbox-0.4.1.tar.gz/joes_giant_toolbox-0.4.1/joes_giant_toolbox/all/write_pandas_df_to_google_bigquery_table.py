"""
This script defines the function write_pandas_df_to_google_bigquery_table()
"""

from typing import List
import pandas as pd
import google.cloud.bigquery


# pylint: disable=line-too-long
def write_pandas_df_to_google_bigquery_table(
    pandas_df: pd.DataFrame,
    bigquery_table_path: str,
    column_schema: List[google.cloud.bigquery.SchemaField],
    overwrite_strategy: str = "WRITE_APPEND",
) -> None:
    """
    Writes a pandas dataframe to a table on Google BigQuery

    Notes
    -----
    If the table already exists on BigQuery, the default behaviour is to append the new data to it

    Parameters
    ----------
    pandas_df: pandas.DataFrame
        Table to be written to BigQuery
    bigquery_table_path : str
        Path to destination table e.g. "project_name.dataset_name.table_name"
    column_schema : list of google.cloud.bigquery.enums.SqlTypeNames objects
        A list of column data types, informing BigQuery of the data type of each column (refer to the example below)
        This list is passed to the parameter "schema" in the function bigquery.LoadJobConfig()
    overwrite_strategy : str
        Controls the behaviour of the write when the destination table already exists and contains data
        One of:
            "WRITE_APPEND"   - new data is appended to existing data in the destination table
            "WRITE_TRUNCATE" - new data overwrites existing data in the destination table
            "WRITE_EMPTY"    - returns an error if there is existing data in the destination table
        Refer to gcloud documentation:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationLoad.FIELDS.write_disposition

    Example Usage
    -------------
    import pandas as pd
    from google.cloud import bigquery
    example_df = pd.DataFrame(
      {
        "string_column": ["a","b","c"],
        "integer_column": [-100,0,100],
        "float_column": [3.14159,6.9,4.2],
      }
    )
    write_pandas_df_to_google_bigquery(
      pandas_df = example_df,
      bigquery_table_path = "project_name.dataset_name.table_name",
      column_schema = [
        google.cloud.bigquery.SchemaField("string_column", google.cloud.bigquery.enums.SqlTypeNames.STRING),
        google.cloud.bigquery.SchemaField("integer_column", google.cloud.bigquery.enums.SqlTypeNames.INT64),
        google.cloud.bigquery.SchemaField("float_column", google.cloud.bigquery.enums.SqlTypeNames.FLOAT64),
      ],
    )
    """
    client = google.cloud.bigquery.Client()
    job = client.load_table_from_dataframe(
        pandas_df,
        bigquery_table_path,
        job_config=google.cloud.bigquery.LoadJobConfig(
            schema=column_schema, write_disposition=overwrite_strategy
        ),
    )
    job.result()  # wait for the job to complete
