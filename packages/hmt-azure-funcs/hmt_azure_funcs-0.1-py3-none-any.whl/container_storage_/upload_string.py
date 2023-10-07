from azure.storage.blob import BlobServiceClient
import json

def upload_string_to_blob(connection_string, container_name, blob_name, data):
    '''
    # get the connection_string in 'Storage Accounts -> (account name) -> Access keys
    # hawkeye one is here:
    # https://portal.azure.com/#@tris42.onmicrosoft.com/resource/subscriptions/0c712683-db62-4326-a898-b4c354818292/resourceGroups/hmt-uks-hawkeye-dev-rg/providers/Microsoft.Storage/storageAccounts/hmtukshawkeyedatalakedev/keys

    # Example of running:

    connection_string = "COPY ME FROM URL ABOVE"
    container_name = "ADD THIS"
    blob_name = "bloomberg_py.txt"
    string_to_upload = json.dumps({
        'some dictionary':'example'
    })

    upload_string_to_blob(connection_string, container_name, blob_name, data)
    '''

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Get a reference to a container
    container_client = blob_service_client.get_container_client(container_name)

    # Create the container if it doesn't exist (Optional)
    container_client.create_container()

    # Convert the string data to bytes, for blob upload
    byte_data = data.encode('utf-8')

    # Get a blob client for our blob
    blob_client = container_client.get_blob_client(blob_name)

    # Upload data to the blob
    blob_client.upload_blob(byte_data)


