# =========================================================================== #
# File    : fitting.py                                                        #
# Author  : Pfesesani V. van Zyl                                              #
# =========================================================================== #

# Standard library imports
# --------------------------------------------------------------------------- #
import os
import sys
import numpy as np
from scipy import interpolate
from sklearn.metrics import mean_squared_error
import bisect
from scipy.optimize import curve_fit
import matplotlib.pyplot as pl

# Local imports
# --------------------------------------------------------------------------- #
from common.messaging import msg_wrapper
import common.exceptions as ex
# =========================================================================== #


def f(x):
    # convert values to floats
    try:
        return np.float(x)
    except:
        return np.nan
    
def sig_to_noise(signalPeak, noise,log):
    """ 
    Calculate the signal to noise ratio. 
    
    Args:
        signalPeak (float) : The maximum valueof a desired signal
        noise (array): array of fit residuals
        log(object): file logging object
        
    Returns:
        sig2noise (float): signal to noise ratio
    """
    sig2noise = signalPeak/np.std(noise)
    #sig2noise = signalPeak/(max(noise)+abs(min(noise)))
    return sig2noise

def check_for_nans(x,log):
    """ Check for missing data or incomplete data.
    
        Parameters:
            x (array): A 1D array
            log (object): Logging object.
        
        Returns:
            flag (int): The flag value
            x (array) : A 1D array without any NAN values
    """

    isNan = np.argwhere(np.isnan(x))
    if len(isNan) > 0 or len(x) == 0:
        msg_wrapper("debug", log.debug,
                    "Found NANs, file has no data")
        x = np.zeros_like(x)
        flag = 1
        return x, flag
    else:
        msg_wrapper("debug", log.debug,
                    "Checked data has no missing values")
        flag = 0
        return x, flag

def spline_(x, y, anchor_points=9, order=3):
    '''
        Given a set of data points (x,y) determine a smooth spline
        approximation of degree k on the interval x[0] <= x <= x[n]

        Args:
            x (array): 1D array of data representing the x-axis
            y (array): 1D array of data representing the y-axis
            anchor_points (int): the number of anchor points in the data
            order (int): polynomial order to fit, preferrably a cubic spline
        Return:
            spline_fit (array): Spline of the data
    '''

    scanLen = len(x)


    if scanLen <= anchor_points*2:
        print("Too few points to interpolate, consider entering lower knot points")
        print("spline not set")
        spline_fit=[]
    else:
        #anchor_points=7
        anchor_points_intervals = scanLen/anchor_points  # intervals where anchor points will be placed
        anchor_points_pos = [] # list to hold positions where anchor_points will be placed olong the array
        anchor_points_counter = 0 # position counter or locator 

        # create a list of the positions where the anchor_points will be located
        #anchor_points=10
        for i in range(anchor_points-1):
            anchor_points_counter = anchor_points_counter + anchor_points_intervals
            anchor_points_pos.append(int(anchor_points_counter))

        # interpolate the data
        # create linearly spaced data points
        x1 = np.linspace(1, scanLen, scanLen)
        x2 = np.array((anchor_points_pos), int)	# create array of anchor_points positions
        
        try:
            tck = interpolate.splrep(x1, y, k=order, task=-1,
                                    t=x2)  # interpolate, k=5 is max
            spline_fit = interpolate.splev(x1, tck, der=0)
        except:
            print("Failed to interpolate, Error on input data,too few points, min required = 9")
            spline_fit=y

        pl.plot(x,y)
        pl.plot(x,spline_fit)
        pl.plot(x[anchor_points_pos],spline_fit[anchor_points_pos],'r.')
        pl.show()
        pl.close()
        sys.exit()
    return spline_fit,anchor_points_pos

def spline(x, y, anchor_points=9, order=3):
    '''
        Given a set of data points (x,y) determine a smooth spline
        approximation of degree k on the interval x[0] <= x <= x[n]

        Args:
            x (array): 1D array of data representing the x-axis
            y (array): 1D array of data representing the y-axis
            anchor_points (int): the number of anchor points in the data
            order (int): polynomial order to fit, preferrably a cubic spline
        Return:
            spline_fit (array): Spline of the data
    '''

    scanLen = len(x)
    if scanLen <= anchor_points*2:
        print("Too few points to interpolate, consider entering lower knot points")
        print("spline not set")
        spline_fit=[]
    else:
        #anchor_points=7
        anchor_points_intervals = scanLen/anchor_points  # intervals where anchor points will be placed
        anchor_points_pos = [] # list to hold positions where anchor_points will be placed olong the array
        anchor_points_counter = 0 # position counter or locator 

        # create a list of the positions where the anchor_points will be located
        #anchor_points=10
        for i in range(anchor_points-1):
            anchor_points_counter = anchor_points_counter + anchor_points_intervals
            anchor_points_pos.append(int(anchor_points_counter))

        # interpolate the data
        # create linearly spaced data points
        x1 = np.linspace(1, scanLen, scanLen)
        x2 = np.array((anchor_points_pos), int)	# create array of anchor_points positions
        
        try:
            tck = interpolate.splrep(x1, y, k=order, task=-1,
                                    t=x2)  # interpolate, k=5 is max
            spline_fit = interpolate.splev(x1, tck, der=0)
        except:
            print("Failed to interpolate, Error on input data,too few points, min required = 9")
            spline_fit=y

        #print(len(x),len(spline_fit))
    #     #print(spline_fit)
    #     pl.plot(x,y,'k.')
    #     pl.plot(x,spline_fit,'r')
    #    # pl.plot(nx[anchor_points_pos],spline_fit[anchor_points_pos],'r.')
    #     pl.show()
    #     pl.close()
    #     print('closed')
    #     sys.exit()
    return spline_fit#,anchor_points_pos

def spline_fit(x, y, anchor_points=9, order=3):
    '''
        Given a set of data points (x,y) determine a smooth spline
        approximation of degree k on the interval x[0] <= x <= x[n]

        Args:
            x (array): 1D array of data representing the x-axis
            y (array): 1D array of data representing the y-axis
            anchor_points (int): the number of anchor points in the data
            order (int): polynomial order to fit, preferrably a cubic spline
        Return:
            spline_fit (array): Spline of the data
    '''

    nx=[]
    ny=[]
    # remove nan values
    for i in range(len(x)):
        #print(i,y[i],type(y[i]))
        if y[i] == np.nan or str(y[i]) =="nan":
            #print(i,y[i])
            pass
        else:
            nx.append(x[i])
            ny.append(y[i])

    scanLen = len(nx)
    if scanLen <= anchor_points*2:
        print("Too few points to interpolate, consider entering lower knot points")
        print("spline not set")
        spline_fit=[]
    else:
        #anchor_points=7
        anchor_points_intervals = scanLen/anchor_points  # intervals where anchor points will be placed
        anchor_points_pos = [] # list to hold positions where anchor_points will be placed olong the array
        anchor_points_counter = 0 # position counter or locator 

        # create a list of the positions where the anchor_points will be located
        #anchor_points=10
        for i in range(anchor_points-1):
            anchor_points_counter = anchor_points_counter + anchor_points_intervals
            anchor_points_pos.append(int(anchor_points_counter))

        # interpolate the data
        # create linearly spaced data points
        x1 = np.linspace(1, scanLen, scanLen)
        x2 = np.array((anchor_points_pos), int)	# create array of anchor_points positions
        
        try:
            tck = interpolate.splrep(x1, ny, k=order, task=-1,
                                    t=x2)  # interpolate, k=5 is max
            spline_fit = interpolate.splev(x1, tck, der=0)
        except:
            print("Failed to interpolate, Error on input data,too few points, min required = 9")
            spline_fit=ny

        #print(len(x),len(spline_fit))
        #print(spline_fit)
    #     pl.plot(x,y,'k.')
    #     pl.plot(nx,spline_fit,'r')
    #    # pl.plot(nx[anchor_points_pos],spline_fit[anchor_points_pos],'r.')
    #     pl.show()
    #     pl.close()
    #     print('closed')
    #     sys.exit()
    return nx,spline_fit#,anchor_points_pos

def clean_rfi(x, y, log=""):
    """
        Clean the RFI in the data using iterative rms cuts. 
        
        Parameters:
            x (array): Array of the independent variable
            y (array): Array of the dependent variable
            log (object): file logging object

        returns: 
            finX (array): the data representing the x-axis after the removal of rfi data
            finY (array):the data representing the y-axis after the removal of rfi data
            rmsBeforeClean (int): the rms before removal of rfi data
            rmsAfterClean (int): the rms after removal of rfi data
            finspl (array): the spline of the cleaned data
            pointsDeleted (int): number of points deleted when cleaning the data
    """

    msg_wrapper("debug", log.debug, "Cleaning the data of RFI")

    # spline the data
    splined_data = spline(x, y)
    scanLen = len(x)
    resRFI, rmsBeforeClean, rmsAfterClean, finX, finY, finRes, finMaxSpl, finspl, pointsDeleted = clean_data(
        splined_data, x, y, scanLen,log)

    msg_wrapper("debug", log.debug, "Splined RMS before: after cleaning -> {:.3f}: {:.3f} \n".format
                (rmsBeforeClean, rmsAfterClean))

    # pl.title("RFI removal")
    # pl.ylabel('Ta [K]')
    # pl.xlabel('Scandist [Deg]')
    # pl.plot(x,y,label='raw data')
    # pl.plot(finX,finY,label='clean data')
    # pl.legend(loc='best')
    # pl.show()
    return finX, finY, rmsBeforeClean, rmsAfterClean, finspl, pointsDeleted

def clean_data(spl, x, y, scanLen, log=""):
    """
        Clean the data using iterative fitting. 

        Args:
            spl : 1d array
                the splined data
            x : 1d array
                data representing the x-axis
            y : 1d array
                data representing the y-axis
            scanLen : int
                length of the drift scan array
            log : object
                file logging object

        Returns:
            resRFI: 1d array
                the residual before the rfi has been removed
            rmsBeforeClean: int
                the rms before removing rfi data
            rmsAfterClean: int
                the rms after removal of rfi data
            finX: 1d array
                the data representing the x-axis after the removal of rfi data
            finY: 1d array
                the data representing the y-axis after the removal of rfi data
            finRes: 1d array
                the residual of the cleaned data after the rfi has been removed
            finMaxSpl: int
                the maximum of the spline of the cleaned data
            finspl: 1d array
                the spline of the cleaned data
            pointsDeleted: int
                number of points deleted when cleaning the data
    """
    
    #msg_wrapper("debug", log.debug, "Iterative cleaning of RFI")

    # calculate the residual and clean the data
    resRFI, rmsBeforeClean = calc_residual(spl, y,log)
    finX, finY, rmsAfterClean, finRes, finMaxSpl, finspl, pointsDeleted = clean_data_iterative_fitting(
        x, y, scanLen, resRFI, rmsBeforeClean,log)

    return resRFI, rmsBeforeClean, rmsAfterClean, finX, finY, finRes, finMaxSpl, finspl, pointsDeleted

def calc_residual(model, data, log=""):
    """
        Calculate the residual and rms between the model and the data.

        Parameters:
            model (array): 1D array containing the model data
            data (array): 1D array containing the raw data
            log (object): file logging object

        Returns
        -------
        res: 1d array
            the residual
        rms: int
            the rms value
    """

    #print('model: ',model)
    #print('data: ',data)
    res = np.array(model - data)
    rms = np.sqrt(mean_squared_error(data, model))

    return res, rms

def poly_coeff(x, y, deg):
    '''
        Calculate the polynomial coeffecients depending 
        on the degree/order of the polynomial

        Args:
            x (array): 1d array
                data representing the x-axis
            y (array): 1d array
                data representing the y-axis
            deg(int): degree of the polynomial

        Return:
            array of polynomial fitted data
    '''

    return np.polyfit(x, y, deg)

def calc_residual_and_rms(x,y,order=1):
    """Calculate the residual and rms from data
    
        Args:
            x (array): 1d array
            data representing the x-axis
            y (array): 1d array
                data representing the y-axis
            deg(int): degree of the polynomial

        Return:
            model (array): model of 
            res (array):
            rms (float):
            coeff():
        """
    #TODO: remove redundant code
    
    # fit the baseline and get best fit coeffecients
    coeffs = poly_coeff(x, y, order)

    print('coeffs: ',coeffs)

    # get a model for the fit using the best fit coeffecients
    model = np.polyval(coeffs, x)

    #print('model: ', model)

    # Calculate the residual and rms
    res, rms = calc_residual(y, model)

    return model, res, rms, coeffs

def calc_residual_and_rms_fit(x,y,order=1):
    """Calculate the residual and rms from data
    
        Args:
            x (array): 1d array
            data representing the x-axis
            y (array): 1d array
                data representing the y-axis
            deg(int): degree of the polynomial

        Return:
            model (array): model of 
            res (array):
            rms (float):
            coeff():
        """
    #TODO: remove redundant code
    
    nx=[]
    ny=[]
    # remove nan values
    for i in range(len(x)):
        #print(i,y[i],type(y[i]))
        if y[i] == np.nan or str(y[i]) =="nan":
            #print(i,y[i])
            pass
        else:
            nx.append(x[i])
            ny.append(y[i])

    # fit the baseline and get best fit coeffecients
    coeffs = poly_coeff(nx, ny, order)

    print('coeffs: ',coeffs)

    # get a model for the fit using the best fit coeffecients
    model = np.polyval(coeffs, nx)

    #print('model: ', model)

    # Calculate the residual and rms
    res, rms = calc_residual(ny, model)

    return nx, model, res, rms, coeffs
    
