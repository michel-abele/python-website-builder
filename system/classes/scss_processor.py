# ==================================================================================================
# SCSS Processor
#
# This class processes SCSS files and compiles them to CSS.
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import os
import json
import re

# import third-party modules
import sass
from tqdm import tqdm as progress_bar


# ==================================================================================================
# SCSS Processor
class SCSS_Processor:


    # ==============================================================================================
    # static method

    # process
    @staticmethod
    def process(source_directory_scss, target_directory, library_directory_img, partials_directory_scss, partials_file_modification_time, temp_file_images, temp_file_fonts, library_directory_fonts, option_minify):

        # progress bar settings
        progress_bar_format = "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
        progress_bar_ncols  = 75
        progress_bar_ascii  = False
        progress_bar_colour = 'blue'

        # process SCSS files
        for root, dirs, files in os.walk(source_directory_scss):
            for file in progress_bar(files, desc="Processing S/CSS files", unit="file", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):

                # check if file is a SCSS file
                if file.endswith(".scss"):
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(target_directory, os.path.relpath(source_file, source_directory_scss)).replace(".scss", ".css")
                    
                    # check if the partial files is newer than the main SCSS file
                    with open(partials_file_modification_time, "r") as f:
                        modification_times = json.load(f)
                    if os.path.getmtime(source_file) < modification_times["scss"]:
                        os.utime(source_file, (modification_times["scss"], modification_times["scss"]))
                    
                    # check if the target file exists and is newer than the source file
                    if os.path.exists(target_file):
                        if os.path.getmtime(source_file) <= os.path.getmtime(target_file):
                            continue
                    
                    # open the SCSS file to read the content
                    with open(source_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    if content:

                        # process @import statements
                        content = SCSS_Processor._process_imports(content, partials_directory_scss)

                        # process image references in CSS
                        content = SCSS_Processor._process_image_references_css(content, temp_file_images, library_directory_img)

                        # process font references in CSS
                        content = SCSS_Processor._process_font_references_css(content, temp_file_fonts, library_directory_fonts)

                        # compile SCSS to CSS
                        css_content = sass.compile(string=content)

                        # minify CSS if option is set
                        if option_minify:
                            css_content = SCSS_Processor._minify_css(css_content)

                    else:
                        css_content = content

                    # create target directory if it doesn't exist
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)
                    
                    # write CSS content to target file
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(css_content)
                    
                    # set modification time of target file to match source file
                    os.utime(target_file, (os.path.getatime(source_file), os.path.getmtime(source_file)))


    # ==============================================================================================
    # helper methods

    # process imports
    @staticmethod
    def _process_imports(content, partials_directory_scss):
        import_statements = []
        lines = content.split("\n")
        for line in lines:
            if line.startswith("@import") and "url(" not in line:
                import_statements.append(line)
    
        for statement in import_statements:
            file_path = statement.split("'")[1] if "'" in statement else statement.split('"')[1]
            file_dir, file_name = os.path.split(file_path)
            partial_file = os.path.join(partials_directory_scss, file_dir, "_" + file_name + ".scss")
            with open(partial_file, "r", encoding="utf-8") as f:
                partial_content = f.read()
            partial_content = SCSS_Processor._process_imports(partial_content, partials_directory_scss)
            content = content.replace(statement, partial_content)
    
        return content
    
    # minify CSS
    @staticmethod
    def _minify_css(css_content):
        return sass.compile(string=css_content, output_style="compressed")

    # process image references in CSS
    @staticmethod
    def _process_image_references_css(content, temp_file_images, library_directory_img):
        def process_url_references(match):
            img_path = match.group(1)
            if not any(img_path.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp")):
                return match.group(0)
            relative_path = os.path.relpath(img_path, os.path.dirname(library_directory_img))
            new_url = f'url("{relative_path}")'
            with open(temp_file_images, "r") as f:
                image_paths = json.load(f)
            if img_path not in image_paths:
                image_paths.append(img_path)
                with open(temp_file_images, "w") as f:
                    json.dump(image_paths, f)
            return new_url
        
        content = re.sub(r'url\("?(.+?)"?\)', process_url_references, content)
        return content

    # process font references in CSS
    @staticmethod
    def _process_font_references_css(content, temp_file_fonts, library_directory_fonts):
        def process_url_references(match):
            font_name = match.group(1)
            font_values = match.group(2)
            font_file = f"{font_name}.css"
            relative_path = os.path.join("css", font_file)
            new_url = f'url("{relative_path}")'
            
            if os.path.exists(temp_file_fonts):
                with open(temp_file_fonts, "r") as f:
                    font_data = json.load(f)
            else:
                font_data = {}
            
            if font_name in font_data:
                existing_values = font_data[font_name]
                new_values = [v.strip() for v in font_values.split(",") if v.strip() not in existing_values]
                font_data[font_name].extend(new_values)
            else:
                font_data[font_name] = [v.strip() for v in font_values.split(",")]
            
            with open(temp_file_fonts, "w") as f:
                json.dump(font_data, f)
            
            return new_url
        
        content = re.sub(r'@import\s+url\("?(.+?)\s+(.+?)"?\)', process_url_references, content)
        return content
