# =========================================================================== #
# File    : log_conf.py                                                       #
# Author  : Pfesesani V. van Zyl                                              #
# =========================================================================== #

# Standard library imports
# --------------------------------------------------------------------------- #
import logging
import sys

# Local imports
# --------------------------------------------------------------------------- #
sys.path.append("src/")
from common.messaging import msg_wrapper
from inits import logfile
# =========================================================================== #

# setup logger object
logger = logging.getLogger('root')

def configure_logging(toggle="on"):
    """ Setup the logging configuration. 
    
        This creates the log object used to log the code in the program.
        By default all logging information with a level of debug is saved to file and only information with a logging level of info and above is logged to screen. 
    
        returns:
            logger (object): the logging object.
    """

    # create log file and set log levels
    logger.setLevel(logging.DEBUG)
    handler1 = logging.FileHandler(logfile, mode='a')
    logger.addHandler(handler1)

    # setup the format of the file logger
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    handler1.setFormatter(formatter)
    logger.debug("Logging initiated")

    configure_console_logger("off")

    return logger

def configure_console_logger(toggle="on"): #off
    """ Setup the console logger. 
    
        Args:
            toggle (str): toggle the console setting on or off. Default is off.
            When on, debugging is printed to console else debugging printed to file.
    """

    handler2 = logging.StreamHandler(sys.stdout)

    # configure message logging level to info on default
    if toggle=="off":
        handler2.setLevel(logging.INFO)
    else:
        handler2.setLevel(logging.DEBUG)
    logger.addHandler(handler2)