def clean_data_iterative_fitting(x, y, scanLen, res, rms, log="",x2=""):
    ''' Find the best fit to the data by iteratively eliminating data points
    that fall beyond an established cut-off limit.

        Parameters
        ----------
        x : 1d array
            data representing the x-axis
        y : 1d array
            data representing the y-axis
        scanLen : int
            length of the drift scan array
        res: 1d array
            the residual
        rms: int
            the rms value
        log : object
            file logging object
        x2 : 1d array
            filenames

        Returns
        -------
            finalX: 1d array
                the data representing the x-axis after the removal of rfi data
            finalY: 1d array
                the data representing the y-axis after the removal of rfi data
            finalRms: int
                the rms after removal of rfi data
            finRes: 1d array
                the residual of the cleaned data after the rfi has been removed
            finMaxSpl: int
                the maximum of the spline of the cleaned data
            finalSplinedData: 1d array
                the spline of the cleaned data
            pointsDeleted: int
                number of points deleted when cleaning the data
    '''

    #msg_wrapper("debug", log.debug, "Performing RFI cuts on data")
    # ToDo: Make this more effecient

    # set initial values
    smallestY = y
    smallestX = x

    # set final value parameters
    finalNames=[]
    finalX = []
    finalY = []
    finalRms = []
    finalRes = []
    finalMaxSpl = []
    finalSplinedData = []
    smallest = True
    loop = 0

    while smallest:

        #While you don't have the smallest rms, process data

        loop = loop+1
        #print('loop: ',loop)

        #Remove spikes
        if len(x2)==0:
            newX, newY = _remove_RFI(smallestX, smallestY, res, rms)
        else:
            #print('k')
            newX, newY ,newNames= _remove_RFI(smallestX, smallestY, res, rms,log,x2)
            finalNames=newNames

        newX = np.array(newX)
        newY = np.array(newY)
       
        #spline the data if you found RFI
        splineData2 = spline(newX, newY)
        maxSplineData2 = max(splineData2)
        res2, rms2 = calc_residual(splineData2, newY)

        # pl.plot(x,y)
        # pl.plot(newX,newY)
        # pl.plot(newX,splineData2)
        # pl.show()
        # pl.close()

        if rms2 < rms:  # get better values
            rms = rms2
            res = res2
            smallestX = newX
            smallestY = newY
            finalX = newX
            finalY = newY
            finalRms = rms2
            finalRes = res2
            finalSplinedData = splineData2
            finalMaxSpl = maxSplineData2
            if len(x2)!=0:
                #print('o')
                finalNames=newNames
            smallest = True
        else:
            smallest = False

    # If the rms cut only looped once, values dont change
    if loop == 1:

        # If you already have good data, keep values as they are
        finalX = x
        finalY = y
        finalRms = rms
        finalRes = res

        #spline the data
        finalSplinedData = spline(x, y)
        finalMaxSpl = max(finalSplinedData)

        if len(x2)==0:
            #print('p')
            finalNames=x2

    pointsDeleted = scanLen-len(finalY)

    if len(x2)==0:
        return finalX, finalY, finalRms, finalRes, finalMaxSpl, finalSplinedData, pointsDeleted
    else:
        #print('s')
        print(f'\n{abs(len(x)-len(finalNames))} entries removed, after {loop} iterations\n{len(finalNames)} remaining\n')
        #sys.exit()
        return finalX, finalY, finalRms, finalRes, finalMaxSpl, finalSplinedData, pointsDeleted, finalNames
    
def _remove_RFI(x, y, res, rms, log="",x2=""):
    '''
            Removes data points with a residual cutt-off
            more or less than 2.7*rms

            Parameters
            ----------
            x : 1d array
                data representing the x-axis
            y : 1d array
                data representing the y-axis
            res: 1d array
                the residual
            rms: int
                the rms value
            log : object
                file logging object

            Returns
            -------
            cleanX: 1d array
                array of data representing the x-axis
            cleanY: 1d array
                array of data representing the cleaned y-axis data
    '''

    scanLen = len(x)
    cleanX, cleanY, names = ([] for i in range(3))  # create new lists
    cut=3#2.7
    if len(x2)==0:
        for i in range(scanLen):
            if(abs(res[i]) > cut * rms):  # 2.5, 2.7 3.0
                pass
            else:
                # Keep points that lie within the cut_off
                cleanX.append(x[i])
                cleanY.append(y[i])

        return cleanX, cleanY
    else:
        #print('n')
        for i in range(scanLen):
            if(abs(res[i]) > cut* rms):  # 2.5, 2.7 3.0
                pass
            else:
                # Keep points that lie within the cut_off
                cleanX.append(x[i])
                cleanY.append(y[i])
                names.append(x2[i])

        #print('len names: ',len(names))
        return cleanX, cleanY, names

def get_baseline_pts(x, y, indexList, log=""):
    """
        Get baseline points from a list of 
        indexes.

        Parameters
        ----------
        x : 1d array
            data representing the x-axis
        y : 1d array
            data representing the y-axis
        indexList: 1d array
            a list of numbers used to index the data
        log : object
            file logging object
    """

    msg="getting baseline points"
    msg_wrapper("debug", log.info, msg)

    # Get data between the indexes selected
    indList=sorted(indexList)

    # get location of all points
    xb_data, yb_data = ([] for i in range(2))  # create new lists

    if len(indList) == 2:

        ind1 = indList[0]
        ind2 = indList[1]
        xb_data = xb_data + list(x[ind1:ind2])
        yb_data = yb_data + list(y[ind1:ind2])
    else:
        for i in range(len(indList)):
            if i % 2 == 0 and i != 1:
                ind1 = indList[i]
                ind2 = indList[i+1]
                xb_data = xb_data + list(x[ind1:ind2])
                yb_data = yb_data + list(y[ind1:ind2])

    return xb_data, yb_data

