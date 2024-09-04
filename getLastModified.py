import os
import time
import shutil

def get_last_modified_files(path, days, extensions):
    current_time = time.time()
    seconds_per_day = 24 * 60 * 60
    cutoff_time = current_time - (days * seconds_per_day)

    last_modified_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            modified_time = os.path.getmtime(file_path)

            if modified_time > cutoff_time:
                file_extension = os.path.splitext(file_path)[1]
                if len(extensions) != 0:
                    if file_extension.lower() in extensions:
                        last_modified_files.append(file_path)
                else:
                    last_modified_files.append(file_path)

    return last_modified_files

# Ask for input
# path = input("Enter the directory path: ")
path = "proj/main"
# days = int(input("Enter the number of days: "))
days = 3

# extensions = input("Enter the file extensions (separated by comma): ").split(",")
extensions = [".php"]

# Get last modified files
files = get_last_modified_files(path, days, extensions)

# Create the new folder
folder_name = f"modified_{days}"
os.makedirs(folder_name, exist_ok=True)

# Copy modified files to the new folder
for file in files:
    dest_path = os.path.join(folder_name, file)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copy2(file, dest_path)

# Display the results
print(f"Last modified files within the past {days} days:")
for file in files:
    print(file)
print("Modified files have been copied to the folder:", folder_name)
