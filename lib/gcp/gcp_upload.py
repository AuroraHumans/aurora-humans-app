# Python Client Library to upload file
import os
from google.cloud import storage, Client 
from dotenv import load_dotenv
load_dotenv()

def upload_blob(source_file_name, bucket_name=os.getenv("SOURCE_BUCKET"), destination_blob_name=os.getenv("DESTINATION_BLOB")):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Set the generation-match precondition to avoid overwriting existing files
    # unless explicitly intended to do so.
    # `if_generation_match=0` will only allow uploads if the blob does not exist.
    # For updating an existing blob, you can retrieve its generation with
    # `blob.generation` and set `if_generation_match` to that value.
    blob.upload_from_filename(
        source_file_name,
        if_generation_match=0  # Ensures that the file is uploaded only if it does not exist.
    )

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
