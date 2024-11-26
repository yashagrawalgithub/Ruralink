import pymongo
from pymongo import MongoClient
from PIL import Image
import io
import os

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Project']  # Database name
collection = db['patients']  # Collection name

# Folder containing the images
image_folder = r"C:\Users\HP\Downloads\img"  # Replace with the actual path to your image folder

# Iterate through each patient ID and corresponding image
for patient_id in range(1, 2001):  # IDs from 1 to 2000
    # Construct the filename based on patient ID
    image_filename = f"{patient_id}.png"
    image_path = os.path.join(image_folder, image_filename)

    # Check if the image file exists
    if os.path.isfile(image_path):
        # Open the image and convert it to binary data
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        # Create the document to insert
        document = {
            "patient_id": patient_id,
            "img": image_data  # Store image data in binary format
        }

        # Insert the document into MongoDB
        collection.insert_one(document)
        print(f"Stored patient ID {patient_id} with image data.")
    else:
        print(f"Image for patient ID {patient_id} not found.")

print("Data storage complete.")
