# =========================================================================== #
# File   : messages.py                                                        #
# Author : Pfesesani V. van Zyl                                               #
# =========================================================================== #
import os

def print_start():
    """ Print program banner. """

    no_tabs = 2 # number of tab spaces
    print("###########"*(no_tabs*3))
    print("#", "\t"*(no_tabs*4), "#")
    print("#", "\t"*no_tabs, "######  ######  ###### #    # ", "\t"*no_tabs, "#")
    print("#", "\t"*no_tabs, "#     # #    #  #    # # #  # ", "\t"*no_tabs, "#")
    print("#", "\t"*no_tabs, "#     # #####   ###### #  # # ", "\t"*no_tabs, "#")
    print("#", "\t"*no_tabs, "#     # #    #  #    # #   ## ", "\t"*no_tabs, "#")
    print("#", "\t"*no_tabs, "######  #    #  #    # #    # ", "\t"*no_tabs, "#")
    print("#", "\t"*(no_tabs*4), "#")
    print("###########"*(no_tabs*3))
    disclaimer()

def disclaimer():
    """ Print disclaimer. """

    print("\n* Disclaimer *: DRAN is a data reduction and analysis software ")
    print("pipeline developed to systematically reduce and analyze HartRAO's ")
    print("26m telescope drift scan data. It comes with no guarantees ")
    print("whatsoever, but the author does attempt to assist those who use it") 
    print("to get meaningful results.")
    
def msg_wrapper(log_name, log, msg):
    """ Wraps logging messages. 
    
        Args:
            log_name (str)  : The name of the logger e.g. info
            log (object)    : The logging object
            msg (str)       : The message to be wrapped.
    """

    # setup wrappers
    wrappers = {
        'error': "* ERROR * : ",
        'warning': "WARNING! : ",
        'info': "# >>> ",
        'debug': "> DEBUG : ",
        'basic': "# -- "
    }

    log("\n"+wrappers[log_name]+msg)

def load_prog(prog):
    """
    Print message to load the selected program.
    """

    os.system("clear")
    print_start()
    n=66 # number of asterics
    print("\n")
    print("*"*n,"\n")
    print(f"\tLoading: {prog}\n")
    print("*"*n,"\n")