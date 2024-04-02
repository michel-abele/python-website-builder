import json
import os
import shutil
import sass
import sys
import re

class SCSS_Processor:
    def __init__(self, source_dir, target_dir, temp_dir):
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.temp_dir = temp_dir

    # ==============================================================================================
    # process scss files
    def process_scss_files(self):
        os.makedirs(self.target_dir, exist_ok=True)
        scss_files = [f for f in os.listdir(self.source_dir) if f.endswith('.scss') and not f.startswith('_')]

        for scss_file in scss_files:
            temp_file = os.path.join(self.temp_dir, scss_file)
            shutil.copyfile(os.path.join(self.source_dir, scss_file), temp_file)

            with open(temp_file, 'r') as file:
                scss_content = file.read()

            if not scss_content.strip():
                continue

            scss_content = self._process_imports(scss_content)
            css_file = os.path.splitext(scss_file)[0] + '.css'
            css_path = os.path.join(self.target_dir, css_file)
            compiled_css = sass.compile(string=scss_content)

            self._extract_image_links(compiled_css)

            if "-mini" in sys.argv or "-m" in sys.argv:
                compiled_css = self._minify_css(compiled_css)

            with open(css_path, 'w') as file:
                file.write(compiled_css)

    # ==============================================================================================
    # helper methods

    # process imports
    def _process_imports(self, scss_content):
        import_pattern = re.compile(r'@import\s*"([^"]+)";')
        import_statements = import_pattern.findall(scss_content)

        for imported_file_pattern in import_statements:
            if not imported_file_pattern.startswith('_'):
                last_slash_index = max(imported_file_pattern.rfind('/'), imported_file_pattern.rfind('\\'))
                if last_slash_index != -1:
                    imported_file = imported_file_pattern[:last_slash_index + 1] + '_' + imported_file_pattern[last_slash_index + 1:]
                else:
                    imported_file = '_' + imported_file_pattern

            if not imported_file.endswith('.scss'):
                imported_file += '.scss'

            imported_file_path = os.path.join(self.source_dir, imported_file)
            with open(imported_file_path, 'r') as file:
                imported_content = file.read()

            scss_content = scss_content.replace(f'@import "{imported_file_pattern}";', imported_content)

        return scss_content

    # extract image links
    def _extract_image_links(self, content):
        image_links = []

        css_links = re.findall(r'url\([\'"](.*?)[\'"]', content)
        css_links = [link.replace("/lib/img/", "") for link in css_links if link.endswith(('.jpg', '.png'))]
        image_links.extend(css_links)

        image_links = list(set(image_links))
        image_links_file = "./temp/image_links.json"
        os.makedirs(os.path.dirname(image_links_file), exist_ok=True)

        try:
            with open(image_links_file, 'r') as f:
                existing_links = json.load(f)
        except FileNotFoundError:
            existing_links = []

        existing_links.extend(image_links)
        existing_links = list(set(existing_links))

        with open(image_links_file, 'w') as f:
            json.dump(existing_links, f)

    # minify css
    def _minify_css(self, css_content):
        minified_css = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
        minified_css = re.sub(r'//.*', '', minified_css)
        minified_css = re.sub(r'\s+', ' ', minified_css)
        minified_css = re.sub(r'\s*([{};:,])\s*', r'\1', minified_css)
        return minified_css.strip()
