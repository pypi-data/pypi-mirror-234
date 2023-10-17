# Miscellaneous functions
import os

print(__import__(__name__.split('.')[0]))

from inits import logfile

def delete_logs():
    """
    Delete the logfile if it exists
    """

    # delete any previous log file
    try:
        os.remove(logfile)
    except OSError:
        pass

    