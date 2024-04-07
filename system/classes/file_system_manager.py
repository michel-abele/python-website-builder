# ==================================================================================================
# File System Manager
#
# This class provides methods to create and delete directories and files.
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import os
import shutil
import stat

# import third-party modules
from tqdm import tqdm as progress_bar


# ==================================================================================================
# progress bar settings
progress_bar_format = "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
progress_bar_ncols = 75
progress_bar_ascii = False
progress_bar_colour = 'blue'


# ==================================================================================================
# File System Manager
class File_System_Manager:


    # ==============================================================================================
    # static methods

    # create directories
    @staticmethod
    def create_directories(directory_paths):
        for directory_path in progress_bar(directory_paths, desc="Creating directories", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
            os.makedirs(directory_path, exist_ok=True)

    # create files
    @staticmethod
    def create_files(file_paths, content=""):
        for file_path in progress_bar(file_paths, desc="Creating files      ",  ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                file.write(content)

    # delete directories
    @staticmethod
    def delete_directories(directory_paths):
        for directory_path in progress_bar(directory_paths, desc="Deleting directories", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path, onerror=File_System_Manager._remove_readonly)

    # delete files
    @staticmethod
    def delete_files(file_paths):
        for file_path in progress_bar(file_paths, desc="Deleting files      ", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
            if os.path.exists(file_path):
                os.remove(file_path)

    # copy files
    @staticmethod
    def copy_files(src_file_paths, dst_file_paths):
        for src_file_path, dst_file_path in progress_bar(zip(src_file_paths, dst_file_paths), desc="Copying files       ", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
            shutil.copy2(src_file_path, dst_file_path)

    # copy directory
    @staticmethod
    def copy_directories(src_directory_path, dst_directory_path):
        for src_directory_path, dst_directory_path in progress_bar(zip(src_directory_path, dst_directory_path), desc="Copying directory   ", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
            shutil.copytree(src_directory_path, dst_directory_path)


    # ==============================================================================================
    # helper methods

    # remove readonly attribute from file
    @staticmethod
    def _remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
