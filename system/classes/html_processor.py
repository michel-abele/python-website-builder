# ==================================================================================================
# HTML Processor
#
# This class processes HTML files.
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import os
import json
import re

from datetime import datetime

# import third-party modules
from tqdm import tqdm as progress_bar


# ==================================================================================================
# HTML Processor
class HTML_Processor:


    # ==============================================================================================
    # static method

    # process
    @staticmethod
    def process(source_directory_html, target_directory, partials_directory_html, partials_file_modification_time, is_multilingual_website, page_config, temp_file_images, web_path_img, option_minify, temp_directory_sitemaps):

        # progress bar settings
        progress_bar_format = "{desc}: {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}"
        progress_bar_ncols  = 75
        progress_bar_ascii  = False
        progress_bar_colour = 'blue'
        
        # process HTML files
        for root, dirs, files in os.walk(source_directory_html):
            for file in progress_bar(files, desc="Processing HTML files", unit="file", ascii=progress_bar_ascii, ncols=progress_bar_ncols, colour=progress_bar_colour, bar_format=progress_bar_format):
                
                # check if the file is an HTML file
                if file.endswith(".html") or file.endswith(".htm"):
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(target_directory, os.path.relpath(source_file, source_directory_html))

                    # check if the partial files is newer than the main HTML file
                    with open(partials_file_modification_time, "r") as f:
                        modification_times = json.load(f)
                    if os.path.getmtime(source_file) < modification_times["html"]:
                        os.utime(source_file, (modification_times["html"], modification_times["html"]))

                    # check if the target file exists and is newer than the source file
                    if os.path.exists(target_file):
                        if os.path.getmtime(source_file) <= os.path.getmtime(target_file):
                            continue

                    # open the HTML file to read the content
                    with open(source_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # replace include variables with the content of the partial files
                    content = HTML_Processor._replace_partials(content, partials_directory_html)

                    # replace language variable with the language code
                    content = HTML_Processor._replace_language_variable(content, is_multilingual_website, source_directory_html, page_config, source_file)

                    # replace file modification time variable with the modification time of the source file
                    content = HTML_Processor._replace_file_modification_time_variable(content, os.path.getmtime(source_file))

                    # replace custom variables with the values from the page config file
                    content = HTML_Processor._replace_custom_variables(content, page_config)

                    # add missing id attributes to headings
                    content = HTML_Processor._add_heading_ids(content)

                    # create table of contents
                    content = HTML_Processor._create_table_of_contents(content)

                    # remove remaining variables
                    content = HTML_Processor._remove_remaining_variables(content)

                    # process image references
                    content = HTML_Processor._process_image_references(content, temp_file_images, web_path_img)

                    # minify HTML code if option is set
                    if option_minify:
                        content = HTML_Processor._minify_html(content)

                    # create the target directory if it does not exist
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)

                    # write the content to the target file
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(content)

                    # set the modification time of the target file to the modification time of the source file
                    os.utime(target_file, (os.path.getmtime(source_file), os.path.getmtime(source_file)))

                    # save file data for sitemap
                    HTML_Processor._save_sitemap_data(source_file, target_file, is_multilingual_website, source_directory_html, target_directory, temp_directory_sitemaps)


    # ==============================================================================================
    # helper methods

    # replace include variables with the content of the partial files
    @staticmethod
    def _replace_partials(content, partials_directory_html):
        def replace(match):
            partial_file = os.path.join(partials_directory_html, match.group(1).replace(".", "/") + ".html")
            with open(partial_file, "r", encoding="utf-8") as f:
                partial_content = f.read()
            return HTML_Processor._replace_partials(partial_content, partials_directory_html)

        return re.sub(r"<!--\s*(?:inc|include):\s*(.+?)\s*-->", replace, content)

    # replace language variable with the language code
    @staticmethod
    def _replace_language_variable(content, is_multilingual_website, source_directory_html, page_config, source_file):
        if is_multilingual_website:
            language = os.path.relpath(os.path.dirname(source_file), source_directory_html).split(os.path.sep)[0]
        else:
            with open(page_config, "r") as f:
                config = json.load(f)
            language = config["language"]
        return re.sub(r"@\s*LANG\s*@", language, content)

    # replace file modification time variable with the modification time of the source file
    @staticmethod
    def _replace_file_modification_time_variable(content, modification_time):
        formatted_time = datetime.fromtimestamp(modification_time).strftime("%Y-%m-%d %H:%M")
        return re.sub(r"@\s*FMT\s*@", formatted_time, content)

    # replace custom variables with the values from the page config file
    @staticmethod
    def _replace_custom_variables(content, page_config):
        with open(page_config, "r") as f:
            config = json.load(f)

        def replace(match):
            variable_name = match.group(1)
            return config.get(variable_name, "")

        return re.sub(r"@\s*(.+?)\s*@", replace, content)

    # add missing id attributes to headings
    @staticmethod
    def _add_heading_ids(content):
        def replace(match):
            heading_text = match.group(2)
            heading_id = re.sub(r"[^\w\-]+", "-", heading_text.lower())
            return f'<{match.group(1)} id="{heading_id}">{heading_text}</{match.group(1)}>'

        return re.sub(r"<(h[2-4])>(.+?)</\1>", replace, content)

    # create table of contents
    @staticmethod
    def _create_table_of_contents(content):
        toc = ""
        current_level = 2

        def replace(match):
            nonlocal toc, current_level
            heading_level = int(match.group(1)[-1])
            heading_text = match.group(2)
            heading_id = re.sub(r"[^\w\-]+", "-", heading_text.lower())

            if heading_level > current_level:
                toc += "<ol>"
            elif heading_level < current_level:
                toc += "</ol>" * (current_level - heading_level)

            current_level = heading_level

            toc += f'<li><a href="#{heading_id}">{heading_text}</a></li>'

            return match.group(0)

        content = re.sub(r"<(h[2-4])>(.+?)</\1>", replace, content)

        while current_level > 2:
            toc += "</ol>"
            current_level -= 1

        return re.sub(r"<!--\s*TOC\s*-->", toc, content)

    # remove remaining variables
    @staticmethod
    def _remove_remaining_variables(content):
        return re.sub(r"@\s*.+?\s*@", "", content)

    # minify HTML code
    @staticmethod
    def _minify_html(content):
        content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
        content = re.sub(r"^\s+", "", content, flags=re.MULTILINE)
        content = re.sub(r"\s+$", "", content, flags=re.MULTILINE)
        content = re.sub(r">\s+<", "><", content)
        content = re.sub(r">\s+([^\s<])", r">\1", content)
        content = re.sub(r"([^\s>])\s+<", r"\1<", content)
        content = re.sub(r"\n\s*\n", "\n", content)
        return content

    # process image references
    @staticmethod
    def _process_image_references(content, temp_file_images, web_path_img):

        if not os.path.exists(temp_file_images):
            with open(temp_file_images, "w") as f:
                json.dump([], f)
        
        # process src attributes
        def process_src_attributes(match):
            img_path = match.group(1)
            img_width = match.group(2)
            if not any(img_path.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp")):
                return match.group(0)
            img_name, img_ext = os.path.splitext(img_path)
            if img_width:
                new_src = f'{web_path_img}/{img_name}_{img_width}{img_ext}'
                data_fisrc = f'{web_path_img}/{img_path}'
                img_tag = f'<img src="{new_src}" data-fisrc="{data_fisrc}">'
            else:
                new_src = f'{web_path_img}/{img_path}'
                img_tag = f'<img src="{new_src}">'
            with open(temp_file_images, "r") as f:
                image_paths = json.load(f)
            if img_path not in image_paths:
                image_paths.append(img_path)
                with open(temp_file_images, "w") as f:
                    json.dump(image_paths, f)
            return img_tag
        
        # process srcset attributes
        def process_srcset_attributes(match):
            srcset = match.group(1)
            img_paths = re.findall(r'(.+?)(?:\s+(\d+w))?', srcset)
            new_srcset = []
            for img_path, img_width in img_paths:
                if not any(img_path.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".webp")):
                    new_srcset.append(f'{img_path}' if not img_width else f'{img_path} {img_width}')
                    continue
                img_name, img_ext = os.path.splitext(img_path)
                if img_width:
                    new_src = f'{web_path_img}/{img_name}_{img_width}{img_ext}'
                    new_srcset.append(f'{new_src} {img_width}')
                else:
                    new_src = f'{web_path_img}/{img_path}'
                    new_srcset.append(new_src)
                with open(temp_file_images, "r") as f:
                    image_paths = json.load(f)
                if img_path not in image_paths:
                    image_paths.append(img_path)
                    with open(temp_file_images, "w") as f:
                        json.dump(image_paths, f)
            return f'<img srcset="{", ".join(new_srcset)}">'

        content = re.sub(r'<img src="(.+?)(?:\s+(\d+w))?>', process_src_attributes, content)
        content = re.sub(r'<(?:img|source) srcset="(.+?)">', process_srcset_attributes, content)
        return content
    
    # save file data for sitemap
    @staticmethod
    def _save_sitemap_data(source_file, target_file, is_multilingual_website, source_directory_html, target_directory, temp_directory_sitemaps):
        os.makedirs(temp_directory_sitemaps, exist_ok=True)

        if is_multilingual_website:
            language_code = os.path.relpath(os.path.dirname(source_file), source_directory_html).split(os.path.sep)[0]
            json_filename = f"{language_code}.json"

            if language_code == ".":
                json_filename = "global.json"
        else:
            json_filename = "global.json"

        json_file = os.path.join(temp_directory_sitemaps, json_filename)
        relative_file_path = os.path.relpath(target_file, target_directory)
        modification_time = int(os.path.getmtime(target_file))

        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                data = json.load(f)
        else:
            data = {}

        data[relative_file_path] = modification_time

        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)
