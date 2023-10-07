from azure.storage.blob import BlobServiceClient
import polars as pl
from io import BytesIO


def read_parquet_from_container(
    blob_name: str,
    container_name: str,
    connection_string: str,
) -> pl.DataFrame:
    '''
    # Example
    connection_string = 'LONG AND SECRET CONNECTION STRING'container_name = "gold-curated"
    blob_name = "bloomberg_daily/parquet/bloomberg_daily_v4.parquet"


    original_daily = read_parquet_from_container(
        blob_name,
        container_name,
        connection_string,
    )

    # Show the DataFrame
    print(original_daily.shape)
    '''

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Download the blob data into a stream
    stream = blob_client.download_blob()

    # Read the stream into a DataFrame
    buffer = BytesIO(stream.readall())
    return pl.read_parquet(buffer)




