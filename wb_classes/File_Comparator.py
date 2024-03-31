import os
import shutil

class File_Comparator:
    def __init__(self, source, target, exclude_dir=None):
        self.source = source
        self.target = target
        self.exclude_dir = exclude_dir


    # ==============================================================================================
    # compare_and_delete
    def compare_and_delete(self):
        self._compare_and_delete_files()
        self._delete_empty_directories()


    # ==============================================================================================
    # helper methods
        
    # compare and delete files
    def _compare_and_delete_files(self):
        for item in os.listdir(self.target):
            target_item = os.path.join(self.target, item)
            source_item = os.path.join(self.source, item)

            if os.path.isfile(target_item) and not os.path.exists(source_item):
                os.remove(target_item)
            elif os.path.isdir(target_item) and item != self.exclude_dir:
                self.compare_and_delete_subdirectory(source_item, target_item)

    # compare and delete subdirectory
    def _compare_and_delete_subdirectory(self, source_subdir, target_subdir):
        if not os.path.exists(source_subdir):
            shutil.rmtree(target_subdir)
        else:
            File_Comparator(source_subdir, target_subdir, self.exclude_dir).compare_and_delete()

    # delete empty directories
    def _delete_empty_directories(self):
        for root, dirs, files in os.walk(self.target, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
