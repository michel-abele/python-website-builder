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
# File System Manager
class File_System_Manager:


    # ==================================================================================================
    # progress bar settings
    @staticmethod
    def pb(value):
           
        if value == "format":
            return "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
        
        if value == "ncols":
            return 75
        
        if value == "ascii":
            return False
        
        if value == "colour":
            return 'blue'


    # ==============================================================================================
    # static methods

    # create directories
    @staticmethod
    def create_directories(directory_paths):
        if isinstance(directory_paths, str):
            directory_paths = [directory_paths]
        for directory_path in progress_bar(directory_paths, desc="Creating directories", ascii=File_System_Manager.pb("ascii"), ncols=File_System_Manager.pb("ncols"), colour=File_System_Manager.pb("colour"), bar_format=File_System_Manager.pb("format")):
            os.makedirs(directory_path, exist_ok=True)

    # create files
    @staticmethod
    def create_files(file_paths, content=""):
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        for file_path in progress_bar(file_paths, desc="Creating files",  ascii=File_System_Manager.pb("ascii"), ncols=File_System_Manager.pb("ncols"), colour=File_System_Manager.pb("colour"), bar_format=File_System_Manager.pb("format")):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                file.write(content)

    # delete directories
    @staticmethod
    def delete_directories(directory_paths):
        if isinstance(directory_paths, str):
            directory_paths = [directory_paths]
        for directory_path in progress_bar(directory_paths, desc="Deleting directories", ascii=File_System_Manager.pb("ascii"), ncols=File_System_Manager.pb("ncols"), colour=File_System_Manager.pb("colour"), bar_format=File_System_Manager.pb("format")):
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path, onerror=File_System_Manager._remove_readonly)

    # delete files
    @staticmethod
    def delete_files(file_paths):
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        for file_path in progress_bar(file_paths, desc="Deleting files", ascii=File_System_Manager.pb("ascii"), ncols=File_System_Manager.pb("ncols"), colour=File_System_Manager.pb("colour"), bar_format=File_System_Manager.pb("format")):
            if os.path.exists(file_path):
                os.remove(file_path)

    # copy files
    @staticmethod
    def copy_files(src_file_paths, dst_file_paths):
        if isinstance(src_file_paths, str):
            src_file_paths = [src_file_paths]
        if isinstance(dst_file_paths, str):
            dst_file_paths = [dst_file_paths]
        total = min(len(src_file_paths), len(dst_file_paths))
        for src_file_path, dst_file_path in progress_bar(zip(src_file_paths, dst_file_paths), total=total, desc="Copying files", ascii=File_System_Manager.pb("ascii"), ncols=File_System_Manager.pb("ncols"), colour=File_System_Manager.pb("colour"), bar_format=File_System_Manager.pb("format")):
            shutil.copy2(src_file_path, dst_file_path)

    # copy directory
    @staticmethod
    def copy_directories(src_directories, dst_directories):
        if isinstance(src_directories, str):
            src_directories = [src_directories]
        if isinstance(dst_directories, str):
            dst_directories = [dst_directories]
        total = min(len(src_directories), len(dst_directories))
        for src_path, dst_path in progress_bar(zip(src_directories, dst_directories), total=total, desc="Copying directories", ascii=File_System_Manager.pb("ascii"), ncols=File_System_Manager.pb("ncols"), colour=File_System_Manager.pb("colour"), bar_format=File_System_Manager.pb("format")):
            shutil.copytree(src_path, dst_path)


    # ==============================================================================================
    # helper methods

    # remove readonly attribute from file
    @staticmethod
    def _remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
