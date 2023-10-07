
from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO

def upload_pandas_dataframe_to_parquet(
    df: pd.DataFrame,
    blob_name: str,
    container_name: str,
    connection_string: str
) -> None:

    """
    # Usage example:
    df = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
    connection_string = 'LONG AND SECRET CONNECTION STRING'
    container_name = "gold-curated"
    blob_name = "bloomberg_daily/parquet/test.parquet"
    upload_pandas_dataframe_to_parquet(df, 'test.parquet', container_name, connection_string)
    """

    # Create a BlobServiceClient using the Azure connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get a BlobClient object representing the named blob within the named container
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Use Pandas DataFrame to_parquet method to write DataFrame to BytesIO object
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, engine='pyarrow')

    # Go to the start of the BytesIO object
    buffer.seek(0)

    # Create the blob in Azure Blob Storage using the data in buffer
    blob_client.upload_blob(buffer.read(), overwrite=True)

