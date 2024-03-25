import os
import re
import json
import shutil

def process_html_files(source_path, target_path, config_file, html_parts_file_modification_file, is_multilingual_website):
    for root, dirs, files in os.walk(source_path + "/content"):
        for file in files:
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_path, os.path.relpath(source_file_path, source_path + "/content"))


            # ======================================================================================
            # handle sitemap JSON files
            if is_multilingual_website:
                first_directory = os.path.basename(os.path.dirname(target_file_path.replace(target_path, "")))
                json_file_path = os.path.join("./temp", "sitemap", f"{first_directory}.json")
            else:
                json_file_path = os.path.join("./temp", "sitemap.json")

            # add the target file path and modification time to the JSON file
            with open(json_file_path, 'r+') as json_file:
                try:
                    sitemap_data = json.load(json_file)
                    if isinstance(sitemap_data, dict):
                        sitemap_data[target_file_path.replace(source_path, "").rsplit(".", 1)[0]] = os.path.getmtime(target_file_path)
                        json_file.seek(0)
                        json.dump(sitemap_data, json_file)
                        json_file.truncate()
                except (json.JSONDecodeError, FileNotFoundError):
                    pass

            # ======================================================================================
            # check for up-to-dateness
            if os.path.exists(target_file_path):
                source_file_modification_time = os.path.getmtime(source_file_path)
                target_file_modification_time = os.path.getmtime(target_file_path)
                if source_file_modification_time == target_file_modification_time:

                    html_files_to_import = []
                    with open(source_file_path, 'r') as f:
                        content = f.read()
                        matches = re.findall(r"<!-- include: (.*?) -->", content)
                        for match in matches:
                            file_path = match.split(".")[0]
                            html_files_to_import.append(file_path)

                    with open(html_parts_file_modification_file, 'r') as json_file:
                        try:
                            modification_times = json.load(json_file)
                            if isinstance(modification_times, dict) and modification_times:
                                for file_path in html_files_to_import:
                                    if file_path in modification_times:
                                        partial_file_modification_time = os.path.getmtime(file_path)
                                        if partial_file_modification_time <= modification_times[file_path]:
                                            continue
                        except (json.JSONDecodeError, FileNotFoundError):
                            pass

            # ======================================================================================
            # copy file an include partials
            shutil.copy2(source_file_path, target_file_path)
            with open(target_file_path, 'r+') as f:
                content = f.read()
                matches = re.findall(r"<!-- include: (.*?) -->", content)
                for match in matches:
                    file_path = source_path + "/parts/" + match.strip() + ".html"
                    with open(file_path, 'r') as file:
                        replacement = file.read()
                        nested_matches = re.findall(r"<!-- include: (.*?) -->", replacement)
                        for nested_match in nested_matches:
                            nested_file_path = source_path + "/parts/" + nested_match.strip() + ".html"
                            with open(nested_file_path, 'r') as nested_file:
                                nested_replacement = nested_file.read()
                            replacement = replacement.replace(f"<!-- include: {nested_match} -->", nested_replacement)
                        content = content.replace(f"<!-- include: {match} -->", replacement)
                f.seek(0)
                f.write(content)
                f.truncate()

            # ======================================================================================
            # replace static values
            with open(target_file_path, 'r+') as f:
                content = f.read()
                with open(config_file, 'r') as config_file:
                    try:
                        config = json.load(config_file)
                        if isinstance(config, dict) and config:
                            for key, value in config.items():
                                content = content.replace(f"<!-- var_static: {key} -->", value)
                            f.seek(0)
                            f.write(content)
                            f.truncate()
                    except (json.JSONDecodeError, FileNotFoundError):
                        pass
