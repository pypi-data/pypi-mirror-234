from azure.storage.blob import BlobServiceClient
import json


def download_blob_to_string(connection_string, container_name, blob_name):
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Get a reference to a container
    container_client = blob_service_client.get_container_client(container_name)
    
    # Get a blob client for our blob
    blob_client = container_client.get_blob_client(blob_name)
    
    # Download the blob content
    blob_data = blob_client.download_blob()
    
    # Convert blob data to string and return
    return blob_data.readall().decode('utf-8')
