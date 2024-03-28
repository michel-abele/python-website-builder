import os

def delete_file(file_path):

    # ==============================================================================================
    # delete file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
