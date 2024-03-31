import os
import json
import datetime
import re

class Sitemap_Generator:
    def __init__(self, is_multilingual_website, config_file, directory_page):
        self.is_multilingual_website = is_multilingual_website
        self.config_file = config_file
        self.directory_page = directory_page
        self.max_entries_per_file = 50000
        self.sitemap_temp_directory = './temp/sitemap'
        self.sitemap_global_json = './temp/sitemap.json'
        self.sitemap_index = []

    # ==============================================================================================
    # generate sitemap
    def generate_sitemap(self):
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)

        if self.is_multilingual_website:
            self._generate_multilingual_sitemap(config_data)
        else:
            self._generate_single_language_sitemap(config_data)

        self._generate_index_sitemap(config_data)

    # ==============================================================================================
    # helper methods
        
    # generate sitemap for multilingual website
    def _generate_multilingual_sitemap(self, config_data):
        sitemap_dir = self.sitemap_temp_directory
        sitemap_files = os.listdir(sitemap_dir)
        
        for file in sitemap_files:
            if file.endswith('.json'):
                file_path = os.path.join(sitemap_dir, file)
                with open(file_path, 'r') as f:
                    sitemap_data = json.load(f)
                self._generate_xml_sitemap(config_data, sitemap_data, file[:-5])

        global_sitemap_path = os.path.join(self.sitemap_global_json)
        with open(global_sitemap_path, 'r') as f:
            sitemap_data = json.load(f)
        self._generate_xml_sitemap(config_data, sitemap_data, 'sitemap')

    # generate sitemap for single language website
    def _generate_single_language_sitemap(self, config_data):
        global_sitemap_path = os.path.join(self.sitemap_global_json)
        with open(global_sitemap_path, 'r') as f:
            sitemap_data = json.load(f)
        self._generate_xml_sitemap(config_data, sitemap_data, 'sitemap')

    # generate XML sitemap
    def _generate_xml_sitemap(self, config_data, sitemap_data, sitemap_name):
        domain = config_data['webserver_tld']
        entries = list(sitemap_data.items())
        num_entries = len(entries)
        num_files = num_entries // self.max_entries_per_file + 1

        for i in range(num_files):
            sitemap_xml = f'{sitemap_name}-{i}.xml' if i > 0 else f'{sitemap_name}.xml'
            sitemap_dir_ex = os.path.join(self.directory_page, 'lib', 'sitemap')
            os.makedirs(sitemap_dir_ex, exist_ok=True)
            sitemap_path = os.path.join(sitemap_dir_ex, sitemap_xml)
            self.sitemap_index.append(sitemap_xml)

            with open(sitemap_path, 'w') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
                start_index = i * self.max_entries_per_file
                end_index = min((i + 1) * self.max_entries_per_file, num_entries)
                for path, lastmod in entries[start_index:end_index]:
                    path = re.sub(r"index$", "", path)
                    url = domain + "/" + path
                    lastmod = str(float(lastmod))
                    lastmod = datetime.datetime.fromtimestamp(float(lastmod)).strftime("%Y-%m-%d")
                    f.write('\t<url>\n')
                    f.write(f'\t\t<loc>{url}</loc>\n')
                    f.write(f'\t\t<lastmod>{lastmod}</lastmod>\n')
                    f.write('\t</url>\n')
                f.write('</urlset>')

    # generate index sitemap
    def _generate_index_sitemap(self, config_data):
        domain = config_data['webserver_tld']
        index_sitemap_path = os.path.join(self.directory_page, 'sitemap.xml')
        with open(index_sitemap_path, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for sitemap in self.sitemap_index:
                url = domain + '/lib/sitemap/' + sitemap
                f.write('\t<sitemap>\n')
                f.write(f'\t\t<loc>{url}</loc>\n')
                f.write('\t</sitemap>\n')
            f.write('</sitemapindex>')
