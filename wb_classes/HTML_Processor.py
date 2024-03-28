import json
import os
import re
import shutil
import sys

class HTML_Processor:
    def __init__(self, source_path, target_path, config_file_path, html_parts_file_modification_file, is_multilingual_website):
        self.source_path = source_path
        self.target_path = target_path
        self.config_file_path = config_file_path
        self.html_parts_file_modification_file = html_parts_file_modification_file
        self.is_multilingual_website = is_multilingual_website

    def process_html_files(self):
        for root, dirs, files in os.walk(os.path.join(self.source_path, "content")):
            for file in files:
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(self.target_path, os.path.relpath(source_file_path, os.path.join(self.source_path, "content")))


                # ==================================================================================
                # check for up-to-dateness
                if self.is_up_to_date(source_file_path, target_file_path):
                    continue


                # ==================================================================================
                # copy and open file
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                shutil.copy2(source_file_path, target_file_path)


                # ==================================================================================
                # process file
                with open(target_file_path, 'r+') as f:
                    content = f.read()

                    # include partials
                    content = self.include_partials(content)

                    # replace static values
                    content = self.replace_static_values(content)

                    # target file modification time
                    file_modification_time = os.path.getmtime(target_file_path)
                    content = content.replace("<!-- value_dynamic: file_modification_time -->", str(file_modification_time))

                    # generate heading id attributes
                    content = self.generate_heading_ids(content)

                    # generate table of contents
                    content = self.generate_table_of_contents(content)

                    # minify html content
                    if "-mini" in sys.argv or "-m" in sys.argv:
                        content = self.minify_content(content)

                    # write content to target file
                    f.seek(0)
                    f.write(content)
                    f.truncate()

                # ==================================================================================
                # handle sitemap JSON files
                json_file_path = self.get_json_file_path(target_file_path)
                self.update_sitemap_data(json_file_path, target_file_path)


    # ==============================================================================================
    # helper methods

    # get JSON file path
    def get_json_file_path(self, target_file_path):
        if self.is_multilingual_website:
            first_directory = os.path.basename(os.path.dirname(target_file_path.replace(self.target_path, "")))
            if first_directory != "":
                json_file_path = os.path.join("./temp", "sitemap", f"{first_directory}.json")
            else:
                json_file_path = os.path.join("./temp", "sitemap.json")
        else:
            json_file_path = os.path.join("./temp", "sitemap.json")
        return json_file_path

    # update sitemap data
    def update_sitemap_data(self, json_file_path, target_file_path):
        with open(json_file_path, 'r+') as json_file:
            try:
                sitemap_data = json.load(json_file)
                if isinstance(sitemap_data, dict):
                    sitemap_data[target_file_path.replace(self.target_path, "").rsplit(".", 1)[0].lstrip("\\").replace("\\", "/")] = os.path.getmtime(target_file_path)
                    json_file.seek(0)
                    json.dump(sitemap_data, json_file)
                    json_file.truncate()
            except (json.JSONDecodeError, FileNotFoundError):
                pass

    # check if file is up to date
    def is_up_to_date(self, source_file_path, target_file_path):
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
                with open(self.html_parts_file_modification_file, 'r') as json_file:
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
                return True
        return False

    # include partials
    def include_partials(self, content):
        matches = re.findall(r"<!-- include: (.*?) -->", content)
        for match in matches:
            file_path = os.path.join(self.source_path, "parts", match.strip() + ".html")
            with open(file_path, 'r') as file:
                replacement = file.read()
                nested_matches = re.findall(r"<!-- include: (.*?) -->", replacement)
                for nested_match in nested_matches:
                    nested_file_path = os.path.join(self.source_path, "parts", nested_match.strip() + ".html")
                    with open(nested_file_path, 'r') as nested_file:
                        nested_replacement = nested_file.read()
                    replacement = replacement.replace(f"<!-- include: {nested_match} -->", nested_replacement)
                content = content.replace(f"<!-- include: {match} -->", replacement)
        return content

    # replace static values
    def replace_static_values(self, content):
        with open(self.config_file_path, 'r') as config_file:
            try:
                config = json.load(config_file)
                if isinstance(config, dict) and config:
                    for key, value in config.items():
                        content = content.replace(f"<!-- value_static: {key} -->", value)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return content

    # generate heading id attributes
    def generate_heading_ids(self, content):
        main_content = re.search(r'<main>(.*?)</main>', content, re.DOTALL)
        if main_content:
            main_content_text = main_content.group(1)
            headings = re.findall(r'<h([2-4])>(.*?)</h[2-4]>', main_content_text)
            for heading in headings:
                level, text = heading
                id_attr = re.search(r'id="(.*?)"', text)
                if not id_attr:
                    id_value = re.sub(r'[^\w\-\u0080-\uFFFF]', '', text.replace(' ', '-'))
                    text = f'<h{level} id="{id_value}">{text}</h{level}>'
                main_content_text = main_content_text.replace(f'<h{level}>{heading[1]}</h{level}>', text)
            content = content.replace(main_content.group(0), f'<main>{main_content_text}</main>')
        return content

    # generate table of contents
    def generate_table_of_contents(self, content):
        if '<!-- toc -->' in content:
            main_content = re.search(r'<main>(.*?)</main>', content, re.DOTALL)
            if main_content:
                main_content = main_content.group(1)
                headings = re.findall(r'<h([2-4]).*?id="(.*?)".*?>(.*?)</h[2-4]>', main_content)
                if headings:
                    toc = '<div class="toc"><ol>'
                    current_level = 2
                    stack = []
                    for heading in headings:
                        level, id_value, text = heading
                        text = re.sub(r'<.*?>', '', text)
                        level = int(level)
                        while level > current_level:
                            toc += '<ol>'
                            stack.append(current_level)
                            current_level += 1
                        while level < current_level:
                            toc += '</ol></li>'
                            current_level = stack.pop()
                        toc += f'<li><a href="#{id_value}">{text}</a>'
                    while current_level > 2:
                        toc += '</li></ol>'
                        current_level -= 1
                    toc += '</li></ol></div>'
                    toc = toc.replace('</a><li>', '</a></li><li>').replace('</a></ol>', '</a></li></ol>')
                    content = content.replace('<!-- toc -->', toc)
        return content

    # minify html content
    def minify_content(self, content):
        content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
        content = re.sub(r"\s+", " ", content)
        content = re.sub(r"\s*(<.*?>)\s*", r"\1", content)
        content = re.sub(r">\s+<", "><", content)
        content = re.sub(r"\s*=\s*", "=", content)
        content = re.sub(r"\s+([^\s>]+?)=\"([^\"]*)\"", r' \1="\2"', content)
        content = re.sub(r"\n\s*", "", content)
        return content
