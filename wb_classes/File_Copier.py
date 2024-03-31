import os
import shutil

class File_Copier:
    def __init__(self, source_dir, target_dir):
        self.source_dir = source_dir
        self.target_dir = target_dir

    # ==============================================================================================
    # copy files
    def copy_files(self):
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        files = os.listdir(self.source_dir)
        for file in files:
            source_file = os.path.join(self.source_dir, file)
            destination_file = os.path.join(self.target_dir, file)
            
            if os.path.isfile(source_file):
                shutil.copy2(source_file, destination_file)
            elif os.path.isdir(source_file):
                shutil.copytree(source_file, destination_file)
