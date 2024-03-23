import os
import shutil

def copy_misc_files(source_dir, target_dir):

    # Create the destination directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Get a list of all files in the source directory
    files = os.listdir(source_dir)

    # Copy each file from the source directory to the destination directory
    for file in files:
        source_file = os.path.join(source_dir, file)
        destination_file = os.path.join(target_dir, file)
        shutil.copy2(source_file, destination_file)
