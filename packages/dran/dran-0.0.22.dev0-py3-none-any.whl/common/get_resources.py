import importlib.resources as resources
import pandas as pd 

def get_cal_list() -> pd.DataFrame:
    """ Get list of calibrator names from file"""
    with resources.path("predefs", "cal_names_list.txt") as df:
        return pd.read_fwf(df,names=['CALS'])
    
def get_jpl_results() -> pd.DataFrame:
    """ Get list of calibrator names from file"""
    with resources.path("predefs", "nasa_jpl_results.txt") as df:
        return pd.read_csv(df,delimiter=",", skiprows=1, names=['DATE','MJD','RA','DEC','ANG-DIAM'])
    
def get_calsky_results(year) -> pd.DataFrame:
    """ Get list of calibrator names from file"""
    with resources.path("predefs", f"Jupiter_calsky_{year}.dat") as df:
        return pd.read_csv(df,delimiter=",", skiprows=1, names=['month','day','ra','dec','radius'])
    