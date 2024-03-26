# ==============================================================================
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
# ==============================================================================

import sys
import os
import tqdm
import importlib.util

modules_path = "./wb_modules"

def import_module(module_name, module_path):
    for i in tqdm.tqdm(range(100), desc="Processing", ascii=False, ncols=75):

        if os.path.exists(module_path):
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except ImportError as e:
                exit(f"Error: {e}")
        else:
            exit(f"Error: The module '{module_name}' does not exist")

if len(sys.argv) > 1:

    if "init" in sys.argv or "i" in sys.argv:
        init_module = os.path.join(modules_path, "init.py")
        import_module("init", init_module)

    if "build" in sys.argv or "b" in sys.argv:
        build_module = os.path.join(modules_path, "build.py")
        import_module("build", build_module)

else:
    exit("You have not entered an argument")
