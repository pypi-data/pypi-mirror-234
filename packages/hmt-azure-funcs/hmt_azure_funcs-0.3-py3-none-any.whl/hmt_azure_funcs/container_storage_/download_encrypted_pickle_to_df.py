# for when it comes to decryption
from azure.storage.blob import BlobServiceClient
from cryptography.fernet import Fernet
import pickle
import pandas as pd

def download_encrypted_pickle_to_df(
    connection_string: str, 
    container_name: str, 
    blob_name: str,
    fernet_key_string: str,
):
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_data_encrypted = blob_client.download_blob().readall()
    
    fernet = Fernet(fernet_key_string)
    df_as_dictionary = pickle.loads(fernet.decrypt(blob_data_encrypted))
    return pd.DataFrame(df_as_dictionary)

