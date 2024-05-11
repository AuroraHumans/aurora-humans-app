# We use the S3 Compatible Storage Service (S3) to store the image and metadata on R2 on Cloudflare
import os
import json
import boto3
from botocore.client import Config
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

# Environment variables
BUCKET_NAME = "aurora-humans"
ACCESS_KEY = os.getenv("ACCESS_KEY_ID")
SECRET_KEY = os.getenv("SECRET_KEY_ACCESS")
R2_ENDPOINT = os.getenv("AURORA_ENDPOINT")


def auth_s3_r2(r2_endpoint=R2_ENDPOINT):
    # Initialize AWS S3 Client using custom config
    s3 = boto3.client(
        's3',
        endpoint_url=r2_endpoint
    )
    return s3

def upload_single_photo(s3,image, metadata):
    try:
        s3 = auth_s3_r2(R2_ENDPOINT)
    except Exception as e:
        print(f"Error in authentication: {e}")
        
    try:
        # Upload image
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=image,
            Body=image.read(),
            ContentType='image/jpeg'  # Adjust this to match your image format
        )
        print(f"IMAGE {image.name} uploaded")

        # Upload metadata
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"{image.name}.json",
            Body=json.dumps(metadata),
            ContentType='application/json'
        )
        print(f"META DATA for {image} uploaded")

    except Exception as e:
        print(f"Error in uploading to S3: {e}")
        return

    print("Upload Successful")


    
#### @TODO IMPLEMENT WHEN WORKING
def upload_batch(photos, metadata, destination):
    pass

def list_buckets(s3):
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])
        

