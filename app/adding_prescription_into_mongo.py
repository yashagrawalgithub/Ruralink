from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Project']  # Replace with your database name
patients_collection = db['patients']  # Replace with your collection name

# Example update: add a prescription for patient_id 1
for i in range(1,2001):
    patients_collection.update_one(
        {"patient_id": i},
        {"$set": {"prescription": "None"}}
    )

print("Prescription added for patient_id")
