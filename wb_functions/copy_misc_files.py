import os
import shutil

def copy_misc_files(source_dir, target_dir):

    # ==============================================================================================
    # copy miscellaneous files
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    files = os.listdir(source_dir)

    for file in files:
        source_file = os.path.join(source_dir, file)
        destination_file = os.path.join(target_dir, file)
        shutil.copy2(source_file, destination_file)
