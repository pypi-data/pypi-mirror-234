# =========================================================================== #
# File: fits_file_reader.py                                                   #
# Author: Pfesesani V. van Zyl                                                #
# =========================================================================== #

# Standard library imports
# --------------------------------------------------------------------------- #
# import exceptions
import sys,os
from astropy.io import fits as pyfits
import math
import numpy as np
from datetime import datetime
import pandas as pd
# import pkg_resources


# Local imports
# --------------------------------------------------------------------------- #
# sys.path.append("src/")
from pathlib import Path
from common.scan_parameters import ScanParameters
import common.exceptions as ex
from common.file_handler import FileHandler
from common.messaging import msg_wrapper
from common.get_resources import get_cal_list, get_jpl_results,get_calsky_results
# =========================================================================== #

# # handle/ignore python warnings
# import warnings
# def fxn():
#     warnings.warn("deprecated", DeprecationWarning)

class FitsFileReader():
    """ Fits file reader reads a fits file and returns the data. 

        Args:
            log (object): logging object
            filePath (str): path to file
    """

    def __init__(self, log, filePath=""):

        self.log = log
        self.file = FileHandler(log,filePath)
        self.filePath = filePath
        self.fileName = self.file.get_file_name_from_path()
        if not self.fileName.endswith('.fits'):
            return

        # Setup the drift scan parameters and dictionary for storage
        # then read in the data
        self.scan_parameters = ScanParameters()
        self.scans = {} 
        self.hdu = None

        self.read_file()

    def open_file(self):
        """ 
        Open fits file for processing. 
        """

        try:
            self.hdu = pyfits.open(self.filePath)
            msg_wrapper("debug",self.log.debug,'Opening file: ' + self.fileName)
        except OSError as e:
            msg_wrapper("error",self.log.error, f'Caught OSError: {e}')
            self.hdu=[]
            return 
        except FileNotFoundError:
            msg_wrapper("error",self.log.error,
                "The file '{self.filePath}' is missing or does not exists. \n")
            sys.exit()

    def read_file(self):
        """ Read data from the fits file. """

        self.open_file()
        if len(self.hdu)==0:
            return
        
        self.__get_beam_type()
        self.object=self.hdu[0].header["OBJECT"]
        self.srcFolderName=self.object.replace(" ","")

        if "18.0" in self.beam_type:
            self.objectDIR=f"{self.srcFolderName}_1600"
        elif "13.0" in self.beam_type:
            self.objectDIR=f"{self.srcFolderName}_2280"
        elif "06.0D" in self.beam_type:
            self.objectDIR=f"{self.srcFolderName}_4800"
        elif "03.5D" in self.beam_type:
            self.objectDIR=f"{self.srcFolderName}_8400"
        elif "02.5S" in self.beam_type:
            self.objectDIR=f"{self.srcFolderName}_12218"
        elif "01.3S" in self.beam_type:
            self.objectDIR=f"{self.srcFolderName}_22000"
        elif "04.5S" in self.beam_type:
            self.objectDIR=f"{self.srcFolderName}_6700"
        else:
            print(f'setup beamtype for {self.beam_type}')
            sys.exit()

        # print("\n","*"*50,'\n')
        # print('object: ',self.object.upper())
        # print('file path: ',self.filePath)
        # print('file name: ',self.fileName)
        # print('src folder name: ',self.srcFolderName)
        # print('src data folder name: ',self.objectDIR)
        # print("\n","*"*50)
        
        self.__set_source_type()
        self.validate_file()
        
    def validate_file(self):
        """validate that all requirements have been met for a processed file to be valid. """
        # BEGIN POPULATING SCAN PROPERTIES
        # Validate the HDU length of the fits files.
        # Some files in the early observing dates have
        # invalid hdu lengths giving rise to problems
        # processing the data. For this reason the program
        # flags these files and does not process them.

        self.HDU_LEN = len(self.hdu)  # length of header data unit
        # print(self.hdu.info())

        if self.HDU_LEN <= 7:

            # Get calibrator data
            if self.src_type == "CAL":
                # print("SRC: ",self.src_type, ', BEAM: ',self.beam_type )
                
                # get data for dual beam drift scans
                if self.beam_type == "03.5D" or self.beam_type == "06.0D":
                    self.scan_parameters.set_db_cal_dict()

                # get data for single narrow beam scans
                elif self.beam_type == "02.5S" or self.beam_type == "04.5S":

                    # Force jupiter 12.178 GHz data to perform 22 GHz fit
                    if( self.object=="Jupiter_12.178GHz"):#,self.scans)
                        self.scan_parameters.set_jupiter_dict()
                    else:
                        self.scan_parameters.set_nb_cal_dict()

                elif self.beam_type == "01.3S":
                    self.scan_parameters.set_jupiter_dict()

                    # for k,v in self.scan_parameters.parameters.items():
                    #     if "TAPEAK" in k:
                    #         print(k,v)
                    #print('pars: ',self.scan_parameters.parameters)
                    #
                    # sys.exit()

                # get data for single wide beam scans
                # L-band==18cm
                elif self.beam_type == "13.0S" or self.beam_type == "18.0S":
                    self.scan_parameters.set_wb_cal_dict()

                # get data for single wide beam scans
                #elif self.beam_type == "04.5S":
                #    self.scan_parameters.set_nb_cal_dict()

                # # get data for single wide beam scans
                # elif self.beam_type == "18.0S":
                #     self.scan_parameters.set_nb_cal_dict()

                else:
                    print('Freq: ',self.beam_type)
                    msg_wrapper("error",self.log.error,
                        f"The frequency '{self.beam_type}' your trying to process hasn't been modelled yet for calibrators, please log a bug if you want it modeled in.")
                    #sys.exit()
                    pass

            elif self.src_type == "TAR":

                # get data for dual beam drift scans
                if self.beam_type == "03.5D" or self.beam_type == "06.0D":
                    self.scan_parameters.set_db_src_dict()

                # get data for single narrow beam scans
                elif self.beam_type == "02.5S" or self.beam_type == "04.5S":
                    self.scan_parameters.set_nb_src_dict()

                elif self.beam_type == "01.3S":
                    self.scan_parameters.set_nb_22ghz_src_dict()

                # get data for single wide beam scans
                elif self.beam_type == "13.0S" or self.beam_type == "18.0S":
                    self.scan_parameters.set_wb_src_dict()

                else:
                    print('Freq: ',self.beam_type )
                    msg_wrapper("error", self.log.error,
                                "The frequency your trying to process hasn't been modelled yet, please log a bug if you want it modeled in.")
                    sys.exit()

            else:
                msg_wrapper("error",self.log.error,"Invalid source type detected")
                sys.exit()

            # populate drift scan parameters
            self.data = self.scan_parameters.parameters 
            self.data["HDULENGTH"] = self.HDU_LEN
            self.data["OBJECTTYPE"] = self.src_type
            self.data["FILENAME"] = self.fileName
            self.data["SOURCEDIR"] = self.objectDIR
            self.data["BEAMTYPE"] = self.beam_type

        else:
            msg_wrapper("error",self.log.error,"The file being processed has an invalid HDU length: {}.".format(self.HDU_LEN))
            sys.exit()

        self.set_scan_properties()

    def __get_beam_type(self):
        """ Get the beam type of the scan. e.g. 13.0S i.e. 13 cm single beam. """
        self.beam_type = self.hdu[1].header["EXTNAME"]
        
    def __set_source_type(self):
        """
            Get the scan source type. There are two basic types.
            Calibrator (CAL) and target (TAR) sources.
        """

        calNamesDir = "predefs"

        # validate calibration list exists
        cal_names=self.validate_cal_list()#, calNamesList)

        if os.path.splitext(self.fileName)[1] == ".fits":

            for src in cal_names:
                if (self.object in src):
                    # Set source as calibrator
                    msg_wrapper("debug", self.log.debug,
                                "This source is a calibrator")
                    self.src_type = "CAL"
                    break

                else:
                    # Set source as target
                    msg_wrapper("debug", self.log.debug, "This source is a target")
                    self.src_type = "TAR"

    def validate_cal_list(self):
        """ 
            Validate the calibrator list exists. We need it to 
            determine whether a source is a calibrator or target
            object. 

            Args: 
                calNamesDir (str):  Name of the directory containing the calibrator list of sources.
                calNamesList (str): The calibrator list of sources.
        """

        
        try:
            getcalibratorList=get_cal_list()
            calibratorList=list(getcalibratorList['CALS'])
        except ex.FileResourceNotFoundError:
            msg_wrapper("error", self.log.error,
                        "\nFileResourceNotFoundError: The 'cal_names_list.txt' resource is not in the distribution\n")
            sys.exit()

        return calibratorList

    def set_scan_properties(self):
        """ Set all relevant scan properties. """

        msg_wrapper("debug",self.log.debug,'Setting scan properties')
        self.get_cur_date_time()
        self.get_scan_data()
        self.set_chart_header_stats()

        if self.CHH == 0:
            self.xAxis = []
            return
        else:
            self.get_derived_properties()
            self.convert_counts_to_kelvins()

        # close hdu file
        self.hdu.close()
        
    def get_cur_date_time(self):
        """ Get current date and time. """

        msg_wrapper("debug", self.log.debug, 'Setting current date and time')
        cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.data['CURDATETIME'] = cur_time

    def get_scan_data(self):
        """ Get the file header and data units from the fits file. """

        msg_wrapper("debug", self.log.debug, 'Getting scan data')
        self.get_main_HDUs()
        self.get_source_parameters()
        self.get_source_parameters_data()

    def get_main_HDUs(self):
        """ Get the HDU's that are available in all scan types. """

        msg_wrapper("debug", self.log.debug, 'Getting main HDU data')
        self.primary_HDU = self.hdu[0]    # Primary HDU
        self.obs_info_HDU = self.hdu[1]   # Observation information HDU
        self.noise_cal_HDU = self.hdu[2]  # Noise calibrator HDU

    def get_source_parameters(self):
        """Get the parameters recorded for each source. """

        msg_wrapper("debug", self.log.debug, "Getting source parameters")
        
        if self.HDU_LEN == 7 or self.HDU_LEN == 6:

            # Get drift scans
            # NORTH_SCAN for all other drift scan unmodified data above 2280 MHz
            self.hpnScanHDU = self.hdu[3]

            # ON_SCAN for all other drift scan unmodified data above 2280 MHz
            self.onScanHDU = self.hdu[4]

            # SOUTH_SCAN for all other drift scan unmodified data above 2280 MHz
            self.hpsScanHDU = self.hdu[5]

            # Chart data HDU
            try:
                self.chartHDU = self.hdu[6]
            except:
                msg_wrapper("warning", self.log.warning, "Chart header not found, this analysis will be flagged.")

        elif len(self.hdu) <= 5:
 
            if self.beam_type == "13.0S" or self.beam_type == "18.0S":
                self.onScanHDU = self.hdu[3]
                self.chartHDU = self.hdu[-1]

            elif self.beam_type == "04.5S" or self.beam_type == "06.0D" or self.beam_type == "03.5D" or self.beam_type == "01.3S" or self.beam_type == "02.5S":

                # Generate placeholder data for corrupted driftscans
                place_holder_data = np.full_like(1000, np.nan)
                beams=["HPSLCP","HPNLCP","ONLCP","HPSRCP","HPNRCP","ONRCP"]
                for i in range(len(beams)):
                    self.scans[beams[i]] = place_holder_data 
                
            else:
                msg_wrapper("error", self.log.error,
                            "Invalid frequency detected: {} MHz".format(self.beam_type))
                sys.exit()
     
        else:
            msg_wrapper("error", self.log.error, "Invalid hdu length detected: hdu length = {} \nFile {} is corrupted.".format(self.HDU_LEN,self.fileName))
            sys.exit()

    def get_source_parameters_data(self):
        """ Get the main parameters from the file. """

        msg_wrapper("debug", self.log.debug,
                    'Get the main parameters from the file')

        self.set_headers()
        if self.CHH == 0:
            return
        else:
            self.set_primary_header_stats()
            self.set_obs_info_header_stats()
            self.set_noise_cal_header_stats()

    def set_headers(self):
        """ Set the fits file header access. """

        msg_wrapper("debug", self.log.debug, 'Set the fits file header access')

        self.PRH = self.primary_HDU.header
        self.OIH = self.obs_info_HDU.header
        self.NCH = self.noise_cal_HDU.header
        try:
            self.CHH = self.chartHDU.header
        except:
            #TODO: Error handle this properly
            msg_wrapper("warning", self.log.warning,"This file is missing a chart header, setting chart header hdu to zero.")
            self.CHH = 0

    def set_primary_header_stats(self):
        """
            Setup the main statistics of each source that are common to all.
        """

        msg_wrapper("debug", self.log.debug,
            'Setup the main statistics of each source ')

        self.data['OBSDATE'] = (self.PRH["DATE"])[:10]
        self.data['OBSTIME'] = (self.PRH["DATE"])[11:]
        self.data['OBJECT'] = self.PRH["OBJECT"]
        self.data['LONGITUDE'] = self.PRH["LONGITUD"]
        self.data['LATITUDE'] = self.PRH["LATITUDE"]
        self.data['OBSERVER'] = self.PRH["OBSERVER"]
        self.data['OBSLOCAL'] = self.PRH["OBSLOCAL"]
        self.data['PROJNAME'] = self.PRH["PROJNAME"]
        self.data['PROPOSAL'] = self.PRH["PROPOSAL"]
        self.data['TELESCOPE'] = self.PRH["TELESCOP"]
        self.data['UPGRADE'] = self.PRH["UPGRADE"]
        self.data['FOCUS'] = self.PRH["FOCUS"]
        self.data['TILT'] = self.PRH["TILT"]

        self.set_parameter('TAMBIENT', self.PRH)
        self.set_parameter('PRESSURE', self.PRH)
        self.set_parameter('HUMIDITY', self.PRH)

        self.data['SCANTYPE'] = self.PRH["SCANTYPE"]
        self.data['RADIOMETER'] = self.PRH["INSTRUME"]
        self.data['SCANDIST'] = self.PRH["SCANDIST"]
        self.data['SCANTIME'] = self.PRH["SCANTIME"]

        self.set_parameter('WINDSPD', self.PRH)
        self.set_parameter('INSTFLAG',self.PRH)

    def set_parameter(self, parameterName, header):
        """ set the value of a given parameter in the data dictionary """
        
        try:
            self.data[parameterName] = header[parameterName]
        except:
            msg_wrapper("warning", self.log.warning, f"{parameterName} is missing from the fits file. Setting it to NAN.")
            self.data[parameterName] = np.nan
            
    def set_obs_info_header_stats(self):
        """ Setup common observational info parameters from fits file. """

        msg_wrapper("debug", self.log.debug,
                    'Setup common observational info parameters from fits file.')

        # get beam widths
        self.data['HPBW'] = self.OIH['HPBW']
        self.data['FNBW'] = self.OIH['FNBW']
        self.data['NOMTSYS'] = self.OIH['NOMTSYS']

    def set_noise_cal_header_stats(self):
        """ Setup common noise header parameters."""

        msg_wrapper("debug", self.log.debug,
            'Setup common parameters from fits file noise calibrator.')

        self.set_parameter('CENTFREQ', self.NCH)
        self.data['BANDWDTH'] = self.NCH["BANDWDTH"]

    def calc_log_freq(self):
        """ Calculate the log(frequency) """

        msg_wrapper("debug", self.log.debug, "Calculating log of frequency")
        try:
            self.data['LOGFREQ'] = np.log10(float(self.data['CENTFREQ']))
        except:
            self.data['LOGFREQ'] = np.nan
            msg_wrapper("warning", self.log.debug, "missing 'CENTFREQ', setting it to NAN")

    def set_chart_header_stats(self):
        """
        Setup common chart header parameters from fits file.
        """

        msg_wrapper("debug", self.log.debug, "Setting chart header stats")
        self.set_parameter('TSYS1', self.CHH)
        self.set_parameter('TSYSERR1', self.CHH)
        self.set_parameter('TSYS2', self.CHH)
        self.set_parameter('TSYSERR2', self.CHH)
        self.set_parameter('TCAL1', self.CHH)
        self.set_parameter('TCAL2', self.CHH)

    def get_derived_properties(self):
        """ Set the calculated derived of the scan."""

        msg_wrapper("debug", self.log.debug, "Getting calculated properties")

        #self.data['HA'] = np.mean(self.onScanHDU.data.field('Hour_Angle'))
        #self.data['ZA'] = np.mean(
        #    self.onScanHDU.data.field('Dec_J2000'))  

        self.HA = self.onScanHDU.data.field('Hour_Angle')
        self.ELEVATION = self.onScanHDU.data.field('Elevation')
        self.MJD = self.onScanHDU.data.field('MJD')

        # find centre point of the data
        self.MID = int(len(self.MJD)/2)

        # get Julian date, elevation, ha and Zenith from center of on source scan
        self.data['MJD'] = self.MJD[self.MID]
        self.data['HA'] = self.HA[self.MID] # corrected with help from Jon/Marisa
        self.data['ELEVATION'] = self.ELEVATION[self.MID]
        self.data['ZA'] = 90.0 - self.ELEVATION[self.MID]

        self.calc_log_freq()
        if self.data['OBJECTTYPE'] == "CAL":
            self.calc_flux()
        else:
            pass

        # Calibrate atmosphere
        if self.data['BEAMTYPE'] != '13.0S':
            self.calibrate_nb_Atm()
        else:
            self.calibrate_wb_Atm()

    def calc_flux(self):
        """
            Calculate the source flux for the calibrator.
            Use the Ott and Baars system.
        """

        msg_wrapper("debug", self.log.debug,
                    "Calculating flux density for the calibrator")

        baars = { 
            # Baars 1977 paper - J. W. M. Baars, R. Genzel, T. T. K. Pauliny-Toth,A. Witzel, 
            # 'The Absolute Spectrum of Cas A; An Accurate Flux Density Scale and a Set of 
            # Secondary Calibrators," Astronomy & Astrophysics, 61, 1977, pp. 99-106.
            
            #"CygnusA20M": {'range_from': 20, 'range_to': 2000, 'a': 4.695, 'b': 0.085, 'c':-0.178},
            "CYGNUSA" : {'range_from': 2000, 'range_to': 31000, 'a': 7.161, 'b': -1.244, 'c':0},
            "TAURUSA"   : {'range_from': 1000, 'range_to': 35000, 'a': 3.915, 'b': -0.299, 'c':0},
            "VIRGO A"    : {'range_from': 400, 'range_to': 25000, 'a': 5.023, 'b': -0.856, 'c':0},
            "3C48"      : {'range_from': 405, 'range_to': 15000, 'a': 2.345, 'b':0.071, 'c': -0.138},
            "3C123"     : {'range_from': 405, 'range_to': 15000, 'a': 2.921, 'b': -0.002, 'c': -0.124},
            "3C161"     : {'range_from': 405, 'range_to': 10700, 'a': 1.633, 'b': 0.498, 'c': 0.194},
            "HYDRA A"   : {'range_from': 405, 'range_to': 10700, 'a': 4.497, 'b': -0.910, 'c':  0},
            "3C218"     : {'range_from': 405, 'range_to': 10700, 'a': 4.497, 'b': -0.910, 'c':  0}, #aka HYDRA A
            "3C286"     : {'range_from': 405, 'range_to': 15000, 'a': 1.480, 'b': 0.292, 'c': -0.124},
            "3C348"     : {'range_from': 405, 'range_to': 10700, 'a': 4.963, 'b': -1.052, 'c':0},
            "3C353"     : {'range_from': 405, 'range_to': 10700, 'a': 2.944, 'b': -0.034, 'c': -0.109},
            'DR21'      : {'range_from': 7000, 'range_to': 31000, 'a': 1.81, 'b': -0.122, 'c': 0},
            "NGC7027"   : {'range_from': 10000, 'range_to': 31000, 'a': 1.32, 'b': -0.127, 'c': 0}
        }
              
        ott = { 
            # OTT 1994 PAPER - M. Ott, A. Quirrenbach, T. P. Krichbaum, K. J. Standke, C. J. Schalinski, and C. A. Hummel,
            # An updated list of radio flux density calibrators, Astronomy & Astrophysics, 284, 1994, pp. 331-339.

                "3C48"   : {'range_from': 1408, 'range_to': 23780, 'a': 2.465, 'b': -0.004, 'c': -0.1251},
                "3C123"  : {'range_from': 1408, 'range_to': 23780, 'a': 2.525, 'b': 0.246, 'c': -0.1638},
                "3C147"  : {'range_from': 1408, 'range_to': 23780, 'a': 2.806, 'b': -0.140, 'c': -0.1031},
                "3C161"  : {'range_from': 1408, 'range_to': 10550, 'a': 1.250, 'b': 0.726, 'c': -0.2286},
                "HYDRA A": {'range_from': 1408, 'range_to': 15000, 'a': 4.729, 'b': -1.025, 'c':  0.0130},
                "3C218"  : {'range_from': 1408, 'range_to': 15000, 'a': 4.729, 'b': -1.025, 'c':  0.0130}, #aka HYDRA A
                "3C218"  : {'range_from': 1408, 'range_to': 10550, 'a': 4.729, 'b': -1.025, 'c':  0.0130},
                "3C227"  : {'range_from': 1408, 'range_to': 4750, 'a': 6.757, 'b': -2.801, 'c':  0.2969},
                "3C249.1": {'range_from': 1408, 'range_to': 4750, 'a': 2.537, 'b': -0.565, 'c': -0.0404},
                "3C286"  : {'range_from': 1408, 'range_to': 43200, 'a': 0.956, 'b': 0.584, 'c': -0.1644},
                "3C295"  : {'range_from': 1408, 'range_to': 32000, 'a': 1.490, 'b': 0.756, 'c': -0.2545},
                "3C348"  : {'range_from': 1408, 'range_to': 10550, 'a': 3.852, 'b': -0.361, 'c': -0.1053},
                "3C353"  : {'range_from': 1408, 'range_to': 10550, 'a': 3.148, 'b': -0.157, 'c': -0.0911},
                "VIRGO A": {'range_from': 4750, 'range_to': 10550, 'a': 4.484, 'b': -0.603, 'c': -0.0280}, 
                "CYGNUSA": {'range_from': 20, 'range_to': 2000, 'a': 8.360, 'b': 1.565, 'c':0},
                "NGC7027": {'range_from': 10550, 'range_to': 43200, 'a': 1.322, 'b': -0.134, 'c': 0}
                }
        
        # first try Ott then fall back onto Baars
        # log S[Jy] = a + b*log(freq)[MHz] + c*log**2(freq) [MHz]
        if self.data['OBJECT'].upper() in ott.keys():
            if ott[self.data['OBJECT']]["range_from"] < self.data['CENTFREQ'] < ott[self.data['OBJECT']]["range_to"]:
                self.data['FLUX'] = (10**(ott[self.data['OBJECT']]["a"] + ott[self.data['OBJECT']]
                            ["b"]*self.data['LOGFREQ'] + ott[self.data['OBJECT']]["c"]*self.data['LOGFREQ']**2))
        else:
            if self.data['OBJECT'].upper() in baars.keys():
                if baars[self.data['OBJECT']]["range_from"] < self.data['CENTFREQ'] < baars[self.data['OBJECT']]["range_to"]:
                    self.data['FLUX'] = (10**(baars[self.data['OBJECT']]["a"] + baars[self.data['OBJECT']]
                        ["b"]*self.data['LOGFREQ'] + baars[self.data['OBJECT']]["c"]*self.data['LOGFREQ']**2))
            else:
                print(f'{self.data["OBJECT"]} - does not have calibration flux density spectral parameters in Ott 1994 or Barrs 1977.')
                #pass
                #sys.exit()
  
    def calibrate_nb_Atm(self):
        """
        Calibrate the atmosphere for narrow beam observations.
        """

        msg_wrapper("debug", self.log.debug,
                    "Calibrate atmosphere.")

        if self.data['BEAMTYPE'] == "01.3S":

            self._calibrate_atmosphere()

            if self.data["OBJECTTYPE"] == "CAL":
                self._calibrate_jupiter_atm()
            else:
                pass

        if self.data['BEAMTYPE'] == '02.5S':
            # Force jupiter 12.178 GHz data to perform 22 GHz fit
            if( self.beam_type=="02.5S" and self.object=="Jupiter_12.178GHz"):
                self._calibrate_atmosphere()
                if self.data["OBJECTTYPE"] == "CAL":
                    self._calibrate_jupiter_atm()
                else:
                    pass
            else:
                self._calibrate_atmosphere()
                self._add_12ghz_vars()
                self._calc_mean_atm_corr()

        elif self.data['BEAMTYPE'] == '06.0D' or self.data['BEAMTYPE'] == '03.5D':
            self._add_db_vars()
            self._calibrate_atmosphere()
            self._calc_zenith_absorption()

    def _calibrate_atmosphere(self):
        """
            Calculate the atmospheric optical depth Tau and brightness temperature Tb at zenith.
        """

        if (self.data['TAMBIENT'] > 0.0 and self.data['PRESSURE'] > 0.0 and self.data['HUMIDITY'] > 0.0):
            if self.data["BEAMTYPE"] != "13.0S":  
                self._calc_water_vapour()
                if self.data["BEAMTYPE"] == "02.5S":

                    # Force jupiter 12.178 GHz data to perform 22 GHz fit
                    if( self.beam_type=="02.5S" and self.object=="Jupiter_12.178GHz"):#,self.scans)
                        pass
                    else:
                        self._calc_12ghz_optical_depths()
                        self._calc_12ghz_brightness_temps()
                elif self.data["BEAMTYPE"] == "01.3S":
                    if self.data["OBJECTTYPE"] == "CAL":
                        pass
                    else:
                        self.calc_tau_tb()
                else:
                    pass
            else:
                pass
        else:
            if self.data["BEAMTYPE"] != "13.0S":
                self._set_water_vapour()

                if self.data["BEAMTYPE"] == "01.3S":
                    self._set_22ghz_optical_depths()
                    self._set_22ghz_brightness_temps()

                elif self.data["BEAMTYPE"] == "02.5S":

                    # Force jupiter 12.178 GHz data to perform 22 GHz fit
                    if( self.beam_type=="02.5S" and self.object=="Jupiter_12.178GHz"):#,self.scans)
                        self._set_22ghz_optical_depths()
                        self._set_22ghz_brightness_temps()
                    else:
                        self._calc_12ghz_optical_depths()
                        self._calc_12ghz_brightness_temps()
                else:
                    pass

            else:
                pass

    def _calc_water_vapour(self):
        """ Calculate water vapor """

        msg_wrapper("debug", self.log.debug, "Calculate the water vapour")

        # ensure PWV and WVD do not go negative! 
        # calculate PWV values - copy from Mikes drift_fits2asc_HINDv16.c file

        self.data['PWV'] = max(0.0, 4.39 * self.data['HUMIDITY']/100.0/self.data['TAMBIENT'] * math.exp(26.23-5416/self.data['TAMBIENT']))  # [mm] precip_water_vapour
        # [kPa] sat_vap_pressure
        self.data['SVP'] = 0.611 * math.exp(
                17.27*(self.data['TAMBIENT']-273.13)/(self.data['TAMBIENT']-273.13+237.3))
        # [kPa] amb_vap_pressure
        self.data['AVP'] = self.data['SVP'] * self.data['HUMIDITY']/100.0
        
        if self.data['AVP'] <= 0:
            self.data['DPT'] = 0
        else:
            self.data['DPT'] = (116.9 + 237.3*math.log(self.data['AVP'])) / (16.78-math.log(self.data['AVP']))  # [oC] dew_point_temp
        # [g/m^3]water_vapour_density
        self.data['WVD'] = max(0.0, 2164.0*self.data['AVP']/self.data['TAMBIENT'])

    def _calc_12ghz_optical_depths(self):
        """ 
        
        """
        
        msg_wrapper("debug", self.log.debug, "Calculate the optical depths")

        self._calc_water_vapour()

        self.data['TAU10'] = 0.0071 + 0.00021 * self.data['PWV']  # tau10, from SKA doc, i.e. measurements made in karnavon
        # tau15, from Meeks 1976 exptl Physics 12B p175
        self.data['TAU15'] = (0.055 + 0.004 * self.data['WVD'])/4.343
        
    def _calc_12ghz_brightness_temps(self):
        """ Calculate brightness temperratures."""

        msg_wrapper("debug", self.log.debug,
                    "Calculate the brightness temperature")

        self.data['TBATMOS10'] = 260 * (1.0 - math.exp(-self.data['TAU10']))  # tbatmos10
        self.data['TBATMOS15'] = 260 * (1.0 - math.exp(-self.data['TAU15']))  # tbatmos15

    def calc_tau_tb(self):
        """ Calculate optical depths. """

        msg_wrapper("debug", self.log.debug,
                    "Calculate the optical depth")

        self.data['TAU221'] = 0.0140 + 0.00780 * self.data['PWV']  # tau221 , from SKA doc
        self.data['TAU2223'] = (0.110 + 0.048 * self.data['WVD'])/4.343  # tau222
        self.data['TBATMOS221'] = 260 * \
            (1.0 - math.exp(-self.data['TAU221']))  # tbatmos221
        self.data['TBATMOS2223'] = 260 * \
            (1.0 - math.exp(-self.data['TAU2223']))  # tbatmos222

    def _set_water_vapour(self):
    
        """ Set default water vapour estimates to one . """

        msg_wrapper("debug", self.log.debug,
                    "Set water vapour to default to one")

        # calculate PWV values - copy from Sunell's code
        self.data['PWV'] = 1  # [mm] precip_water_vapour
        self.data['SVP'] = 1  # [kPa] sat_vap_pressure
        self.data['AVP'] = 1  # [kPa] amb_vap_pressure
        self.data['DPT'] = 1  # [oC] dew_point_temp
        self.data['WVD'] = 1  # [g/m^3] water_vapour_density

    def _set_22ghz_optical_depths(self):
        """ set the optical depth at 22 GHz atult to one. """

        msg_wrapper("debug", self.log.debug,
                    "set optical depths to default to 1")

        self._set_water_vapour()

        self.data['TAU221'] = 1  # tau221
        self.data['TAU2223'] = 1  # tau222

    def _set_22ghz_brightness_temps(self):
        """ Set brightness temperature to default to one"""

        msg_wrapper("debug", self.log.debug,
                    'Set brightness temperature to default to one')

        self.data['TBATMOS221'] = 1  # tbatmos221
        self.data['TBATMOS2223'] = 1  # tbatmos222

    def _calibrate_jupiter_atm(self):
        """ Calibrate jupiter atmospheric data.
        """

        msg_wrapper("debug", self.log.debug,
                    'Calibrate jupiter atmospheric data.')

        self.get_planet_ang_diam()
        self.get_jupiter_dist()

        # TODO: Verify this number
        self.data["HPBW_ARCSEC"] = 0.033*3600  # why 0.033 ?, self.data["HPBW"]*3600

        # TODO: VERIFY ADOPTED TB
        # from Jupiter Tb = 138.2 + 1.6 K = 139.8 K: Gibson, Welch, de Pater 2005, Icarus 173, 439;
        self.data["ADOPTED_PLANET_TB"] = 136
        self.data["SYNCH_FLUX_DENSITY"] = 1.6 * (4.04/self.data["JUPITER_DIST_AU"])**2
        self.data["PLANET_ANG_EQ_RAD"] = self.data["PLANET_ANG_DIAM"]/3600*math.pi/180./2.
        self.data["PLANET_SOLID_ANG"] = math.pi*self.data["PLANET_ANG_EQ_RAD"]**2*0.935
        self.data["THERMAL_PLANET_FLUX_D"] = 2*1380*self.data["ADOPTED_PLANET_TB"] * \
            self.data["PLANET_SOLID_ANG"]/(300/self.data["CENTFREQ"])**2
        self.data["TOTAL_PLANET_FLUX_D"] = self.data["SYNCH_FLUX_DENSITY"] + \
            self.data["THERMAL_PLANET_FLUX_D"]
    
        self.data["TOTAL_PLANET_FLUX_D_WMAP"] = 2*1380*135.2 * \
            self.data["PLANET_SOLID_ANG"]/(300/self.data["CENTFREQ"])**2
        self.data["SIZE_FACTOR_IN_BEAM"] = self.data["PLANET_ANG_DIAM"] / \
            2.*np.sqrt(0.935)/(0.6*self.data["HPBW_ARCSEC"])
        self.data["SIZE_CORRECTION_FACTOR"] = self.data["SIZE_FACTOR_IN_BEAM"]**2 / \
            (1-math.exp(-self.data["SIZE_FACTOR_IN_BEAM"]**2))

        # from ztcal (zenith temperature calibration - read mikes notes)
        self.data["MEASURED_TCAL1"] = 71.4 # zenith measured value
        self.data["MEASURED_TCAL2"] = 70.1 # check mikes notes

        self.data["MEAS_TCAL1_CORR_FACTOR"] = self.data["MEASURED_TCAL1"]/self.data["TCAL1"]
        self.data["MEAS_TCAL2_CORR_FACTOR"] = self.data["MEASURED_TCAL2"]/self.data["TCAL2"]
        self.calc_tau_tb()
        self.data["ZA_RAD"] = self.data["ZA"]*math.pi/180.
        self.data["ATMOS_ABSORPTION_CORR"] = math.exp(
            self.data["TAU221"]/math.cos(self.data["ZA_RAD"]))

    def get_planet_ang_diam(self):
        """
            Get the planet angular diameter from horizon data
        """
        import datetime

        msg_wrapper("debug", self.log.debug,
                    'Get the planet angular diameter from horizon data.')

        # Get observation date and split it
        year = int(self.data["OBSDATE"][:4])
        month = int(self.data["OBSDATE"][5:7])
        day = int(self.data["OBSDATE"][8:])

        # Get month of date in words
        mydate = datetime.date(year, month, day)

        # extract data from file
        try:
            jplResults=get_jpl_results()
        except ex.FileResourceNotFoundError:
            msg_wrapper("error", self.log.error,
                        "\nFileResourceNotFoundError: The 'nasa_jpl_results.txt' resource is not in the distribution\n")
            sys.exit()

        try:
            date=mydate.strftime("%Y-%b-%d")
            ret = jplResults[jplResults['DATE']==date]
            self.data["PLANET_ANG_DIAM"] = ret["ANG-DIAM"].iloc[0]
        except ex.ValueOutOfRangeException:
            print(f"\nValueOutOfRangeException: The date {mydate} has not been accounted for, contact mantainer")
            sys.exit()


    def get_jupiter_dist(self):
        """
        Get Jupiter AU distance from calsky website data.
        """

        import datetime

        msg_wrapper("debug", self.log.debug,
                    'Get Jupiter AU distance from calsky data')

        # Get observation date and split it
        year = int(self.data["OBSDATE"][:4])
        month = int(self.data["OBSDATE"][5:7])
        day = int(self.data["OBSDATE"][8:])

        # Get month of date in words
        myDate = datetime.date(year, month, day)
        myMonth=myDate.strftime("%b")

        # Get AU distance / radius
        try:
            calskyRes=get_calsky_results(year)
            row=calskyRes[(calskyRes['month']==myMonth) & (calskyRes['day']==day)]
            self.data["JUPITER_DIST_AU"] = row['radius'].iloc[0]
        except ex.ValueOutOfRangeException:
            print(f"\nValueOutOfRangeException: The date {myDate} has not been accounted for, contact mantainer")
            sys.exit()

    def convert_counts_to_kelvins(self):
        """
            Convert counts to antenna temperature.
        """

        msg_wrapper("debug", self.log.debug, "Converting counts to kelvins")

        #extract the scan data, convert counts to Kelvins
        #--------------------------------------------------
        namesOfConversionFactors = []

        try:
            # get counts conversion factor, the number of hz per kelvin
            namesOfConversionFactors, lcpHzPerK, rcpHzPerK = self._get_counts_conversion_factor()
        except Exception:
            lcpHzPerK, rcpHzPerK = self._get_counts_if_err_in_conversion_factor(
                namesOfConversionFactors)

        if self.data['BEAMTYPE'] == "13.0S" or (self.data['BEAMTYPE'] == "18.0S"):
            self.get_wb_scans(self.data['SCANDIST'], lcpHzPerK, rcpHzPerK)
        else:
            self.get_nb_scans(self.data['SCANDIST'], lcpHzPerK, rcpHzPerK)

    def get_wb_scans(self, scandist, lcpHzPerK, rcpHzPerK):
        """
        Get the drift scans
        """

        msg_wrapper("debug", self.log.debug, "Getting scan data for WB scans")

        # construct an array for the x-axis in terms of scan offset from the centre
        self.offset = np.linspace(-1*scandist/2.0, scandist/
                                  2.0, len(self.onScanHDU.data['MJD']))
        self.scans["OFFSET"] = self.offset
        self.ra = self.onScanHDU.data['RA_J2000']
        self.scans["RA"] = self.ra

        # TODO: Fix the exceptions and naming convention
        # if this is a 13cm drift scan, setup 2 scans
        # Get ONLCP counts and convert to antenna temperature
        try:
            self.onLcp = self.onScanHDU.data['Count1']
            # Convert to antenna temperature
            self.onScanLCP = (self.onLcp/lcpHzPerK)-(self.onLcp[0]/lcpHzPerK)
            self.scans["ONLCP"] = self.onScanLCP

        except Exception:
            self.onScanLCP = np.full_like(self.offset, np.nan)
            self.scans["ONLCP"] = self.onScanLCP

        # Get ONRCP counts and convert to antenna temperature
        try:
            self.onRcp = self.onScanHDU.data['Count2']
            self.onScanRCP = (self.onRcp/rcpHzPerK)-(self.onRcp[0]/rcpHzPerK)
            self.scans["ONRCP"] = self.onScanRCP

        except Exception:
            self.onScanRCP = np.full_like(self.offset, np.nan)
            self.scans["ONRCP"] = self.onScanRCP

    def _get_counts_conversion_factor(self):
        """
        Get counts measured.
        """
        
        msg_wrapper("debug", self.log.debug, "Getting counts without errors")
        namesOfConversionFactors = []

        # AS PER GEORGE'S EMAIL:
        # Low noise diodes are for continuum flux density calibrations and high noise diodes are for spectroscopy
        # Get noise diode conversion factor LO-NOISE DIODE
        #lcpHzPerK = self.NCH['HZPERK1']
        #rcpHzPerK = self.NCH['HZPERK2']

        # Get noise diode conversion factor HI-NOISE-DIODE
        lcpHzPerK = self.chartHDU.header['HZPERK1']
        rcpHzPerK = self.chartHDU.header['HZPERK2']

        namesOfConversionFactors.append("lcpHzPerK")
        namesOfConversionFactors.append("rcpHzPerK")

        return namesOfConversionFactors, lcpHzPerK, rcpHzPerK

    def _get_counts_if_err_in_conversion_factor(self, counts):
        """
        Get counts, if an error occured these counts will be set to 
        an array of zeros.

        Args:
            counts(list): list of observed counts 

        Returns:
            lcpHzPerK: lcp observed counts
            rcpHzPerK: rcp observed counts
        """

        msg_wrapper("debug", self.log.debug,"Getting counts with errors")

        if len(counts) == 0:  # could not find hzperk1
            msg_wrapper("debug", self.log.debug," MISSING 'HZPERK1', setting to zero")
            lcpHzPerK = np.zeros_like(self.chartHDU.header['NAXIS2'])
            try:
                rcpHzPerK = self.NCH['HZPERK2']
            except Exception:
                msg_wrapper("debug", self.log.debug,
                            "MISSING 'HZPERK2', setting to zero")
                rcpHzPerK = np.zeros_like(
                    self.chartHDU.header['NAXIS2'])

        elif len(counts) == 1:  # could not find hzperk2
            if (counts[0] == "lcpHzPerK"):
                msg_wrapper("debug", self.log.debug,
                            " MISSING 'HZPERK2', setting to zero")
                rcpHzPerK = np.zeros_like(
                    self.chartHDU.header['NAXIS2'])
            else:
                pass

        return lcpHzPerK, rcpHzPerK

    def get_nb_scans(self, scandist, lcpHzPerK, rcpHzPerK):
        """
        Get the drift scan counts and convert them to antenna temperature.

        Args:
            scandist: Scan length in degrees.
            lcpHzPerK: Source counts for lcp scan.
            rcpHzPerK: Source counts for rcp scan.
        """

        msg_wrapper("debug", self.log.debug, "Getting scan data for NB scans")

        #construct an array for the x-axis in terms of scan offset from the centre
        self.offset = np.linspace(-1*scandist/2.0,
                                  scandist/2.0, len(self.onScanHDU.data['MJD']))
        self.scans["OFFSET"] = self.offset

        self.ra = self.onScanHDU.data['RA_J2000']
        self.scans["RA"] = self.ra

        # for all other drift scans, setup 6 scans
        # Get HPSLCP counts and convert to antenna temperature
        try:
            self.hps_lcp = self.hpsScanHDU.data['Count1']
            self.hpsScanLCP = (self.hps_lcp/lcpHzPerK) - \
                (self.hps_lcp[0]/lcpHzPerK)
            self.scans["HPSLCP"] = self.hpsScanLCP

        except Exception:
            self.hpsScanLCP = np.full_like(self.offset, np.nan)
            self.scans["HPSLCP"] = self.hpsScanLCP

        # Get HPNLCP counts and convert to antenna temperature
        try:
            self.hpn_lcp = self.hpnScanHDU.data['Count1']
            # Convert to antenna temperature
            self.hpnScanLCP = (self.hpn_lcp/lcpHzPerK) - \
                (self.hpn_lcp[0]/lcpHzPerK)
            self.scans["HPNLCP"] = self.hpnScanLCP

        except Exception:
            self.hpnScanLCP = np.full_like(self.offset, np.nan)
            self.scans["HPNLCP"] = self.hpnScanLCP

        # Get ONLCP counts and convert to antenna temperature
        try:
            self.on_lcp = self.onScanHDU.data['Count1']
            self.onScanLCP = (self.on_lcp/lcpHzPerK) - (self.on_lcp[0]/lcpHzPerK)
            self.scans["ONLCP"] = self.onScanLCP

        except Exception:
            self.onScanLCP = np.full_like(self.offset, np.nan)
            self.scans["ONLCP"] = self.onScanLCP

        # Get HPSRCP counts and convert to antenna temperature
        try:
            self.hps_rcp = self.hpsScanHDU.data['Count2']
            self.hpsScanRCP = (self.hps_rcp/rcpHzPerK) - \
                (self.hps_rcp[0]/rcpHzPerK)
            self.scans["HPSRCP"] = self.hpsScanRCP

        except Exception:
            self.hpsScanRCP = np.full_like(self.offset, np.nan)
            self.scans["HPSRCP"] = self.hpsScanRCP

        # Get HPNRCP counts and convert to antenna temperature
        try:
            self.hpn_rcp = self.hpnScanHDU.data['Count2']
            self.hpnScanRCP = (self.hpn_rcp/rcpHzPerK) - \
                (self.hpn_rcp[0]/rcpHzPerK)
            self.scans["HPNRCP"] = self.hpnScanRCP

        except Exception:
            self.hpnScanRCP = np.full_like(self.offset, np.nan)
            self.scans["HPNRCP"] = self.hpnScanRCP

        # Get ONRCP counts and convert to antenna temperature
        try:
            self.on_rcp = self.onScanHDU.data['Count2']
            self.onScanRCP = (self.on_rcp/rcpHzPerK) - (self.on_rcp[0]/rcpHzPerK)
            self.scans["ONRCP"] = self.onScanRCP

        except Exception:
            self.onScanRCP = np.full_like(self.offset, np.nan)
            self.scans["ONRCP"] = self.onScanRCP

    def _calc_zenith_absorption(self):
        """ Calculation of zenith absorption. 
        
            Args:
                data: driftscan parameters"""

        msg_wrapper("debug",self.log.debug,"Calculate zenith absorption")

        dtr = 0.01745329 # where does this number come from??

        self.data['SEC_Z'] = 1.0 / np.cos(self.data['ZA'] * dtr)
        self.data['X_Z'] = -0.0045 + 1.00672 * self.data['SEC_Z'] - 0.002234 * \
            self.data['SEC_Z'] ** 2 - 0.0006247 * self.data['SEC_Z']**3
        self.data['DRY_ATMOS_TRANSMISSION'] = 1.0 / \
            np.exp(0.0069*(1/np.sin((90-self.data['ZA'])*dtr)-1))
        self.data['ZENITH_TAU_AT_1400M'] = 0.00610 + 0.00018 * self.data['PWV']
        self.data['ABSORPTION_AT_ZENITH'] = np.exp(
            self.data['ZENITH_TAU_AT_1400M'] * self.data['X_Z'])

    def calibrate_wb_Atm(self):
        """
        Calculate atmosphere for wide beam observations.
        """

        msg_wrapper("debug", self.log.debug,
                    "Calibrate atmosphere.")
        self.data['ATMOSABS'] = np.exp(
            0.005/np.cos(self.data['ZA']*0.017453293))

    def _add_12ghz_vars(self):
        """
        parameters found only in 12ghz beams.
        """

        msg_wrapper("debug", self.log.debug, "Add narrow beam params")
        self.data["MEAN_ATMOS_CORRECTION"] = 0

    def _add_db_vars(self):
        """ Add dual beam parameters """

        msg_wrapper("debug", self.log.debug, "Add dual beam params")

        self.data["SEC_Z"] = 0.
        self.data["X_Z"] = 0.
        self.data["DRY_ATMOS_TRANSMISSION"] = 0.
        self.data["ZENITH_TAU_AT_1400M"] = 0.
        self.data["ABSORPTION_AT_ZENITH"] = 0.

    def _calc_mean_atm_corr(self):
        """ 
        Calculate the mean atmospheric correction.
        """
        msg_wrapper("debug", self.log.debug,
                    "Calculate the mean atmospheric correction")
        self.data['MEAN_ATMOS_CORRECTION'] = np.exp(
            (self.data['TAU15'] + self.data['TAU10'])/2.0/np.cos(self.data['ZA']*np.pi/180.0))
