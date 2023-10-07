# save as encrypted so others can't reach it
from azure.storage.blob import BlobServiceClient
from cryptography.fernet import Fernet
import pickle
import pandas as pd

def upload_df_as_encrypted_pickle(
    df_to_upload: pd.DataFrame,
    connection_string: str, 
    container_name: str, 
    blob_name: str,
    fernet_key_string: str,
):
    '''
    Uploads to container: file will be unreadable without the fernet_key_string

    Useful if you don't have access to a secure container and need to enforce access control

    fernet_key_string must be a string of 32 characters

    You can make a key with:
    key = Fernet.generate_key()
    fernet_key_string = key.decode()
    '''

    fernet_key = bytes(fernet_key_string, 'UTF-8')
    fernet = Fernet(fernet_key)

    df_as_string = pickle.dumps(df_to_upload.to_dict())
    encoded_bytes = fernet.encrypt(df_as_string)

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # Upload data to the blob
    blob_client.upload_blob(encoded_bytes, overwrite = True)
    
    print(f'Uploaded file to {container_name}/{blob_name}')




