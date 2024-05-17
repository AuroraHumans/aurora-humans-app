import io
import json
import os
import streamlit as st
from lib.gcp.gcp_upload import authenticate_implicit_with_adc
from lib.extract_metadata import extract_metadata
from lib.gcp.gcp_upload import upload_blob
from google.cloud import storage, Client 
from dotenv import load_dotenv
from PIL import Image
from lib.database import insert_metadata

load_dotenv()

@st.cache_data
def uploaded_file(file):
    return file
# Constants
MAX_IMAGE_SIZE = (224, 224)  # Change to your requirements

st.title("💚💚🥰 Aurora Humans Worldwide Upload Dataset")
st.divider()
file_upload = st.file_uploader("Upload Your Image", type=["png", "jpg", "jpeg"])


# Streamlit file uploader
# Metadata form
event = st.multiselect("Event?", ["Aurora2024"], default="Aurora2024")

title = st.text_input("Title of the Image")
city = st.text_input("City")
date = st.date_input("Date")
person_in_image=st.checkbox("Person in the image?")
other_objects=st.checkbox("Other objects in the image?")
description = st.text_area("Write something about your experience")
st.divider()

st.text("🤗🤗🤗")
st.markdown("## Privacy Policy:") 
st.markdown("No personal information is collected or stored after your visit.")
st.divider()
clicked = st.button("Submit")

st.divider()


if clicked:
    with st.spinner("Uploading to Aurora Humans..."):
        
        up_file = uploaded_file(file_upload)
        # For saving
        # file_path = f"./tmp/{up_file}"
        
        # Read the image file
        image = Image.open(up_file)
        
        # Compress the image
        image.thumbnail(MAX_IMAGE_SIZE)

        # Convert back to bytes
        img_byte_arr = io.BytesIO()
    
        #image.save(format=image.format, fp=file_path)
        img_byte_arr = img_byte_arr.getvalue()
        metadata = extract_metadata(up_file)
        

        # Display image preview in Streamlit
        st.image(image, caption='Uploaded Image', use_column_width=True)
        metadata = {
            "filename": up_file.name,
            "event": event,
            "title": title,
            "date": date,
            "city": city,
            "latitude": metadata[0],
            "longitude": metadata[1],
            "description": description,
            "person_in_image:": person_in_image,
            "other_objects": other_objects
            
        }
        upload_blob(image, image)
        logging.info(f"Image: {image} uploaded")
        upload_blob(metadata,f"{image_metadata}")
        logging.info(f"Metadata: {metadata} uploaded")
        insert_metadata(metadata)
        logging.info(f"Metadata: {metadata} stored in Mongo")
        st.success("Image and metadata successfully uploaded to Google Cloud")
        st.text("The preview is lower quality but do not be alarmed - yours is fine.")
else:
    st.error("Please provide both title and description for the image.")
    