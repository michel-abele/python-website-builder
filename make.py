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
from system.modules.build import Build as build_module
from system.modules.ftp import Ftp as ftp_module
from system.modules.init import Init as init_module
from system.modules.server import Server as server_module

# import functions
from system.functions.python_package_manager import python_package_manager as ppm


# ==================================================================================================
# variables
module_config_file = './system/config/modules.json'
page_config_file = './system/config/pages.json'

# ==================================================================================================
# main program
def main():
    parser = argparse.ArgumentParser(description='PyWesB - Python Website Builder')


    # ==============================================================================================
    # arguments and options

    # module arguments
    parser.add_argument('module_long', choices=['build', 'ftp', 'init', 'server'], help='long argument for module')
    parser.add_argument('module_short', choices=['b', 'f', 'i', 's'], help='short argument for module')

    # globale options
    parser.add_argument('-c', '--clear', action='store_true', help='first deletes the contents of the target directory')
    parser.add_argument('-m', '--minify', action='store_true', help='minimizes the output code')


    # server options
    parser.add_argument('-s', '--start', action='store_true', help='starts a service')
    parser.add_argument('-S', '--stop', action='store_true', help='stops a service')
    parser.add_argument('-r', '--restart', action='store_true', help='restarts a service')
    parser.add_argument('-i', '--init', action='store_true', help='initializes a service')
    parser.add_argument('-d', '--delete', action='store_true', help='deletes a service')


    # ==============================================================================================
    # parse arguments
    try:
        args = parser.parse_args()


        # ==============================================================================================
        # modules

        # load build module
        if args.module_long == 'build' or args.module_short == 'b':
            build_module(module_config_file, page_config_file, args.clear, args.minify)

        # load ftp module
        if args.module_long == 'ftp' or args.module_short == 'f':
            ftp_module(module_config_file, args.clear, args.minify)

        # load init module
        if args.module_long == 'init' or args.module_short == 'i':
            ppm(module_config_file)
            init_module(module_config_file)

        # load server module
        if args.module_long == 'server' or args.module_short == 's':
            server_module(module_config_file, args.start, args.stop, args.restart, args.init, args.delete)


    # ==============================================================================================
    # error handling
    except argparse.ArgumentError as e:
        parser.error(str(e))


# ==================================================================================================
# main
if __name__ == '__main__':
    main()