def locate_baseline_blocks_auto(x, y, peakCenterGuess,hfnbw,log=""):
    """
        Find the locations to fit a baseline automatically.

        These locations are found/determined by fitting a 
        spline to the data and using the 
        locations of the local minimum as baseline regions.

        Parameters:
            x (array): 1D array of data representing the x-axis
            y (array): 1D array of data representing the y-axis
            peakCenterGuess (float): value of x at peak center in x array
            hfnbw (float): half the first null beam width
            log (object): loffing object
    """

    # setup parameters
    msg = "" # message to write on plot
    flag = 0 # error flag, default to no error detected 
    saveFolder = "currentScanPlots/"

    # generate a spline to help locate where to best fit our baseline model.
    yspl = spline(x, y)

    # find location of maximum peak, assumed to be at center
    try:
        peakPosition = (np.where(x >= peakCenterGuess)[0])[0]
        peakSpline = np.where(yspl == max(yspl))[0]
    except Exception:
        msg = "Failed to determine center peak location"
        msg_wrapper("warning",log.warning,msg)
        flag = 22
        return [], [], [], 0, flag, msg, 0, 0, 0, 0
    
    # LOCATE LOCAL MINUMUM/MAXIMUM POSITIONS
    # these values are used to figure out where to
    # select our baseline points/locations
    localMinPositions = (np.diff(np.sign(np.diff(yspl))) > 0).nonzero()[
        0] + 1  # local min positions / first nulls
    localMaxPositions = (np.diff(np.sign(np.diff(yspl))) < 0).nonzero()[
        0] + 1  # local max positions / peak

    # print(f'mins: {localMinPositions}, maxs: {localMaxPositions}')
    ymax=max(yspl)
    
    # Delete min point within 50 points of a max point
    p=25
    dels=[]
    for i in range(len(localMaxPositions)):
        window=np.arange(localMaxPositions[i]-p,localMaxPositions[i]+p,1)
        for j in range(len(localMinPositions)):
            if localMinPositions[j] in window:
                print(j, localMinPositions[j] , i, localMaxPositions[i])#, window)
                dels.append(localMinPositions[j] )
   
    if len(dels)!=0:
        for k in range(len(dels)):
            if dels[k] in localMinPositions:
                
                localMinPositions=list(localMinPositions)
                ind=localMinPositions.index(dels[k])
                del localMinPositions[ind]
    localMinPositions=np.array(localMinPositions)

    
    print(f'min locs: {localMinPositions}, max locs: {localMaxPositions}')
    
    # pl.plot(x,yspl)
    # pl.plot(x[window],y[window],'m.')
    
    # pl.plot(x[localMinPositions],yspl[localMinPositions],'r.')
    # pl.plot(x[localMaxPositions],yspl[localMaxPositions],'k.')
    
    # #pl.show()
    # sys.exit()

    
    #print(len(localMinPositions), len(localMaxPositions))

    #if len(localMaxPositions)==0:
    if len(localMinPositions) == 0 :
        msg = "Failed to locate local min positions, set to FNBW locs"
        msg_wrapper("warning", log.warning, msg)
        flag = 21

        try:
            h=np.where(x<=-hfnbw)[0][-1]
        except:
            h=x[0]
        #print("hfnbw: ",hfnbw,", len: ",len(x),x[0],x[-1])
        
        try:
            # write better notes on why i do this
            hh=[np.where(x>=hfnbw)[0][0]][0]
        except:
            hh=x[-1]

        localMinPositions=[h,hh]

        #print(localMinPositions)
        #print(h,hh,localMinPositions)
        #sys.exit()
        # print(f'mins: {localMinPositions}, maxs: {localMaxPositions}')
        # pl.plot(x,y)
        # pl.plot(x,yspl)
        # pl.plot(x[localMinPositions],yspl[localMinPositions],'r.')
        # pl.show()

        #return [], [], [], 1, flag, msg, 0, 0, 0, 0

    if len(localMinPositions) == 0 or len(localMaxPositions) == 0:
        msg = "Failed to locate local min and max positions"
        msg_wrapper("warning", log.warning, msg)
        flag = 19
        return [], [], [], 1, flag, msg, 0, 0, 0, 0

    # localMinPositions must be = 2, number of local minimum positions found
    # IF MORE ARE FOUND WE MOST PROBABLY HAVE SIDELOBES
    numberOfMinPositions = len(localMinPositions)

    # Find the index or insertion point for the peakPosition in the
    # locMinPositions list. i.e. where we most likely expect the 
    # peak to be located.
    peakInd = bisect.bisect(localMinPositions, peakPosition)
    scanLen = len(x)

    # basic parameter info
    msg_wrapper("debug", log.debug, "-"*30)
    msg_wrapper("debug",log.debug,"Drift scan basic info: ")
    msg_wrapper("debug",log.debug,"-"*30)
    msg_wrapper("debug", log.debug,
                "Found local minimums at = {}".format(localMinPositions))
    msg_wrapper("debug", log.debug,
                "Found local maximums at = {}".format(localMaxPositions))

    msg_wrapper("debug", log.debug, "no local min positions = {} \nindex of peak in local mins = {}".format(numberOfMinPositions, peakInd))
    #msg_wrapper("debug", log.info, "Length of scan = {}".format(scanLen))

    # check location of peak
    msg_wrapper("debug", log.debug, "Peak locations: ")
    msg_wrapper("debug", log.debug, "Peak pos from Gauss fit: {}\nPeak pos from Spline fit: {} \nPeak pos if at mid of scan: {}\n".format(
        peakPosition, peakSpline[0], int(scanLen/2)))

    # plot all local min/max positions
    '''pl.plot(x, y)
    pl.plot(x, yspl)
    pl.ylabel("Ta [K]")
    pl.xlabel("offset [deg]")
    pl.title("Plot of fit locations for baseline")
    for i in range(len(localMinPositions)):
        if i==0:
            pl.plot(x[localMinPositions[i]],
                yspl[localMinPositions[i]], 'k*', label="minimums")
        else:
            pl.plot(x[localMinPositions[i]],
                    yspl[localMinPositions[i]], 'k*')
    for i in range(len(localMaxPositions)):
        if i==0:
            pl.plot(x[localMaxPositions[i]],
                    yspl[localMaxPositions[i]], 'r*', label="peaks")
        else:
            pl.plot(x[localMaxPositions[i]],
                yspl[localMaxPositions[i]], 'r*')
    pl.legend(loc="best")
    pl.show()
    pl.savefig(saveFolder+"peaksandmins.png")
    pl.close()'''

    # Ensure peak falls within expected range, beyond 25% of the length and
    # below 75% of the length of thee drift scan.
    peakLocMinLimit = int(scanLen*.25)
    peakLocMaxLimit = int(scanLen*.75)

    #print("peakPosition: ",peakPosition)
    #print("peakLocMinLimit: ", peakLocMinLimit)
    #print("peakLocMaxLimit: ", peakLocMaxLimit)
    if ( peakPosition < peakLocMinLimit or peakPosition > peakLocMaxLimit ):

        msg = "\nPeak not within expected range."
        msg_wrapper("info", log.info, msg)
        flag=20
        msg_wrapper("info", log.info, "Peak limit left: {} \nPeak position: {} \nPeak limit right: {}\n".format(
            peakLocMinLimit, peakPosition, peakLocMaxLimit))
        return [],[],[],1,flag,msg,[],[],0,0

    else:

        # locate/setup fnbw location on left and right of beam
        # if we can't locate base locations program defaults
        # to fnbw locations
        try:
            leftFNBWPoint = (np.where(x >= (peakCenterGuess-hfnbw))[0])[0]
        except:
            leftFNBWPoint = []

        try:
            rightFNBWPoint = (np.where(x >= (peakCenterGuess+hfnbw))[0])[0]
        except:
            rightFNBWPoint = []

        if rightFNBWPoint == 0 or leftFNBWPoint == 0:
            flag=27
            msg="Failed to locate FNBW locations"
            msg_wrapper("info", log.info, msg)
            return [], [], [], 1, flag, msg, 0, 0, 0, 0

        msg_wrapper("debug", log.debug, "Location of FNBW: ")
        msg_wrapper("debug", log.debug, "HFNBW: {} \nleft fnbw loc: {} \nright fnbw loc: {}\n".format(
            hfnbw, leftFNBWPoint, rightFNBWPoint))

        # SEARCH FOR MINIMUMS
        # We only need two points, one on left of peak and one on right of peak
        # if we have more points this means there are side lobes and we
        # need to adjust the baseline accordingly
        msg_wrapper("debug", log.debug,
                    "Finding locations of local minimum from scan: ")

        # set fault parameters
        rf = 0  # right is faulty
        lf = 0  # left is faulty

        if peakInd == 0 and len(localMinPositions) == 1:
            # there is only one peak index position found

            if localMinPositions[peakInd] < peakPosition:
                # the position found is to the left of the assumed peak location

                minPosOnLeftOfPeak = localMinPositions
                minPosOnRightOfPeak = rightFNBWPoint
                msg_wrapper("debug", log.debug,
                            "leftMinLoc found: {}\n".format(minPosOnLeftOfPeak))
                msg_wrapper("debug", log.debug, "setting rightMinLoc: {}\n".format(
                    minPosOnRightOfPeak))
                flag = 6
                rf = 1
                msg = "Failed to locate right min pos"
                msg_wrapper("info", log.info,msg)

            if localMinPositions[peakInd] > peakPosition:
                # the position found is to the right of the assumed peak location

                minPosOnLeftOfPeak = leftFNBWPoint
                minPosOnRightOfPeak = localMinPositions
                msg_wrapper("debug", log.debug,"setting leftMinLoc: {}\n".format(minPosOnLeftOfPeak))
                msg_wrapper("debug", log.debug,"rightMinLoc found: {}\n".format(
                    minPosOnRightOfPeak))

                flag = 7
                lf = 1
                msg = "Failed to locate left min pos"
                msg_wrapper("info", log.info,msg)

        elif peakInd < len(localMinPositions):

            if (localMinPositions[peakInd] < peakPosition) or (localMinPositions[peakInd] > peakPosition):
                # grab all the local min positions to the left and right of the peak

                minPosOnLeftOfPeak = localMinPositions[:peakInd]
                minPosOnRightOfPeak = localMinPositions[peakInd:]
      
                msg_wrapper("debug", log.debug,"all leftMinLoc: {}\n".format(minPosOnLeftOfPeak))
                msg_wrapper("debug", log.debug,"all rightMinLoc: {}\n".format(minPosOnRightOfPeak))

                if len(minPosOnLeftOfPeak) == 0:
                    # there are no left min positons, set left min to fnbw point
                    minPosOnLeftOfPeak = leftFNBWPoint
                    flag = 7
                    lf = 1
                    msg = "Failed to locate left min pos"
                    msg_wrapper("info", log.info, msg)

                if len(minPosOnRightOfPeak) == 0:
                    # there are no right min positions, set right min to fnbw point
                    minPosOnRightOfPeak = rightFNBWPoint
                    flag = 6
                    rf = 1
                    msg = "Failed to locate right min pos"
                    msg_wrapper("info", log.info, msg)

        else:

            if localMinPositions[peakInd-1] < peakPosition:
                # can't find local mins beyond peak

                minPosOnLeftOfPeak = localMinPositions[:peakInd]
                minPosOnRightOfPeak = rightFNBWPoint
                msg_wrapper("debug", log.debug,"cleftMinLoc: {}\n".format(minPosOnLeftOfPeak))
                msg_wrapper("debug", log.debug,"rightMinLoc: {}\n".format(
                    minPosOnRightOfPeak))

                flag = 6
                rf = 1
                msg = "Failed to locate right min pos"
                print(msg)

            if localMinPositions[0] > peakPosition:
                # all local mins are beyond peak

                minPosOnLeftOfPeak = leftFNBWPoint
                minPosOnRightOfPeak = localMinPositions
                msg_wrapper("debug", log.debug,
                            "setting leftMinLocs : {}\n".format(minPosOnLeftOfPeak))
                msg_wrapper("debug", log.debug, "rightMinLoc beyond peak: {}\n".format(
                    minPosOnRightOfPeak))

                flag = 7
                lf = 1
                msg = "Failed to locate left min pos"
                print(msg)

        # Determine if data has large sidelobes by evaluating the region
        # around the center peak
        maxPosInMaxs = localMaxPositions[np.abs(localMaxPositions-peakPosition).argmin()]
        indOfmaxPosInMaxs = np.where(localMaxPositions == maxPosInMaxs)[0]

        msg_wrapper("debug", log.debug, "local max positions: {} \nmaxPosInMaxs: {} \nIndexOfMaxPos: {} \nlenmaxpos: {} ".format(localMaxPositions, maxPosInMaxs, indOfmaxPosInMaxs,len(localMaxPositions)))

        sidelobes = 0  # data contains no sidelobes
        msg_wrapper("debug", log.debug, "\n* Looking for large sidelobes")

        if len(localMaxPositions) > 1:
            # theres more than one peak

            if len(localMaxPositions) == indOfmaxPosInMaxs[0]:
                leftSidelobe = localMaxPositions[indOfmaxPosInMaxs[0]-1]
                rightSidelobe = localMaxPositions[indOfmaxPosInMaxs[0]]
            else:
                if indOfmaxPosInMaxs == len(localMaxPositions)-1:
                    leftSidelobe = localMaxPositions[indOfmaxPosInMaxs[0]-1]
                    rightSidelobe = []
                else:
                    leftSidelobe = localMaxPositions[indOfmaxPosInMaxs[0]-1]
                    rightSidelobe = localMaxPositions[indOfmaxPosInMaxs[0]+1]

            maxPeakInSpline = yspl[maxPosInMaxs]
            halfOfMaxPeakInSpline = 0.5*maxPeakInSpline

            # check if sidelobes are larger than half the peak
            if (yspl[leftSidelobe] >= halfOfMaxPeakInSpline) or (yspl[rightSidelobe] >= halfOfMaxPeakInSpline):

                # large sidelobes detected
                msg_wrapper("info", log.info, "Large sidelobes detected: {} < {} < {}".format(
                    yspl[leftSidelobe], maxPeakInSpline, yspl[rightSidelobe]))
                sidelobes = 1
                msg = "Large sidelobes detected"
                flag = 9
            else:
                msg_wrapper("info", log.info, "No sidelobes detected\n")

        elif len(localMaxPositions) == 1:
            sidelobes = 0
            msg_wrapper("info", log.info, "No sidelobes detected\n")
        else:
            msg_wrapper("info", log.info, "\nFailed to locate a maximum")
            sys.exit()

        maxloc = np.where(yspl==max(yspl))[0]
        #print(maxloc,maxloc[0],len(yspl),yspl[0],yspl[-1])

        if maxloc[0] < leftFNBWPoint or maxloc[0]> rightFNBWPoint:
            # found peak in noise
            msg_wrapper("info", log.info,"peak found in baselocs")
            msg = "peak found in baselocs"
            flag = 16

            # we have sidelobes
            # find local min positions ----------------------------------------
            locminpos = (np.diff(np.sign(np.diff(yspl))) > 0).nonzero()[0] + 1
            baseLine, leftBaselineBlock, rightBaselineBlock, minPosOnLeftOfPeak, minPosOnRightOfPeak, lp, rp = get_base(
                locminpos,int((scanLen*.05)/2), len(x))
                #locminpos, int((scanLen*.05)/2), len(x)), # why 5% ???
            # ----------------------------------------------------------------

            #print(lp, rp)

            # pl.plot(x,y)
            # pl.plot(x,yspl)
            # pl.plot(x[leftBaselineBlock], y[leftBaselineBlock], 'b.')
            # pl.plot(x[rightBaselineBlock],y[rightBaselineBlock],'m.')
            # pl.plot(x[lp], y[lp], 'k.')
            # pl.plot(x[rp],y[rp],'k*')
            # pl.plot(x[minPosOnLeftOfPeak],yspl[minPosOnLeftOfPeak],"y*")
            # pl.plot(x[minPosOnRightOfPeak], yspl[minPosOnRightOfPeak], "r*")
            # pl.show()
            # pl.close()
            # sys.exit()
            sidelobes=1
            #sys.exit()
            return baseLine, leftBaselineBlock, rightBaselineBlock, sidelobes, flag, msg, minPosOnLeftOfPeak, minPosOnRightOfPeak,lp,rp
            #return [],[],[],1,flag,msg,[],[],0,0

        else:

            # print(minPosOnRightOfPeak,minPosOnLeftOfPeak,[minPosOnLeftOfPeak])
            # pl.plot(x,y)
            # pl.plot(x,yspl)
            # pl.plot(x[leftBaselineBlock], y[leftBaselineBlock], 'b.')
            # pl.plot(x[rightBaselineBlock],y[rightBaselineBlock],'m.')
            # pl.plot(x[lp], y[lp], 'k.')
            # pl.plot(x[rp],y[rp],'k*')
            # pl.plot(x[minPosOnLeftOfPeak],yspl[minPosOnLeftOfPeak],"y*")
            # pl.plot(x[minPosOnRightOfPeak], yspl[minPosOnRightOfPeak], "r*")
            # pl.show()
            # pl.close()
            # sys.exit()
            try:
                type(minPosOnRightOfPeak)
                # check you are returned something, dummy check
    
            except:
                print("No minPosOnRightOfPeak")
                flag=6
                msg="Failed to locate right min pos"
                return [], [], [], np.nan, flag, msg, np.nan, np.nan, [], []

            try:
                # check you are returned something, dummy check
                type(minPosOnLeftOfPeak)
            except:
                print("No minPosOnLeftOfPeak")
                flag=7
                msg="Failed to locate left min pos"
                return [], [], [], np.nan, flag, msg, np.nan, np.nan, [], []

            # print(type(minPosOnLeftOfPeak).__name__)
            if(type(minPosOnRightOfPeak).__name__) != 'ndarray':

                if(type(minPosOnRightOfPeak).__name__) == 'list':
                    pass
                else:
                    try:
                        minPosOnRightOfPeak=[minPosOnRightOfPeak]
                    except:
                        minPosOnRightOfPeak = [len(x)-100]

            if(type(minPosOnLeftOfPeak).__name__) != 'ndarray':
                if(type(minPosOnRightOfPeak).__name__) == 'list':
                    # pass
                    ls=[]
                    # check all values are integers
                    for val in minPosOnLeftOfPeak:
                        print(type(val).__name__)
                        if "float" in (type(val).__name__):
                            pass
                        else:
                            ls.append(val)
                    minPosOnLeftOfPeak=ls

                
                else:
                    try:
                        minPosOnLeftOfPeak=[minPosOnLeftOfPeak]
                    except:
                        minPosOnLeftOfPeak = [100]


            print("\n* Center of baseline blocks on left and right of peak: ")
            #print(leftFNBWPoint, maxloc, rightFNBWPoint, minPosOnRightOfPeak)
            print("min pos left: {} @ loc/s {}\nmin pos right: {} @ loc/s {}\nscan len: {}".format(
               x[minPosOnLeftOfPeak],minPosOnLeftOfPeak, x[minPosOnRightOfPeak],minPosOnRightOfPeak,scanLen))
            # print(minPosOnLeftOfPeak)
            # sys.exit()

            # Select the points to fit your baseline
            pl.title("Baseline points selection")
            pl.plot(x, y)
            pl.plot(x, yspl)
            pl.plot(x[minPosOnLeftOfPeak], yspl[minPosOnLeftOfPeak], 'r*', label="left local minumums")
            pl.plot(x[minPosOnRightOfPeak], yspl[minPosOnRightOfPeak], 'y*',label="right local minimums")
            pl.legend(loc='best')
            # pl.show()
            try:
                pl.savefig(saveFolder+"baselocpoints.png")
            except:
                pass
            pl.close('all')
            # sys.exit()

            # Locate the baselines
            # the number of points to use for baseline on each side of beam
            # limited to 5% of length of the scan, this works well for 
            # situations where there are large sidelobes e.g. Jupiter
            maxPointsInBaselineBlock = int(scanLen*.05)
            hMaxPointsInBaselineBlock = int(maxPointsInBaselineBlock/2)
            nums = np.arange(1, scanLen, 1)  # array of numbers from 1 to len(list)

            # set left and right baseline points placeholders
            lb=[]
            rb=[]

            # Get baseline block on left of beam
            if type(minPosOnLeftOfPeak).__name__ == "int64":

                if lf == 1:
                    # left is faulty, set baseline points
                    leftBaselineBlock = np.arange(0, minPosOnLeftOfPeak-hMaxPointsInBaselineBlock, 1)

                    lb = lb+[0, minPosOnLeftOfPeak-hMaxPointsInBaselineBlock]

                else:
                    leftBaselineBlock = np.arange(
                        minPosOnLeftOfPeak-hMaxPointsInBaselineBlock, minPosOnLeftOfPeak+hMaxPointsInBaselineBlock, 1)
                    lb = lb+[minPosOnLeftOfPeak-hMaxPointsInBaselineBlock, minPosOnLeftOfPeak+hMaxPointsInBaselineBlock]

                    if minPosOnLeftOfPeak < len(leftBaselineBlock):
                        # min pos left is too close to the edge, adjust accordingly
                        leftBaselineBlock = np.arange(0, len(leftBaselineBlock), 1)
                        lb = lb+[0, len(leftBaselineBlock)]
                        print("mix: ", leftBaselineBlock)
                        sys.exit()

            else:

                leftBaselineBlock = []
                slots = []
              
                if lf == 0:
                    #print(minPosOnLeftOfPeak,len(minPosOnLeftOfPeak),"\n")

                    for i in range(len(minPosOnLeftOfPeak)):
                        slots = (np.arange(
                            minPosOnLeftOfPeak[i]-hMaxPointsInBaselineBlock, minPosOnLeftOfPeak[i]+hMaxPointsInBaselineBlock, 1))
                        lb = lb+[minPosOnLeftOfPeak[i]-hMaxPointsInBaselineBlock,
                                 minPosOnLeftOfPeak[i]+hMaxPointsInBaselineBlock]
                        for j in range(len(slots)):
                            leftBaselineBlock.append(slots[j])
                else:
                    # struggled to find left base so use all data to fnbw point
                    #print(minPosOnLeftOfPeak)

                    if len(minPosOnLeftOfPeak)==1:
                        leftBaselineBlock = np.arange(0,minPosOnLeftOfPeak[0],1)

                    lb = lb+[0,minPosOnLeftOfPeak[0]]
                    flag=7
                    msg="Failed to locate left min pos"
                    print(msg)
                    
                    #sys.exit()
            
            # Get baseline block on right of beam
            if type(minPosOnRightOfPeak).__name__ == "int64":

                if rf == 1:
                    flag=6
                    msg="Failed to locate right min pos"
                    rightBaselineBlock = np.arange(minPosOnRightOfPeak+hMaxPointsInBaselineBlock, scanLen, 1)
                    rb= rb+[minPosOnRightOfPeak +
                             hMaxPointsInBaselineBlock, scanLen]
                else:

                    rightBaselineBlock = np.arange(minPosOnRightOfPeak-hMaxPointsInBaselineBlock, minPosOnRightOfPeak+hMaxPointsInBaselineBlock, 1)
                    rb=rb+[minPosOnRightOfPeak-hMaxPointsInBaselineBlock,
                             minPosOnRightOfPeak+hMaxPointsInBaselineBlock]
                    #print("rb: ", rb)
                    if (scanLen - len(rightBaselineBlock)) < minPosOnRightOfPeak:
                        # min pos right is too close to the edge, adjust accordingly
                        rightBaselineBlock = np.arange(scanLen - len(rightBaselineBlock), scanLen, 1)
                        rb= rb+[scanLen - len(rightBaselineBlock), scanLen]
                    #print("rb: ",rb)
            else:
                rightBaselineBlock=[]
                slots = []
                #rf=[]

                if rf == 0:
                    for i in range(len(minPosOnRightOfPeak)):

                        end=minPosOnRightOfPeak[i]+hMaxPointsInBaselineBlock
                        if end>len(x):
                            end = len(x)#-1
                        else:
                            pass

                        slots=(np.arange(
                            minPosOnRightOfPeak[i]-hMaxPointsInBaselineBlock, end-1, 1))
                        rb = rb+[minPosOnRightOfPeak[i]-hMaxPointsInBaselineBlock, end-1]

                        #print("rb+: ", rb)
                        #print(minPosOnRightOfPeak[i]+hMaxPointsInBaselineBlock)

                        for j in range(len(slots)):
                            rightBaselineBlock.append(slots[j])
                            #print("slots: ",slots[j])
                else:
                    #print(minPosOnRightOfPeak)
                    #print(rightFNBWPoint, maxPointsInBaselineBlock, scanLen)
                    rightBaselineBlock = np.arange(
                        scanLen-maxPointsInBaselineBlock, scanLen, 1)

                    rb = rb+[scanLen-maxPointsInBaselineBlock, scanLen-1]
                    #print("rb+1: ",rb)
                    flag = 6
                    msg = "Failed to locate right min pos"
                          
            # ensure data makes sence
            try:
                # find if data contains negatives and move/shift points
                # forward

                zeroIndex = leftBaselineBlock.index(0)
                #print("\nzeroIndex found at index: {}".format(zeroIndex))
                
                # find the difference between adjacent numbers and identify
                # where to allocate shift
                res = np.array([leftBaselineBlock[i + 1] - leftBaselineBlock[i] for i in range(len(leftBaselineBlock)-1)])
                    #print(res)
                    
                if len(res)>0:
                        # if more than one location for baseline is selected,
                        # determine shift and adjust accordingly
                        l = np.where(res!=1)[0]
                        #("shift parameter: ",l)
                        #print("value at shift parametera: ",leftBaselineBlock[l[0]],"\n")
                        left = leftBaselineBlock[zeroIndex:l[0]+1]
                        right = leftBaselineBlock[l[0]+1:]
                        s = np.arange(
                            leftBaselineBlock[l[0]]+1, leftBaselineBlock[l[0]]+1+zeroIndex, 1)
                        shiftedBlock = left+list(s)+right #np.arange(0, shift,1)
                        #print("shiftedleftbaselineblock: ", shiftedBlock)
                        leftBaselineBlock = shiftedBlock
                        print("Shifted baseline block")
        
                else:
                    pass
            except Exception:
                pass

            try:
                # find if data contains goes beyond max of scan 
                # and move/shift points backwards
                maxIndex = rightBaselineBlock.index(scanLen)
                #print("maxIndex: {}".format(maxIndex))
        
                # find the difference between adjacent numbers and identify
                # where to allocate shift
                res = np.array([rightBaselineBlock[i + 1] - rightBaselineBlock[i] for i in range(len(rightBaselineBlock)-1)])
                #print(res)

                if len(res)>0:
                    # if more than one location for baseline is selected,
                    # determine shift and adjust accordingly
                    l = np.where(res != 1)[0]
                    #print("shift parameter: ",l)

                    if len(l) == 0:
                        print("Shifting entire block")
                        last = rightBaselineBlock[-1]
                        shift =abs(scanLen-last)
                        shiftedBlock = np.arange(
                            rightBaselineBlock[0]-shift, scanLen, 1)
                        #print("shiftedrightbaselineblock: ", shiftedBlock)
                        rightBaselineBlock = shiftedBlock

                    else:
                        #print("value at shift parameterb: ",
                        #    rightBaselineBlock[l[0]], "\n")
                        print("Shifting block")

                        if len(l)==1:
                            left = rightBaselineBlock[:l[0]+1]
                            right = rightBaselineBlock[l[0]+1:]
                            shift = abs(rightBaselineBlock[-1]-scanLen)
                            s = np.arange(
                                rightBaselineBlock[l[0]+1]-shift, rightBaselineBlock[-1]-shift, 1)
                            shiftedBlock = left+list(s)
                            #print("shiftedrightbaselineblock: ", shiftedBlock)
                            rightBaselineBlock = shiftedBlock

                        elif len(l)==2:
                            #print("Length l > 1")
                            
                            # find value closest to max
                            nearest = min(l, key=lambda t: abs(t-maxIndex))
                            index=[np.where(l==nearest)[0]][0]
                            #print(nearest,index[0])
                            #print("value at shift parameter: ",
                            #    rightBaselineBlock[nearest], "\n")
                            # shift backwards
                            left = rightBaselineBlock[:nearest+1]
                            right = rightBaselineBlock[nearest+1:]
                            #print("left: ", left)
                            #print("right: ", right)
                            shift = abs(rightBaselineBlock[-1]-scanLen)
                            #print("shifting back by: ", shift)
                            s = np.arange(
                                rightBaselineBlock[nearest+1]-shift, rightBaselineBlock[-1]-shift, 1)
                            shiftedBlock = left+list(s)
                            #print("shiftedrightbaselineblock: ", shiftedBlock)
                            rightBaselineBlock = shiftedBlock

                        else:
                            #print("l > 2")
                            msg = "\nToo many shift parameters."
                            print(msg)
                            flag=18
                            print("Peak limit left: {} \nPeak position: {} \nPeak limit right: {}\n".format(peakLocMinLimit, peakPosition, peakLocMaxLimit))
                            sys.exit()
                            return [],[],[],1,flag,msg,np.nan    
            except Exception:
                pass

            pl.title("Plot with baseline blocks outlined")
            pl.plot(x, y)
            pl.plot(x, yspl)
            pl.plot(x[leftBaselineBlock], y[leftBaselineBlock], 'r.')
            pl.plot(x[rightBaselineBlock], y[rightBaselineBlock], 'r.')
            pl.plot(x[lb],yspl[lb],'y*')
            pl.plot(x[rb],yspl[rb],'y*')
            # pl.show()
            try:
                pl.savefig(saveFolder+"baselocs.png")
            except:
                pass
            pl.close()
            #sys.exit()
            
            # create a single baseline block
            baseLine = list(leftBaselineBlock) + list(rightBaselineBlock)
            baseLine = np.array(baseLine, int)

            # print(leftBaselineBlock,rightBaselineBlock)
            # sys.exit()
            return baseLine, leftBaselineBlock, rightBaselineBlock, sidelobes, flag, msg, minPosOnLeftOfPeak, minPosOnRightOfPeak,lb,rb

