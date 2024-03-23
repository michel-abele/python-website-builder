import os

def create_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("")
