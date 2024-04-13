# ==================================================================================================
#
# PyWesB - Python Website Builder
#
#
#        FILE: make.py
#       USAGE: py make.py arguments options
#
# DESCRIPTION: Python script for automatically generating static or dynamic websites with Node.js.
#
#      AUTHOR: Michel Abele
#     LICENSE: GNU General Public License, Version 3
#
# ==================================================================================================


# ==================================================================================================
# import modules, classes and functions

# import standard modules
import argparse

# import custom modules
from system.modules.build import build as build_module
from system.modules.ftp import ftp as ftp_module
from system.modules.init import init as init_module
from system.modules.server import server as server_module

# import functions
from system.functions.python_package_manager import python_package_manager as ppm


# ==================================================================================================
# variables
module_config_file = './system/config/modules.json'
page_config_file = './system/config/page.json'

# ==================================================================================================
# main program
def main():
    parser = argparse.ArgumentParser(description='PyWesB - Python Website Builder')


    # ==============================================================================================
    # arguments and options

    # module arguments
    parser.add_argument('-B', "--build", action='store_true', help='builds the website')
    parser.add_argument('-F', "--ftp", action='store_true', help='uploads the website to a webserver')
    parser.add_argument('-I', "--init", action='store_true', help='initializes the workbench')
    parser.add_argument('-S', "--server", action='store_true', help='managed a server')

    # globale options
    parser.add_argument('-c', '--clear', action='store_true', help='first deletes the contents of the target directory')
    parser.add_argument('-m', '--minify', action='store_true', help='minimizes the output code')

    # server options
    parser.add_argument('-s', '--start', action='store_true', help='starts a service')
    parser.add_argument('-o', '--stop', action='store_true', help='stops a service')
    parser.add_argument('-r', '--restart', action='store_true', help='restarts a service')
    parser.add_argument('-i', '--install', action='store_true', help='installed a service')
    parser.add_argument('-d', '--delete', action='store_true', help='deletes a service')


    # ==============================================================================================
    # parse arguments
    try:
        args = parser.parse_args()


        # ==============================================================================================
        # modules

        # load build module
        if args.build:
            build_module(module_config_file, page_config_file, args.clear, args.minify)

        # load ftp module
        if args.ftp:
            ftp_module(module_config_file, args.clear, args.minify)

        # load init module
        if args.init:
            ppm(module_config_file)
            init_module(module_config_file)

        # load server module
        if args.server:
            server_module(module_config_file, args.start, args.stop, args.restart, args.init, args.delete)


    # ==============================================================================================
    # error handling
    except argparse.ArgumentError as e:
        parser.error(str(e))


# ==================================================================================================
# main
if __name__ == '__main__':
    main()
