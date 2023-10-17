
# ============================================================================#
# File: commands.py                                                     #
# Author: Pfesesani V. van Zyl                                                #
# ============================================================================#

# Standard library imports
# --------------------------------------------------------------------------- #
import sys

# Local imports
# --------------------------------------------------------------------------- #
sys.path.append("src/")
from common.messaging import msg_wrapper
# =========================================================================== #


class Command:
    """
        The Command class manages a set of commands with associated descriptions.
        These commands are typically used for controlling and interacting with a program.
        The class optimizes memory usage by storing command descriptions in a single dictionary.
        Each command is a key in the dictionary, and its associated information, including usage,
        short descriptions, and detailed descriptions, is stored as values.

        Attributes:
            commands (dict): A dictionary containing available commands as keys and their
            associated information as values.

        Methods:
            __init__(): Initializes the Command class by setting up the dictionary of commands
            and their descriptions.
            
            get_commands(): Returns the dictionary of available commands and their associated information.
            This method is used to access command information.

        Usage:
            cmd = Command()
            available_commands = cmd.get_commands()
            for command, info in available_commands.items():
                print(f"Command: {command}")
                print(f"Usage: {info['use']}")
                print(f"Short Description: {info['shortdesc']}")
                print(f"Description: {info['desc']}\n")
    """

    def __init__(self):
        
        self.commands={
            'read': {
                'use': 'read [filename or filepath]',
                'shortdesc': 'read in a file',
                'desc': '''\n Read drift scan data from the file given.\
                        \n If the filename is not given as part of the command string,\
                        \n the user is prompted for the filename parameter. \
                        \n The filename parameter[filename or filepath] is the name \
                        \n or full path of the file to read from. It is \
                        \n assumed the file name/path is not given at the start \
                        \n of the program. Please review code documentation for more info.'''
            },
            
            'reset': {
                'use': 'reset',
                'shortdesc': 'reset all parameters to default settings',
                'desc': '''\nReset data to default values. 
            \n Deletes all previously fit data and sets the data to those of 
            \n the original drift scan file.'''
            },

            'show': {
                'use': 'show ',
                'shortdesc': 'display the file extracted parameters',
                'desc': '''Show all the parameters that were extracted from the file. 
                This prints out a dictionary of all the source parameters of interest of 
                a given source.\n\nExample: show\n\n You can also show parameters that 
                have already been established like the baseline fit points, the peak fit points 
                and the current scan being processed\n\nExample:\n\nshow bf\n\nshow pf \n\nshow scan'''
            },
            'bf': {
                'use': 'bf [list of points to fit] order',
                'shortdesc': 'list all fitting blocks',
                'desc': '''Set the start and end blocks for fitting a polynomial to the baseline of a spectrum. 
                If PB is entered without parameters, the current values are shown
        and the user is prompted for another start, end velocity pair.

        If PB is entered with start and end velocities, these are added to the
        current list of start, end pairs.

        If SHOW is given as the second parameter, the current values are shown.

        If CLEAR is given as the second parameter, all values are cleared.

        Baseline block limits must be set prior to an automated polynomial fit.
        These may be present from a previous fit, and can be seen using PB SHOW
        otherwise they must be entered using PB, or set via a previous PO fit.+

        After carrying out a polynomial fit, the baseline blocks that were used
        are stored and can be reused.  Executing PB after PO will show the start
        and end values of each block.  This can be exploited when processing many
        spectra of the same source:
        * use RAV to average many or all of the spectra, to obtain a high
        signal to noise ratio and show up weak features
        * use PO to fit a polynomial to the average spectrum
        * use a DO loop to:
            * read the individual spectra
                * fit polynomials to the spectra using PO with PB option
                * write out each spectrum to a new file

        example:

        pb - 100 - 45
        pb - 30 - 10
        pb 0.5 90'''
            },
            'pf': {
                'use': 'pf [list of points to fit] order',
                'shortdesc': 'give the locations where the fit is to be performed',
                'desc': 'Set the start and end velocities of blocks for fitting a polynomial to the baseline of a spectrum...'
            },
            'fit': {
                'use': 'fit [list of points to fit] order',
                'shortdesc': 'perform a polynomial fit on the listed data points',
                'desc': 'Set the start and end velocities of blocks for fitting a polynomial to the baseline of a spectrum...'
            },
            'cs': {
                'use': 'cs 1',
                'shortdesc': 'change drift-scan',
                'desc': '''Change the scan that is currently 
        being processed. By default, upon opening a file the scan number is 0
        which can indicate one of the following.
        
        For low frequencies e.g. 2280 MHz, there are only 2 scans, 
        ONLCP = 0
        ONRCP = 1
        
        For higher frequencies with 6 scans,  
        HPSLCP = 0
        HPNLCP = 1
        ONLCP = 2
        HPSRCP = 3
        HPNRCP = 4
        ONRCP = 5
        
        \n\nExample:\n\ncs 1'''

            },
            'exit': {
                'use': 'exit',
                'shortdesc': 'exit the program',
                'desc': 'Exits the program...'
            },
            'pl': {
                'use': 'pl ',
                'shortdesc': 'plot the data',
                'desc': 'Plot the data...'
            }
        }

        self.cmdList=self.commands.keys()
        
    def get_commands(self):
        return self.commands