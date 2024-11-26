import pandas as pd
import mysql.connector
from mysql.connector import Error

# Load the CSV file
file_path = r'C:\Users\HP\Downloads\Patient_Data.csv'  # Replace with the actual file path
patient_data = pd.read_csv(file_path)

# Connect to MySQL database
try:
    connection = mysql.connector.connect(
        host='localhost',    # or the hostname of your database
        database='project',   # Replace with your database name
        user='root',
        password='root'   # Replace with your MySQL root password
    )

    if connection.is_connected():
        cursor = connection.cursor()
        
        # Define the table creation query
        create_table_query = """
        CREATE TABLE patient (
            Patient_ID INT PRIMARY KEY,
            Age INT NOT NULL,
            Gender VARCHAR(10),
            Employer_Category VARCHAR(100),
            Diabetic BOOLEAN DEFAULT 0,
            Over_Weight BOOLEAN DEFAULT 0,
            Blood_Pressure BOOLEAN DEFAULT 0,
            Smoker BOOLEAN DEFAULT 0
        );
        """  # Removed the extra comma after the last column definition
        
        cursor.execute(create_table_query)
        connection.commit()
        
        # Insert data into the Patient table
        insert_query = """
        INSERT INTO patient (Patient_ID, Age, Gender, Employer_Category, 
                             Diabetic, Over_Weight, Blood_Pressure, Smoker)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """  # Adjusted the number of placeholders to match the columns in the table
        
        # Prepare data for insertion
        data = [
            (int(row['Patient_ID']), int(row['Age']), row['Gender'], row['Employer_Category'],
             bool(row['Diabetic']), bool(row['Over_Weight']), bool(row['Blood_Pressure']), bool(row['Smoker']))
            for _, row in patient_data.iterrows()
        ]  # Converted Gender and Employer_Category to strings and Diabetic, Over_Weight, Blood_Pressure, and Smoker to booleans
        
        # Execute the insert query
        cursor.executemany(insert_query, data)
        connection.commit()
        print("All data inserted successfully.")
        
except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
