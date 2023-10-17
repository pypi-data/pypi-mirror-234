# =========================================================================== #
# File    : process_selection.py                                              #
# Author  : Pfesesani V. van Zyl                                              #
# =========================================================================== #

# Standard library imports
# --------------------------------------------------------------------------- #
import os
import sys
from pathlib import Path

# Local imports
# --------------------------------------------------------------------------- #
import common.exceptions as ex
from common.file_handler import FileHandler
from common.messaging import msg_wrapper
from common.fits_file_reader import FitsFileReader
from common.sqlite_db import SQLiteDB
from common.plot_manager import PlotManager
from common.populate_fit_parameters import PopulateFitParameters
# =========================================================================== #

class ProcessSelector:

    """
        The `ProcessSelector` class is responsible for processing drift scan data for 
        reduction and analysis. It provides step-by-step instructions for reducing 
        drift scan files and optimizes memory usage for large datasets. The class is 
        used for both single-file and multi-file processing.

        Parameters:
            - `pathToFile` (str): The absolute path to the file or folder to be processed.
            - `autoKey` (int): An indicator of the chosen processing option (1 for single 
            file, 2 for multiple files in a single folder).
            - `log` (object): The logging object for recording program logs.
            - `processingOption` (int): A value representing the chosen processing option 
            (1 for single file, 2 for multiple files in a folder).
            - `force` (str): A flag indicating whether to force fitting on all data (y/n).
            - `keep` (str): A flag indicating whether to keep the original plots (y/n).
            - `saveLocs` (list): A list of save locations for data.
            - `fitTheoretical` (list): A list of flags for fitting theoretical data.
            - `applyRFIremoval` (list): A list of flags for applying RFI removal.
            - `autoFit` (dict): A dictionary indicating the auto-fit configuration.

        Attributes:
            - `pathToFile` (str): The absolute path to the file or folder being processed.
            - `autoKey` (int): An indicator of the chosen processing option.
            - `log` (object): The logging object.
            - `force` (str): A flag for forcing fitting on all data.
            - `processingOption` (int): The chosen processing option.
            - `keep` (str): A flag for keeping original plots.
            - `saveLocs` (list): A list of save locations for data.
            - `fitTheoretical` (list): A list of flags for fitting theoretical data.
            - `applyRFIremoval` (list): A list of flags for applying RFI removal.
            - `autoFit` (dict): Auto-fit configuration.
            - `db_initiated` (bool): A flag indicating whether the database is initiated.

        Methods:
            - `processFile(filePath="")`: Processes data from a single file.
            - `processFolder()`: Processes data from multiple files in a folder.
            - `process_fitting()`: Sets up data fitting and initiates data processing.
            - `setup_database_dir(tableName="")`: Sets up the database for storing data.

        Usage:
            The `ProcessSelector` class is used to process drift scan data, with options for single-file or multi-file processing. It optimizes memory usage by processing data in smaller chunks, releasing resources, and using efficient data structures.
    """
    

    def __init__(self, pathToFile="",autoKey="",log="", processingOption="",force="n",keep="n",saveLocs=None,fitTheoretical=None,applyRFIremoval=None,autoFit=None):

        self.pathToFile = os.path.realpath(pathToFile)
        self.autoKey = autoKey
        self.log=log

        self.force=force
        self.log=log
        # self.path = os.path.realpath(path)
        self.processingOption=processingOption
        self.keep=keep
        self.saveLocs=saveLocs
        self.fitTheoretical=fitTheoretical
        self.applyRFIremoval=applyRFIremoval
        self.autoFit=autoFit
        self.db_initiated=False

        self.fileHandler = FileHandler(log,pathToFile)
        self.fileHandler.create_folder("plots")
        
        if self.autoKey == 1:
            self.processFile()
        elif self.autoKey == 2:
            self.processFolder()
        else:
            pass

    def processFile(self, filePath=""):

        if filePath=="":
            fileReader = FitsFileReader(self.log, filePath=self.pathToFile)
        else:
            fileReader = FitsFileReader(self.log, filePath)

        # Handle for files without a .fits extension or no data
        if ('.fits' not in fileReader.fileName) or (len(fileReader.hdu)==0):
            return
        
        self.data   = fileReader.data
        self.scans  = fileReader.scans

        #--- Setup database where you will be storing information
        msg_wrapper("debug",self.log.debug,"Setup database")

        # consider using calibrator names to identify cals
        # instead of folder names

        self.db = SQLiteDB(
                self.data["OBJECTTYPE"], self.data["SOURCEDIR"], log=self.log)
        self.db.setup_database()

        # Read the names of all the previously processed files
        # if any exists
        processedFiles = self.db.read_data_from_database("FILENAME")
       
       
        if self.data['FILENAME'] in processedFiles:
            msg_wrapper("info", self.log.info, "File '{}' has already been  processed".format(self.data["FILENAME"]))
        else:
            print("\n"+"*"*60)
            print("# PROCESSING SOURCE: ")
            print("*"*60)
            print("# File name: ", self.data["FILENAME"])
            print("# Object: ", self.data["OBJECT"])
            print("# Object type: ", self.data["OBJECTTYPE"])
            print("# Central Freq: ", self.data["CENTFREQ"])
            print("# Observed : ", self.data["OBSDATE"])
            print("# Storage: ", self.data['SOURCEDIR'])
            print("*"*60)

            msg_wrapper("debug", self.log.debug, "Processing file '{}'".format(
                self.data["FILENAME"]))

            #--- SETUP DATA FITTING AND PLOTTING
            self.process_fitting()
            self.db.close_db()

    def processFolder(self):

        for dirpath, dirs, files in os.walk(self.pathToFile):
            dirp=os.path.basename(dirpath)
            try:
                ind=files.index('.DS_Store')
                files.pop(ind)
            except:
                pass

            if len(files)==0:
                continue
            for srcFile in files:
                    pathToFile=os.path.join(dirpath,srcFile)
                    self.processFile(pathToFile)

    def process_fitting(self):
        """
        Setup data fitting process.
        """

        msg_wrapper("debug", self.log.debug, "Data fitting initiated")
        
        # create the source folder for the plots and current plots
        scanSaveFolder=f'plots/{self.data["OBJECT"].replace(" ","")}/{self.data["SOURCEDIR"]}'
        self.fileHandler.create_folder(scanSaveFolder)
        self.fileHandler.create_folder_overwrite_existing("currentScanPlots")

        # if there is no recorded source data or the frequency is zero, abort fitting
        if str(self.data['CENTFREQ']) == 'nan': # or len(scans)==0
            msg_wrapper("warning", self.log.warning, "no data found, aborting fit")
        else:
            # setup keys to access drift scans, this consists of 
            # the ra and scan distance as well as the actual drift
            # scans
            scan_keys = list(self.scans.keys())
            
            # Begin plotting data, loop through the drift scans
            for i in range (2,len(scan_keys)):
                try:
                    self.plot = PlotManager(self.data, i-2,scan_keys, self.scans["OFFSET"], self.scans[scan_keys[i]], self.log, self.force,self.keep,self.saveLocs,self.fitTheoretical,self.applyRFIremoval,self.autoFit[str(i-2)],scanSaveFolder)    
                except:
                    self.plot = PlotManager(self.data, i-2,scan_keys, self.scans["OFFSET"], self.scans[scan_keys[i]], self.log, self.force,self.keep,self.saveLocs,self.fitTheoretical,self.applyRFIremoval,scanSaveFolder=scanSaveFolder)
                self.plot.process_plot()
         
                # populate the data from the fit into the database
                populateFit = PopulateFitParameters(
                    i-2, self.data, self.plot,self.log)

                if int(self.data['CENTFREQ']) < 4000: # S band: 2000 - 4000 MHz
                    populateFit.calc_wb_parms()
                else:
                    if "D" in self.data['BEAMTYPE']:
                        populateFit.calc_db_parms()
                    else:
                        populateFit.calc_nb_parms()
            del self.plot
            del populateFit
    
        self.db.save_to_database(self.data, self.data["SOURCEDIR"])
 
    def setup_database_dir(self, tableName=""):
        """
        Setup the database that will be used to store our data.
        """

        msg_wrapper("debug", self.log.debug, "create database")

        CAL_NAMES_DIR = "predefs"
        CAL_NAMES_LIST = "cal_names_list.txt"
        CAL_NAMES_LIST_PATH = os.path.join(CAL_NAMES_DIR, CAL_NAMES_LIST)

        try:
            calNamesFile = os.listdir(CAL_NAMES_DIR)
        except FileNotFoundError:
            msg_wrapper("error", self.log.error,
                        f'Directory {CAL_NAMES_DIR} is missing, please contact author to get it')
            sys.exit()

        if len(calNamesFile) == 0:
            msg_wrapper("error", self.log.error,
                        'Calibrator list file is empty.')
            sys.exit()

        elif CAL_NAMES_LIST not in calNamesFile:
            msg_wrapper("error", self.log.error,
                        'Calibrator list file does not exists')
            sys.exit()

        else:

            #Found the file
            filePath = os.path.abspath(CAL_NAMES_LIST_PATH)

            calNames = open(filePath, 'r').read()
            calList = []

            for line in calNames.split("\n"):
                calList.append(line)

            if tableName in calList:
                self.db = SQLiteDB("CAL", tableName, log=self.log)
            else:
                self.db = SQLiteDB("TAR", tableName, log=self.log)
        
        self.db.setup_database()