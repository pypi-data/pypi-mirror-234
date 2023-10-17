# ============================================================================#
# File: _auto.py                                                     #
# Author: Pfesesani V. van Zyl                                                #
# ============================================================================#

# Standard library imports
# --------------------------------------------------------------------------- #
# The automated part of dran
import os
import sys
from sys import argv
import argparse

# # Local imports
# # --------------------------------------------------------------------------- #
from inits import __version__, logfile
from common.messaging import msg_wrapper, load_prog
from common.misc_funcs import delete_logs
from common.log_conf import configure_logging
from common.process_selection import ProcessSelector
from common.load_prog import LoadProg


def run(args):
    """
        The `run` method handles the automated data processing within the DRAN-AUTO program. 
        It is responsible for processing the data based on the provided command-line arguments. 
        This method performs the following tasks:

        1. Initializes and configures logging for the program.
        2. Determines if a file or folder has been specified for processing based on the `-f` command-line argument.
        3. Processes the specified data:
            - If a file is specified, it invokes the `process_file` method to handle data from a single file.
            - If a folder is specified, it invokes the `process_folder` method to handle data from multiple 
            files in the folder.
        4. Provides error messages and exits the program if the provided path is not a valid file or folder.

        Parameters:
        - `args` (argparse.Namespace): A namespace containing parsed command-line arguments that control 
        the program's behavior.

        Returns:
        - None

        Usage:
        The `run` method is typically called from the `main` function and is responsible for executing the 
        automated data processing based on user-configured command-line arguments.
     """

    # initiate and configure logging
    delete_logs() # delete any previously generated logfiles

    log = configure_logging()

    load_prog("Automated processing")
    LoadProg(args,log)

    if args.f:
        # Process the data from the specified file or folder
        readFile = os.path.isfile(args.f)
        readFolder = os.path.isdir(args.f)

        if readFile:
            process_file(args.f, log)
        elif readFolder and args.f != "../":
            process_folder(args.f,log)
        else:
            print(f"{args.f} is neither an acceptable file nor folder, please refer to the documentation and try again\n")
            sys.exit()
    else:
        print("\nNo arguments added, closing program\n")

def process_file(file_path,log):
    # Process the data from a file, use generators or iterators as needed.
    msg_wrapper("info",log.info,f"Attempting to process file {file_path}")
    ProcessSelector(file_path, autoKey=1,log=log)

def process_folder(folder_path,log):
    # Process data from files in a folder, use generators or iterators as needed.
    msg_wrapper("info",log.info,f"Attempting to process file {folder_path}")
    ProcessSelector(folder_path, autoKey=2,log=log)

def main():
    """
        The `main` function is the entry point for the DRAN-AUTO program, which facilitates the automated processing of 
        HartRAO drift scan data. It parses command-line arguments using the `argparse` module to provide control and 
        configuration options for the program. The function initializes and configures the program based on the provided arguments.

        Attributes:
            None

        Methods:
            run(args): Responsible for handling the automated data processing based on the provided command-line 
            arguments. It sets up logging, processes specified files or folders, and invokes the appropriate 
            functions for data processing.

            process_file(file_path): Processes data from a specified file. Use generators or iterators as needed to 
            optimize memory usage when dealing with large files.

            process_folder(folder_path): Processes data from files in a specified folder. Utilize memory-efficient 
            data structures and iterators when processing data from multiple files.

            main(): The main entry point for the DRAN-AUTO program. Parses command-line arguments, defines available 
            options, and executes the appropriate function based on the provided arguments.

        Usage:
            Call the `main` function to run the DRAN-AUTO program, specifying command-line arguments to configure and 
            control the automated data processing.
            e.g. _auto.py -h
    """

    parser = argparse.ArgumentParser(prog='DRAN-AUTO', description="Begin processing HartRAO drift scan data")
    parser.add_argument("-db", help="Turn debugging on or off, e.g., -db on (default is off)", type=str, required=False)
    parser.add_argument("-f", help="Process a file or folder at the given path, e.g., -f data/HydraA_13NB/2019d133_16h12m15s_Cont_mike_HYDRA_A.fits or -f data/HydraA_13NB", type=str, required=False)
    parser.add_argument("-delete_db", help="Delete the database on program run, e.g., -delete_db all or -delete_db CALDB.db", type=str, required=False)
    parser.add_argument("-conv", help="Convert database tables to CSV, e.g., -conv CALDB", type=str, required=False)
    parser.add_argument("-quickview", help="Get a quick view of data, e.g., -quickview y", type=str.lower, required=False, choices=['y', 'yes'])
    parser.add_argument('-version', action='version', version='%(prog)s ' + f'{__version__}')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()