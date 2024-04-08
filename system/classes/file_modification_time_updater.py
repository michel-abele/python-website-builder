# ==================================================================================================
# File Mod Time Updater
#
# This class updates the modification time of all files with a specific file extension in a
# directory to the latest modification time.
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import os
import json

# import third-party modules
from tqdm import tqdm as progress_bar


# ==================================================================================================
# File Modification Time Updater
class File_Modification_Time_Updater:


    # ==============================================================================================
    # update file modification times
    @staticmethod
    def update_file_modification_times(directory, file_extension, temp_directory, temp_file):
        latest_mod_time = 0

        # progress bar settings
        progress_bar_format = "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
        progress_bar_ncols  = 75
        progress_bar_ascii  = False
        progress_bar_colour = 'blue'
        
        # analyze the directory and find the latest modification time
        for root, dirs, files in progress_bar(os.walk(directory), desc="Analyzing directory", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
            for file in files:
                if file.endswith(file_extension):
                    file_path = os.path.join(root, file)
                    mod_time  = os.path.getmtime(file_path)
                    latest_mod_time = max(latest_mod_time, mod_time)

        # update the modification time of all files to the latest time
        for root, dirs, files in progress_bar(os.walk(directory), desc="Updating files", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
            for file in files:
                if file.endswith(file_extension):
                    file_path = os.path.join(root, file)
                    os.utime(file_path, (latest_mod_time, latest_mod_time))

        # save the latest modification time to the JSON file
        File_Modification_Time_Updater._save_modification_time_to_json(latest_mod_time, file_extension, temp_directory, temp_file)


    # ==============================================================================================
    # helper methods

    # save the latest modification time to a JSON file
    @staticmethod
    def _save_modification_time_to_json(latest_mod_time, file_extension, temp_directory, temp_file):
        json_file_path = temp_directory + "/" + temp_file
        data = {}
        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as file:
                data = json.load(file)
        data[file_extension] = int(latest_mod_time)
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent=4)
        print("Latest modification time saved to temp file.")
