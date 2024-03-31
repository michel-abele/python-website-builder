import json

class Build_Config_Loader:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            self.data = json.load(file)

    # ==============================================================================================
    # get directories
    def get_directory(self, key):
        return self.data['directories'][key]
