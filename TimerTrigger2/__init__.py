import datetime
import logging
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient
import os
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:

    account_url = os.getenv("timerStorageAccountUrl")
    default_credential = os.getenv("timerDefaultCredentials")

    containerName = os.getenv("timerContainerName")
    today = datetime.utcnow()
    blob_service_client = BlobServiceClient(
        account_url, credential=default_credential)
    blob_container = blob_service_client.get_container_client(
        container=containerName)
    blob_list = blob_container.list_blobs()
    for blobs in blob_list:
        blob_last_modified = blobs.last_modified
        blob_last_modified = blob_last_modified.replace(tzinfo=None)
        difference = today-blob_last_modified
        totalMinutes = difference.total_seconds() / 60
        if totalMinutes > 20:

            blob = BlobClient(container_name=containerName,
                              blob_name=blobs.name, account_url=account_url, credential=default_credential)
            blob.set_standard_blob_tier(standard_blob_tier="Archive")
        else:
            continue

    logging.info('Python timer trigger function ran at',)
