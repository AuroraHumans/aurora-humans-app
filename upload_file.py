# We use the S3 Compatible Storage Service (S3) to store the image and metadata on R2 on Cloudflare
import os
import json
import boto3
from botocore.client import Config
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()



BUCKET_NAME="aurora-humans"
ACCESS_KEY=os.getenv("ACCESS_KEY_ID")
SECRET_KEY=os.getenv("SECRET_KEY_ACCESS")
R2_ENDPOINT=os.getenv("AURORA_ENDPOINT")


def auth_s3_r2(r2_endpoint=R2_ENDPOINT):
    # Initialize AWS S3 Client
    s3 = boto3.client('s3', region_name='auto')
    session = boto3.session.Session()

# Create a client using the R2 endpoint
    s3 = session.client(
        service_name='s3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url=r2_endpoint,
        config=Config(signature_version='s3v4')
    )


# Assuming auth_s3_r2 is a function that authenticates and sets the environment variables for R2
def upload_single_photo(image, metadata):
    try:
        auth_s3_r2(r2_endpoint=R2_ENDPOINT)
    except Exception as e:
        print(f"Error in authentication: {e}")
        return

    # Initialize the S3 client
    s3 = boto3.client('s3')

    try:
        # Upload image
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=image.name,
            Body=image.read(),
            ContentType='image/jpeg'  # Adjust this to match your image format
        )
        print(f"IMAGE {image.name} uploaded")

        # Upload metadata
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"{image.name}.json",  # This will associate metadata with the image name
            Body=json.dumps(metadata),
            ContentType='application/json'
        )
        print(f"META DATA for {image.name} uploaded")
        
        s3.upload_file(image, BUCKET_NAME, image)
        s3.upload_file(metadata, BUCKET_NAME, f"{image}.json")()

    except Exception as e:
        print(f"Error in uploading to S3: {e}")
        return

    print("Upload Successful")

    
#### @TODO IMPLEMENT WHEN WORKING
def upload_batch(photos, metadata, destination):
    pass

def list_buckets():
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])
        

