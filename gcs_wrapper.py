import platform
import json
import sys
import os
import time
from dotenv import load_dotenv
from google.cloud import storage as gcs

def get_gcs_client():
    if platform.system() == 'Linux':
        # run at cloud
        client = gcs.Client()
    elif platform.system() == 'Darwin':
        # run locally
        load_dotenv('.env')
        client = gcs.Client.from_service_account_json(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

    return(client)

def check_gcs_file_exists(bucket_name, file_path):

    client = get_gcs_client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob(file_path)
    if blob is None:
        return(False)
    else:
        return(True)

def upload_gcs_file_from_dictlist(bucket_name, file_path, result):
    dmplist = []
    for line in result:
        dmplist.append(json.dumps(line, ensure_ascii=False))

    client = get_gcs_client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.upload_from_string('\n'.join(dmplist))
    print(file_path + " upload success!!")

def get_gcs_file_to_dictlist(bucket_name, file_name):
    client = get_gcs_client()

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    lines = blob.download_as_string().decode().rstrip('\n')
    result = []
    for line in lines.split('\n'):
        result.append(json.loads(line))

    return(result)

