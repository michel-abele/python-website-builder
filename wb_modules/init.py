from wb_functions import delete_directory
from wb_functions import delete_file
from wb_functions import create_directory
from wb_functions import create_file


# ==============================================================================
# directories

# main directories
directory_source = "./source"
directory_page   = "./page"

# directories to delete
directories_to_delete = [
    "./.git",
    "./.vscode"
]

# directories to create
directories_to_create = [
    directory_page,

    directory_source,
    directory_source + "/scss",
    directory_source + "/js",
    directory_source + "/html",
    directory_source + "/fonts",
    directory_source + "/img",
    directory_source + "/misc",

    directory_source + "/html/content",
    directory_source + "/html/parts"
]


# ==============================================================================
# files

# files to delete
files_to_delete = [
    "./.gitignore",
    "./LICENSE",
    "./README.md"
]

# files to create
files_to_create = [
    directory_source + "/scss/framework.scss",
    directory_source + "/scss/main.scss",
    
    directory_source + "/js/framework.js",
    directory_source + "/js/main.js",
    
    directory_source + "/html/content/index.html",
    
    directory_source + "/misc/.htaccess",
    directory_source + "/misc/robots.txt",
    directory_source + "/misc/sitemap.xml"
]


# ==============================================================================
# start initiation

# delete files
for file in files_to_delete:
    delete_file(file)

# delete directories
for directory in directories_to_delete:
    delete_directory(directory)

# create directories
for directory in directories_to_create:
    create_directory(directory)

# create files
for file in files_to_create:
    create_file(file)
