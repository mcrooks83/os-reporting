

#collection of functions to access azure blob storage
from azure.storage.blob import BlobServiceClient
import pandas as pd
import logging
import os

logging.basicConfig(level=os.getenv("LOG_LEVEL", "info").upper())

#returns a service client
def blob_service_client(account_url, sas_token):
    return BlobServiceClient(account_url=account_url, credential=sas_token)

#returns a container client
def blob_container_client(blob_service_client, container_name):
    return blob_service_client.get_container_client(container=container_name)

# creates a new blob container
def create_blob_container(blob_service_client, container_name_to_create):
    created_container = blob_service_client.create_container(container_name_to_create)
    return created_container

#gets all blobs for a profile
def list_blobs_container_for_profile_id(profile_id, container_client):
    blob_list = container_client.list_blobs(name_starts_with=profile_id + "/")
    return blob_list

#gets file's in the file path
def get_files_in_container_by_file_path(profile_id, file_path, container_client):
    path = profile_id + "/" + file_path
    logging.info(path)
    blobs = container_client.list_blobs(name_starts_with=path)

    return blobs

def download_file_from_azure_blob_storage(blob_service_client, container_name, blob, local_file_name ):
    blob_client = blob_service_client.get_blob_client(container_name, blob, snapshot=None )
    with open(local_file_name, "wb") as my_blob:
        blob_data = blob_client.download_blob()
        blob_data.readinto(my_blob)
    blob_df = pd.read_csv(local_file_name)
    return blob_df

def list_all_blobs(profile_id, account_url, sas_token,  container_name):
    service_client =blob_service_client(account_url, sas_token)
    container_client = blob_container_client(service_client, container_name)
    files = list_blobs_container_for_profile_id(profile_id, container_client)
    return files

def upload_blob_file_binary(account_url, sas_token, container_name, file_to_upload, blob_path):
    service_client = blob_service_client(account_url, sas_token)
    blob_client = service_client.get_blob_client(container=container_name, blob=blob_path)
    blob_client.upload_blob(file_to_upload, blob_type="BlockBlob")
    
def upload_blob_file(account_url, sas_token, container_name, file_path, file_name):
    service_client =blob_service_client(account_url, sas_token)
    container_client = blob_container_client(service_client, container_name)
    with open(file=file_path, mode="rb") as data:
        blob_client = container_client.upload_blob(name=file_name, data=data, overwrite=True)

# alter this to accept the service client
def get_files_from_azure(profile_id, account_url, sas_token, file_path, container_name):
    #get a service client
    service_client = blob_service_client(account_url, sas_token)
    container_client = blob_container_client(service_client, container_name)
    files = get_files_in_container_by_file_path(profile_id, file_path, container_client)
    return files

def get_files_from_azure_as_df(profile_id, account_url, sas_token, file_path, container_name):
    service_client = blob_service_client(account_url, sas_token)
    files = get_files_from_azure(profile_id, account_url, sas_token, file_path, container_name)

    data_frames = []
    for blob in files:
        local_file_name = blob.name.split('/')[4]
        df = download_file_from_azure_blob_storage(service_client, container_name, blob.name, local_file_name )
        data_frames.append({
            "file_name": local_file_name,
            "df" : df
        })
    return data_frames
