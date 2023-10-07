from azure.storage.blob import BlobServiceClient

def list_files_in_container(
    connection_string: str,
    container_name: str,
):
    '''
    # Example of using func
    connection_string = 'LONG AND SECRET CONNECTION STRING'
    container_name = 'test'
    list_files_in_container(connection_string, container_name)
    '''
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()

    return [blob.name for blob in blob_list]



