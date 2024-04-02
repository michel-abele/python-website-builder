import os
import shutil
import sys
import re

class JS_Processor:
    def __init__(self, source_dir, target_dir, temp_dir):
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.temp_dir = temp_dir
        self.pattern = "// import:"

    # ==============================================================================================
    # process javascript files
    def process_js_files(self):
        os.makedirs(self.target_dir, exist_ok=True)
        for filename in os.listdir(self.source_dir):
            source_path = os.path.join(self.source_dir, filename)
            temp_path = os.path.join(self.temp_dir, filename)
            if os.path.getsize(source_path) == 0:
                continue
            with open(source_path, "r") as file:
                content = file.read()
                if self.pattern in content:
                    os.makedirs(self.temp_dir, exist_ok=True)
                    shutil.copy(source_path, temp_path)
                    modified_content = self._process_imports(content)
                    if "-mini" in sys.argv or "-m" in sys.argv:
                        modified_content = self._minify_content(modified_content)
                    with open(temp_path, "w") as file:
                        file.write(modified_content)
                    shutil.copy(temp_path, self.target_dir)
                else:
                    shutil.copy(source_path, self.target_dir)

    # ==============================================================================================
    # helper methods
                    
    # process imports
    def _process_imports(self, content):
        lines = content.split("\n")
        modified_content = []
        for line in lines:
            if line.startswith(self.pattern):
                imported_file = line.split(" ")[2].strip()
                imported_file_path = os.path.join(self.source_dir, imported_file + ".js")
                with open(imported_file_path, "r") as imported_file:
                    imported_content = imported_file.read()
                    modified_content.append(imported_content)
            else:
                modified_content.append(line)
        return "\n".join(modified_content)

    # minify content
    def _minify_content(self, content):
        content = re.sub(r'\/\/.*|\/\*[\s\S]*?\*\/', '', content)
        content = re.sub(r'\s+', ' ', content)
        return content.strip()
