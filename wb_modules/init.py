from wb_functions import delete_directory
from wb_functions import delete_file
from wb_functions import create_directory
from wb_functions import create_file

directoriesToDelete = [
    "./.git",
    "./.vscode"
]

directoriesToCreate = [
    "./page",
    "./source",
    "./source/scss",
    "./source/js",
    "./source/html",
    "./source/html/content",
    "./source/html/parts",
    "./source/fonts",
    "./source/img",
    "./source/misc"
]

filesToDelete = [
    "./.gitignore",
    "./LICENSE",
    "./README.md"
]

filesToCreate = [
    "./source/config.json",
    "./source/scss/framework.scss",
    "./source/scss/main.scss",
    "./source/js/framework.js",
    "./source/js/main.js",
    "./source/html/content/index.html",
    "./source/misc/.htaccess",
    "./source/misc/robots.txt",
    "./source/misc/sitemap.xml"
]

for directory in directoriesToDelete:
    delete_directory(directory)

for file in filesToDelete:
    delete_file(file)

for directory in directoriesToCreate:
    create_directory(directory)

for file in filesToCreate:
    create_file(file)
