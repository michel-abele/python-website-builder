from wb_classes import Build_Config_Loader
from wb_classes import File_Comparator
from wb_classes import File_Copier
from wb_classes import File_System_Manager as FSM
from wb_classes import HTML_Parts_Modification_Tracker
from wb_classes import HTML_Processor
from wb_classes import Image_Processor
from wb_classes import JS_Processor
from wb_classes import Multilingual_Website_Checker
from wb_classes import SCSS_Processor
from wb_classes import Sitemap_Generator

import sys

from tqdm import tqdm

# tqdm settings
tqdm_format = "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
tqdm_ncols = 75
tqdm_ascii = False
tqdm_colour = 'green'


# ==================================================================================================
# files

# config files
build_config = "./wb_database/build_config.json"
page_config = "./wb_database/page_config.json"

# temp files
html_parts_modification_file = "./temp/html_parts_file_modifications.json"

# config loader
bcl = Build_Config_Loader(build_config)

# library page directories array
library_page_directories = [
    bcl.get_directory("page_lib"),
    bcl.get_directory("page_lib_css"),
    bcl.get_directory("page_lib_js"),
    bcl.get_directory("page_lib_img"),
    bcl.get_directory("page_lib_fonts"),
]


# ==================================================================================================
# prepare directories and files

# clean page directory
for i in tqdm(range(100), desc="Cleaning Page Directory", ascii=tqdm_ascii, ncols=tqdm_ncols, colour=tqdm_colour, bar_format=tqdm_format):
    if "-clear" in sys.argv or "-c" in sys.argv:
        FSM.delete_directory(bcl.get_directory("page"))
        FSM.delete_directory(bcl.get_directory("temp"))
        FSM.create_directory(bcl.get_directory("page"))

    # create or update page directory
    else:
        file_comparator = File_Comparator(bcl.get_directory("source_html_content"), bcl.get_directory("page"), "lib")
        file_comparator.compare_and_delete()

        for directory in library_page_directories:
            FSM.create_directory(directory)


# ==================================================================================================
# create temp directory
FSM.create_directory(bcl.get_directory("temp"))


# ==================================================================================================
# process html files
for i in tqdm(range(100), desc="Processing HTML Files  ", ascii=tqdm_ascii, ncols=tqdm_ncols, colour=tqdm_colour, bar_format=tqdm_format):
    mod_tracker = HTML_Parts_Modification_Tracker(bcl.get_directory("source_html_parts"), html_parts_modification_file)
    mod_tracker.track_modifications()

    mw_checker = Multilingual_Website_Checker(bcl.get_directory("source_html_content"))
    is_multilingual_website = mw_checker.check_multilingual_website()

    html_processor = HTML_Processor(bcl.get_directory("source_html"), bcl.get_directory("page"), page_config, html_parts_modification_file, is_multilingual_website)
    html_processor.process_html_files()

    sm_generator = Sitemap_Generator(is_multilingual_website, page_config, bcl.get_directory("page"))
    sm_generator.generate_sitemap()


# ==================================================================================================
# process scss files
for i in tqdm(range(100), desc="Processing CSS Files   ", ascii=tqdm_ascii, ncols=tqdm_ncols, colour=tqdm_colour, bar_format=tqdm_format):
    scss_processor = SCSS_Processor(bcl.get_directory("source_scss"), bcl.get_directory("page_lib_css"), bcl.get_directory("temp"))
    scss_processor.process_scss_files()


# ==================================================================================================
# process javascript files
for i in tqdm(range(100), desc="Processing JS Files    ", ascii=tqdm_ascii, ncols=tqdm_ncols, colour=tqdm_colour, bar_format=tqdm_format):
    js_processor = JS_Processor(bcl.get_directory("source_js"), bcl.get_directory("page_lib_js"), bcl.get_directory("temp"))
    js_processor.process_js_files()


# ==================================================================================================
# process images
for i in tqdm(range(100), desc="Processing Images      ", ascii=tqdm_ascii, ncols=tqdm_ncols, colour=tqdm_colour, bar_format=tqdm_format):
    img_processor = Image_Processor(bcl.get_directory("source_img"), bcl.get_directory("page_lib_img"))
    img_processor.process_images()


# ==================================================================================================
# finalize directories and files

# copy misc files
for i in tqdm(range(100), desc="Copying Misc Files     ", ascii=tqdm_ascii, ncols=tqdm_ncols, colour=tqdm_colour, bar_format=tqdm_format):
    file_copier = File_Copier(bcl.get_directory("source_misc"), bcl.get_directory("page"))
    file_copier.copy_files()


# ==================================================================================================
# delete temp directory
FSM.delete_directory(bcl.get_directory("temp"))
