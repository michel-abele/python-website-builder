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

    # minify css
    def _minify_css(self, css_content):
        minified_css = re.sub(r'\s+', ' ', css_content)
        minified_css = re.sub(r'/\*.*?\*/', '', minified_css, flags=re.DOTALL)
        minified_css = re.sub(r'\s*([{};:,])\s*', r'\1', minified_css)
        return minified_css.strip()
