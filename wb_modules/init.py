from wb_classes import Init_Config_Loader
from wb_classes import File_System_Manager as FSM

from tqdm import tqdm

# tqdm settings
tqdm_format = "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
tqdm_ncols = 75
tqdm_ascii = False
tqdm_colour = 'blue'

# ==============================================================================
# start initiation
config_file = "./wb_database/init_config.json"
icl = Init_Config_Loader(config_file)

# delete files
for file_to_delete in tqdm(icl.files_to_delete, desc="Delete Files      ", ascii=tqdm_ascii, ncols=tqdm_ncols, colour=tqdm_colour, bar_format=tqdm_format):
    FSM.delete_file(file_to_delete)

# delete directories
for directory_to_delete in tqdm(icl.directories_to_delete, desc="Delete Directories", ascii=tqdm_ascii, ncols=tqdm_ncols, colour=tqdm_colour, bar_format=tqdm_format):
    FSM.delete_directory(directory_to_delete)

# create directories
for directory_to_create in tqdm(icl.directories_to_create, desc="Create Directories", ascii=tqdm_ascii, ncols=tqdm_ncols, colour=tqdm_colour, bar_format=tqdm_format):
    FSM.create_directory(directory_to_create)

# create files
for file_to_create in tqdm(icl.files_to_create, desc="Create Files      ", ascii=tqdm_ascii, ncols=tqdm_ncols, colour=tqdm_colour, bar_format=tqdm_format):
    FSM.create_file(file_to_create)
