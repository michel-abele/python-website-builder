import json
import os
import re


class Multilingual_Website_Checker:
    def __init__(self, source_path):
        self.source_path = source_path
        self.is_multilingual_website = True
        self.subdirectories = []


    # ==============================================================================================
    # check multilingual website
    def check_multilingual_website(self):
        # check for multilingual website
        self.subdirectories = [subdir for subdir in os.listdir(self.source_path) if os.path.isdir(os.path.join(self.source_path, subdir))]
        for subdir in self.subdirectories:
            if not self._is_valid_language_code(subdir):
                self.is_multilingual_website = False
                break

        self._create_sitemap_files()

        return self.is_multilingual_website


    # ==============================================================================================
    # helper methods

    # check valid language code
    def _is_valid_language_code(self, code):
        pattern = r'^[a-z]{2}(-[a-zA-Z]{2,3})?$'
        return bool(re.match(pattern, code))

    # create sitemap files
    def _create_sitemap_files(self):
        sitemap_dir = os.path.join("temp", "sitemap")
        os.makedirs(sitemap_dir, exist_ok=True)

        for subdir in self.subdirectories:
            json_file = os.path.join(sitemap_dir, f"{subdir}.json")
            with open(json_file, "w") as f:
                json.dump({}, f)

        json_file = os.path.join("temp", "sitemap.json")
        with open(json_file, "w") as f:
            json.dump({}, f)
