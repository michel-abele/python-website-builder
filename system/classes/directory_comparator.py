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

# import third-party modules
from tqdm import tqdm as progress_bar


# ==================================================================================================
# Directory Comparator
class Directory_Comparator:


    # ==============================================================================================
    # compare directories
    @staticmethod
    def compare_directories(source_dir, target_dir, source_extension=None, target_extension=None, exclude_dir=None):
        Directory_Comparator._process_directory(source_dir, target_dir, target_extension, source_extension, exclude_dir)


    # ==============================================================================================
    # helper methods

    # process directory
    @staticmethod
    def _process_directory(source_dir, target_dir, target_extension, source_extension, exclude_dir):

        # progress bar settings
        progress_bar_format = "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
        progress_bar_ncols = 75
        progress_bar_ascii = False
        progress_bar_colour = 'blue'

        # method
        items = list(os.listdir(target_dir))
        with progress_bar(total=len(items), desc='Processing ({target_extension})', unit='item', ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format) as pbar:
            for item in items:
                target_path = os.path.join(target_dir, item)
                source_item = Directory_Comparator._get_source_item(item, source_extension, target_extension)
                source_path = os.path.join(source_dir, source_item)
                if os.path.isdir(target_path):
                    if Directory_Comparator._should_exclude(target_path, exclude_dir):
                        pbar.update(1)
                        continue
                    if not os.path.exists(source_path):
                        Directory_Comparator._remove_directory(target_path)
                    else:
                        Directory_Comparator._process_directory(source_path, target_path, target_extension, source_extension, exclude_dir)
                        if not os.listdir(target_path):
                            Directory_Comparator._remove_directory(target_path)
                else:
                    if not os.path.exists(source_path) or not Directory_Comparator._has_valid_extension(item, target_extension):
                        Directory_Comparator._remove_file(target_path)
                pbar.update(1)
    
    # get source item
    @staticmethod
    def _get_source_item(item, source_extension, target_extension):
        if source_extension and target_extension:
            return item.replace(target_extension, source_extension)
        return item

    # should exclude
    @staticmethod
    def _should_exclude(path, exclude_dir):
        return exclude_dir and os.path.normpath(path) == os.path.normpath(exclude_dir)

    # has valid extension
    def _has_valid_extension(item, extension):
        return not extension or item.endswith('.' + extension)

    # remove directory
    @staticmethod
    def _remove_directory(directory):
        shutil.rmtree(directory)

    # remove file
    @staticmethod
    def _remove_file(file):
        os.remove(file)
