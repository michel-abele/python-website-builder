import os
import platform

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def delete_directory(directory_path):
    if os.path.exists(directory_path):
        if platform.system() == "Windows":
            os.system(f'rmdir /s /q "{directory_path}"')
        else:
            os.system(f'rm -r "{directory_path}"')

def create_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("This is an example file.")

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

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
    "./source/scss/framework.scss",
    "./source/scss/main.scss",
    "./source/js/framework.js",
    "./source/js/main.js",
    "./source/html/index.html",
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
