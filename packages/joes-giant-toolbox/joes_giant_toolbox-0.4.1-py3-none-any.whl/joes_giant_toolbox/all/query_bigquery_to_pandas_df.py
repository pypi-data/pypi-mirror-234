import google.cloud.bigquery
import pandas as pd


def query_bigquery_to_pandas_df(query_str: str) -> pd.DataFrame:
    """Runs a query on Google BigQuery and writes the result into a local pandas.DataFrame

    Parameters
    ----------
    query_str
        A string containing the query to run on Google BigQuery

    Returns
    -------
    pandas.DataFrame
        A pandas dataframe
    """
    client = google.cloud.bigquery.Client()

    return client.query(query_str).result().to_dataframe()
