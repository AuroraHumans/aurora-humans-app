import io
import logging
import os

from lib.gcp.upload_to_gcp import upload_photo_to_gcs
from lib.db.database import insert_metadata_db 
import streamlit as st
from dotenv import load_dotenv
from google.cloud import storage
from PIL import Image

from lib.db.database import insert_metadata_db
from lib.extract_metadata import extract_metadata

load_dotenv()
_logger = logging.getLogger(__name__)


@st.cache_data
def uploaded_file(file):
    return file
# Constants
MAX_IMAGE_SIZE = (224, 224)  # Change to your requirements  - Optimized for PyTorch.

st.title("🌎💚 :: Connected Hearts - Aurora 2024 Event :: 💚🌎") 
st.subheader("A Worldwide Moment in Time")
st.divider()
st.text("The world watched as the sky came alive. Take a minute to remind the world.")
st.divider()
file_upload = st.file_uploader("Upload Your Image", type=["png", "jpg", "jpeg", "webp"])


# Streamlit file uploader
# Metadata form
event = st.multiselect("Event?", ["Aurora2024"], default="Aurora2024")
continent = st.multiselect(label="Continent",options=["North America", "South America", "Europe", "Asia", "Africa", "Australia", "Antarctica"], default=None, max_selections=1)
title = st.text_input("Your Name For the Image")
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
        file_path = f"./tmp/{up_file}"
        
        # Read the image file
        image = Image.open(up_file)
        
        # Compress the image
        image.thumbnail(MAX_IMAGE_SIZE)

        # Convert back to bytes
        img_byte_arr = io.BytesIO()
        
        #RM temp
        os.removedirs(f"./tmp/{up_file}")
    
        #image.save(format=image.format, fp=file_path)
        img_byte_arr = img_byte_arr.getvalue()
        metadata = extract_metadata(up_file)
        

        # Display image preview in Streamlit
        st.image(image, caption='Uploaded Image', use_column_width=True)
        metadata = {
            "filename": up_file.name,
            "event": event,
            "title": title,
            "continent": continent,
            "date": date,
            "city": city,
            "latitude": metadata[0],
            "longitude": metadata[1],
            "description": description,
            "person_in_image:": person_in_image,
            "other_objects": other_objects
            
        }
        
        upload_photo_to_gcs(image, os.getenv("GCP_PROJECT_ID"), os.getenv("GCP_SECRET_ID"), bucket_name)
        _logger.info(f"Image: {filename} uploaded")
        # INSERT METADATA INTO MONGO
        insert_metadata_db(metadata)
        _logger.info(f"Metadata: {metadata} stored in Mongo")
        st.success("Image and metadata successfully uploaded to Google Cloud")
        st.text("The preview is lower quality but do not be alarmed - the size is perfect for processing.")
else:
    st.error("Please provide both title and description for the image.")
    