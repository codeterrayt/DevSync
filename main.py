import os
import filecmp
import shutil
import difflib

def compare_folders(folder1, folder2, extensions_to_compare=None):
    comparison = filecmp.dircmp(folder1, folder2)

    if extensions_to_compare is None:
        extensions_to_compare = []

    # Compare files with the specified extensions in both folders
    for common_file in comparison.common_files:
        file1 = os.path.join(folder1, common_file)
        file2 = os.path.join(folder2, common_file)
        if not extensions_to_compare or (extensions_to_compare and os.path.splitext(common_file)[1] in extensions_to_compare):
            if filecmp.cmp(file1, file2):
                print(f"File '{common_file}' is identical in both folders.")
            else:
                print(f"File '{common_file}' differs in content. (Differing in '{folder1}' and '{folder2}')")
                show_file_differences(file1, file2)
                fix_file = input(f"Do you want to fix '{common_file}'? (y/n): ")
                if fix_file.lower() == 'y':
                    source_path = os.path.join(folder2, common_file)
                    destination_path = os.path.join(folder1, common_file)
                    shutil.copy2(source_path, destination_path)
                    print(f"File '{common_file}' is copied to the second code folder.")
                    continue
                else:
                    show_file_differences(file1, file2)

    # Check for new and old files in both folders
    for new_file in comparison.right_only:
        path = os.path.join(folder2, new_file)
        if os.path.isfile(path):
            if not extensions_to_compare or (extensions_to_compare and os.path.splitext(new_file)[1] in extensions_to_compare):
                print(f"File '{new_file}' is not present in the second folder. (Located in '{folder2}')")
                fix_file = input(f"Do you want to fix '{new_file}'? (y/n): ")
                if fix_file.lower() == 'y':
                    source_path = os.path.join(folder2, new_file)
                    destination_path = os.path.join(folder1, new_file)
                    shutil.copy2(source_path, destination_path)
                    print(f"File '{new_file}' is copied to the second code folder.")
        elif os.path.isdir(path):
            print(f"Directory '{new_file}' is not present in the second folder. (Located in '{folder2}')")
            fix_dir = input(f"Do you want to fix '{new_file}'? (y/n): ")
            if fix_dir.lower() == 'y':
                source_path = os.path.join(folder2, new_file)
                destination_path = os.path.join(folder1, new_file)
                shutil.copytree(source_path, destination_path)
                print(f"Directory '{new_file}' is copied to the second code folder.")

    for old_file in comparison.left_only:
        path = os.path.join(folder1, old_file)
        if os.path.isfile(path):
            if not extensions_to_compare or (extensions_to_compare and os.path.splitext(old_file)[1] in extensions_to_compare):
                print(f"File '{old_file}' is present only in second code folder. (Located in '{folder1}')")
                fix_file = input(f"Do you want to fix '{old_file}'? (y/n): ")
                if fix_file.lower() == 'y':
                    source_path = os.path.join(folder1, old_file)
                    destination_path = os.path.join(folder2, old_file)
                    shutil.copy2(source_path, destination_path)
                    print(f"File '{old_file}' is copied to the main code folder.")
        elif os.path.isdir(path):
            print(f"Directory '{old_file}' is present only in second code folder. (Located in '{folder1}')")
            fix_dir = input(f"Do you want to fix '{old_file}'? (y/n): ")
            if fix_dir.lower() == 'y':
                source_path = os.path.join(folder1, old_file)
                destination_path = os.path.join(folder2, old_file)
                shutil.copytree(source_path, destination_path)
                print(f"Directory '{old_file}' is copied to the main code folder.")

    # Recursively compare subdirectories
    for sub_dir in comparison.common_dirs:
        sub_folder1 = os.path.join(folder1, sub_dir)
        sub_folder2 = os.path.join(folder2, sub_dir)
        compare_folders(sub_folder1, sub_folder2, extensions_to_compare)

def show_file_differences(file1, file2):
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            diff = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file1, tofile=file2)
            for line in diff:
                print(line.strip())
    except:
        print("cant read differences")

# Example usage

folder2 = input("Please Enter Folder Name or Path of the Code Folder with All Data and Files: \n ") # complete data folder

folder1 = input("Please Enter Folder Name or Path of the Code Folder where Data and Files seems missing: \n ") # missing data folder
extensions_to_compare = []  # Specify the file extensions to compare; leave empty for all files
compare_folders(folder1, folder2, extensions_to_compare)
