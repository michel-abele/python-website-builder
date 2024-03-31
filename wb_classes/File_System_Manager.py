import os
import shutil
import stat

class File_System_Manager:

    # ==============================================================================================
    # static methods

    # create a directory
    @staticmethod
    def create_directory(directory_path):
        os.makedirs(directory_path, exist_ok=True)

    # create a file
    @staticmethod
    def create_file(file_path, content=""):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(content)

    # delete a directory
    @staticmethod
    def delete_directory(directory_path):
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path, onerror=File_System_Manager._remove_readonly)

    # delete a file
    @staticmethod
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    # ==============================================================================================
    # helper methods
            
    # remove readonly attribute from file
    @staticmethod
    def _remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
