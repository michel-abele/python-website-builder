import json

class Init_Config_Loader:
    def __init__(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            self.directories_to_delete = data['directories_to_delete']
            self.directories_to_create = data['directories_to_create']
            self.files_to_delete = data['files_to_delete']
            self.files_to_create = data['files_to_create']
