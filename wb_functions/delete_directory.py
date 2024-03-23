import os
import platform

def delete_directory(directory_path):
    if os.path.exists(directory_path):
        if platform.system() == "Windows":
            os.system(f'rmdir /s /q "{directory_path}"')
        else:
            os.system(f'rm -r "{directory_path}"')
