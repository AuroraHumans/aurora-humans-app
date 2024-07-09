"""

####### Database integration is not yet implemented #####

"""
import os 
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGO_URI=os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
# Initialize MongoDB Client
mongo_client = MongoClient("MONGO_URI")
db = mongo_client["MONGO_DB_NAME"]


def mongo_connection():
    # Create a new client and connect to the server
    uri = MONGO_URI
    client = MongoClient(uri)
    return client

def insert_metadata_db(metadata):
    """
    Insert metadata into MongoDB collection.
    :param metadata: Dict containing metadata fields
    :return: Inserted ID or None if an error occurs
    """
    try:
        client = mongo_connection()
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
    try:
        database = client[MONGO_DB_NAME]
        collection = database[MONGO_COLLECTION]
    except Exception as e:
        print(e)

    try:
        result = collection.insert_one(metadata)
        return result.inserted_id
    except ConnectionRefusedError as e:
        print(f"Error inserting metadata: {e}")
        return None
'''
def find_metadata(query):
    """
    Retrieve metadata from MongoDB collection based on a query.
    :param query: Dictionary specifying the search criteria
    :return: Cursor containing the matching documents
    """
    try:
        return collection.find(query)
    except Exception as e:
        print(f"Error retrieving metadata: {e}")
        return None '''