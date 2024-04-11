# ==================================================================================================
# JavaScript Processor
#
# This class processes JavaScript files.
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import os
import json
import re

# import third-party modules
from tqdm import tqdm as progress_bar
from slimit import minify


# ==================================================================================================
# JavaScript Processor
class JavaScript_Processor:


    # ==============================================================================================
    # static method
    
    # process
    @staticmethod
    def process(source_directory_js, target_directory, partials_directory_js, partials_file_modification_time, option_minify):

        # progress bar settings
        progress_bar_format = "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
        progress_bar_ncols  = 75
        progress_bar_ascii  = False
        progress_bar_colour = 'blue'
        
        # process JavaScript files
        for root, dirs, files in os.walk(source_directory_js):
            for file in progress_bar(files, desc="Processing JavaScript files", unit="file", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):

                # check if file is a JavaScript file
                if file.endswith(".js"):
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(target_directory, os.path.relpath(source_file, source_directory_js))
                   
                    # check if the partial files is newer than the main JavaScript file
                    with open(partials_file_modification_time, "r") as f:
                        modification_times = json.load(f)
                    if os.path.getmtime(source_file) < modification_times["js"]:
                        os.utime(source_file, (modification_times["js"], modification_times["js"]))
                   
                    # check if the target file exists and is newer than the source file
                    if os.path.exists(target_file):
                        if os.path.getmtime(source_file) <= os.path.getmtime(target_file):
                            continue
                   
                    # open the JavaScript file to read the content
                    with open(source_file, "r", encoding="utf-8") as f:
                        content = f.read()
                   
                    # process import statements
                    content = JavaScript_Processor._process_imports(content, partials_directory_js)
                    # minify JavaScript if option is set
                    if option_minify:
                        js_content = JavaScript_Processor._minify_js(js_content)
                   
                    # create target directory if it doesn't exist
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)
                   
                    # write JavaScript content to target file
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(js_content)
                   
                    # set modification time of target file to match source file
                    os.utime(target_file, (os.path.getatime(source_file), os.path.getmtime(source_file)))


    # ==============================================================================================
    # helper methods

    # process imports
    @staticmethod
    def _process_imports(content, partials_directory_js):
        import_statements = re.findall(r'// import (.*)', content)
       
        for statement in import_statements:
            partial_file = os.path.join(partials_directory_js, statement)
            with open(partial_file, "r", encoding="utf-8") as f:
                partial_content = f.read()
            content = content.replace(f'// import {statement}', partial_content)
       
        return content
   
    # minify JavaScript
    @staticmethod
    def _minify_js(js_content):
        return minify(js_content, mangle=True, mangle_toplevel=True)
