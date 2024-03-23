from wb_functions import delete_directory
from wb_functions import create_directory
from wb_functions import compare_and_delete
from wb_functions import process_html_files
from wb_functions import process_scss_files
from wb_functions import process_js_files
from wb_functions import copy_misc_files

import sys

tempDir = "./temp"

create_directory(tempDir)

if "-clear" in sys.argv or "-c" in sys.argv:
    delete_directory("./page")
    create_directory("./page")

libraryDirectories = [
    "./page/lib",
    "./page/lib/css",
    "./page/lib/js",
    "./page/lib/fonts",
    "./page/lib/img",
]

for directory in libraryDirectories:
    create_directory(directory)

if not "-clear" in sys.argv and not "-c" in sys.argv:
    sourceDir  = "./source/html/content"
    targetDir  = "./page"
    excludeDir = "lib"
    compare_and_delete(sourceDir, targetDir, excludeDir)

sourceDir  = "./source/html/content"
targetDir  = "./page"
configFile = "./source/config.json"

process_html_files(sourceDir, targetDir, configFile)

sourceDir = "./source/scss"
targetDir = "./page/lib/css"
tempDir   = "./temp"

process_scss_files(sourceDir, targetDir, tempDir)

sourceDir = "./source/js"
targetDir = "./page/lib/js"
tempDir = "./temp"

process_js_files(sourceDir, targetDir, tempDir)

sourceDir = "./source/misc"
targetDir = "./page"

copy_misc_files(sourceDir, targetDir)

delete_directory(tempDir)
