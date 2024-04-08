# ==================================================================================================
# Multilingual Webseite Checker
#
# This class checks if a website is multilingual. It checks if the subfolders of a directory are
# valid language codes.
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import os
import json

# import third-party modules
from tqdm import tqdm as progress_bar


# ==================================================================================================
# Multilingual Webseite Checker
class Multilingual_Webseite_Checker:


    # ==============================================================================================
    # load JSON file
    @staticmethod
    def load_json(file_path):
        with open(file_path, "r") as file:
            return json.load(file)


    # ==============================================================================================
    # static method

    # is multilingual
    @staticmethod
    def is_multilingual(directory, iso_639_2_path, iso_639_3_path, iso_3166_1_2_path, iso_3166_1_3_path):

        # load JSON files
        iso_639_2 = Multilingual_Webseite_Checker.load_json(iso_639_2_path)
        iso_639_3 = Multilingual_Webseite_Checker.load_json(iso_639_3_path)
        iso_3166_1_2 = Multilingual_Webseite_Checker.load_json(iso_3166_1_2_path)
        iso_3166_1_3 = Multilingual_Webseite_Checker.load_json(iso_3166_1_3_path)

        # progress bar settings
        progress_bar_format = "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
        progress_bar_ncols  = 75
        progress_bar_ascii  = False
        progress_bar_colour = 'blue'

        # check if the subfolders are valid language codes
        subfolders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        for subfolder in progress_bar(subfolders, desc="Multilingual Webseite Check", unit="folder", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
            if not Multilingual_Webseite_Checker._is_valid_language_code(subfolder, iso_639_2, iso_639_3, iso_3166_1_2, iso_3166_1_3):
                return False
        return True


    # ==============================================================================================
    # helper methods

    # is valid language code
    @staticmethod
    def _is_valid_language_code(code, iso_639_2, iso_639_3, iso_3166_1_2, iso_3166_1_3):

        # example: en, de, fr, ...
        if len(code) == 2 and code.islower() and code in iso_639_2:
            return True
        
        # example: eng, deu, fra, ...
        elif len(code) == 3 and code.islower() and code in iso_639_3:
            return True
        
        # example: en-US, de-DE, fr-FR, ...
        elif len(code) == 5 and code[2] == "-":
            language_code = code[:2].lower()
            country_code = code[3:].upper()
            if language_code in iso_639_2 and country_code in iso_3166_1_2:
                return True
            
        # example: eng-US, deu-DE, fra-FR, ...
        elif len(code) == 6 and code[3] == "-":
            language_code = code[:3].lower()
            country_code = code[4:].upper()
            if language_code in iso_639_3 and country_code in iso_3166_1_2:
                return True
            
        # example: en-USA, de-DEU, fr-FRA, ...
        elif len(code) == 6 and code[2] == "-":
            language_code = code[:2].lower()
            country_code = code[3:].upper()
            if language_code in iso_639_2 and country_code in iso_3166_1_3:
                return True
        
        # example: eng-USA, deu-DEU, fra-FRA, ...
        elif len(code) == 7 and code[3] == "-":
            language_code = code[:3].lower()
            country_code = code[4:].upper()
            if language_code in iso_639_3 and country_code in iso_3166_1_3:
                return True

        # single language
        return False
