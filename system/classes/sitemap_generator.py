# ==================================================================================================
# Sitemap Generator
#
# This class generates XML sitemaps from JSON files.
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import os
import json
import math

# import third-party modules
from tqdm import tqdm as progress_bar


# ==================================================================================================
# Sitemap Generator
class Sitemap_Generator:


    # ==============================================================================================
    # static method

    # generate
    @staticmethod
    def generate(temp_directory_sitemaps, library_directory_sitemaps, target_directory, base_url):

        # progress bar settings
        progress_bar_format = "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
        progress_bar_ncols  = 75
        progress_bar_ascii  = False
        progress_bar_colour = 'blue'

        # create the library directory if it does not exist
        os.makedirs(library_directory_sitemaps, exist_ok=True)

        # loop through all JSON files in the temp directory
        for json_file in progress_bar(os.listdir(temp_directory_sitemaps), desc="Generating sitemaps", unit="file", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
            if json_file.endswith(".json"):
                json_file_path = os.path.join(temp_directory_sitemaps, json_file)

                # load the data from the JSON file
                with open(json_file_path, "r") as f:
                    data = json.load(f)

                # variables
                language_code = os.path.splitext(json_file)[0]
                base_filename = f"{language_code}.xml"
                max_entries = 50000
                max_file_size = 50 * 1024 * 1024
                num_files = math.ceil(len(data) / max_entries)
                current_file_num = 1
                current_file_size = 0
                current_file_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

                # loop through all entries in the data
                for file_path, modification_time in data.items():

                    # variables
                    file_path_without_extension = os.path.splitext(file_path)[0]
                    url_entry = f'<url><loc>{base_url}/{file_path_without_extension}</loc><lastmod>{modification_time}</lastmod></url>\n'

                    # check if adding the entry would exceed the maximum file size or number of entries
                    if current_file_size + len(url_entry) > max_file_size or (current_file_num - 1) * max_entries + current_file_content.count('<url>') >= max_entries:
                        
                        # close the current file
                        current_file_content += '</urlset>'

                        # variables
                        filename = base_filename if num_files == 1 else f"{language_code}_{current_file_num}.xml"
                        file_path = os.path.join(library_directory_sitemaps, filename)

                        # write the current file content to the file
                        with open(file_path, "w") as f:
                            f.write(current_file_content)

                        # variables
                        current_file_num += 1
                        current_file_size = 0
                        current_file_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

                    # add the entry to the current file content
                    current_file_content += url_entry

                    # update the current file size
                    current_file_size += len(url_entry)

                # close the last file
                current_file_content += '</urlset>'

                # set the filename for the last file
                filename = base_filename if num_files == 1 else f"{language_code}_{current_file_num}.xml"

                # set the path for the last file
                file_path = os.path.join(library_directory_sitemaps, filename)

                # write the last file content to the file
                with open(file_path, "w") as f:
                    f.write(current_file_content)

                # create the index sitemap for the language
                Sitemap_Generator._create_index_sitemap(language_code, num_files, target_directory, base_url)

    # ==============================================================================================
    # helper method

    # create index sitemap
    @staticmethod
    def _create_index_sitemap(language_code, num_files, target_directory, base_url):
        filename = f"{language_code}.xml"
        file_path = os.path.join(target_directory, filename)
        sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        # add the entries for the sitemaps
        for i in range(1, num_files + 1):
            sitemap_url = f"{base_url}/sitemaps/{language_code}.xml" if num_files == 1 else f"{base_url}/sitemaps/{language_code}_{i}.xml"
            sitemap_content += f'<sitemap><loc>{sitemap_url}</loc></sitemap>\n'

        # close the sitemap
        sitemap_content += '</sitemapindex>'

        # write the sitemap content to the file
        with open(file_path, "w") as f:
            f.write(sitemap_content)
