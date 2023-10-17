# ============================================================================#
# File: scan_parameters.py                                                    #
# Author: Pfesesani V. van Zyl                                                #
# ============================================================================#

# Standard library imports
# --------------------------------------------------------------------------- #
import numpy as np
# =========================================================================== #


class ScanParameters:
    """
        Class of parameters to be collected/saved to a database from the drift 
        scan fits file. These are the values that will be populated in the 
        CALDB or TARDB databases.

        Args:
            parameters (dict): dictionary of all properties to be stored.
    """

    def __init__(self):

        self.parameters = {}    

    def print_keys(self):
        """ Print the keys of the dictionary. """

        print(self.parameters.keys())

    def print_dict(self):
        """ Print the dictionary key value pairs. """

        print("\n# parameters: \n")
        [print(i, ": ", j) for i, j in zip(
                list(self.parameters.keys()), list(self.parameters.values()))]
    
    def reset_dict(self):
        """ Reset the dictionary. """

        self.parameters = {}

    def combine_parameters(self, new_dict_entries):
        """ Add new dictionary to existing dictionary.

            Combine parameters to get a single dictionary of all
            values you want to save and populate for you drift scan
            database.

        Args:
            new_dict_entries (dict): set of new dictionary entries to store
        """

        self.parameters = {**self.parameters, **new_dict_entries}

    def info_dict(self):
        """ Dictionary of parameters and their descriptions."""

        parameters = {
            "FILENAME": "Name of fits file being processed",
            "HDULENGTH": "Length of fits file header data unit (HDU)",
            "SOURCEDIR": " Name of folder containing fits file",
            "CURDATETIME": "Date file was reduced",
            "OBSDATE": "Date of source observation, file creation date",
            "OBSTIME": "Time of source observation",
            "MJD": "Modified julian date of observation",
            "OBJECT": "Name of object observed",
            "OBJECTTYPE": "Object type i.e. calibrator or target",
            "CENTFREQ": "Central frequency",
            "LOGFREQ": "Log of central frequency",
            "FOCUS": "Sub-reflector focus",
            "TILT": "Sub-reflector tilt",
            "HA": "Hour angle",
            "ZA": "Zenith angle , used to be DEC",
            "RADIOMETER": "Radiometer type",
            "BANDWDTH": "Band width",
            "TCAL1": "Left circular polirization noise diode",
            "TCAL2": "Right circular polirization noise diode",
            "NOMTSYS": "Nominal system temperature",
            "TSYS1": "Left circular polirization system temperature",
            "TSYSERR1": "Error in Left circular polirization system temperature",
            "TSYS2": "Right circular polirization system temperature",
            "TSYSERR2": "Error in Right circular polirization system temperature",
            "TAMBIENT": "Ambient temperature [K]",
            "PRESSURE": "Atmospheric Pressure [mbar]",
            "HUMIDITY": "Humidity [%]",
            "WINDSPD": "Wind speed [m/s]",
            "HPBW": "Half power beam width",
            "FNBW": np.nan,     # First null beam width
            "ELEVATION": np.nan,  # Elevation
            "LONGITUDE": np.nan,  # Longitude
            "LATITUDE": np.nan,  # Latitude
            "SCANTYPE": "",  # The scan type/mode
            "BEAMTYPE": "",  # Beam type
            "OBSERVER": "",  # Principal investigator
            "OBSLOCAL": "",  # Local/on-site observer
            "PROJNAME": "",  # Short name for project
            "PROPOSAL": "",  # Observing Proposal ID
            "TELESCOPE": "",  # Telescope name
            "UPGRADE": "",  # INFO ON POSSIBLE UPGRSDES TO TELESCOPE
            "INSTFLAG": np.nan,  # Radiometer flags
            "SCANDIST": np.nan,  # Scan length (deg)
            "SCANTIME": "",  # Scan time (s)
        }

        self.combine_parameters(parameters)


    # =========================================================================
    #   COMMON SETTINGS
    # =========================================================================

    def set_common_parameters(self):
        """
            Dictionary of default values for parameters common to all scan types.
        """

        self.parameters = {
            "FILENAME": "",  # Name of fits file being processed
            "HDULENGTH": "",  # Length of fits file header data unit (HDU)
            "SOURCEDIR": "",  # Name of folder containing fits file
            "CURDATETIME": "",  # Date file was reduced
            "OBSDATE": "",  # Date of source observation, file creation date
            "OBSTIME": "",  # Time of source observation
            "MJD": np.nan,  # Modified julian date of observation
            "OBJECT": "",  # Name of object observed
            "OBJECTTYPE": "",  # Object type i.e. calibrator or target
            "CENTFREQ": np.nan,  # Central frequency
            "LOGFREQ": np.nan,  # Log of central frequency
            "FOCUS": np.nan,    # Sub-reflector focus
            "TILT": np.nan,     # Sub-reflector tilt
            "HA": np.nan,     # Hour angle
            "ZA": np.nan,     # Zenith angle , used to be DEC
            "RADIOMETER": "",  # Radiometer type
            "BANDWDTH": np.nan,  # Band width
            "TCAL1": np.nan,    # Left circular polirization noise diode
            "TCAL2": np.nan,    # Right circular polirization noise diode
            "NOMTSYS": np.nan,   # Nominal system temperature
            # [K] Left circular polirization system temperature
            "TSYS1": np.nan,
            # [K] Error in Left circular polirization system temperature
            "TSYSERR1": np.nan,
            # [K] Right circular polirization system temperature
            "TSYS2": np.nan,
            # [K] Error in Right circular polirization system temperature
            "TSYSERR2": np.nan,
            "TAMBIENT": np.nan,  # Ambient temperature [K]
            "PRESSURE": np.nan,  # Atmospheric Pressure [mbar]
            "HUMIDITY": np.nan,  # Humidity [%]
            "WINDSPD": np.nan,  # Wind speed [m/s]
            "HPBW": np.nan,  # Half power beam width
            "FNBW": np.nan,     # First null beam width
            "ELEVATION": np.nan,  # Elevation
            "LONGITUDE": np.nan,  # Longitude
            "LATITUDE": np.nan,  # Latitude
            "SCANTYPE": "",  # The scan type/mode
            "BEAMTYPE": "",  # Beam type
            "OBSERVER": "",  # Principal investigator
            "OBSLOCAL": "",  # Local/on-site observer
            "PROJNAME": "",  # Short name for project
            "PROPOSAL": "",  # Observing Proposal ID
            "TELESCOPE": "",  # Telescope name
            "UPGRADE": "",  # INFO ON POSSIBLE UPGRSDES TO TELESCOPE
            "INSTFLAG": np.nan,  # Radiometer flags
            "SCANDIST": np.nan,  # Scan length (deg)
            "SCANTIME": "",  # Scan time (s)
        }
        #self.combine_parameters(parameter)

    def set_flux_parameter(self):
        """ Set the flux. """

        parameter = {
            "FLUX": np.nan
        }

        self.combine_parameters(parameter)

    # =========================================================================
    #   WIDE BEAM SCAN SETTINGS
    # =========================================================================

    def set_atmosabs_parameter(self):
        """ Set the atmospheric absorption parameter. """

        parameter = {
            "ATMOSABS": np.nan
        }

        self.combine_parameters(parameter)

    def set_onlcp_flag_parameter(self):
        """ Set the on scan lcp flag parameter. """

        parameter = {
            "OLFLAG": np.nan
        }

        self.combine_parameters(parameter)

    def set_onrcp_flag_parameter(self):
        """ Set the on scan rcp flag parameter. """

        parameter = {
            "ORFLAG": np.nan
        }

        self.combine_parameters(parameter)

    def set_wb_lcp_parameters(self):
        """ Set the parameters specific to a wide beam on lcp drift scan. """

        parameters = {

            "OLTA": np.nan,     # On LCP antenna temperature
            "OLDTA": np.nan,    # Error in OLTA
            "OLS2N": np.nan,    # On LCP signal to noise
            "OLTAPEAKLOC": np.nan, # On LCP peak fit location
            "OLRMSB": np.nan,   # RMS BEFORE SPLINE TO ALL DATA
            "OLRMSA": np.nan,   # RMS AFTER SPLINE TO ALL DATA
            "OLBSLOPE": np.nan,  # Slope of baseline fit
            "OLBSRMS": np.nan  # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_wb_lcp_pss_parameters(self):
        """ Set the parameters specific to a wide beam scan on lcp pss. """

        parameters = {
            "OLPSS": np.nan,    # On scan LCP point source sensitivity
            "OLDPSS": np.nan,    # Error in OLPSS
            "OLAPPEFF": np.nan  # On lcp apperture effeciency
        }

        self.combine_parameters(parameters)

    def set_wb_rcp_parameters(self):
        """ Set the parameter specific to a wide beam on rcp drift scan. """

        parameters = {

            "ORTA": np.nan,     # On RCP antenna temperature
            "ORDTA": np.nan,    # Error in ORTA
            "ORS2N": np.nan,    # On RCP signal to noise ratio
            "ORTAPEAKLOC": np.nan,  # On RCP peak fit location
            "ORRMSB": np.nan,   # RMS BEFORE SPLINE TO ALL DATA
            "ORRMSA": np.nan,   # RMS AFTER SPLINE TO ALL DATA
            "ORBSLOPE": np.nan,  # Slope of baseline fit
            "ORBSRMS": np.nan  # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_wb_rcp_pss_parameters(self):
        """ Set the parameters specific to a wide beam on rcp pss. """

        parameters = {
            "ORPSS": np.nan,    # On RCP point source sensitivity
            "ORDPSS": np.nan,    # Error in ORPSS
            "ORAPPEFF": np.nan  # On rcp apperture effeciency
        }

        self.combine_parameters(parameters)

    def set_wb_cal_dict(self):
        """ Combine wide beam common calibration parameters. """

        self.set_common_parameters()
        self.set_atmosabs_parameter()
        self.set_flux_parameter()
        self.set_wb_lcp_parameters()
        self.set_wb_lcp_pss_parameters()
        self.set_onlcp_flag_parameter()
        self.set_wb_rcp_parameters()
        self.set_wb_rcp_pss_parameters()
        self.set_onrcp_flag_parameter()

    def set_wb_src_dict(self):
        """ Combine wide beam common target parameters. """

        self.set_common_parameters()
        self.set_atmosabs_parameter()
        self.set_wb_lcp_parameters()
        self.set_onlcp_flag_parameter()
        self.set_wb_rcp_parameters()
        self.set_onrcp_flag_parameter()

    def set_wb_cal_dict_no_comm(self):
        """ Set calibration wide beam parameters without the common parameters."""

        self.set_atmosabs_parameter()
        self.set_flux_parameter()
        self.set_wb_lcp_parameters()
        self.set_wb_lcp_pss_parameters()
        self.set_onlcp_flag_parameter()
        self.set_wb_rcp_parameters()
        self.set_wb_rcp_pss_parameters()
        self.set_onrcp_flag_parameter()

    def set_wb_src_dict_no_comm(self):
        """ Set target wide beam parameters without the common parameters."""

        self.set_atmosabs_parameter()
        self.set_wb_lcp_parameters()
        self.set_onlcp_flag_parameter()
        self.set_wb_rcp_parameters()
        self.set_onrcp_flag_parameter()

    # =========================================================================
    #   NARROW BEAM, 12 GHZ SCAN SETTINGS
    # =========================================================================

    def set_nb_12ghz_tau_parameters(self):
        """ Set Narrow beam 12 GHz tau (optical depth) parameters. """

        parameters = {
            "TAU10": np.nan,
            "TAU15": np.nan}

        self.combine_parameters(parameters)

    def set_nb_12ghz_tbatmos_parameters(self):
        """ Set Narrow beam 12 GHz tbatmos (atmospheric temperature) parameters. """

        parameters = {
            "TBATMOS10": np.nan,
            "TBATMOS15": np.nan}

        self.combine_parameters(parameters)

    def set_comm_weather_parameters(self):
        """
        Set Common weather parameters.
        """

        # TODO: finalize descriptions
        parameters = {
            "PWV": np.nan,  # Precipitable water vapour
            "SVP": np.nan,  # Saturated vapour pressure
            "AVP": np.nan,  # Ambient vapour pressure
            "DPT": np.nan,  # Dew point temperature
            "WVD": np.nan  # Water vapor density
        }

        self.combine_parameters(parameters)

    def set_nb_mean_atm(self):
        """
        Set mean atmospheric correction parameter.
        """

        parameters = {
            "MEAN_ATMOS_CORRECTION": np.nan  # mean atmospheric correction
        }

        self.combine_parameters(parameters)

    def set_nb_hpslcp_fit_parameters(self):
        """
        Set the parameters specific to a narrow beam hps lcp drift scan.
        """

        parameters = {
            "SLTA": np.nan,      # HPS LCP ANTENNA TEMPERATURE
            "SLDTA": np.nan,     # ERROR IN SLTA
            "SLS2N": np.nan,      # HPS LCP SIGNAL TO NOISE RATIO
            "SLTAPEAKLOC": np.nan,  # HPS LCP peak fit location
            "SLFLAG": np.nan,     # HPS LCP SCAN FLAG
            "SLRMSB": np.nan,    # RMS BEFORE SPLINE TO ALL DATA
            "SLRMSA": np.nan,    # RMS AFTER SPLINE TO ALL DATA
            "SLBSLOPE": np.nan,  # Slope of baseline fit
            "SLBSRMS": np.nan   # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_nb_hpnlcp_fit_parameters(self):
        """
        Set the parameters specific to a narrow beam hpn lcp drift scan.
        """

        parameters = {
            "NLTA": np.nan,       # HPN LCP ANTENNA TEMPERATURE
            "NLDTA": np.nan,      # ERROR IN NLTA
            "NLS2N": np.nan,      # HPN LCP SIGNAL TO NOISE RATIO
            "NLTAPEAKLOC": np.nan,  # HPN LCP peak fit location
            "NLFLAG": np.nan,     # HPN LCP SCAN FLAG
            "NLRMSB": np.nan,     # RMS BEFORE SPLINE TO ALL DATA
            "NLRMSA": np.nan,     # RMS AFTER SPLINE TO ALL DATA
            "NLBSLOPE": np.nan,   # Slope of baseline fit
            "NLBSRMS": np.nan    # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_nb_onlcp_fit_parameters(self):
        """
        Set the parameters specific to a narrow beam on lcp drift scan.
        """

        parameters = {
            "OLTA": np.nan,     # On LCP antenna temperature
            "OLDTA": np.nan,    # Error in OLTA
            "OLPC": np.nan,      # On LCP pointing correction
            "COLTA": np.nan,     # Corrected ON LCP antenna temp
            "COLDTA": np.nan,   # Error in COLDTA
            "OLS2N": np.nan,    # On LCP signal to noise
            "OLTAPEAKLOC": np.nan,  # On LCP peak fit location
            "OLFLAG": np.nan,   # On LCP flag
            "OLRMSB": np.nan,   # RMS BEFORE SPLINE TO ALL DATA
            "OLRMSA": np.nan,   # RMS AFTER SPLINE TO ALL DATA
            "OLBSLOPE": np.nan,  # Slope of baseline fit
            "OLBSRMS": np.nan  # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_nb_hpsrcp_fit_parameters(self):
        """
        Set the parameters specific to a narrow beam hps rcp drift scan.
        """

        parameters = {
            "SRTA": np.nan,     # HPS RCP ANTENNA TEMPERATURE
            "SRDTA": np.nan,    # ERROR IN SRTA
            "SRS2N": np.nan,    # HPS RCP SIGNAL TO NOISE RATIO
            "SRTAPEAKLOC": np.nan,  # HPS RCP peak fit location
            "SRFLAG": np.nan,   # HPS RCP SCAN FLAG
            "SRRMSB": np.nan,   # RMS BEFORE SPLINE TO ALL DATA
            "SRRMSA": np.nan,   # RMS AFTER SPLINE TO ALL DATA
            "SRBSLOPE": np.nan,  # Slope of baseline fit
            "SRBSRMS": np.nan  # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_nb_hpnrcp_fit_parameters(self):
        """
        Set the parameters specific to a narrow beam hpn rcp drift scan.
        """

        parameters = {
            "NRTA": np.nan,       # HPN RCP ANTENNA TEMPERATURE
            "NRDTA": np.nan,      # ERROR IN NRTA
            "NRS2N": np.nan,      # HPN RCP SIGNAL TO NOISE RATIO
            "NRTAPEAKLOC": np.nan,  # HPN RCP peak fit location
            "NRFLAG": np.nan,     # HPS RCP SCAN FLAG
            "NRRMSB": np.nan,     # RMS BEFORE SPLINE TO ALL DATA
            "NRRMSA": np.nan,     # RMS AFTER SPLINE TO ALL DATA
            "NRBSLOPE": np.nan,   # Slope of baseline fit
            "NRBSRMS": np.nan    # Rms of baseline fit
        }
        #print(parameters)

        self.combine_parameters(parameters)

    def set_nb_onrcp_fit_parameters(self):
        """
        Set the parameters specific to a narrow beam on lcp drift scan.
        """

        parameters = {
            "ORTA": np.nan,     # On RCP antenna temperature
            "ORDTA": np.nan,    # Error in ORTA
            "ORPC": np.nan,     # ON RCP pointing correction
            "CORTA": np.nan,    # Corrected ON RCP antenna temp
            "CORDTA": np.nan,   # Error in CORDTA
            "ORS2N": np.nan,    # On RCP signal to noise
            "ORTAPEAKLOC": np.nan,  # On RCP peak fit location
            "ORFLAG": np.nan,   # On RCP flag
            "ORRMSB": np.nan,   # RMS BEFORE SPLINE TO ALL DATA
            "ORRMSA": np.nan,   # RMS AFTER SPLINE TO ALL DATA
            "ORBSLOPE": np.nan,  # Slope of baseline fit
            "ORBSRMS": np.nan  # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_nb_onlcp_pss_parameters(self):
        """
        Set the parameters specific to a narrow beam scan on lcp pss.
        """

        parameters = {
            "OLPSS": np.nan,    # On LCP point source sensitivity
            "OLDPSS": np.nan,   # Error in OLPSS
            "OLAPPEFF": np.nan,  # On lcp apperture effeciency
        }

        self.combine_parameters(parameters)

    def set_nb_onrcp_pss_parameters(self):
        """
        Set the parameters specific to a narrow beam scan on rcp pss.
        """

        parameters = {
            "ORPSS": np.nan,    # On RCP point source sensitivity
            "ORDPSS": np.nan,    # Error in ORPSS
            "ORAPPEFF": np.nan  # On rcp apperture effeciency
        }

        self.combine_parameters(parameters)

    def set_nb_cal_dict(self):
        """
            Set Narrow beam calibration data dictionary.
        """

        self.set_common_parameters()
        self.set_flux_parameter()
        self.set_comm_weather_parameters()
        self.set_nb_mean_atm()
        self.set_nb_12ghz_tau_parameters()
        self.set_nb_12ghz_tbatmos_parameters()
        self.set_nb_hpslcp_fit_parameters()
        self.set_nb_hpnlcp_fit_parameters()
        self.set_nb_onlcp_fit_parameters()
        self.set_nb_onlcp_pss_parameters()
        self.set_nb_hpsrcp_fit_parameters()
        self.set_nb_hpnrcp_fit_parameters()
        self.set_nb_onrcp_fit_parameters()
        self.set_nb_onrcp_pss_parameters()

    def set_nb_cal_dict_no_comm(self):
        """
        Set Narrow beam calibration data dictionary without common parameters.
        """

        self.set_flux_parameter()
        self.set_comm_weather_parameters()
        self.set_nb_mean_atm()
        self.set_nb_12ghz_tau_parameters()
        self.set_nb_12ghz_tbatmos_parameters()
        self.set_nb_hpslcp_fit_parameters()
        self.set_nb_hpnlcp_fit_parameters()
        self.set_nb_onlcp_fit_parameters()
        self.set_nb_onlcp_pss_parameters()
        self.set_nb_hpsrcp_fit_parameters()
        self.set_nb_hpnrcp_fit_parameters()
        self.set_nb_onrcp_fit_parameters()
        self.set_nb_onrcp_pss_parameters()

    def set_nb_src_dict(self):
        """
           Set Narrow beam target data dictionary.
        """

        self.set_common_parameters()
        self.set_comm_weather_parameters()
        self.set_nb_mean_atm()
        self.set_nb_12ghz_tau_parameters()
        self.set_nb_12ghz_tbatmos_parameters()
        self.set_nb_hpslcp_fit_parameters()
        self.set_nb_hpnlcp_fit_parameters()
        self.set_nb_onlcp_fit_parameters()
        self.set_nb_hpsrcp_fit_parameters()
        self.set_nb_hpnrcp_fit_parameters()
        self.set_nb_onrcp_fit_parameters()

    def set_nb_src_dict_no_comm(self):
        """
            Set Narrow beam target data dictionary without common parameters.
        """

        self.set_flux_parameter()
        self.set_comm_weather_parameters()
        self.set_nb_mean_atm()
        self.set_nb_12ghz_tau_parameters()
        self.set_nb_12ghz_tbatmos_parameters()
        self.set_nb_hpslcp_fit_parameters()
        self.set_nb_hpnlcp_fit_parameters()
        self.set_nb_onlcp_fit_parameters()
        self.set_nb_hpsrcp_fit_parameters()
        self.set_nb_hpnrcp_fit_parameters()
        self.set_nb_onrcp_fit_parameters()

    # =========================================================================
    #   JUPITER SETTINGS
    # =========================================================================

    def set_nb_22ghz_tau_parameters(self):
        """
        Set Narrow beam 22 GHz tau (optical depth) parameters.
        """

        parameters = {
            "TAU221": np.nan,
            "TAU2223": np.nan}

        self.combine_parameters(parameters)

    def set_nb_22ghz_tbatmos_parameters(self):
        """
        Set Narrow beam 22 GHz tbatmos (atmospheric temperature) parameters.
        """

        parameters = {
            "TBATMOS221": np.nan,
            "TBATMOS2223": np.nan
        }

        self.combine_parameters(parameters)

    def set_jupiter_parameters(self):
        """
            Set Jupiter specific calibration parameters.
        """

        parameters = {
            "HPBW_ARCSEC": np.nan,           # half power beam width in arcseconds
            "ADOPTED_PLANET_TB": np.nan,           # adopted planet temperature brightness
            "PLANET_ANG_DIAM": np.nan,           # planet angular diameter
            "JUPITER_DIST_AU": np.nan,           # jupiter distance in astronomical units
            "SYNCH_FLUX_DENSITY": np.nan,           # synchrotron flux density
            "PLANET_ANG_EQ_RAD": np.nan,           # planet angular equatorial radius
            "PLANET_SOLID_ANG": np.nan,           # planet solid angle in steradians
            "THERMAL_PLANET_FLUX_D": np.nan,           # thermal planet flux density
            "TOTAL_PLANET_FLUX_D": np.nan,           # total planet flux density
            "TOTAL_PLANET_FLUX_D_WMAP": np.nan,   # total planet flux density from WMAP
            "SIZE_FACTOR_IN_BEAM": np.nan,           # size factor in beam
            "SIZE_CORRECTION_FACTOR": np.nan,           # size correction factor
            "MEASURED_TCAL1": np.nan,           # measured noise diode temp in lcp
            "MEASURED_TCAL2": np.nan,           # measured noise diode temp in rcp
            # measured noise diode temp correction factor in lcp
            "MEAS_TCAL1_CORR_FACTOR": np.nan,
            # measured noise diode temp correction factor in rcp
            "MEAS_TCAL2_CORR_FACTOR": np.nan,
            "ATMOS_ABSORPTION_CORR": np.nan,           # atmospheric absorption correction
            "ZA_RAD": np.nan            # zenith angle in radians
        }

        self.combine_parameters(parameters)

    def set_jupiter_dict(self):
        """
        Set jupiter calibration data dictionary.
        """
        self.set_common_parameters()
        self.set_comm_weather_parameters()
        self.set_jupiter_parameters()
        self.set_nb_22ghz_tau_parameters()
        self.set_nb_22ghz_tbatmos_parameters()
        self.set_nb_hpslcp_fit_parameters()
        self.set_nb_hpnlcp_fit_parameters()
        self.set_nb_onlcp_fit_parameters()
        self.set_nb_onlcp_pss_parameters()
        self.set_nb_hpsrcp_fit_parameters()
        self.set_nb_hpnrcp_fit_parameters()
        self.set_nb_onrcp_fit_parameters()
        self.set_nb_onrcp_pss_parameters()

    def set_jupiter_dict_no_comm(self):
        """
        Set jupiter calibration data dictionary without common parameters.
        """

        self.set_comm_weather_parameters()
        self.set_jupiter_parameters()
        self.set_nb_22ghz_tau_parameters()
        self.set_nb_22ghz_tbatmos_parameters()
        self.set_nb_hpslcp_fit_parameters()
        self.set_nb_hpnlcp_fit_parameters()
        self.set_nb_onlcp_fit_parameters()
        self.set_nb_onlcp_pss_parameters()
        self.set_nb_hpsrcp_fit_parameters()
        self.set_nb_hpnrcp_fit_parameters()
        self.set_nb_onrcp_fit_parameters()
        self.set_nb_onrcp_pss_parameters()

    def set_nb_22ghz_src_dict(self):
        """
        Set narrow beam 22 GHz target data dictionary.
        """

        self.set_common_parameters()
        self.set_comm_weather_parameters()
        self.set_nb_22ghz_tau_parameters()
        self.set_nb_22ghz_tbatmos_parameters()
        self.set_nb_hpslcp_fit_parameters()
        self.set_nb_hpnlcp_fit_parameters()
        self.set_nb_onlcp_fit_parameters()
        self.set_nb_hpsrcp_fit_parameters()
        self.set_nb_hpnrcp_fit_parameters()
        self.set_nb_onrcp_fit_parameters()

    def set_nb_22ghz_src_dict_no_comm(self):
        """
        Set narrow beam 22 GHz target data dictionary without common parameters.
        """

        self.set_comm_weather_parameters()
        self.set_nb_22ghz_tau_parameters()
        self.set_nb_22ghz_tbatmos_parameters()
        self.set_nb_hpslcp_fit_parameters()
        self.set_nb_hpnlcp_fit_parameters()
        self.set_nb_onlcp_fit_parameters()
        self.set_nb_hpsrcp_fit_parameters()
        self.set_nb_hpnrcp_fit_parameters()
        self.set_nb_onrcp_fit_parameters()

    # =========================================================================
    #   DUAL BEAM SETTINGS
    # =========================================================================

    def set_db_hpslcp_fit_parameters(self):
        """
        Set dual beam hps lcp parameters.
        """

        parameters = {
            "ASLTA": np.nan,     # A BEAM HPS LCP ANTENNA TEMPERATURE
            "ASLDTA": np.nan,    # A BEAM HPS LCP ERROR IN ANTENNA TEMPERATURE
            "ASLS2N": np.nan,    # A BEAM HPS LCP SIGNAL TO NOISE RATIO
            "ASLTAPEAKLOC": np.nan,  # A BEAM HPS LCP peak fit location
            "BSLTA": np.nan,     # B BEAM HPS LCP ANTENNA TEMPERATURE
            "BSLDTA": np.nan,    # B BEAM HPS LCP ERROR IN ANTENNA TEMPERATURE
            "BSLS2N": np.nan,    # B BEAM HPS LCP SIGNAL TO NOISE RATIO
            "BSLTAPEAKLOC": np.nan,  # B BEAM HPS LCP peak fit location
            "SLFLAG": np.nan,    # HPS LCP SCAN FLAG
            "SLRMSB": np.nan,    # RMS BEFORE SPLINE TO ALL DATA
            "SLRMSA": np.nan,    # RMS AFTER SPLINE TO ALL DATA
            "SLBSLOPE": np.nan,  # Slope of baseline fit
            "SLBSRMS": np.nan   # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_db_hpnlcp_fit_parameters(self):
        """
        Set dual beam hpn lcp parameters.
        """

        parameters = {
            "ANLTA": np.nan,     # A BEAM HPN LCP ANTENNA TEMPERATURE
            "ANLDTA": np.nan,    # A BEAM HPN LCP ERROR IN ANTENNA TEMPERATURE
            "ANLS2N": np.nan,    # A BEAM HPN LCP SIGNAL TO NOISE RATIO
            "ANLTAPEAKLOC": np.nan,  # A BEAM HPN LCP peak fit location
            "BNLTA": np.nan,     # B BEAM HPN LCP ANTENNA TEMPERATURE
            "BNLDTA": np.nan,    # B BEAM HPN LCP ERROR IN ANTENNA TEMPERATURE
            "BNLS2N": np.nan,    # B BEAM HPN LCP SIGNAL TO NOISE RATIO
            "BNLTAPEAKLOC": np.nan,  # A BEAM HPN LCP peak fit location
            "NLFLAG": np.nan,    # HPN LCP SCAN FLAG
            "NLRMSB": np.nan,    # RMS BEFORE SPLINE TO ALL DATA
            "NLRMSA": np.nan,    # RMS AFTER SPLINE TO ALL DATA
            "NLBSLOPE": np.nan,  # HPN LCP Slope of baseline fit
            "NLBSRMS": np.nan   # HPN LCP Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_db_onlcp_fit_parameters(self):
        """
        Set dual beam on lcp parameters.
        """

        parameters = {
            "AOLTA": np.nan,     # A BEAM On LCP antenna temperature
            "AOLDTA": np.nan,    # A BEAM Error in OLTA
            "AOLPC": np.nan,      # A BEAM ON LCP POINTING CORRECTION
            "ACOLTA": np.nan,     # A BEAM Corrected ON LCP antenna temp
            "ACOLDTA": np.nan,   # A BEAM ERROR IN CORRECTED ON LCP ANTENNA TEMPERATURE
            "AOLS2N": np.nan,    # A BEAM On LCP signal to noise
            "AOLTAPEAKLOC": np.nan,  # A BEAM ON LCP peak fit location
            "BOLTA": np.nan,     # B BEAM On LCP antenna temperature
            "BOLDTA": np.nan,    # B BEAM Error in OLTA
            "BOLPC": np.nan,     # B BEAM ON LCP POINTING CORRECTION
            "BCOLTA": np.nan,    # B BEAM Corrected ON LCP antenna temp
            "BCOLDTA": np.nan,   # B BEAM ERROR IN CORRECTED ON LCP ANTENNA TEMPERATURE
            "BOLS2N": np.nan,    # B BEAM On LCP signal to noise RATIO
            "BOLTAPEAKLOC": np.nan,  # B BEAM ON LCP peak fit location
            "OLFLAG": np.nan,    # On LCP flag
            "OLRMSB": np.nan,    # RMS BEFORE SPLINE TO ALL DATA
            "OLRMSA": np.nan,    # RMS AFTER SPLINE TO ALL DATA
            "OLBSLOPE": np.nan,  # Slope of baseline fit
            "OLBSRMS": np.nan   # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_db_hpsrcp_fit_parameters(self):
        """
        Set dual beam hps rcp parameters.
        """

        parameters = {
            "ASRTA": np.nan,     # A BEAM HPS RCP ANTENNA TEMPERATURE
            "ASRDTA": np.nan,    # A BEAM HPS RCP ERROR IN ANTENNA TEMPERATURE
            "ASRS2N": np.nan,    # A BEAM HPS RCP SIGNAL TO NOISE RATIO
            "ASRTAPEAKLOC": np.nan,  # A BEAM HPS RCP peak fit location
            "BSRTA": np.nan,     # B BEAM HPS RCP ANTENNA TEMPERATURE
            "BSRDTA": np.nan,    # B BEAM HPS RCP ERROR IN ANTENNA TEMPERATURE
            "BSRS2N": np.nan,    # B BEAM HPS RCP SIGNAL TO NOISE RATIO
            "BSRTAPEAKLOC": np.nan,  # B BEAM HPS RCP peak fit location
            "SRFLAG": np.nan,    # HPS RCP SCAN FLAG
            "SRRMSB": np.nan,    # RMS BEFORE SPLINE TO ALL DATA
            "SRRMSA": np.nan,    # RMS AFTER SPLINE TO ALL DATA
            "SRBSLOPE": np.nan,  # Slope of baseline fit
            "SRBSRMS": np.nan   # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_db_hpnrcp_fit_parameters(self):
        """
        Set dual beam hpn rcp parameters.
        """

        parameters = {
            "ANRTA": np.nan,     # A BEAM HPN RCP ANTENNA TEMPERATURE
            "ANRDTA": np.nan,    # A BEAM HPN RCP ERROR IN ANTENNA TEMPERATURE
            "ANRS2N": np.nan,    # A BEAM HPN RCP SIGNAL TO NOISE RATIO
            "ANRTAPEAKLOC": np.nan,  # A BEAM HPN RCP peak fit location
            "BNRTA": np.nan,     # B BEAM HPN RCP ANTENNA TEMPERATURE
            "BNRDTA": np.nan,    # B BEAM HPN RCP ERROR IN ANTENNA TEMPERATURE
            "BNRS2N": np.nan,    # B BEAM HPN RCP SIGNAL TO NOISE RATIO
            "BNRTAPEAKLOC": np.nan,  # B BEAM HPN RCP peak fit location
            "NRFLAG": np.nan,    # HPS RCP SCAN FLAG
            "NRRMSB": np.nan,    # RMS BEFORE SPLINE TO ALL DATA
            "NRRMSA": np.nan,    # RMS AFTER SPLINE TO ALL DATA
            "NRBSLOPE": np.nan,  # Slope of baseline fit
            "NRBSRMS": np.nan   # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_db_onrcp_fit_parameters(self):
        """
        Set dual beam on rcp parameters.
        """

        parameters = {
            "AORTA": np.nan,     # A BEAM On RCP antenna temperature
            "AORDTA": np.nan,    # A BEAM Error in ORTA
            "AORPC": np.nan,     # A BEAM ON RCP POINTING CORRECTION
            "ACORTA": np.nan,    # A BEAM Corrected ON RCP antenna tempERATURE
            "ACORDTA": np.nan,   # A BEAM ERROR IN CORRECTED ON RCP ANTENNA TEMPERATURE
            "AORS2N": np.nan,    # A BEAM On RCP signal to noise RATIO
            "AORTAPEAKLOC": np.nan,  # A BEAM ON RCP peak fit location
            "BORTA": np.nan,     # B BEAM On RCP antenna temperature
            "BORDTA": np.nan,    # B BEAM Error in ORTA
            "BORPC": np.nan,     # B BEAM ON RCP POINTING CORRECTION
            "BCORTA": np.nan,    # B BEAM Corrected ON RCP antenna temp
            "BCORDTA": np.nan,   # B BEAM ERROR IN CORRECTED ON RCP ANTENNA TEMPERATURE
            "BORS2N": np.nan,    # B BEAM On RCP signal to noise
            "BORTAPEAKLOC": np.nan,  # B BEAM ON RCP peak fit location
            "ORFLAG": np.nan,    # On RCP flag
            "ORRMSB": np.nan,    # RMS BEFORE SPLINE TO ALL DATA
            "ORRMSA": np.nan,    # RMS AFTER SPLINE TO ALL DATA
            "ORBSLOPE": np.nan,  # Slope of baseline fit
            "ORBSRMS": np.nan,   # Rms of baseline fit
        }

        self.combine_parameters(parameters)

    def set_db_onlcp_pss_parameters(self):
        """
        Set dual beam on lcp pss parameters.
        """

        parameters = {
            "AOLPSS": np.nan,    # A BEAM On LCP point source sensitivity
            "AOLDPSS": np.nan,   # A BEAM Error in OLPSS
            "AOLAPPEFF": np.nan,  # A Beam On lcp apperture effeciency
            "BOLPSS": np.nan,    # B BEAM On LCP point source sensitivity
            "BOLDPSS": np.nan,   # B BEAM Error in OLPSS
            "BOLAPPEFF": np.nan  # B Beam On lcp apperture effeciency
        }

        self.combine_parameters(parameters)

    def set_db_onrcp_pss_parameters(self):
        """
        Set dual beam on rcp pss parameters.
        """

        parameters = {
            "AORPSS": np.nan,    # A BEAM On RCP point source sensitivity
            "AORDPSS": np.nan,   # A BEAM Error in ORPSS
            "AORAPPEFF": np.nan,  # A Beam On rcp apperture effeciency
            "BORPSS": np.nan,    # B BEAM On RCP point source sensitivity
            "BORDPSS": np.nan,    # B BEAM Error in ORPSS
            "BORAPPEFF": np.nan  # B Beam On rcp apperture effeciency
        }

        self.combine_parameters(parameters)

    def set_db_weather_parameters(self):
        """
        Set dual beam weather related parameters.
        """

        # TODO: complete descriptions
        parameters = {
            "SEC_Z": np.nan,  # secant of zenith
            "X_Z": np.nan,
            "DRY_ATMOS_TRANSMISSION": np.nan,  # dry atmospheric transmission
            # zenith tau (optical depth) at 1400m
            "ZENITH_TAU_AT_1400M": np.nan,
            "ABSORPTION_AT_ZENITH": np.nan  # absorption at zenith
        }

        self.combine_parameters(parameters)

    def set_db_cal_dict(self):
        """
        Set dual beam calibrator parameters
        """

        self.set_common_parameters()
        self.set_flux_parameter()
        self.set_comm_weather_parameters()
        self.set_db_weather_parameters()
        self.set_db_hpslcp_fit_parameters()
        self.set_db_hpnlcp_fit_parameters()
        self.set_db_onlcp_fit_parameters()
        self.set_db_onlcp_pss_parameters()
        self.set_onlcp_flag_parameter()
        self.set_db_hpsrcp_fit_parameters()
        self.set_db_hpnrcp_fit_parameters()
        self.set_db_onrcp_fit_parameters()
        self.set_db_onrcp_pss_parameters()
        self.set_onrcp_flag_parameter()

    def set_db_cal_dict_no_comm(self):
        """
        Set dual beam calibrator parameters
        without the common settings.
        """

        self.set_flux_parameter()
        self.set_comm_weather_parameters()
        self.set_db_weather_parameters()
        self.set_db_hpslcp_fit_parameters()
        self.set_db_hpnlcp_fit_parameters()
        self.set_db_onlcp_fit_parameters()
        self.set_db_onlcp_pss_parameters()
        self.set_onlcp_flag_parameter()
        self.set_db_hpsrcp_fit_parameters()
        self.set_db_hpnrcp_fit_parameters()
        self.set_db_onrcp_fit_parameters()
        self.set_db_onrcp_pss_parameters()
        self.set_onrcp_flag_parameter()

    def set_db_src_dict(self):
        """
        Set dual beam target source parameters
        """

        self.set_common_parameters()
        self.set_comm_weather_parameters()
        self.set_db_weather_parameters()
        self.set_db_hpslcp_fit_parameters()
        self.set_db_hpnlcp_fit_parameters()
        self.set_db_onlcp_fit_parameters()
        self.set_onlcp_flag_parameter()
        self.set_db_hpsrcp_fit_parameters()
        self.set_db_hpnrcp_fit_parameters()
        self.set_db_onrcp_fit_parameters()
        self.set_onrcp_flag_parameter()

    def set_db_src_dict_no_comm(self):
        """
        Set dual beam target parameters
        without the common settings.
        """

        self.set_comm_weather_parameters()
        self.set_db_weather_parameters()
        self.set_db_hpslcp_fit_parameters()
        self.set_db_hpnlcp_fit_parameters()
        self.set_db_onlcp_fit_parameters()
        self.set_onlcp_flag_parameter()
        self.set_db_hpsrcp_fit_parameters()
        self.set_db_hpnrcp_fit_parameters()
        self.set_db_onrcp_fit_parameters()
        self.set_onrcp_flag_parameter()
