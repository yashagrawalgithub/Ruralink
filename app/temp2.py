import os
import json

def create_patient_images_json(folder_path, output_json_path):
    # Initialize an empty dictionary to store Patient_ID and associated image filenames
    patient_data = {}
    
    # Start the Patient_ID at 1
    patient_id = 1001
    
    # Iterate over each file in the specified folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if it's an image file
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Add key-value pair with Patient_ID as key and filename as value
            patient_data[patient_id] = filename
            
            # Print to check the added data
            print(f"Added Patient_ID {patient_id}: {filename}")
            
            # Increment Patient_ID and reset to 1 if it exceeds 1000
            patient_id += 1
            if patient_id > 2000:
                patient_id = 1001
    
    # Save the data as a JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(patient_data, json_file, indent=4)
    
    print(f"JSON file created at {output_json_path}")

# Usage
folder_path = r"C:\Users\HP\Downloads\Female"  # Replace with the path to your image folder
output_json_path = r"C:\Users\HP\Downloads\patient_images2.json"  # Desired path for JSON output
create_patient_images_json(folder_path, output_json_path)
