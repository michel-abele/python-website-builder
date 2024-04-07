# ==================================================================================================
# Directory Comparator
#
# This class is used to compare two directories and remove files and directories that are not
# present in the source directory.
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import os
import shutil


# ==================================================================================================
# Directory Comparator
class Directory_Comparator:
    def __init__(self, source_dir, target_dir, file_extension=None, exclude_dir=None):
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.file_extension = file_extension
        self.exclude_dir = exclude_dir


    # ==============================================================================================
    # compare directories
    def compare_directories(self):
        self._process_directory(self.source_dir, self.target_dir)


    # ==============================================================================================
    # helper methods

    # process directory
    def _process_directory(self, source_dir, target_dir):
        for item in os.listdir(target_dir):
            target_path = os.path.join(target_dir, item)
            source_path = os.path.join(source_dir, item)

            if os.path.isdir(target_path):
                if self._should_exclude(target_path):
                    continue
                if not os.path.exists(source_path):
                    self._remove_directory(target_path)
                else:
                    self._process_directory(source_path, target_path)
                    if not os.listdir(target_path):
                        self._remove_directory(target_path)
            else:
                if not os.path.exists(source_path) or not self._has_valid_extension(item):
                    self._remove_file(target_path)

    # should exclude
    def _should_exclude(self, path):
        return self.exclude_dir and os.path.normpath(path) == os.path.normpath(self.exclude_dir)

    # has valid extension
    def _has_valid_extension(self, item):
        return not self.file_extension or item.endswith('.' + self.file_extension)

    # remove directory
    def _remove_directory(self, directory):
        shutil.rmtree(directory)

    # remove file
    def _remove_file(self, file):
        os.remove(file)
