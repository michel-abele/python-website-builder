# ==================================================================================================
#
#          FILE: wb.py
#
#         USAGE: python wb.py argument
#
#   DESCRIPTION: Python script file for the automatic creation of a static website.
#
#        AUTHOR: Michel Abele
#       CREATED: 2024-03-21
#       LICENSE: GNU General Public License, Version 3
#
# ==================================================================================================

import sys

from wb_classes import Module_Loader


# ==================================================================================================
# modules path
modules_path = "./wb_modules"


# ==================================================================================================
# main program
module_loader = Module_Loader(modules_path)

if len(sys.argv) > 1:
    module_names = []

    if "init" in sys.argv or "i" in sys.argv:
        module_names.append("init")

    if "build" in sys.argv or "b" in sys.argv:
        module_names.append("build")
    
    module_loader.load_modules(module_names)
else:
    print("You have not entered an argument!")
    exit(1)