def locate_baseline_blocks_fnbw(x, hfnbw):
    """
        Find the locations to fit a baseline. We assume the 
        baseline gives a good fit beyond the fnbw points on either
        side of the beam.
    """

    # If all looks we'll get the locations or positions where
    # a first order polynomial is going to be fit in order to
    # correct for any drift in the data. We are assuming that the
    # data is devoid of any RFI beyond the fnbw locations on either
    # side of the main beam
    left=-hfnbw#coeff[1]-hfnbw
    right=hfnbw#coeff[1]+hfnbw
    baseLine = np.where(np.logical_or(
        x <= left, x >= right))[0]

    # get coeffecients of a first order polynomial fit to
    # either ends of the baseline selection locations
    # baseline locations to the left of the beam
    leftBaseline = np.where(x <= left)[0]
    # baseline locations to the right of the beam
    rightBaseline = np.where(x >= right)[0]

    sidelobes=0 # no sidelobes/sidelobes ignored

    return baseLine, leftBaseline, rightBaseline, sidelobes

def fit_gauss_lin(x, y, p):

    """ 
        Fit data with a gaussian. The function uses the python 
        module curve_fit which uses a non-linear least square 
        to fit a function f, to data. It assumes
        ydata = f(xdata, params_list) + eps.

        Parameters:
            x (1d array): data representing the x-axis
            y (1d array): data representing the y-axis
            p (tuple): tuple of gaussian parameters

        Returns:
            coeff (list): Best fit coeffecients 
            covarMatrix(matrix): the covariant matrix
            fit (list): gaussian fit with the best fit parameters.
    """

    # fit initial guess parameters to data and get best fit parameters
    # returns best fit coeffecients and
    coeff, covarMatrix = curve_fit(gauss_lin, x, y, p)

    # Get gaussian fit with best parameters
    fit = gauss_lin(x, *coeff)
    # pl.plot(x,y)
    # pl.plot(x,fit)
    # pl.show()
    # pl.close()

    return coeff, fit

def gauss_lin(x, *p):
    """
        Generate a gaussian plus first-order polynomial to fit the drift scan beam. Note that the width of the Gaussian is hard-coded to the half-power beamwidth.

        Parameters
        ----------
            x : 1D array
                1D array of data representing the x-axis
            p : tuple
                tuple of gaussian parameters 

        Returns
        -------
            gaussFit: 1d array 
                array of data representing the gaussian fit
     """

    amp, mu, hpbw, a, c = p
    sigma = hpbw/(2*np.sqrt(2*np.log(2)))
    gaussFit = amp*np.exp(-(x-mu)**2/(2.*sigma**2)) + a*x + c
    return gaussFit

def correct_drift(xBase, yBase, x, log,order=1):
    '''
        Correct for a drifting baseline in the scan by fitting
        a first order polynomial to a region with no
        signal.	

        Parameters
        -----------
            xBase : x data of the baseline
            yBase : y data of the baseline
            x : x data of the entire drift scan
    '''

    # fit the baseline and get best fit coeffecients
    driftModel, driftRes, driftRms, driftCoeffs = calc_residual_and_rms(
        xBase, yBase, order)
    dataModel = np.polyval(driftCoeffs, x)

    msg_wrapper("info", log.info, "Fit the baseline")
    print("*"*60)
    msg = "Fit = {:.3}x + ({:.3}), rms error = {:.3}".format(driftCoeffs[0], driftCoeffs[1], driftRms)
    msg_wrapper("info", log.info, msg)

    return dataModel, driftModel, driftRes, driftRms, driftCoeffs

