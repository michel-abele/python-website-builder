# ==================================================================================================
# Build module
#
#
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import json
import os

# import classes
from system.classes.directory_comparator import Directory_Comparator as dc
from system.classes.file_system_manager import File_System_Manager as fsm


# ==================================================================================================
# build module
def build(module_config_file, page_config_file, option_clear, option_minify):
    

    # ==============================================================================================
    # load config files

    # load module json file
    with open(module_config_file, 'r') as file:
        module_config = json.load(file)

    # load page json file
    with open(page_config_file, 'r') as file:
        page_config = json.load(file)

    # get data from module config file
    target_directory = module_config['build']['target_directory']
    temp_directory = module_config['build']['temp_directory']
    create_library_directories = module_config['build']['create_library_directories']
    library_directory = module_config['build']['library_directory']
    library_directory_css = module_config['build']['library_directory_css']
    library_directory_js = module_config['build']['library_directory_js']
    source_directory_html = module_config['build']['source_directory_html']
    source_directory_js = module_config['build']['source_directory_js']
    source_directory_scss = module_config['build']['source_directory_scss']

    # get data from page config file
    var456 = page_config['var456']


    # ==============================================================================================
    # preparation

    # if target directory is not empty
    if os.listdir(target_directory):

        # clear directories
        if option_clear:
            fsm.delete_directories(target_directory)
            fsm.delete_directories(temp_directory)
            fsm.create_directories(target_directory)

        # synchronize target directories
        else:
            dc.compare_directories(source_directory_html, target_directory, 'html', library_directory)
            dc.compare_directories(source_directory_js, library_directory_js, 'js')
            dc.compare_directories(source_directory_scss, library_directory_css, 'css')

    # if target directory is empty
    else:
        fsm.create_directories(create_library_directories)

    # create temp directory
    fsm.create_directories(temp_directory)














    # ==============================================================================================
    # finalization

    # delete temp directory
    fsm.delete_directories(temp_directory)
