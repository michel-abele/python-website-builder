import os
import shutil
import re
import json

def process_html_files(sourceDir, targetDir, configFile):
    for root, dirs, files in os.walk(sourceDir):
        for file in files:
            sourcePath = os.path.join(root, file)
            targetPath = os.path.join(targetDir, os.path.relpath(sourcePath, sourceDir))

            shutil.copy2(sourcePath, targetPath)

            with open(targetPath, 'r+') as f:
                content = f.read()
                matches = re.findall(r"<% (.*?) %>", content)
                for match in matches:
                    file_path = "./source/html/parts/" + match.strip() + ".html"
                    with open(file_path, 'r') as file:
                        replacement = file.read()
                        nested_matches = re.findall(r"<% (.*?) %>", replacement)
                        for nested_match in nested_matches:
                            nested_file_path = "./source/html/parts/" + nested_match.strip() + ".html"
                            with open(nested_file_path, 'r') as nested_file:
                                nested_replacement = nested_file.read()
                            replacement = replacement.replace(f"<% {nested_match} %>", nested_replacement)
                        content = content.replace(f"<% {match} %>", replacement)
                f.seek(0)
                f.write(content)
                f.truncate()

            with open(targetPath, 'r+') as f:
                content = f.read()
                with open(configFile, 'r') as config_file:
                    try:
                        config = json.load(config_file)
                        if isinstance(config, dict) and config:
                            for key, value in config.items():
                                content = content.replace(f"<$ {key} $>", value)
                            f.seek(0)
                            f.write(content)
                            f.truncate()
                    except (json.JSONDecodeError, FileNotFoundError):
                        pass