def fit_beam(x, y, p, fnbw, dec, data, scanNum, force, log,fitTheoretical,autoFit=None):
    """
        Fit single beam data.

        Parameters:
            x (array): 1D array of data representing the x-axis
            y (array): 1D array of data representing the y-axis
            p (list): list of initial fit parameters
            fnbw (float): source first null beam width from file
            dec (float): source declination
            data (dict): dictionary of source parameters
            scanNum (int):  Value representing the current scan
            force (str): String to determine whether to force a fit or not   
            log (object): loffing object
    """

    # Setup parameters
    scanLen = len(x)                # length of the scan
    hhpbw = p[2]/2                  # half of the hpbw
    hfnbw = fnbw/2                  # half of the fnbw
    flag = 0                        # default flag set to zero
    msg = ""                          # flag message to go on plot
    saveFolder = "currentScanPlots/"

    # pl.plot(x,y)
    # pl.show()
    # pl.close()

    # Try to fit a gaussian to determine peak location
    # this also works as a bad scan filter
    try:
        coeff, fit = fit_gauss_lin(x, y, p)
        print('gauss fit test: ',f'{max(fit):.3f} [K]')
        # pl.plot(x,y)
        # pl.show()
        # pl.close()
    except Exception as e:
        print(e)
        msg = "gaussian curve_fit algorithm failed"
        msg_wrapper("debug", log.debug, msg)
        flag = 3
        #pl.plot(x,y)
        #pl.show()
        #pl.close()
        #sys.exit()

        if force=="y":
            pass
        else:
            return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan,0,0

    if autoFit !=None and len(autoFit)>1:

        #print(autoFit, autoFit['baselocs'])

        #print(float(autoFit['baselocs']))
        # fit baseline
        # 2) correct the drift in the data and get the residual and rms
        baseLocs=[]#np.where()[0]

        for i in range(len(autoFit['baselocs'])):
            if i%2==0:
                #print(autoFit['baselocs'][i],autoFit['baselocs'][i+1])
                if i==0:
                    baseLocsl=np.where((x>=autoFit['baselocs'][i]) & (x<=autoFit['baselocs'][i+1]))[0]
                else:
                    baseLocsr=np.where((x>=autoFit['baselocs'][i]) & (x<=autoFit['baselocs'][i+1]))[0]

                d=np.where((x>=autoFit['baselocs'][i]) & (x<=autoFit['baselocs'][i+1]))[0]
                baseLocs=baseLocs+list(d)

        #print(baseLocs)
        #baseLocsl=x[b1]
        #baseLocsr=x[b2]
        lb=[baseLocsl[0],baseLocsl[-1]]
        rb=[baseLocsr[0],baseLocsr[-1]]
        #print(lb,rb)
        #sys.exit()
        # fit baseline blocks
        dataModel, driftModel, driftRes, driftRms, driftCoeffs = correct_drift(
            x[baseLocs], y[baseLocs], x,log)

        # 4) apply a polynomial fit to the baseline data
        lin_first_null = np.poly1d(np.polyfit(x[baseLocs], y[baseLocs], 1))

        # 5) Subtract the polynomial fitted to the baseline to get corrected beam
        yCorrected = y - lin_first_null(x)

        # 6) get sline of corrected data
        s = spline(x, yCorrected)

        pl.title("Baseline corrected data")
        pl.xlabel("Scandist [Deg]")
        pl.ylabel("Ta [K]")
        #pl.plot(x,y)
        pl.plot(x, yCorrected, 'k',label="baseline corrected data")
        #pl.plot(x[main_beam], yCorrected[main_beam])
        pl.plot(x[baseLocs], yCorrected[baseLocs],".")
        pl.plot(x[lb], yCorrected[lb],".")
        #pl.plot(x,s)
        pl.plot(x,np.zeros_like(x),'k')
        #pl.grid()
        pl.legend(loc="best")
        try:
            pl.savefig(saveFolder+"baseline_corrected_data.png")
        except:
            pass
        #pl.show()
        pl.close()
        #sys.exit()

        # fit a polynomial to peak data

        msg_wrapper("info", log.info, "Fit the peak")
        print("*"*60)
        hmain_beam=np.where((x>=autoFit['peaklocs'][0]) & (x<=autoFit['peaklocs'][1]))[0]
        ypeak = np.polyval(np.polyfit(x[hmain_beam],
                                    yCorrected[hmain_beam],  2), x[hmain_beam])

        # get residual and rms of peak fit
        fitRes, err_peak = calc_residual(yCorrected[hmain_beam], ypeak)

        pl.title("Plot of final peak fitted data")
        pl.xlabel("Scandist [Deg]")
        pl.ylabel("Ta [K]")
        pl.plot(x, yCorrected, "k", label="corrected data")
        #pl.plot(x[main_beam],yCorrected[main_beam])
        pl.plot(x[hmain_beam], yCorrected[hmain_beam])
        #pl.plot(x,fit)
        pl.plot(x[hmain_beam],ypeak,"r",label="Ta[K] = %.3f +- %.3f" %(max(ypeak),err_peak))
        pl.plot(x,np.zeros(scanLen),"k")
        #pl.grid()
        pl.legend(loc="best")
        try:
            pl.savefig(saveFolder+"peak_fit_data.png")
        except:
            pass
        #pl.show()
        pl.close()
        #sys.exit()

        # find final peak loc
        ploc = np.where(ypeak == max(ypeak))[0]
        peakLoc = (x[hmain_beam])[ploc[0]]
        
        return max(ypeak), ypeak, err_peak, yCorrected, hmain_beam, "", driftRes, driftRms, driftCoeffs, fitRes, coeff[1], flag, baseLocsl, baseLocsr, baseLocs, peakLoc,lb,rb

        sys.exit()
    else:
        # 1. Locate baseline blocks
        # These are the blocks that will be used to correct the drift in the data
        if force=="y" and flag==3:
            baseLocsl=[]
            baseLocsr=[]
        else:

            if fitTheoretical=="y":
                #baseLocs, baseLocsl, baseLocsr, sidelobes, flag, msg, minPosOnLeftOfPeak, minPosOnRightOfPeak, lb, rb = locate_baseline_blocks_auto(
                #x, y, coeff[1], hfnbw,log)
                baseLocs, baseLocsl, baseLocsr, sidelobes = locate_baseline_blocks_fnbw(
                x, hfnbw)
                #print(baseLocsl,baseLocsr)
                flag = 26 
                msg =  "Fitting left and right theoretical (FNBW) points"
                minPosOnLeftOfPeak = baseLocsl[int(len(baseLocsl)/2)]
                minPosOnRightOfPeak = baseLocsr[int(len(baseLocsr)/2)]
                lb = [baseLocsl[0],baseLocsl[-1]]
                rb = [baseLocsr[0],baseLocsr[-1]]
                #sys.exit()

            else:
                # print("\nauto location on.")
                msg_wrapper("info",log.info,"Automated fitting started")
                baseLocs, baseLocsl, baseLocsr, sidelobes, flag, msg, minPosOnLeftOfPeak, minPosOnRightOfPeak, lb, rb = locate_baseline_blocks_auto(
                x, y, coeff[1], hfnbw,log)
                print(minPosOnLeftOfPeak, minPosOnRightOfPeak)
                # sys.exit()
                if 'int' in type(minPosOnRightOfPeak).__name__ or len(minPosOnRightOfPeak) == 0:
                    print("Failed to locate right min pos")
                    return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, 6, [], [], [], np.nan,0,0
                elif 'int' in type(minPosOnLeftOfPeak).__name__ or len(minPosOnLeftOfPeak) == 0:
                    print("Failed to locate left min pos")
                    return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, 7, [], [], [], np.nan,0,0
                else:
                    pass
                # sys.exit()
        
        if len(baseLocsl) == 0 or len(baseLocsr) == 0:

            # one side of the basline has could not be located possibly due to rfi
            msg = "failed to locate base locs"
            msg_wrapper("warning", log.warning, msg)
            flag=30

            # Force the fit
            if force=="y":
                print("Forcing the fit")

                # set baseline points and fit edges or fnbw points
                #print()

                # 1. try fitting the data with the centre at 0
                baseLocs, baseLocsl, baseLocsr, sidelobes, flag, msg, minPosOnLeftOfPeak, minPosOnRightOfPeak, lb, rb = locate_baseline_blocks_auto(x, y, 0, hfnbw,log)
                msg="force fitted local mins"

                

                if len(baseLocsl) == 0 or len(baseLocsr) == 0:

                    # 2. try fitting the hfnbw points
                    baseLocsl  = (np.where(x <= (-hfnbw))[0]) 
                    baseLocsr = (np.where(x >= (hfnbw))[0])
                    baseLocs = list(baseLocsl)+list(baseLocsr)
                    msg="force fitted fnbw locs"
                sidelobes=2 #error fitting the data

                # if both methods failed, exit
                if len(baseLocsl) == 0 or len(baseLocsr) == 0:
                    return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [], np.nan

                '''pl.title("Plot of baseline corrected data")
                pl.xlabel("Scandist [Deg]")
                pl.ylabel("Ta [K]")
                #pl.plot(x,y)
                pl.plot(x, y, 'k',label="baseline corrected data")
                #pl.plot(x[main_beam], yCorrected[main_beam])
                pl.plot(x[baseLocs], y[baseLocs],".")
                pl.show()
                pl.close()
                sys.exit()'''

                # fit the baseline
                dataModel, driftModel, driftRes, driftRms, driftCoeffs = correct_drift(x[baseLocs], y[baseLocs], x,log)

                # get main beam
                try:
                    main_beam = np.where(np.logical_and(x >= coeff[1]-hfnbw, x <= coeff[1]+hfnbw))[0]
                except:
                    print("Failed to get coeff[1], setting beam to fnbw window")
                    main_beam = np.where(np.logical_and(
                        x >= hfnbw, x <= hfnbw))[0]

                # 4) apply a polynomial fit to the baseline data
                lin_first_null = np.poly1d(np.polyfit(x[baseLocs], y[baseLocs], 1))

                # 5) Subtract the polynomial fitted to the baseline to get corrected beam
                yCorrected = y - lin_first_null(x)

                # 6) get sline of corrected data
                s = spline(x, yCorrected)

                pl.title("Plot of baseline corrected data")
                pl.xlabel("Scandist [Deg]")
                pl.ylabel("Ta [K]")
                #pl.plot(x,y)
                pl.plot(x, yCorrected, 'k',label="baseline corrected data")
                #pl.plot(x[main_beam], yCorrected[main_beam])
                pl.plot(x[baseLocsl], yCorrected[baseLocsl],".")
                pl.plot(x[baseLocsr], yCorrected[baseLocsr],".")
                #pl.plot(x,s)
                pl.plot(x,np.zeros_like(x),'k')
                pl.grid()
                pl.legend(loc="best")
                try:
                    pl.savefig(saveFolder+"baseline_corrected_data.png")
                except:
                    pass
                #pl.show()
                pl.close()
                #sys.exit()

                # fit the peak
                # 3) GET LOCATIONS OF DATA FOR THE MAIN BEAM ONLY
                # this is limited by the fnbw
                # check peak is at centre
                main_beam = np.where(np.logical_and(
                    x >= -hfnbw, x <= hfnbw))[0]
                    
                # 4) apply a polynomial fit to the baseline data
                lin_first_null = np.poly1d(np.polyfit(x[baseLocs], y[baseLocs], 1))

                # 5) Subtract the polynomial fitted to the baseline to get corrected beam
                yCorrected = y - lin_first_null(x)

                # 6) get sline of corrected data
                s = spline(x, yCorrected)

                # 7. Fit the peak
                # find max location
                msg_wrapper("info", log.info, "Fit the peak")
                print("*"*60)
                maxp = max(s)
                maxloc = np.where(s == maxp)[0]
                xmaxloc = x[maxloc[0]]

                # max is not at center, found at extreme ends of scan
                if (max(s) == s[0]) or (max(s) == s[-1]):
                    msg = "max of peak is not at center, failed peak fit "
                    msg_wrapper("warning", log.warning, msg)
                    flag  = 10
                    return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan,0,0
                else:
                    pass

                # 7) Get indices where the x values are within the main beam
                # Get top 30% of beam
                xMainBeam = x[main_beam]
                yMainBeam = s[main_beam]
                maxs = max(s[main_beam])

                loc = np.where(s[main_beam] == maxs)[0]
                midxMainBeam = xMainBeam[loc[0]]  

                # Get main beam for peak fitting
                try:
                    hmain_beamn = np.where(np.logical_and(
                        xMainBeam >= coeff[1]-hhpbw, xMainBeam <= coeff[1]+hhpbw))[0]
                except:
                    hmain_beamn = np.where(np.logical_and(
                        xMainBeam >= -hhpbw, xMainBeam <= hhpbw))[0]

                # Fit top 50% or 30% depending on sidelobe confirmation
                if sidelobes == 1:
                    hmain_beamp = np.where(yMainBeam[hmain_beamn] >= 0.5*maxp)[0]
                    flag = 9
                    msg = "large sidelobes detected"
                    msg_wrapper("warning", log.warning, msg)
                else:
                    hmain_beamp = np.where(yMainBeam[hmain_beamn] >= 0.7*maxp)[0]
                    flag = 0

                if (len(hmain_beamp) == 0) or len(hmain_beamn) ==0:
                    msg = "couldn't find peak main beam data"
                    flag=4
                    msg_wrapper("warning", log.warning, msg)

                    # find peak of spline
                    sloc = np.where(s == max(s))[0]
                    print("sloc: ", sloc, ", len: ", len(
                        yCorrected), ", mid: ", len(yCorrected)/2)

                    #print(data)
                    pl.title("Baseline corrected data")
                    pl.xlabel("Scandist [Deg]")
                    pl.ylabel("Ta [K]")
                    pl.plot(x,y)
                    pl.plot(x, yCorrected, 'k',label="baseline corrected data")
                    pl.plot(x[main_beam], yCorrected[main_beam])
                    pl.plot(x[baseLocsl], yCorrected[baseLocsl],".")
                    pl.plot(x[baseLocsr], yCorrected[baseLocsr],".")
                    #pl.plot(x,s)
                    pl.plot(x,np.zeros_like(x),'k')
                    #pl.grid()
                    pl.legend(loc="best")
                    #pl.savefig(saveFolder+"baseline_corrected_data.png")
                    pl.show()
                    pl.close()

                    sys.exit()
                    
                    # peak shifted left
                    if sloc < len(yCorrected)/2 and sloc != 0:
                        print("Peak is shifted to left, but not first element")
                        print(x[sloc], hhpbw)

                        # look for peak around new max loc
                        beam = np.where(np.logical_and(
                            x >= x[sloc]-hhpbw, x <= x[sloc]+hhpbw))[0]

                        # fit peak
                        if len(beam) > 0:
                            ypeak = np.polyval(np.polyfit(
                                    x[beam], yCorrected[beam],  2), x[beam])

                            # get residual and rms of peak fit
                            fitRes, err_peak = calc_residual(
                                    yCorrected[beam], ypeak)

                            # find final peak loc
                            ploc = np.where(ypeak == max(ypeak))[0]
                            peakLoc = (x[beam])[ploc[0]]
                            return max(ypeak), ypeak, err_peak, yCorrected, beam, msg, driftRes, driftRms, driftCoeffs, fitRes, np.nan, flag, baseLocsl, baseLocsr, baseLocs, peakLoc

                        else:
                            # couldn't locate peak
                            return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [], np.nan,0,0

                    else:
                        # peak shifted right

                        print("Peak is shifted to left, but not first element")
                        print(x[sloc], hhpbw)

                        # look for peak around new max loc
                        beam = np.where(np.logical_and(
                            x >= x[sloc]-hhpbw, x <= x[sloc]+hhpbw))[0]

                        # fit peak
                        if len(beam) > 0:
                            ypeak = np.polyval(np.polyfit(
                                    x[beam], yCorrected[beam],  2), x[beam])

                            # get residual and rms of peak fit
                            fitRes, err_peak = calc_residual(
                                    yCorrected[beam], ypeak)

                            # find final peak loc
                            ploc = np.where(ypeak == max(ypeak))[0]
                            peakLoc = (x[beam])[ploc[0]]

                            #sys.exit()
                            return max(ypeak), ypeak, err_peak, yCorrected, beam, msg, driftRes, driftRms, driftCoeffs, fitRes, np.nan, flag, baseLocsl, baseLocsr, baseLocs, peakLoc

                    return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan
                
                hmain_beam = hmain_beamp + hmain_beamn[0]+main_beam[0]

                if hmain_beam[0] > baseLocsr[-1] or hmain_beam[-1] < baseLocsl[0]:
                    # peak loctaion is beyond fnbw locations
                    msg = "peak location is beyond fnbw locations"
                    msg_wrapper("warning", log.warning, msg)
                    flag = 24
                    return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan

                # fit a polynomial to peak data
                ypeak = np.polyval(np.polyfit(x[hmain_beam],
                                            yCorrected[hmain_beam],  2), x[hmain_beam])

                # check if peak was fit correctly
                if max(ypeak) == ypeak[0] or max(ypeak) == ypeak[-1]:
                    # peak is concave, try fitting wider range
                    hmain_beamp = np.where(yMainBeam[hmain_beamn] >= 0.5*maxp)[0]
                    hmain_beam = hmain_beamp + hmain_beamn[0]+main_beam[0]
                    ypeak = np.polyval(np.polyfit(x[hmain_beam],
                                                yCorrected[hmain_beam],  2), x[hmain_beam])

                    if (max(ypeak) == ypeak[0]) or (max(ypeak) == ypeak[-1]):
                        # still struggling to fit ?, stop fitting
                        msg = "failed to accurately establish peak fit location, 1"
                        msg_wrapper("warning", log.warning, msg)
                        flag = 5

                        pl.title("Plot of baseline corrected data")
                        pl.xlabel("Scandist [Deg]")
                        pl.ylabel("Ta [K]")
                        #pl.plot(x,y)
                        pl.plot(x, yCorrected, 'k',label="baseline corrected data")
                        pl.plot(x,s)
                        pl.plot(x[hmain_beamp], yCorrected[hmain_beamp],label=msg)
                        pl.plot(x[baseLocsl], yCorrected[baseLocsl],".")
                        pl.plot(x[baseLocsr], yCorrected[baseLocsr],".")
                        #pl.plot(x,s)
                        pl.plot(x,np.zeros_like(x),'k')
                        pl.grid()
                        pl.legend(loc="best")
                        #pl.savefig(saveFolder+"baseline_corrected_data.png")
                        #pl.show()
                        pl.close()
                        #sys.exit()
                        
                        # find peak of spline
                        sloc = np.where(s==max(s))[0]
                        print("sloc: ",sloc,", len: ", len(yCorrected),", mid: ",len(yCorrected)/2)

                        # peak shifted left
                        if sloc < len(yCorrected)/2 and sloc!=0:
                            print("Peak is shifted to left, but not first element")
                            print(x[sloc],hhpbw)

                            # look for peak around new max loc
                            beam = np.where(np.logical_and(
                                x >= x[sloc]-hhpbw, x <= x[sloc]+hhpbw))[0]

                            # fit peak
                            if len(beam) > 0:
                                ypeak = np.polyval(np.polyfit(
                                    x[beam], yCorrected[beam],  2), x[beam])

                                # get residual and rms of peak fit
                                fitRes, err_peak = calc_residual(yCorrected[beam], ypeak)

                                # find final peak loc
                                ploc = np.where(ypeak == max(ypeak))[0]
                                peakLoc = (x[beam])[ploc[0]]
                                

                                return max(ypeak), ypeak, err_peak, yCorrected, beam, msg, driftRes, driftRms, driftCoeffs, fitRes, np.nan, flag, baseLocsl, baseLocsr, baseLocs,peakLoc
                                
                            else:
                                # couldn't locate peak
                                return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan

                        sys.exit()
                        return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan

                # get residual and rms of peak fit
                fitRes, err_peak = calc_residual(yCorrected[hmain_beam], ypeak)

                # find final peak loc
                ploc = np.where(ypeak == max(ypeak))[0]
                peakLoc = (x[hmain_beam])[ploc[0]]
                
                return max(ypeak), ypeak, err_peak, yCorrected, hmain_beam, "", driftRes, driftRms, driftCoeffs, fitRes, np.nan, flag, baseLocsl, baseLocsr, baseLocs,peakLoc
            else:
                flag = 37
                return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan,0,0
        else:
            pass

        # 2) correct the drift in the data and get the residual and rms
        dataModel, driftModel, driftRes, driftRms, driftCoeffs = correct_drift(
            x[baseLocs], y[baseLocs], x,log)

        # 3) GET LOCATIONS OF DATA FOR THE MAIN BEAM ONLY
        # this is limited by the fnbw
        # check peak is at centre
        main_beam = np.where(np.logical_and(
            x >= coeff[1]-hfnbw, x <= coeff[1]+hfnbw))[0]

        # 4) apply a polynomial fit to the baseline data
        lin_first_null = np.poly1d(np.polyfit(x[baseLocs], y[baseLocs], 1))

        # 5) Subtract the polynomial fitted to the baseline to get corrected beam
        yCorrected = y - lin_first_null(x)

        # 6) get spline of corrected data
        s = spline(x, yCorrected)

        pl.title("Baseline corrected data")
        pl.xlabel("Scandist [Deg]")
        pl.ylabel("Ta [K]")
        pl.plot(x,y)
        pl.plot(x, yCorrected, 'k',label="baseline corrected data")
        #pl.plot(x[main_beam], yCorrected[main_beam])
        pl.plot(x[baseLocsl], yCorrected[baseLocsl],".")
        pl.plot(x[baseLocsr], yCorrected[baseLocsr],".")
        #pl.plot(x,s)
        pl.plot(x,np.zeros_like(x),'k')
        #pl.grid()
        pl.legend(loc="best")
        try:
            pl.savefig(saveFolder+"baseline_corrected_data.png")
        except:
            pass
        #pl.show()
        pl.close()
        #sys.exit()


        # 7. Fit the peak
        # find max location
        msg_wrapper("info", log.info, "Fit the peak")
        print("*"*60)
        maxp = max(s)
        maxloc = np.where(s == maxp)[0]
        xmaxloc = x[maxloc[0]]

        # max is not at center, found at extreme ends of scan
        if (max(s) == s[0]) or (max(s) == s[-1]):
            msg = "max of peak is not at center, failed peak fit "
            msg_wrapper("warning", log.warning, msg)
            flag  = 10
            return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan,0,0
        else:
            pass

        # 7) Get indices where the x values are within the main beam
        # Get top 30% of beam
        xMainBeam = x[main_beam]
        yMainBeam = s[main_beam]

        try:
            maxs = max(s[main_beam])
        except:
            msg = "max of peak is not at center, failed peak fit "
            msg_wrapper("warning", log.warning, msg)
            flag  = 10
            return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan,0,0
            
        loc = np.where(s[main_beam] == maxs)[0]
        midxMainBeam = xMainBeam[loc[0]]  

        # Try to fit a gaussian to confirm center peak location after correction of scan
        try:
            coeff, fit = fit_gauss_lin(
                x, yCorrected, [maxs, midxMainBeam, p[2], 0, 0])
        except Exception:
            msg = "couldnt find max in main beam"
            msg_wrapper("warning", log.warning, msg)
            flag = 11
            return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan,0,0

        # Get main beam for peak fitting
        hmain_beamn = np.where(np.logical_and(
            xMainBeam >= coeff[1]-hhpbw, xMainBeam <= coeff[1]+hhpbw))[0]

        # Fit top 50% or 30% depending on sidelobe confirmation
        if sidelobes == 1:
            hmain_beamp = np.where(yMainBeam[hmain_beamn] >= 0.5*maxp)[0]
            flag = 9
            msg = "large sidelobes detected"
            msg_wrapper("warning", log.warning, msg)
        else:
            hmain_beamp = np.where(yMainBeam[hmain_beamn] >= 0.7*maxp)[0]
            flag = 0

        if (len(hmain_beamp) == 0) or len(hmain_beamn) ==0:
            msg = "couldn't find peak main beam data"
            flag=4
            msg_wrapper("warning", log.warning, msg)

            #print(data)
            pl.title("Baseline corrected data")
            pl.xlabel("Scandist [Deg]")
            pl.ylabel("Ta [K]")
            pl.plot(x,y)
            #pl.plot(x, yCorrected, 'k',label="baseline corrected data")
            pl.plot(x[main_beam], yCorrected[main_beam])
            pl.plot(x[baseLocsl], yCorrected[baseLocsl],".")
            pl.plot(x[baseLocsr], yCorrected[baseLocsr],".")
            #pl.plot(x,s)
            pl.plot(x,np.zeros_like(x),'k')
            #pl.grid()
            pl.legend(loc="best")
            #pl.savefig(saveFolder+"baseline_corrected_data.png")
            #pl.show()
            pl.close()
            #sys.exit()
            #sys.exit()
            
            return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [], np.nan,0,0

        if (len(hmain_beamp) < 0.5*len(hmain_beamn)):
            msg = "peak main beam data too noisy"
            flag = 23
            msg_wrapper("warning", log.warning, msg)
            return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan,0,0
        
        hmain_beam = hmain_beamp + hmain_beamn[0]+main_beam[0]

        if hmain_beam[0] > baseLocsr[-1] or hmain_beam[-1] < baseLocsl[0]:
            # peak loctaion is beyond fnbw locations
            msg = "peak location is beyond fnbw locations"
            msg_wrapper("warning", log.warning, msg)
            flag = 24
            return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan,0,0

        # fit a polynomial to peak data
        ypeak = np.polyval(np.polyfit(x[hmain_beam],
                                    yCorrected[hmain_beam],  2), x[hmain_beam])

        # # check if peak was fit correctly
        # print(ypeak[0],max(ypeak) ,ypeak[-1])
        # pl.plot(x,yCorrected)
        # pl.plot(x[hmain_beam],ypeak)
        # pl.show()

        if max(ypeak) == ypeak[0] or max(ypeak) == ypeak[-1]:

            # peak is concave, try fitting wider range
            hmain_beamp = np.where(yMainBeam[hmain_beamn] >= 0.5*maxp)[0]
            hmain_beam = hmain_beamp + hmain_beamn[0]+main_beam[0]
            ypeak = np.polyval(np.polyfit(x[hmain_beam],
                                        yCorrected[hmain_beam],  2), x[hmain_beam])

            if (max(ypeak) == ypeak[0]) or (max(ypeak) == ypeak[-1]):
                # still struggling to fit ?, try this then stop fitting

                try:
                    # LOCATE LOCAL MINUMUM/MAXIMUM POSITIONS
                    # these values are used to figure out where to
                    # select our baseline points/locations
                    localMinPositions = (np.diff(np.sign(np.diff(s))) > 0).nonzero()[
                        0] + 1  # local min positions / first nulls
                    localMaxPositions = (np.diff(np.sign(np.diff(s))) < 0).nonzero()[
                        0] + 1  # local max positions / peak

                    print(f'mins: {localMinPositions}, maxs: {localMaxPositions}')

                    # find peak closest to zero
                    locs=x[localMaxPositions]
                    k = min(locs, key=lambda x:abs(x-0))
                    locs=list(locs)
                    #print(f'locs: {locs}, k: {k}')
                    print(f'pos of possible center peak: {locs.index(k)}')

                    # use this peak as the main peak
                    kpos=np.where(x==k)[0]
                    print(f'peak is at loc: {kpos}')
                    ymax=s[kpos] #max(s)
                    yhalf= ymax/2

                    # find surrounding mins
                    l=min(localMinPositions, key=lambda x:abs(x-kpos))
                    ppos=list(localMinPositions).index(l)
                    # print(l,ppos,kpos)
                    # print(localMinPositions)
                    if l>kpos:
                        v=[localMinPositions[ppos-1],localMinPositions[ppos]]
                        print('window - ',localMinPositions[ppos-1],kpos,localMinPositions[ppos])
                        left=localMinPositions[ppos-1]
                        right=localMinPositions[ppos]
                    elif l < kpos:
                        print(localMinPositions[ppos],kpos,localMinPositions[ppos+1])
                        left=localMinPositions[ppos]
                        right=localMinPositions[ppos+1]
                        print('l < kpos')
                        #sys.exit()
                    else:
                        print(localMinPositions[ppos],kpos,localMinPositions[ppos+1])
                        left=localMinPositions[ppos]
                        right=localMinPositions[ppos+1]
                        print('l ? kpos')
                        sys.exit()
                    top = np.where((s >= yhalf)&(x>x[left])&(x<x[right]))
                
                    # peak is concave, try fitting wider range
                    hmain_beamp = top#np.where(yMainBeam[hmain_beamn] >= 0.5*maxp)[0]
                    #hmain_beam = hmain_beamp + hmain_beamn[0]+main_beam[0]
                    ypeak = np.polyval(np.polyfit(x[hmain_beamp],
                                                yCorrected[hmain_beamp],  2), x[hmain_beamp])
                                                
                    # get residual and rms of peak fit
                    fitRes, err_peak = calc_residual(yCorrected[hmain_beamp], ypeak)

                    # find final peak loc
                    #ploc = np.where(ypeak == max(ypeak))[0]
                    peakLoc = (x[kpos])#[ploc[0]]
                    
                    msg = "attempted to accurately establish peak fit location"
                    msg_wrapper("warning", log.warning, msg)
                    flag = 37

                    pl.title("Plot of final peak fitted data")
                    pl.xlabel("Scandist [Deg]")
                    pl.ylabel("Ta [K]")
                    pl.plot(x, yCorrected, "k", label="corrected data")
                    #pl.plot(x[main_beam],yCorrected[main_beam])
                    pl.plot(x[hmain_beamp], yCorrected[hmain_beamp])
                    #pl.plot(x,fit)
                    pl.plot(x[hmain_beamp],ypeak,"r",label="Ta[K] = %.3f +- %.3f" %(max(ypeak),err_peak))
                    pl.plot(x,np.zeros(scanLen),"k")
                    #pl.grid()
                    pl.legend(loc="best")
                    try:
                        pl.savefig(saveFolder+"peak_fit_data.png")
                    except:
                        pass
                    #pl.show()
                    pl.close()
                    #sys.exit()

                    return max(ypeak), ypeak, err_peak, yCorrected, hmain_beamp, "", driftRes, driftRms, driftCoeffs, fitRes, coeff[1], flag, baseLocsl, baseLocsr, baseLocs, peakLoc,lb,rb
                
                except:
                    msg = "failed to accurately establish peak fit location"
                    msg_wrapper("warning", log.warning, msg)
                    flag = 5
                    print(msg)
                    #sys.exit()
                    return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan,0,0

        if (abs(min(yCorrected)) > max(yCorrected)):
            # still struggling to fit ?, stop fitting
            msg = "min > max"
            msg_wrapper("warning", log.warning, msg)
            flag = 25

            if force=="y":
                pass
            else:
                return np.nan, [], np.nan, [], [], msg, [], [], [], [], np.nan, flag, [], [], [],np.nan,0,0
        else:
            pass

        # get residual and rms of peak fit
        fitRes, err_peak = calc_residual(yCorrected[hmain_beam], ypeak)

        pl.title("Plot of final peak fitted data")
        pl.xlabel("Scandist [Deg]")
        pl.ylabel("Ta [K]")
        pl.plot(x, yCorrected, "k", label="corrected data")
        #pl.plot(x[main_beam],yCorrected[main_beam])
        pl.plot(x[hmain_beam], yCorrected[hmain_beam])
        #pl.plot(x,fit)
        pl.plot(x[hmain_beam],ypeak,"r",label="Ta[K] = %.3f +- %.3f" %(max(ypeak),err_peak))
        pl.plot(x,np.zeros(scanLen),"k")
        #pl.grid()
        pl.legend(loc="best")
        try:
            pl.savefig(saveFolder+"peak_fit_data.png")
        except:
            pass
        #pl.show()
        pl.close()
        #sys.exit()

        # find final peak loc
        ploc = np.where(ypeak == max(ypeak))[0]
        peakLoc = (x[hmain_beam])[ploc[0]]
        
        return max(ypeak), ypeak, err_peak, yCorrected, hmain_beam, "", driftRes, driftRms, driftCoeffs, fitRes, coeff[1], flag, baseLocsl, baseLocsr, baseLocs, peakLoc,lb,rb

