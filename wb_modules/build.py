from wb_functions import copy_misc_files
from wb_functions import create_directory
from wb_functions import create_sitemap
from wb_functions import delete_directory
from wb_functions import process_scss_files
from wb_functions import process_js_files

from wb_classes import File_Comparator
from wb_classes import HTML_Parts_Modification_Tracker
from wb_classes import HTML_Processor
from wb_classes import Multilingual_Website_Checker

import sys


# ==============================================================================
# directories

# main directories
directory_temp   = "./temp"
directory_source = "./source"
directory_page   = "./page"

# html source directories
directory_source_html = directory_source + "/html"
directory_source_html_content = directory_source_html + "/content"
directory_source_html_parts   = directory_source_html + "/parts"

# scss source directories
directory_source_scss = directory_source + "/scss"

# javascript source directories
directory_source_js = directory_source + "/js"

# fonts source directories
directory_source_fonts = directory_source + "/fonts"

# images source directories
directory_source_img = directory_source + "/img"

# misc source directories
directory_source_misc = directory_source + "/misc"

# library page directories
directory_page_lib = directory_page + "/lib"
directory_page_lib_css   = directory_page_lib + "/css"
directory_page_lib_js    = directory_page_lib + "/js"
directory_page_lib_fonts = directory_page_lib + "/fonts"
directory_page_lib_img   = directory_page_lib + "/img"

# library page directories array
library_page_directories = [
    directory_page_lib,
    directory_page_lib_css,
    directory_page_lib_js,
    directory_page_lib_fonts,
    directory_page_lib_img,
]


# ==============================================================================
# files

# general files
config_file = "./wb_database/config.json"
html_parts_modification_file = "./temp/html_parts_file_modifications.json"


# ==============================================================================
# prepare directories and files

# clean page directory
if "-clear" in sys.argv or "-c" in sys.argv:
    delete_directory(directory_page)
    delete_directory(directory_temp)
    create_directory(directory_page)

# create or update page directory
else:
    comparator = File_Comparator(directory_source_html_content, directory_page, "lib")
    comparator.compare_and_delete()

    for directory in library_page_directories:
        create_directory(directory)

# create temp directory
create_directory(directory_temp)


# ==============================================================================
# process html files
tracker = HTML_Parts_Modification_Tracker(directory_source_html_parts, html_parts_modification_file)
tracker.track_modifications()

mw_checker = Multilingual_Website_Checker(directory_source_html_content)
is_multilingual_website = mw_checker.check_multilingual_website()

processor = HTML_Processor(directory_source_html, directory_page, config_file, html_parts_modification_file, is_multilingual_website)
processor.process_html_files()

create_sitemap(is_multilingual_website, config_file, directory_page)


# ==============================================================================
# process scss files
process_scss_files(directory_source_scss, directory_page_lib_css, directory_temp)


# ==============================================================================
# process javascript files
process_js_files(directory_source_js, directory_page_lib_js, directory_temp)


# ==============================================================================
# finalize directories and files

# copy misc files
copy_misc_files(directory_source_misc, directory_page)

# delete temp directory
#delete_directory(directory_temp)
