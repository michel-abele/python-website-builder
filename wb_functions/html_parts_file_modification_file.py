import os
import json

def html_parts_file_modification_file(parts_directory, json_file_path):

    # ==============================================================================================
    # checks if the JSON file exists
    if not os.path.exists(json_file_path):
        with open(json_file_path, "w") as file:
            json.dump({}, file)

    # ==============================================================================================
    # traverse the parts_directory recursively
    html_parts = {}
    for root, dirs, files in os.walk(parts_directory):
        for file in files:
            if file.endswith(".html"):
                relative_path = os.path.join(root, file)[len(parts_directory):]
                relative_path = os.path.splitext(relative_path)[0]
                modification_date = os.path.getmtime(os.path.join(root, file))
                html_parts[relative_path] = modification_date

    # ==============================================================================================
    # save the html parts directory to the JSON file
    with open(json_file_path, "w") as file:
        json.dump(html_parts, file)
