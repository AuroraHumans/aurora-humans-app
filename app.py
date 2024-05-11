import io
import json
import os

import boto3
import streamlit as st
from botocore.client import Config
from upload_file import upload_single_photo
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
# Constants
MAX_IMAGE_SIZE = (224, 224)  # Change to your requirements

st.title("💚💚🥰 Aurora Humans Worldwide Upload Dataset")
st.divider()


# Streamlit file uploader
# Metadata form
event = st.multiselect("Event?", ["Aurora2024"], default="Aurora2024")

title = st.text_input("Title of the Image")
city = st.text_input("City")
date = st.text_input("Date")
person_in_image=st.checkbox("Person in the image?")
other_objects=st.checkbox("Other objects in the image?")
description = st.text_area("Write something about your experience")
st.divider()
uploaded_file = st.file_uploader("Upload Your Image", type=["png", "jpg", "jpeg"])
st.text("🤗🤗🤗")
st.markdown("## Privacy Policy:") 
st.markdown("No personal information is collected or stored after your visit.")
st.divider()
clicked = st.button("Submit")
st.divider()

if clicked:
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
        metadata = {
            "filename": uploaded_file.name,
            "event": event,
            "title": title,
            "date": date,
            "city": city,
            "description": description,
            "person_in_image:": person_in_image,
            "other_objects": other_objects
        }

        # Create S3 bucket path for image and metadata
        s3_image_key = f"images/{uploaded_file.name}"
        s3_metadata_key = f"metadata/{uploaded_file.name}.json"
        
        upload_single_photo(s3_image_key, s3_metadata_key)

        st.success("Image and metadata successfully uploaded to S3")
        st.text("The image here is lower quality but do not be alarmed - yours is fine.")
else:
    st.error("Please provide both title and description for the image.")