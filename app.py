import streamlit as st
from PIL import Image
import io
import boto3
import json

# Constants
MAX_IMAGE_SIZE = (224, 224)  # Change to your requirements

# Initialize AWS S3 Client
s3 = boto3.client('s3', region_name='YOUR_REGION')

st.title("💚💚🥰 Aurora Humans Worldwide Upload Dataset")

# Streamlit file uploader
uploaded_file = st.file_uploader("Upload Your Image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    with st.spinner("Uploading to Aurora Humans..."):
        # Read the image file
        image = Image.open(uploaded_file)

        # Compress the image
        image.thumbnail(MAX_IMAGE_SIZE)

        # Convert back to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        img_byte_arr = img_byte_arr.getvalue()

        # Display image preview in Streamlit
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Metadata form
        event = st.dropdown("Select Event", ["Aurora2024"])
        title = st.text_input("Title of the Image")
        city = st.text_input("City")
        date = st.calendar_input("Date")
        description = st.text_area("Write something about your experience")

        # On button click, store data to S3
        if st.button("Upload to Aurora Humans"):
            if title and description:
                # Create metadata as a JSON object
                metadata = {
                    "filename": uploaded_file.name,
                    "event": event,
                    "title": title,
                    "date": date,
                    "city": city,
                    "description": description,
                }

            # Create S3 bucket path for image and metadata
            s3_image_key = f"images/{uploaded_file.name}"
            s3_metadata_key = f"metadata/{uploaded_file.name}.json"

            # Upload the image to S3
            s3.put_object(
                Bucket='YOUR_BUCKET_NAME',
                Key=s3_image_key,
                Body=img_byte_arr,
                ContentType=uploaded_file.type
            )

            # Upload metadata to S3
            s3.put_object(
                Bucket='YOUR_BUCKET_NAME',
                Key=s3_metadata_key,
                Body=json.dumps(metadata),
                ContentType='application/json'
            )

            st.success("Image and metadata successfully uploaded to S3")
        else:
            st.error("Please provide both title and description for the image.")