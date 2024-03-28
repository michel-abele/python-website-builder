import os

def create_directory(directory_path):

    # ==============================================================================================
    # create directory if it does not exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
