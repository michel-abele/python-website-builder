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
from system.classes.directory_comparator           import Directory_Comparator           as dc
from system.classes.file_modification_time_updater import File_Modification_Time_Updater as fmtu
from system.classes.file_system_manager            import File_System_Manager            as fsm
from system.classes.multilingual_webseite_checker  import Multilingual_Webseite_Checker  as mlwc


# ==================================================================================================
# build module
def build(module_config_file, page_config_file, option_clear, option_minify):


    # ==============================================================================================
    # variables
    html_extension = 'html'
    js_extension   = 'js'
    css_extension  = 'css'
    scss_extension = 'scss'


    # ==============================================================================================
    # load config files

    # load module json file
    with open(module_config_file, 'r') as file:
        module_config = json.load(file)

    # load page json file
    with open(page_config_file, 'r') as file:
        page_config = json.load(file)

    # get data from module config file
    target_directory                = module_config['build']['target_directory']
    temp_directory                  = module_config['build']['temp_directory']
    create_library_directories      = module_config['build']['create_library_directories']
    library_directory               = module_config['build']['library']['directory_main']
    library_directory_css           = module_config['build']['library']['directory_css']
    library_directory_js            = module_config['build']['library']['directory_js']
    source_directory_html           = module_config['build']['source']['directory_html']
    source_directory_js             = module_config['build']['source']['directory_js']
    source_directory_scss           = module_config['build']['source']['directory_scss']
    partials_directory_html         = module_config['build']['partials']['directory_html']
    partials_directory_js           = module_config['build']['partials']['directory_js']
    partials_directory_scss         = module_config['build']['partials']['directory_scss']
    partials_file_modification_time = module_config['build']['partials']['file_modification_time']
    iso_639_2_path                  = module_config['build']['iso']['639_2']
    iso_639_3_path                  = module_config['build']['iso']['639_3']
    iso_3166_1_2_path               = module_config['build']['iso']['3166-1_2']
    iso_3166_1_3_path               = module_config['build']['iso']['3166-1_3']

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
            dc.compare_directories(source_directory_html, target_directory, html_extension, html_extension, library_directory)
            dc.compare_directories(source_directory_js, library_directory_js, js_extension, js_extension)
            dc.compare_directories(source_directory_scss, library_directory_css, scss_extension, css_extension)

    # if target directory is empty
    else:
        fsm.create_directories(create_library_directories)

    # create temp directory
    fsm.create_directories(temp_directory)


    # ==============================================================================================
    # HTML processing
    is_multilingual_website = mlwc.is_multilingual(source_directory_html, partials_directory_html, iso_639_2_path, iso_639_3_path, iso_3166_1_2_path, iso_3166_1_3_path)

    fmtu.update_file_modification_times(partials_directory_html, html_extension, temp_directory, partials_file_modification_time)


    # ==============================================================================================
    # S/CSS processing
    fmtu.update_file_modification_times(partials_directory_scss, scss_extension, temp_directory, partials_file_modification_time)


    # ==============================================================================================
    # JavaScript processing
    fmtu.update_file_modification_times(partials_directory_js, js_extension, temp_directory, partials_file_modification_time)


    # ==============================================================================================
    # finalization

    # delete temp directory
    fsm.delete_directories(temp_directory)
