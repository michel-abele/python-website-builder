# ==================================================================================================
# Init module
#
# This module initializes the workbench by deleting and creating directories and files.
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import json

# import functions
from system.classes.file_system_manager import File_System_Manager as fsm


# ==================================================================================================
# init module
def init(module_config_file):

    # load json file
    with open(module_config_file, 'r') as file:
        config = json.load(file)

    # get data from config file
    directories_to_delete      = config['init']['directories_to_delete']
    directories_to_create      = config['init']['directories_to_create']
    files_to_delete            = config['init']['files_to_delete']
    files_to_create            = config['init']['files_to_create']
    directories_to_copy_source = config['init']['directories_to_copy_source']
    directories_to_copy_target = config['init']['directories_to_copy_target']
    files_to_copy_source       = config['init']['files_to_copy_source']
    files_to_copy_target       = config['init']['files_to_copy_target']

    # delete files
    fsm.delete_files(files_to_delete)

    # delete directories
    fsm.delete_directories(directories_to_delete)

    # create directories
    fsm.create_directories(directories_to_create)

    # create files
    fsm.create_files(files_to_create)

    # copy directories
    fsm.copy_directories(directories_to_copy_source, directories_to_copy_target)

    # copy files
    fsm.copy_files(files_to_copy_source, files_to_copy_target)
