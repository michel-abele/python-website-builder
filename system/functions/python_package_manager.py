# ==================================================================================================
# Python Package Manager (pip)
#
# This script checks if the required Python packages are installed and installs them if necessary.
# ==================================================================================================


# ==================================================================================================
# import standard modules
import importlib.util
import json
import subprocess
import sys


# ==================================================================================================
# Python Package Manager
def python_package_manager(json_file):

    # load json file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # get required modules
    required_modules = data['init']['python_required_modules']

    # check if required modules are installed
    missing_modules = [module for module in required_modules if importlib.util.find_spec(module) is None]

    # install missing modules
    if missing_modules:
        print("Missing Python packages detected. Installation process will begin.")
        print("=" * 50)
        for i, module in enumerate(missing_modules, start=1):
            print(f"Installing package {i}/{len(missing_modules)}: {module}")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
                print(f"Package {module} installed successfully.")
            except subprocess.CalledProcessError:
                print(f"Failed to install package {module}.")
            print("-" * 50)
        print("=" * 50)
        print("Installation process completed.")
    else:
        print("All required packages are already installed.")
