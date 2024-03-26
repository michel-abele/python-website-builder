import os
import json
import datetime

def create_sitemap(is_multilingual_website, config_file, directory_page):

    # Read config file
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    
    # ==============================================================================================
    # multilingual sitemap
    if is_multilingual_website:
        sitemap_dir = './temp/sitemap'
        sitemap_files = os.listdir(sitemap_dir)
        sitemap_index = []

        # Convert JSON files to Google XML Sitemap
        for file in sitemap_files:
            if file.endswith('.json'):
                file_path = os.path.join(sitemap_dir, file)
                with open(file_path, 'r') as f:
                    sitemap_data = json.load(f)
                
                domain = config_data['webserver_tld']
                entries = sitemap_data.items()
                num_entries = len(entries)
                max_entries_per_file = 50000
                num_files = num_entries // max_entries_per_file + 1

                for i in range(num_files):
                    sitemap_xml = f'{file[:-5]}-{i}.xml' if i > 0 else f'{file[:-5]}.xml'
                    sitemap_path = os.path.join(directory_page, 'lib', 'sitemap', sitemap_xml)
                    sitemap_index.append(sitemap_xml)

                    with open(sitemap_path, 'w') as f:
                        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
                        for url, lastmod in entries[i * max_entries_per_file: (i + 1) * max_entries_per_file]:
                            url = domain + "/" + url.rstrip('/index')
                            lastmod = str(float(lastmod))  # Convert lastmod to a float and then to a string
                            lastmod = datetime.datetime.fromtimestamp(float(lastmod)).strftime("%Y-%m-%d")  # Convert Unix timestamp to datetime and format as string
                            f.write('\t<url>\n')
                            f.write(f'\t\t<loc>{url}</loc>\n')
                            f.write(f'\t\t<lastmod>{lastmod}</lastmod>\n')
                            f.write('\t</url>\n')
                        f.write('</urlset>')

        # Convert global JSON file to Google XML Sitemap
        global_sitemap_path = os.path.join('./temp/sitemap.json')

        # Convert global JSON file to Google XML Sitemap
        with open(global_sitemap_path, 'r') as f:
            sitemap_data = json.load(f)
        
        domain = config_data['webserver_tld']
        entries = sitemap_data.items()
        num_entries = len(entries)
        max_entries_per_file = 50000
        num_files = num_entries // max_entries_per_file + 1

        for i in range(num_files):
            sitemap_xml = f'sitemap-{i}.xml' if i > 0 else 'sitemap.xml'
            sitemap_path = os.path.join(directory_page, 'lib', 'sitemap', sitemap_xml)
            os.makedirs(os.path.dirname(sitemap_path), exist_ok=True)
            sitemap_index.append(sitemap_xml)

            with open(sitemap_path, 'w') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
                entries_list = list(entries)  # Convert entries to a list
                for url, lastmod in entries_list[i * max_entries_per_file: (i + 1) * max_entries_per_file]:
                    url = domain + "/" + url.rstrip('/index')
                    lastmod = str(float(lastmod))  # Convert lastmod to a float and then to a string
                    lastmod = datetime.datetime.fromtimestamp(float(lastmod)).strftime("%Y-%m-%d")  # Convert Unix timestamp to datetime and format as string
                    f.write('\t<url>\n')
                    f.write(f'\t\t<loc>{url}</loc>\n')
                    f.write(f'\t\t<lastmod>{lastmod}</lastmod>\n')
                    f.write('\t</url>\n')
                f.write('</urlset>')

    # ==============================================================================================
    # single language sitemap
    else:

        # Convert global JSON file to Google XML Sitemap
        global_sitemap_path = os.path.join('./temp/sitemap.json')

        # Convert global JSON file to Google XML Sitemap
        with open(global_sitemap_path, 'r') as f:
            sitemap_data = json.load(f)
        
        domain = config_data['webserver_tld']
        entries = sitemap_data.items()
        num_entries = len(entries)
        max_entries_per_file = 50000
        num_files = num_entries // max_entries_per_file + 1

        for i in range(num_files):
            sitemap_xml = f'sitemap-{i}.xml' if i > 0 else 'sitemap.xml'
            sitemap_path = os.path.join(directory_page, 'lib', 'sitemap', sitemap_xml)
            sitemap_index.append(sitemap_xml)

            with open(sitemap_path, 'w') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
                for url, lastmod in entries[i * max_entries_per_file: (i + 1) * max_entries_per_file]:
                    url = domain + "/" + url.rstrip('/index')
                    lastmod = str(float(lastmod))  # Convert lastmod to a float and then to a string
                    lastmod = datetime.datetime.fromtimestamp(float(lastmod)).strftime("%Y-%m-%d")  # Convert Unix timestamp to datetime and format as string
                    f.write('\t<url>\n')
                    f.write(f'\t\t<loc>{url}</loc>\n')
                    f.write(f'\t\t<lastmod>{lastmod}</lastmod>\n')
                    f.write('\t</url>\n')
                f.write('</urlset>')

    # ==============================================================================================
    # Create index sitemap file
    domain = config_data['webserver_tld']
    index_sitemap_path = os.path.join(directory_page, 'sitemap.xml')
    sitemap_path = os.path.join(directory_page, 'lib', 'sitemap')
    with open(index_sitemap_path, 'w') as f:
        # Write XML content to index sitemap file
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for sitemap in sitemap_index:
            url = domain + '/' + sitemap
            f.write('\t<sitemap>\n')
            f.write(f'\t\t<loc>{url}</loc>\n')
            f.write('\t</sitemap>\n')
        f.write('</sitemapindex>')
