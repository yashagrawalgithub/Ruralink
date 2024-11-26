# import os

# # Path to the folder containing the PNG files
# folder_path = r"C:\Users\HP\Downloads\Male"

# # Get a list of all PNG files in the folder
# files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# # Sort the files to ensure they are renamed in the correct order
# files.sort()

# # Rename each file
# for i, filename in enumerate(files, start=1):
#     new_name = f"{i}.png"  # New name format
#     old_path = os.path.join(folder_path, filename)
#     new_path = os.path.join(folder_path, new_name)
#     os.rename(old_path, new_path)

# print("Renaming complete.")
import os

# Path to the folder containing the PNG files
folder_path = r"C:\Users\HP\Downloads\Female"

# Get a list of all PNG files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# Sort the files to ensure they are renamed in the correct order
files.sort()

# Rename each file
for i, filename in enumerate(files, start=1001):
    new_name = f"{i}.png"  # New name format
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_name)
    os.rename(old_path, new_path)

print("Renaming complete.")