def fit_dual_beam(x, y, hpbw, fnbw, factor, npts, dec, srcType, data, scanNum, force, log):
    """ Fit dual beam data. 
    
        Parameters:
            x (array): 1D array of data representing the x-axis
            y (array): 1D array of data representing the y-axis
            hpbw (float): source half power beam width from file
            fnbw (float): source first null beam width from file
            npts (int): number of points ti use for baseline block
            dec (float): source declination
            srcType (string): type of source
            data (dict): dictionary of source parameters
            scanNum (int):  Value representing the current scan
            force (str): String to determine whether to force a fit or not   
            log (object): loffing object
    """

    # Setup parameters
    scanLen = len(x)              # length of the scan
    midLeftLoc = int(scanLen/4)   # estimated location of peak on left beam
    midRightLoc = midLeftLoc * 3  # estimated location of peak on right beam
    hhpbw = hpbw/2                # half of the hpbw
    hfnbw = fnbw/2                # half of the fnbw
    factoredfnbw = (fnbw*factor)  # fnbw multiplied by factor
    flag=0                        # default flag set to zero
    msg=""                        # flag message to go on plot image
    saveFolder="currentScanPlots/"
    fl = 0                        # failed left gaussian fit
    fr = 0                        # failed right gaussian fit

    # LOCATE BASELINE BLOCKS
    msg_wrapper("debug", log.debug, "-- Locate baseline blocks")
    
    # we don't worry about sidelobes here so baseline
    # blocks are set to edges or fnbw points

    ptLimit = int(scanLen*0.04) # Point limit, number of allowed points per base block
    baseLocsLeft  = np.arange(0,ptLimit,1)
    baseLocsRight = np.arange(scanLen-ptLimit,scanLen,1)
    baseLocs      = list(baseLocsLeft)+list(baseLocsRight)
    
    if len(baseLocsLeft) == 0 or len(baseLocsRight) == 0:
        msg = "failed to locate base locs"
        flag = 30
        msg_wrapper("warning", log.warning, msg)
        return [], [], [], np.nan, [], \
                    [], [], np.nan, np.nan, [], \
                    [], [], np.nan, np.nan, [],\
            msg, flag, np.nan, np.nan

    msg_wrapper("debug", log.debug,
                f'BaseLocsLeft: {baseLocsLeft[0]} to {baseLocsLeft[-1]} = {len(baseLocsLeft)} pts')
    msg_wrapper("debug", log.debug,
                f'BaseLocsLeft: {baseLocsRight[0]} to {baseLocsRight[-1]} = {len(baseLocsRight)} pts')
  
    dataModel, driftModel, driftRes, driftRms, driftCoeffs = correct_drift(x[baseLocs], y[baseLocs], x,log)

    # Correct the data and get global max/min
    yCorrected = y-dataModel
    maxyloc = np.argmax(yCorrected)
    minyloc = np.argmin(yCorrected)
    maxy = yCorrected[maxyloc]
    miny = yCorrected[minyloc]

    # Spline the data and get global max/min
    yspl = spline(x, yCorrected)
    ysplmaxloc = np.argmax(yspl)
    ysplminloc = np.argmin(yspl)
    ysplmax = yspl[ysplmaxloc]
    ysplmin = yspl[ysplminloc] 

    msg_wrapper("debug", log.debug, "maxyloc: {}, maxy: {:.3f}, minyloc: {}, miny: {:.3f}".format(maxyloc, maxy, minyloc, miny))
    msg_wrapper("debug", log.debug, "maxyloc: {}, maxy: {:.3f}, minyloc: {}, miny: {:.3f}\n".format(ysplmaxloc, ysplmax, ysplminloc, ysplmin))
    msg_wrapper("debug", log.debug, "A beam peakloc: {} \n# B beam peakloc: {}".format(ysplmaxloc, ysplminloc))


    # A/B BEAM DATA PROCESSING
    AbeamScan = np.where(np.logical_and(x > -factoredfnbw, x < 0))[0]
    BbeamScan = np.where(np.logical_and(x > 0, x < factoredfnbw))[0]

    if len(AbeamScan) == 0 or len(BbeamScan) == 0:
        msg="A/B beam scan data == 0, no data"
        flag = 8
        msg_wrapper("warning", log.warning, msg)
        return [], [], [], np.nan, [], \
            [], [], np.nan, np.nan, [], \
            [], [], np.nan, np.nan, [],\
            msg, flag,  np.nan, np.nan

    msg_wrapper("debug", log.debug, "- Beam seperation:")
    msg_wrapper("debug", log.debug, "Left beam indeces: {} to {}".format(AbeamScan[0], AbeamScan[-1]))
    msg_wrapper("debug", log.debug, "Right beam indeces: {} to {}\n".format(
        BbeamScan[0], BbeamScan[-1]))

    msg_wrapper("debug", log.debug, "- Data Limits")
    msg_wrapper("debug", log.debug, "base left: {}, drift A left: {}, peak A: {}, drift A right: {}".format(baseLocsLeft[-1], AbeamScan[0], ysplminloc, AbeamScan[-1]))
    msg_wrapper("debug", log.debug, "drift B left: {}, peak B: {}, drift B right: {}, base right: {}\n".format(
        BbeamScan[0], ysplmaxloc, BbeamScan[-1], baseLocsRight[0]))

    #print(min(yspl[AbeamScan]), max(yspl[AbeamScan]), )
    #print(min(yspl[BbeamScan]), max(yspl[BbeamScan]))

    # figure out orientation of beam. With some scans the beams
    # are flipped e.g, pks2326-502, A beam is positive, whereas
    # j0450-81 A beam is negative.
    # find value closest to zero and use the other value to determine
    # which side to fit positive/negative peak
    lstA=[min(yspl[AbeamScan]), max(yspl[AbeamScan])]
    minA = min(lstA,key=abs)
    fa=""
    if minA==min(yspl[AbeamScan]):
        # fit A beam positive B beam negative
        #print("Fitting positive")
        fa="p"

        
    else:
        # fit A beam negative B beam positive
        #print("Fitting negative")
        fa="n"


    # Ensure peak is within accepted limits
    if fa=="p":
        if ysplmaxloc > AbeamScan[-1]:# or ysplminloc > beamScan[0]:
            msg = "Max is beyond left baseline block"
            flag = 31
            msg_wrapper("warning", log.warning, msg)
            return [], [], [], np.nan, [], \
                [], [], np.nan, np.nan, [], \
                [], [], np.nan, np.nan, [],\
                msg, flag, np.nan, np.nan

        if ysplminloc < BbeamScan[0]:#baseLocsRight[0]:  # ysplminloc < BbeamScan[0] or
            msg="Min is beyond right baseline block"
            print(msg)
            flag=32
            msg_wrapper("warning", log.warning, msg)
            return [], [], [], np.nan, [], \
                        [], [], np.nan, np.nan, [], \
                        [], [], np.nan, np.nan, [],\
                        msg, flag, np.nan, np.nan

        # Try to fit a gaussian to determine peak parameters
        try:
            # set initial parameters for data fitting
            p = [max(y), x[midLeftLoc], hpbw, .01, .0]
            coeffl, covar_matrixl, fitLeft = fit_gauss_lin(
                x[AbeamScan], y[AbeamScan], p)
        except Exception:
            fl=1
            msg = "gaussian curve_fit algorithm failed"
            msg_wrapper("debug", log.debug, msg)
            fitLeft = y[AbeamScan]
            flag = 3

        try:
            # set initial parameters for data fitting
            p = [min(y), x[midRightLoc], hpbw, .01, .0]
            coeffr, covar_matrixr, fitRight = fit_gauss_lin(
                x[BbeamScan], y[BbeamScan], p)
        except Exception:
            fr = 1
            msg = "gaussian curve_fit algorithm failed"
            msg_wrapper("debug", log.debug, msg)
            fitRight = y[BbeamScan]
            flag = 3

        # Determine peak fitting location
        BbeamLeftLimit  = x[ysplminloc]-hhpbw #coeffl[1] - hhpbw  # *2*.6
        BbeamRightLimit = x[ysplminloc]+hhpbw
        AbeamLeftLimit  = x[ysplmaxloc]-hhpbw #coeffl[1] - hhpbw  # *2*.6
        AbeamRightLimit = x[ysplmaxloc]+hhpbw

        leftlocs = np.where(np.logical_and(
            x >= AbeamLeftLimit, x <= AbeamRightLimit))[0]
        rightlocs = np.where(np.logical_and(
            x >= BbeamLeftLimit, x <= BbeamRightLimit))[0]

        # setup beam fitting peak selection criteria
        if srcType == "CAL":
            beamCut = 0.7
        else:
            beamCut = 0.5

        # select part of beam to fit
        if ysplmax < 0.1:
            flag = 36
            msg = "fit entire left beam, max yspl < 0.1"
            msg_wrapper("warning", log.warning, msg)
            leftMainBeamLocs = leftlocs
            
        else:
            topCut = np.where(yspl[leftlocs] >= ysplmax*beamCut)[0]
            leftMainBeamLocs = leftlocs[0]+np.array(topCut)

        if ysplmin > -0.1:
            flag = 35
            msg = "fit entire right beam, min yspl > -0.1"
            msg_wrapper("warning", log.warning, msg)
            rightMainBeamLocs = rightlocs
        else:
            bottomCut = np.where(yspl[rightlocs] <= ysplmin*beamCut)[0]
            rightMainBeamLocs = rightlocs[0]+np.array(bottomCut)

    if fa=="n":
        # A beam is min
        if ysplmaxloc < AbeamScan[-1]:# or ysplminloc > beamScan[0]:
            msg = "Max is beyond left baseline block"
            flag = 31
            msg_wrapper("warning", log.warning, msg)
            return [], [], [], np.nan, [], \
                [], [], np.nan, np.nan, [], \
                [], [], np.nan, np.nan, [],\
                msg, flag, np.nan, np.nan

        if ysplminloc > BbeamScan[0]:#baseLocsRight[0]:  # ysplminloc < BbeamScan[0] or
            msg="Min is beyond right baseline block"
            print(msg)
            flag=32
            msg_wrapper("warning", log.warning, msg)
            return [], [], [], np.nan, [], \
                        [], [], np.nan, np.nan, [], \
                        [], [], np.nan, np.nan, [],\
                        msg, flag, np.nan, np.nan

        # Try to fit a gaussian to determine peak parameters
        try:
            # set initial parameters for data fitting
            p = [min(y), x[midLeftLoc], hpbw, .01, .0]
            coeffl, covar_matrixl, fitLeft = fit_gauss_lin(
                x[AbeamScan], y[AbeamScan], p)
        except Exception:
            fl=1
            msg = "gaussian curve_fit algorithm failed"
            msg_wrapper("debug", log.debug, msg)
            fitLeft = y[AbeamScan]
            flag = 3

        try:
            # set initial parameters for data fitting
            p = [max(y), x[midRightLoc], hpbw, .01, .0]
            coeffr, covar_matrixr, fitRight = fit_gauss_lin(
                x[BbeamScan], y[BbeamScan], p)
        except Exception:
            fr = 1
            msg = "gaussian curve_fit algorithm failed"
            msg_wrapper("debug", log.debug, msg)
            fitRight = y[BbeamScan]
            flag = 3

    
        # Determine peak fitting location
        AbeamLeftLimit  = x[ysplminloc]-hhpbw #coeffl[1] - hhpbw  # *2*.6
        AbeamRightLimit = x[ysplminloc]+hhpbw
        BbeamLeftLimit  = x[ysplmaxloc]-hhpbw #coeffl[1] - hhpbw  # *2*.6
        BbeamRightLimit = x[ysplmaxloc]+hhpbw


        leftlocs = np.where(np.logical_and(
            x >= AbeamLeftLimit, x <= AbeamRightLimit))[0]
        rightlocs = np.where(np.logical_and(
            x >= BbeamLeftLimit, x <= BbeamRightLimit))[0]

        # setup beam fitting peak selection criteria
        if srcType == "CAL":
            beamCut = 0.7
        else:
            beamCut = 0.5

        #select part of beam to fit
        if ysplmax < 0.1:
            flag = 36
            msg = "fit entire left beam, max yspl < 0.1"
            msg_wrapper("warning", log.warning, msg)
            rightMainBeamLocs = rightlocs
        else:
            topCut = np.where(yspl[rightlocs] >= ysplmax*beamCut)[0]
            rightMainBeamLocs = rightlocs[0]+np.array(topCut)

        if ysplmin > -0.1:
            flag = 35
            msg = "fit entire right beam, min yspl > -0.1"
            msg_wrapper("warning", log.warning, msg)
            leftMainBeamLocs = leftlocs
        else:
            bottomCut = np.where(yspl[leftlocs] <= ysplmin*beamCut)[0]
            leftMainBeamLocs = leftlocs[0]+np.array(bottomCut)

    # fit left peak
    ypeakl = np.polyval(np.polyfit(x[leftMainBeamLocs], yCorrected[leftMainBeamLocs],  2), x[leftMainBeamLocs])
    fitResl, err_peakl = calc_residual(yCorrected[leftMainBeamLocs], ypeakl)

    # fit right peak
    ypeakr = np.polyval(np.polyfit(
        x[rightMainBeamLocs], yCorrected[rightMainBeamLocs],  2), x[rightMainBeamLocs])
    fitResr, err_peakr = calc_residual(yCorrected[rightMainBeamLocs], ypeakr)

    if fa=="p":
        ymin = min(ypeakr)
        ymax = max(ypeakl)
    else:
        ymin = min(ypeakl)
        ymax = max(ypeakr)

    msg_wrapper("debug", log.debug, "A/B beam peak")
    if fa=="p":
        msg_wrapper("debug", log.debug, "left: {:.3f}, max: {:.3f}, right: {:.3f}".format(
            ypeakl[0], ymax, ypeakl[-1]))
        msg_wrapper("debug", log.debug, "left: {:.3f}, min: {:.3f}, right{:.3f}".format(
            ypeakr[0], ymin, ypeakr[-1]))

        ypeakrdata = x[rightMainBeamLocs]
        ypeakldata = x[leftMainBeamLocs]

        # check data doesn't overlap
        overlapRight = set(baseLocsRight) & set(rightMainBeamLocs)
        overlapLeft = set(baseLocsLeft) & set(leftMainBeamLocs)
        overlapbeams = set(leftMainBeamLocs) & set(rightMainBeamLocs)

        msg=("checking for overlapping beams: ")
        msg_wrapper("debug", log.debug, msg)
        
        if len(overlapLeft) != 0:
            msg = "beams don't overlap on left"
            msg_wrapper("debug", log.debug, msg)

            if leftMainBeamLocs[0] > baseLocsLeft[int(
                    len(baseLocsLeft)*.8)]:
                pass
            else:
                overlap = next(iter(overlapLeft))
                shift = list(leftMainBeamLocs).index(int(overlap))
                msg = "Overlap found on A beam"
                flag = 33
                msg_wrapper("warning", log.warning, msg)

                # move beam to the left
                f = abs(len(leftMainBeamLocs)-shift)
                leftMainBeamLocs = abs(leftMainBeamLocs+f)

                # fit left peak
                ypeakl = np.polyval(np.polyfit(
                    x[leftMainBeamLocs], yCorrected[leftMainBeamLocs],  2), x[leftMainBeamLocs])
                fitResl, err_peakl = calc_residual(
                    yCorrected[leftMainBeamLocs], ypeakl)

                ymax = max(ypeakl)
                msg="left: {:.3f}, max: {:.3f}, right: {:.3f}".format(
                    ypeakl[0], ymax, ypeakl[-1])
                msg_wrapper("debug", log.debug, msg)

                if(ypeakl[0] >= ymax or ypeakl[-1] >= ymax):
                    ymax = np.nan
                    err_peakl = np.nan
                else:
                    flag = 36
                    msg = "fit entire left beam"
                    msg_wrapper("debug", log.debug, msg)

                return [], [], [], np.nan, [], \
                    [], [], np.nan, np.nan, [], \
                    [], [], np.nan, np.nan, [],\
                    msg, flag, np.nan, np.nan

        if len(overlapRight) != 0:

            overlap = next(iter(overlapRight))
            shift = list(rightMainBeamLocs).index(int(overlap))

            msg = "Overlap found on B beam"
            flag = 34
            msg_wrapper("warning", log.warning, msg)

            # move beam to the RIGHT
            f = abs(len(rightMainBeamLocs)-shift)
            rightMainBeamLocs = abs(rightMainBeamLocs-f)

            msg="beam shifted to left by {} points".format(f)
            msg_wrapper("debug", log.debug, msg)

            # fit right peak
            ypeakr = np.polyval(np.polyfit(
                x[rightMainBeamLocs], yCorrected[rightMainBeamLocs],  2), x[rightMainBeamLocs])
            fitResr, err_peakr = calc_residual(
                yCorrected[rightMainBeamLocs], ypeakr)

            ymin = min(ypeakr)

            msg="left: {:.3f}, min: {:.3f}, right{:.3f}".format(
                ypeakr[0], ymin, ypeakr[-1])
            msg_wrapper("debug", log.debug, msg)

            if(ypeakr[0] <= ymin or ypeakr[-1] <= ymin):
                ymin = np.nan
                err_peakr = np.nan

            else:
                flag = 35
                msg = "fit entire right beam"
                msg_wrapper("debug", log.debug, msg)

            ypeakrdata = x[rightMainBeamLocs]

            #pl.plot(x, yCorrected)

            '''#pl.plot(x[leftlocs],yCorrected[leftlocs])
            #pl.plot(x[leftMainBeamLocs], yCorrected[leftMainBeamLocs])
            #pl.plot(x[rightlocs],yCorrected[rightlocs])
            pl.plot(x[rightMainBeamLocs], yCorrected[rightMainBeamLocs])
            #pl.plot(x[leftMainBeamLocs], ypeakl)
            pl.plot(x[rightMainBeamLocs], ypeakr)
            pl.plot(x, np.zeros(scanLen))
            pl.plot(x[baseLocs], yCorrected[baseLocs], ".")
            #pl.show()
            pl.close()
            #sys.exit()'''

            return [], [], [], np.nan, [], \
                [], [], np.nan, np.nan, [], \
                [], [], np.nan, np.nan, [],\
                msg, flag, np.nan, np.nan

        if ((x[leftMainBeamLocs])[-1] > 0):
            flag = 28
            msg = "left beam data goes beyond midpoint"
            msg_wrapper("warning", log.warning, msg)
            return [], [], [], np.nan, [], \
                [], [], np.nan, np.nan, [], \
                [], [], np.nan, np.nan, [],\
                msg, flag, np.nan, np.nan

        if ((x[rightMainBeamLocs])[-1] < 0):
            flag = 29
            msg = "right beam data goes beyond midpoint"
            msg_wrapper("warning", log.warning, msg)
            return [], [], [], np.nan, [], \
                [], [], np.nan, np.nan, [], \
                [], [], np.nan, np.nan, [],\
                msg, flag, np.nan, np.nan

        pl.plot(x, yCorrected, label="corrected data")
        pl.plot(x[leftlocs], yCorrected[leftlocs], label="peakl data")
        pl.plot(x[leftMainBeamLocs], yCorrected[leftMainBeamLocs])
        pl.plot(x[rightlocs], yCorrected[rightlocs], label="peakr data")
        pl.plot(x[rightMainBeamLocs], yCorrected[rightMainBeamLocs])
        pl.plot(x[leftMainBeamLocs],
                ypeakl, label="peak fitl: {:.3f} +- {:.3f}".format(ymax, err_peakl))
        pl.plot(x[rightMainBeamLocs], ypeakr,
                label="peak fitr: {:.3f} +- {:.3f}".format(ymin, err_peakr))
        pl.plot(x[baseLocs], yCorrected[baseLocs], ".", label="baselocs")
        pl.plot(x, np.zeros(scanLen))
        pl.legend(loc="best")
        pl.grid()
        #pl.show()
        try:
            pl.savefig(saveFolder+"fitted.png")
        except:
            pass
        pl.close()
        #sys.exit()
        
        msg_wrapper("info", log.info, "Fit the peak")
        print("*"*60)
        msg="\npeak left: {:.3f} +- {:.3f} K\npeak right: {:.3f} +- {:.3f} K\n".format(
            ymax, err_peakl, ymin, err_peakr)
        msg_wrapper("info", log.info, msg)
        
        # find final peak loc
        ploca = np.where(ypeakl == ymax)[0]
        if len(ploca)==0:
            peakLoca=np.nan
        else:
            peakLoca = (x[leftMainBeamLocs])[ploca[0]]

        # find final peak loc
        plocb = np.where(ypeakr == ymin)[0] 
        if len(plocb)==0:    
            peakLocb=np.nan
        else:
            peakLocb = (x[rightMainBeamLocs])[plocb[0]]

        return yCorrected, driftRes, driftRms, driftCoeffs[0], baseLocs, \
            ypeakldata, ypeakl, ymax, err_peakl, fitResl, \
            ypeakrdata, ypeakr, ymin, err_peakr, fitResr,\
            msg, flag, peakLoca, peakLocb

    else:
        msg_wrapper("debug", log.debug, "left: {:.3f}, min: {:.3f}, right: {:.3f}".format(
            ypeakl[0], ymin, ypeakl[-1]))
        msg_wrapper("debug", log.debug, "left: {:.3f}, max: {:.3f}, right{:.3f}".format(
            ypeakr[0], ymax, ypeakr[-1]))

        ypeakrdata = x[rightMainBeamLocs]
        ypeakldata = x[leftMainBeamLocs]

        # check data doesn't overlap
        overlapRight = set(baseLocsRight) & set(rightMainBeamLocs)
        overlapLeft = set(baseLocsLeft) & set(leftMainBeamLocs)
        overlapbeams = set(leftMainBeamLocs) & set(rightMainBeamLocs)

        msg=("checking for overlapping beams: ")
        msg_wrapper("debug", log.debug, msg)

        if len(overlapLeft) != 0:
            msg = "beams don't overlap on left"
            msg_wrapper("debug", log.debug, msg)

            if leftMainBeamLocs[0] > baseLocsLeft[int(
                    len(baseLocsLeft)*.8)]:
                pass
            else:
                overlap = next(iter(overlapLeft))
                shift = list(leftMainBeamLocs).index(int(overlap))
                msg = "Overlap found on A beam"
                flag = 33
                msg_wrapper("warning", log.warning, msg)

                # move beam to the left
                f = abs(len(leftMainBeamLocs)-shift)
                leftMainBeamLocs = abs(leftMainBeamLocs+f)

                # fit left peak
                ypeakl = np.polyval(np.polyfit(
                    x[leftMainBeamLocs], yCorrected[leftMainBeamLocs],  2), x[leftMainBeamLocs])
                fitResl, err_peakl = calc_residual(
                    yCorrected[leftMainBeamLocs], ypeakl)

                ymax = max(ypeakl)
                msg="left: {:.3f}, max: {:.3f}, right: {:.3f}".format(
                    ypeakl[0], ymax, ypeakl[-1])
                msg_wrapper("debug", log.debug, msg)

                if(ypeakl[0] <= ymax or ypeakl[-1] <= ymax):
                    ymax = np.nan
                    err_peakl = np.nan
                else:
                    flag = 36
                    msg = "fit entire left beam"
                    msg_wrapper("debug", log.debug, msg)

                ypeakldata = x[leftMainBeamLocs]

                '''pl.plot(x, yCorrected)
                pl.plot(x[leftMainBeamLocs], yCorrected[leftMainBeamLocs], 'b')
                #pl.plot(x[rightlocs],yCorrected[rightlocs])
                #pl.plot(x[rightMainBeamLocs], yCorrected[rightMainBeamLocs])
                pl.plot(x[leftMainBeamLocs], ypeakl, 'r')
                #pl.plot(x[rightMainBeamLocs], ypeakr)
                pl.plot(x, np.zeros(scanLen))
                pl.plot(x[baseLocs], yCorrected[baseLocs], ".")
                #pl.show()
                pl.close()
                #sys.exit()'''

                return [], [], [], np.nan, [], \
                    [], [], np.nan, np.nan, [], \
                    [], [], np.nan, np.nan, [],\
                    msg, flag, np.nan, np.nan

        if len(overlapRight) != 0:

            overlap = next(iter(overlapRight))
            shift = list(rightMainBeamLocs).index(int(overlap))

            msg = "Overlap found on B beam"
            flag = 34
            msg_wrapper("warning", log.warning, msg)

            # move beam to the RIGHT
            f = abs(len(rightMainBeamLocs)-shift)
            rightMainBeamLocs = abs(rightMainBeamLocs-f)

            msg="beam shifted to left by {} points".format(f)
            msg_wrapper("debug", log.debug, msg)

            # fit right peak
            ypeakr = np.polyval(np.polyfit(
                x[rightMainBeamLocs], yCorrected[rightMainBeamLocs],  2), x[rightMainBeamLocs])
            fitResr, err_peakr = calc_residual(
                yCorrected[rightMainBeamLocs], ypeakr)

            ymin = min(ypeakr)

            msg="left: {:.3f}, min: {:.3f}, right{:.3f}".format(
                ypeakr[0], ymin, ypeakr[-1])
            msg_wrapper("debug", log.debug, msg)

            if(ypeakr[0] <= ymin or ypeakr[-1] <= ymin):
                ymin = np.nan
                err_peakr = np.nan

            else:
                flag = 35
                msg = "fit entire right beam"
                msg_wrapper("debug", log.debug, msg)

            ypeakrdata = x[rightMainBeamLocs]

            #pl.plot(x, yCorrected)

            '''#pl.plot(x[leftlocs],yCorrected[leftlocs])
            #pl.plot(x[leftMainBeamLocs], yCorrected[leftMainBeamLocs])
            #pl.plot(x[rightlocs],yCorrected[rightlocs])
            pl.plot(x[rightMainBeamLocs], yCorrected[rightMainBeamLocs])
            #pl.plot(x[leftMainBeamLocs], ypeakl)
            pl.plot(x[rightMainBeamLocs], ypeakr)
            pl.plot(x, np.zeros(scanLen))
            pl.plot(x[baseLocs], yCorrected[baseLocs], ".")
            #pl.show()
            pl.close()
            #sys.exit()'''

            return [], [], [], np.nan, [], \
                [], [], np.nan, np.nan, [], \
                [], [], np.nan, np.nan, [],\
                msg, flag, np.nan, np.nan

        if ((x[leftMainBeamLocs])[-1] > 0):
            flag = 28
            msg = "left beam data goes beyond midpoint"
            msg_wrapper("warning", log.warning, msg)
            return [], [], [], np.nan, [], \
                [], [], np.nan, np.nan, [], \
                [], [], np.nan, np.nan, [],\
                msg, flag, np.nan, np.nan

        if ((x[rightMainBeamLocs])[-1] < 0):
            flag = 29
            msg = "right beam data goes beyond midpoint"
            msg_wrapper("warning", log.warning, msg)
            return [], [], [], np.nan, [], \
                [], [], np.nan, np.nan, [], \
                [], [], np.nan, np.nan, [],\
                msg, flag, np.nan, np.nan

        pl.plot(x, yCorrected, label="corrected data")
        pl.plot(x[leftlocs], yCorrected[leftlocs], label="peakl data")
        pl.plot(x[leftMainBeamLocs], yCorrected[leftMainBeamLocs])
        pl.plot(x[rightlocs], yCorrected[rightlocs], label="peakr data")
        pl.plot(x[rightMainBeamLocs], yCorrected[rightMainBeamLocs])
        pl.plot(x[leftMainBeamLocs],
                ypeakl, label="peak fitl: {:.3f} +- {:.3f}".format(ymin, err_peakl))
        pl.plot(x[rightMainBeamLocs], ypeakr,
                label="peak fitr: {:.3f} +- {:.3f}".format(ymax, err_peakr))
        pl.plot(x[baseLocs], yCorrected[baseLocs], ".", label="baselocs")
        pl.plot(x, np.zeros(scanLen))
        pl.legend(loc="best")
        #pl.show()
        try:
            pl.savefig(saveFolder+"fitted.png")
        except:
            pass
        pl.close()
        #sys.exit()

        msg_wrapper("info", log.info, "Fit the peak")
        print("*"*60)
        msg="\npeak left: {:.3f} +- {:.3f} K\npeak right: {:.3f} +- {:.3f} K\n".format(
            ymin, err_peakl, ymax, err_peakr)
        msg_wrapper("info", log.info, msg)
      
        # find final peak loc
        ploca = np.where(ypeakl == ymin)[0]
        if len(ploca)==0:
            peakLoca=np.nan
        else:
            peakLoca = (x[leftMainBeamLocs])[ploca[0]]

        # find final peak loc
        plocb = np.where(ypeakr == ymax)[0] 
        if len(plocb)==0:    
            peakLocb=np.nan
        else:
            peakLocb = (x[rightMainBeamLocs])[plocb[0]]

        return yCorrected, driftRes, driftRms, driftCoeffs[0], baseLocs, \
            ypeakldata, ypeakl, ymin, err_peakl, fitResl, \
            ypeakrdata, ypeakr, ymax, err_peakr, fitResr,\
            msg, flag, peakLoca, peakLocb

