import os
import json
from google.cloud import storage
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from threading import Thread
from google.cloud import secretmanager
from google.oauth2 import service_account


# Function to access secret from Google Secret Manager
def access_secret_version(project_id, secret_id, version_id="latest"):
    """
    Access the payload for the given secret version if one exists.
    The version can be a version number as a string (e.g., "5") or an alias (e.g., "latest").
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload

# Define function to upload a photo to GCS
def upload_photo_to_gcs(filename, project_id, secret_id, bucket_name):
    # Authenticate with secret manager
    try:
        sk = access_secret_version(project_id, secret_id, version_id="latest")
        creds = service_account.Credentials.from_service_account_info(json.loads(sk))
        client = storage.Client(credentials=creds, project=project_id)
    except Exception as e:
        print(f"Error accessing secret: {str(e)}")
        return False

    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(os.path.basename(filename))
        blob.upload_from_filename(filename)
    except Exception as e:
        print(f"Error uploading file {filename}: {str(e)}")
        return False
    else:
        print(f"File {filename} uploaded successfully")
        return True