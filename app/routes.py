from flask import render_template, request, redirect, url_for, session ,flash
from app import app, mysql, mongo
from flask import Flask, render_template, request
from pymongo import MongoClient
import base64
# import io

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        password = request.form['password']
        
        # Placeholder for authentication logic
        if password == "admin":  # Replace with real password verification
            session['role'] = role
            session['logged_in'] = True
            if role == 'Junior':
                return redirect(url_for('junior_dashboard'))
            elif role == 'Senior':
                return redirect(url_for('senior_dashboard'))
        else:
            return "Invalid login, please try again."
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('role', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/junior_dashboard')
def junior_dashboard():
    if session.get('logged_in') and session.get('role') == 'Junior':
        return render_template('junior_dashboard.html')
    return redirect(url_for('login'))

@app.route('/senior_dashboard')
def senior_dashboard():
    if session.get('logged_in') and session.get('role') == 'Senior':
        return render_template('senior_dashboard.html')
    return redirect(url_for('login'))

# Route to display patient details
@app.route('/patient_detail', methods=['POST', 'GET'])
def patient_detail():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')

        # Fetch patient details from MySQL
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM patient WHERE Patient_ID = %s", (patient_id,))
        patient_data = cur.fetchone()  # Assuming you're using a single patient_id query
        cur.close()

        #mongodb connection
        client = MongoClient('mongodb://localhost:27017/')
        mongo_db = client['Project']  # Your MongoDB database
        mongo_patient_images = mongo_db['patients']  # The collection storing patient_id and filenames
        
        # Ensure data is correctly structured as a dictionary if needed
        # print(patient_data)
        if patient_data:
            # If `patient_data` is a tuple, convert it to a dictionary
            patient_data = {
            "Patient_ID": patient_data[0],
            "Age": patient_data[1]-10,
            "Gender": patient_data[2],
            "Employer_Category": patient_data[3],
            "Diabetic": patient_data[4],
            "Over_Weight": patient_data[5],
            "Blood_Pressure": patient_data[6],
            "Smoker": patient_data[7],
        }
        
        # Step 1: Retrieve the document with patient metadata based on patient_id
        image_data_document = mongo_patient_images.find_one({"patient_id": int(patient_id)})
        # print(image_metadata_document)  # Print to debug and verify the document structure

        # Step 2: Check if the document and the 'img' field exist
        if image_data_document and "img" in image_data_document:
            # Convert the image data to a Base64 string for HTML rendering
            profile_pic_data = base64.b64encode(image_data_document["img"]).decode('utf-8')
        else:
            # If no image data found, set profile_pic_data to None
            profile_pic_data = None

        #prescription
        # Get the patient_id from the URL query parameter
        patient_id = request.args.get('patient_id')

        # Check if patient data exists
        if image_data_document:
            # Get prescription if available, or show default message
            prescription = image_data_document.get("prescription", "No prescription available.")

            # Determine user role from session (assuming `user_role` is stored in the session on login)
            role = session.get('role', 'Junior')  # default to 'junior' if not set
            # print(role)
            return render_template(
                'patient_detail.html', 
                profile_pic=profile_pic_data, 
                data=patient_data, 
                prescription=prescription, 
                role=role
            )
        else:
            flash("Patient not found.")

    return redirect(url_for('senior_dashboard'))

# Route to update prescription (for seniors only)
@app.route('/update_prescription', methods=['POST'])
def update_prescription():
    
    client = MongoClient('mongodb://localhost:27017/')
    mongo_db = client['Project']  # Your MongoDB database

    # Ensure only seniors can update
    if session.get('role') != 'Senior':
        flash("Only senior users can update prescriptions.")
        # print(request.form.get('patient_id'))
        return redirect(url_for('patient_detail', patient_id=request.form.get('patient_id')))
    
    # print(request.form.get('patient_id'))
    # Retrieve patient_id and new prescription from the form
    patient_id = request.form.get('patient_id')
    new_prescription = request.form.get('prescription')

    # Update the prescription in MongoDB
    result = mongo_db['patients'].update_one(
        {"patient_id": int(patient_id)},
        {"$set": {"prescription": new_prescription}}
    )

    # Confirm update status
    if result.matched_count > 0:
        flash("Prescription updated successfully.")
    else:
        flash("Failed to update prescription. Patient not found.")

    return redirect(url_for('patient_detail', patient_id=patient_id))


# Route for juniors to upload a file to MongoDB
@app.route('/upload_file', methods=['POST'])
def upload_file():
    client = MongoClient('mongodb://localhost:27017/')
    mongo_db = client['Project']  # Your MongoDB database

    # Check if user is a junior
    if session.get('role') != 'Junior':
        flash("Only junior users can upload files.")
        return redirect(url_for('junior_dashboard'))
    
    # Get the patient_id from the form and the uploaded file
    patient_id = request.form.get('patient_id')
    file = request.files.get('file')
    

    if patient_id and file:
        # Read file data and prepare metadata
        file_data = file.read()
        file_info = {
            "filename": file.filename,
            "content_type": file.content_type,
            "data": file_data
        }
        # Update the patient's document in MongoDB to include the file
        result = mongo_db['patients'].update_one(
            {"patient_id": int(patient_id)},
            {"$set": {"file": file_info}}
        )

        if result.matched_count > 0:
            flash("File uploaded and saved successfully.")
        else:
            flash("Failed to upload file. Patient not found.")
    else:
        flash("Please provide both Patient ID and a file.")
    
    return redirect(url_for('junior_dashboard'))


# # Route to download a file associated with a patient by patient_id
# @app.route('/download_file/<int:patient_id>', methods=['GET'])
# def download_file(patient_id):
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client["Project"]  # Replace with your database name
#     patients_collection = db["patients"]  # Replace with your collection name

#     # Retrieve the patient document from MongoDB
#     patient_data = patients_collection.find_one({"patient_id": patient_id})
    
#     if patient_data and "file" in patient_data:
#         file_data = patient_data["file"]
        
#         # Ensure file data exists and is valid
#         if file_data["data"] and file_data["filename"] and file_data["content_type"]:
#             # Convert the binary data for the file into a BytesIO stream
#             file_stream = BytesIO(file_data["data"])
#             file_stream.seek(0)
            
#             # Serve the file to the user as a download
#             return send_file(
#                 file_stream,
#                 mimetype=file_data["content_type"],
#                 as_attachment=True,
#                 download_name=file_data["filename"]
#             )
#         else:
#             flash("No file available for this patient.")
#     else:
#         flash("Patient not found or no file available.")

#     return redirect(url_for('patient_detail', patient_id=patient_id))