# GUI operations
def get_base_pts(x, y, base_index_list):
    """ Get baseline points from a list of 
        indexes.
    """

    # Get data between the indexes selected
    ind_list = sorted(base_index_list)

    # get location of all points
    xb_data = []
    yb_data = []

    if len(ind_list) == 2:
        ind_1 = ind_list[0]
        ind_2 = ind_list[1]
        #print(i, i+1, ind_1, ind_2, len(ind_list))
        xb_data = xb_data + list(x[ind_1:ind_2])
        yb_data = yb_data + list(y[ind_1:ind_2])
    else:
        for i in range(len(ind_list)):
            if i % 2 == 0 and i != 1:
                ind_1 = ind_list[i]
                ind_2 = ind_list[i+1]
                #print(i, i+1, ind_1, ind_2, len(ind_list))
                xb_data = xb_data + list(x[ind_1:ind_2])
                yb_data = yb_data + list(y[ind_1:ind_2])

    return xb_data, yb_data

def get_base(localMinPositions, block_width, scan_len):
        """ get the baseline block/s from data with large sidelobes. """

        base=[] # entire basline block points
        localMinPositions=sorted(localMinPositions)

        basel=[] # left baseline blocks
        baser=[] # right baseline blocks
        lp=[]
        rp=[]
        basell=[]
        baserr=[]

        ind=4
        for i in range(len(localMinPositions)):

            #print(localMinPositions[i], block_width)

            if localMinPositions[i]<=block_width:
                # get everything before and after
                # print("0",localMinPositions[i], block_width+localMinPositions[i])
                base=base+list(np.arange(0,block_width+localMinPositions[i]+1))

                if localMinPositions[i] <= scan_len/2:
                    basel = basel+list(np.arange(0, block_width+localMinPositions[i]+1))

                    lp=lp+[localMinPositions[i]]
                    #print("1- ",localMinPositions[i])
                    basell.append(0)
                    basell.append(block_width+localMinPositions[i]+1)
                
                elif localMinPositions[i] > scan_len/2:
                    baser = baser + \
                        list(np.arange(0, block_width+localMinPositions[i]+1))
                    
                    rp=rp+[localMinPositions[i]]
                    #print("2+ ", localMinPositions[i])
                    baserr.append(0)
                    baserr.append(block_width+localMinPositions[i]+1)

            elif localMinPositions[i]>=scan_len-block_width:
                # get everything before and after
                #print(localMinPositions[i]-block_width, localMinPositions[i], scan_len)
                base=base+list(np.arange(localMinPositions[i]-block_width,scan_len))

                if localMinPositions[i] <= scan_len/2:
                    basel = basel+list(
                            np.arange(localMinPositions[i]-block_width, scan_len))
                    lp=lp+[localMinPositions[i]]
                    #print("3- ", localMinPositions[i])
                    basell.append(localMinPositions[i]-block_width)
                    basell.append(scan_len)

                elif localMinPositions[i] > scan_len/2:
                    baser = baser+list(
                        np.arange(localMinPositions[i]-block_width, scan_len-1))
                    
                    baserr.append(localMinPositions[i]-block_width)
                    baserr.append(scan_len-1)
                    rp = rp+[localMinPositions[i]]
                    #print("4+ ", localMinPositions[i])

            else:
                
                #print(localMinPositions[i]-block_width, localMinPositions[i], block_width+localMinPositions[i])
                
                base=base+list(np.arange(localMinPositions[i]-block_width,block_width+localMinPositions[i]))

                if localMinPositions[i] <= scan_len/2:

                    #print("5- ", localMinPositions[i])

                    basel=basel+list(
                            np.arange(localMinPositions[i]-block_width, block_width+localMinPositions[i]))

                    #print("6- ",lp,localMinPositions[i])
                    lp = lp+[localMinPositions[i]]

                    basell.append(localMinPositions[i]-block_width)
                    basell.append(block_width+localMinPositions[i])

                elif localMinPositions[i] > scan_len/2:
                        baser= baser+list(
                        np.arange(localMinPositions[i]-block_width, block_width+localMinPositions[i]))
                        
                        rp = rp+[localMinPositions[i]]
                    
                        end = block_width+localMinPositions[i]
                        baserr.append(localMinPositions[i]-block_width)

                        if end >=scan_len:

                            baserr.append(scan_len)

        return base, basel,baser,basell,baserr,lp,rp

