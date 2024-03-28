import os
import shutil
import stat

def delete_directory(directory_path):

    # ==============================================================================================
    # delete directory if it exists
    if os.path.exists(directory_path):

        # function for removing the write protection attributes
        def remove_readonly(func, path, _):
            os.chmod(path, stat.S_IWRITE)
            func(path)

        # delete directory
        shutil.rmtree(directory_path, onerror=remove_readonly)