def fit_poly_peak(xp, yp, order,log):
    """
        Fit the peak and estimate the errors.
    """

    peakCoeffs = poly_coeff(xp, yp, order)
    peakModel = np.polyval(peakCoeffs, xp)

    # Calculate the residual and rms of the peak fit
    peakRes, peakRms = calc_residual(peakModel, yp,log)
    return peakRes, peakRms, peakModel

def fit_gauss(offset, drift_power, p0):
    """
        Fit a Gaussian beam plus first-order
        plot the results.
    """

    gaus_coeff, var_matrix = curve_fit(gauss, offset, drift_power, p0)
    sigma = np.sqrt(np.diag(var_matrix))
    err_gauss_fit = 3 * sigma[0]  # we assume 3 sigma errors
    gauss_fit = gauss(offset, *gaus_coeff)

    # estimate the residual
    res, rms = calc_residual(gauss_fit, drift_power)

    # final error is the rms, we chose the larger of the two errors
    return gaus_coeff, var_matrix, gauss_fit, rms, res

def filter_scans(x, window_len=10, window='flat'):
    """
        smooth the data using a window with requested size.
    
        This method is based on the convolution of a scaled window with the signal.
        The signal is prepared by introducing reflected copies of the signal 
        (with the window size) in both ends so that transient parts are minimized
        in the begining and end part of the output signal.
        
        Args:
            x: the input signal 
            window_len: the dimension of the smoothing window; should be an odd integer
            window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 
                'blackman' flat window will produce a moving average smoothing.

        Returns:
            the smoothed signal
    """

    if x.ndim != 1:
        raise (ValueError, "smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise (ValueError, "Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise (
            ValueError, "Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]

    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(), s, mode='valid')
    return y

def cleanRmsCuts2(spl, x, y, scanLen, log):
    """ Clean the data using iterative rms cuts. """

    scanResBefore, scanRmsBefore = calc_residual(spl, y)
    finX, finY, scanRmsAfter, scanResAfter, finMaxSpl, finspl, pt = clean_data_iterative_fitting(
        x, y, scanLen, scanResBefore, scanRmsBefore,log)

    msg_wrapper("debug", log.debug, "scanRmsBefore: "+ str(scanRmsBefore))
    msg_wrapper("debug", log.debug, "scanRmsAfter: "+ str(scanRmsAfter))
    return scanResBefore, finX, finY, scanResAfter, finspl, scanRmsBefore, scanRmsAfter
