# ============================================================================#
# File: plot_manager.py                                                       #
# Author: Pfesesani V. van Zyl                                                #
# ============================================================================#

# Standard library imports
# --------------------------------------------------------------------------- #
from common.fitting import locate_baseline_blocks_auto
import sys
import numpy as np
import matplotlib.pyplot as pl
import os
from scipy import interpolate



# Local imports
# --------------------------------------------------------------------------- #
from common.messaging import msg_wrapper
import common.exceptions as ex
from common.fitting import check_for_nans, clean_rfi, fit_beam, sig_to_noise, fit_dual_beam
# =========================================================================== #


class PlotManager:
    
    """
        Plot manager. Manages the plotting process of the drift scan.

        Args:
            log (object): Logging object
            data (dict): dictionary of source parameters
            scanNum (int): Value representing the current scan
            scanNames (str): The names of the drift scans
            xData (array): x data of current scan
            yData (array): y data of current scan
            force (str): Force drift scan fitting yes or no
            keep (str): Keep original plots of the drift scan yes or no
            saveLocs (None): Save x-axis locations where fitting was done
            fitTheoretical (None): Fit drift scan at theoretical location, i.e. at fnbw 
            applyRFIremoval (None): Apply RFI removal to the data 
            autoFit (None): Fit drift scan at locations selected by the code.
    """

    def __init__(self, data, scanNum, scanNames, xData, yData, log,force="n",keep="n",saveLocs=None,fitTheoretical=None,applyRFIremoval=None,autoFit=None,scanSaveFolder=""):
  
        self.log = log
        self.data = data
        self.scanNum = scanNum              
        self.noTotScans = len(scanNames)
        self.rawX = xData                   
        self.rawY = yData         
        self.force = force        
        self.keep = keep
        self.saveLocs=saveLocs
        self.fitTheoretical=fitTheoretical
        self.applyRFIremoval=applyRFIremoval
        self.autoFit=autoFit
        self.scanSaveFolder=scanSaveFolder

        self.scanNames = scanNames            # Names of the drift scans
        self.flag = 0                         # Default Flag = 0
        self.name = data['FILENAME'][:18]     # Filename of current scan
        self.beamType = data['BEAMTYPE']      # Beam type of current scan
        self.hduLength = data["HDULENGTH"]    # Length of HDU
        self.FNBW = data['FNBW']              # First null beam width
        self.HPBW = data['HPBW']              # Half power beam width

        # Create a tag for the current scan under evaluation
        self.tag = self.create_tag()

    def create_tag(self):
        """
            Create a tag for the plots according to the current scan being processed.
            e.g. ON_RCP
        """

        msg_wrapper("debug",self.log.debug,"Set up name tags")

        if self.data["HDULENGTH"] == 7:
            tag = self._set_file_tag_nb()
        else:
            tag = self._set_file_tag_wb()

        return tag

    def _set_file_tag_wb(self):
        """ Set the name tag for wide beam data/plots. """

        tagId = int(self.scanNum)
        if tagId == 0:
            msg_wrapper("info",self.log.info,"Processing: ON_LCP")
            return "ON_LCP"
        else:
            msg_wrapper("info",self.log.info,"Processing: ON_RCP")
            return "ON_RCP"

    def _set_file_tag_nb(self):
        """ Set the name tag for narrow beam data/plots."""

        tagId = int(self.scanNum)
        if tagId == 0:
            msg_wrapper("info",self.log.info,"Processing: HPS_LCP")
            return "HPS_LCP"

        elif tagId == 1:
            msg_wrapper("info",self.log.info,"Processing: HPN_LCP")
            return "HPN_LCP"

        elif tagId == 2:
            msg_wrapper("info",self.log.info,"Processing: ON_LCP")
            return "ON_LCP"

        elif tagId == 3:
            msg_wrapper("info",self.log.info,"Processing: HPS_RCP")
            return "HPS_RCP"

        elif tagId == 4:
            msg_wrapper("info",self.log.info,"Processing: HPN_RCP")
            return "HPN_RCP"

        elif tagId == 5:
            msg_wrapper("info",self.log.info,"Processing: ON_RCP")
            return "ON_RCP"

    #@profile
    def process_plot(self):
        """ Process data plotting. """

        msg_wrapper("debug", self.log.debug, "Begin data cleansing")
        saveFolder = "currentScanPlots/"+self.data["FILENAME"][:18]+"_"

        # 1. Validate the data contains observations
        # Data with nan values are immediately discarded or ignored.
        self.rawY, self.flag = check_for_nans(self.rawY,self.log)

        if self.flag == 1:
            msg_wrapper("warning", self.log.warning, "Flag 1: Found nans")
            self.set_fit_params_to_zero()
            self.plot_no_fit(self.rawX, self.rawY, "Flag 1: Found nans")
        else:
            # 2. Clean the data, remove RFI
            # RFI can make fitting a drift scan imossible, this is why as 
            # part of the cleaning process we eliminate or remove any data
            # that is an outlier, surpassing all other data points by more than
            # 3 times the rms.

            #print(self.applyRFIremoval)
            if self.applyRFIremoval=="n":
                xCleanedRFI=self.rawX
                yCleanedRFI=self.rawY
                self.rmsBeforeClean=np.nan 
                self.rmsAfterClean=np.nan 
                spl=np.nan 
                pt=np.nan
            else:
                xCleanedRFI, yCleanedRFI, self.rmsBeforeClean, self.rmsAfterClean, spl, pt = clean_rfi(
                self.rawX, self.rawY,self.log)

            # make plots of the current scan for source overview
            # ----------------------------------------------------------------------
            self.plot_beam(self.rawX, self.rawY, self.scanNames[0], self.scanNames[self.scanNum+2],
                                "Raw data", saveFolder+"raw_data.png", col="C0")
            self.plot_beam(xCleanedRFI, yCleanedRFI, self.scanNames[0], self.scanNames[self.scanNum+2],
                            "Cleaned data", saveFolder+"cleaned_data.png", col="C1")
            self.overplot_raw_data(xCleanedRFI, yCleanedRFI, self.scanNames[0], self.scanNames[self.scanNum+2], "clean data", "currentScanPlots/overlay_data.png", "C1")
            # ----------------------------------------------------------------------

            #sys.exit()
            # if the data gets too cleaned, i.e. 1/2 or more of the peak is lost, keep the raw data
            cleanedPeakRatio = max(yCleanedRFI)/max(self.rawY) # ratio of peak cleaned / raw peak
            rmsRatio = self.rmsBeforeClean/ self.rmsAfterClean
            #print(f'max raw: {max(self.rawY):.3f}, max cleaned: {max(yCleanedRFI):.3f}, ratio: {cleanedPeakRatio:.3f}')
            #print(f'rmsb: {self.rmsBeforeClean:.3f}, rmsa: {self.rmsAfterClean:.3f},  ratio: {rmsRatio:.3f}, diff: {self.rmsBeforeClean-self.rmsAfterClean:.3f}')

            # if cleanedPeakRatio <0.9:
            #     xCleanedRFI=self.rawX
            #     yCleanedRFI=self.rawY
            #     print(self.rmsBeforeClean, self.rmsAfterClean)
            #     #sys.exit()

            # pl.plot(self.rawX, self.rawY, label=self.scanNames[0])
            # pl.plot(xCleanedRFI, yCleanedRFI)
            # pl.show()
            # pl.close()
            # sys.exit()

            # 3. Check rms for error handling of bad data
            if self.rmsAfterClean >= 1.0:
                self.flag = 2
                msg_wrapper("warning", self.log.warning, "RMS >= 1.0")
                self.set_fit_params_to_zero()
                self.plot_no_fit(xCleanedRFI, yCleanedRFI, 
                "Flag "+str(self.flag)+": High rms > 1")#,self.scanNames[0])#, self.scanNames[self.scanNum+2],
                # "Plot of drift scan "+self.data["FILENAME"][:18])
            else:

                # 4. Correct baseline and Create a new data set with no drift
                #sys.exit()
                # For dual beam data
                if "D" in self.beamType:
                    msg_wrapper("info",self.log.info,"Dual beam processing")
                    if self.data["BEAMTYPE"] == "06.0D":
                        npts = 150 # number of pts for baseline fit
                        if self.data["OBJECTTYPE"] == "CAL":
                            self.factor = .55
                        else:
                            self.factor = .8  # .65

                    elif self.data["BEAMTYPE"] == "03.5D":
                        npts = 100  # number of pts for baseline fit
                        if self.data["OBJECTTYPE"] == "CAL":
                            self.factor = .6
                        else:
                            self.factor = .65

                    # fit the data
                    self.yCorrected, self.driftRes, self.driftRms, self.driftSlope, self.baseLocs,\
                    self.xPeakDataAbeam, self.yPeakDataAbeam, self.yMaxAbeam, self.erryMaxAbeam, self.resAbeam,\
                    self.xPeakDataBbeam, self.yPeakDataBbeam, self.yMinBbeam, self.erryMinBbeam, self.resBbeam,\
                        msg, self.flag, self.peakLoca, self.peakLocb = fit_dual_beam(
                        xCleanedRFI, yCleanedRFI, self.HPBW, self.FNBW, self.factor, npts, self.data["LATITUDE"], self.data["OBJECTTYPE"], self.data, self.scanNum, self.force, self.log)

                    
                    if len(self.yCorrected) > 1:
              
                        if self.erryMaxAbeam > 1. or self.erryMinBbeam > 1.:
                            msg = "Peak rms > 1"
                            self.flag = 13
                            msg_wrapper("warning", self.log.warning, msg)
                            self.set_fit_params_to_zero()
                            self.plot_no_fit(self.rawX, self.rawY, msg)

                        elif np.isinf(self.erryMaxAbeam) or np.isinf(self.erryMinBbeam):
                            msg = "RMS is +- inf"
                            self.flag = 14
                            msg_wrapper("warning", self.log.warning, msg)
                            self.set_fit_params_to_zero()
                            self.plot_no_fit(self.rawX, self.rawY, msg)

                        else:
                            # Estimate the signal to noise ratio
                            self.s2na = sig_to_noise(
                                        abs(self.yMaxAbeam), self.driftRes, self.log)
                            self.s2nb = sig_to_noise(
                                        abs(self.yMinBbeam), self.driftRes, self.log)
                            print("S/N A beam: {:.2f} \nS/N B beam: {:.2f}".format(self.s2na, self.s2nb))

                            if self.s2na < 3. or self.s2nb < 3.:
                                msg="Got a s2n < 3"
                                self.flag = 15
                                msg_wrapper("warning", self.log.warning, msg)
                            else:
                                pass

                            scanLen=len(xCleanedRFI)
                            ptLimit = int(scanLen*0.04) # Point limit, number of allowed points per base block
                            lb  = [0,ptLimit]
                            rb = [scanLen-ptLimit,scanLen-1]
                            
                            lbl=[]
                            rbl=[]
                            [lbl.append(float(f'{xCleanedRFI[xx]:.3f}')) for xx in lb]
                            [rbl.append(float(f'{xCleanedRFI[xx]:.3f}')) for xx in rb]

                            datadict={}
                            datadict['name']=self.data['FILENAME'][:18]
                            datadict['scan']=self.tag
                            datadict['leftBaselinePts']=lbl
                            datadict['rightBaselinePts']=rbl
                            datadict['baselineRms']=self.driftRms
                            
                            # potential for buggy behavior
                            try:
                                datadict['baselineSlope']=self.driftSlope
                                datadict['baselineIntercept']=np.nan#self.driftCoeffs[1]
                                datadict['peakPtsA']= [float(f'{self.xPeakDataAbeam[0]:.3f}'), float(f'{self.xPeakDataAbeam[-1]:.3f}')]
                                datadict['peakPtsB']= [float(f'{self.xPeakDataBbeam[0]:.3f}'), float(f'{self.xPeakDataBbeam[-1]:.3f}')]
                            except:
                                datadict['baselineSlope'] = np.nan 
                                datadict['baselineIntercept'] = np.nan      
                                datadict['peakPtsA']= np.nan        
                                datadict['peakPtsB']= np.nan            
                            
                            datadict['yMaxA']= self.yMaxAbeam
                            datadict['yMaxErrA']= self.erryMaxAbeam
                            datadict['yMinB']= self.yMinBbeam
                            datadict['yMinErrB']= self.erryMinBbeam
                            
                            #print("\nRaw Data ")
                            #print(self.autoFit)
                            #print("\nProcessed Data ")
                            #print(datadict,"\n")

                            if self.saveLocs=="y":
                                msg_wrapper("debug", self.log.debug,"Saving theoretical locs")
                                with open('plot_locs.txt','a') as fl:
                                    fl.write(('{};{};{};{};{:.3f};{:.3f};{:.3f};{};{:.3f};{:.3f}\n').format(
                                        datadict['name'], datadict['scan'], datadict['leftBaselinePts'],datadict['rightBaselinePts'], 
                                        datadict['baselineSlope'], datadict['baselineIntercept'], datadict['baselineRms'],
                                        datadict['peakPtsA'],datadict['yMaxA'] ,datadict['yMaxErrA'],
                                        datadict['peakPtsB'],datadict['yMaxB'] ,datadict['yMaxErrB']))
                            
                            elif(self.saveLocs!="y"):
                                pass

                            # If all is good, plot basic
                            self.plot_basic_db(
                                        xCleanedRFI, self.yCorrected)

                    else:
                        msg="No data"
                        self.flag = 1
                        msg_wrapper("warning", self.log.warning, msg)
                        self.set_fit_params_to_zero()
                        self.plot_no_fit(self.rawX, self.rawY, msg)

                # for single beam data
                if "S" in self.beamType:
                    
                    # set initial parameters for data fitting
                    p0 = [max(yCleanedRFI), np.mean(xCleanedRFI), self.HPBW, .01, .0]

                    self.peakFit, self.peakModel, self.peakRms, yCorrected, peakPts, msg, self.driftRes, self.driftRms, self.driftCoeffs, self.fitRes, self.mid, self.flag,  self.baseLeft, self.baseRight, self.base, self.peakLoc,self.lb,self.rb = fit_beam(
                        xCleanedRFI, yCleanedRFI, p0, self.FNBW, self.data["LATITUDE"], self.data, self.scanNum, self.force, self.log, self.fitTheoretical, self.autoFit)

                    # Check residuals make sense
                    data = self.driftRes

                    # expect gaussian noise, need to figure out how to treat outlier data
                    # generate random gaussian noise and subtract it from residal result and 
                    # examine results.

                    #print(data)

                    # if len(data)==0:
                    #     msg = "\nPossible spike in Residuals "
                    #     msg_wrapper("warning", self.log.warning, msg)
                    #     self.flag = 120
                    #     self.set_fit_params_to_zero()
                    #     #pl.hist(data)
                    #     #pl.show()
                    #     self.plot_no_fit(self.rawX, self.rawY, msg)

                    # #print(min(data),max(data), abs(min(data)/max(data)), abs(max(data)/min(data)) )
                    # elif abs(min(data)) > ((abs(max(data))) + 0.8*abs(max(data))):
                    #     msg = "\nPossible spike in Residuals 1"
                    #     msg_wrapper("warning", self.log.warning, msg)
                    #     self.flag = 121
                    #     self.set_fit_params_to_zero()
                    #     #pl.hist(data)
                    #     #pl.show()
                    #     self.plot_no_fit(self.rawX, self.rawY, msg)

                    # elif abs(max(data)) > ((abs(min(data))) + 0.8*abs(min(data))):
                    #     msg = "\nPossible spike in Residuals 2"
                    #     msg_wrapper("warning", self.log.warning, msg)
                    #     self.flag = 122
                    #     self.set_fit_params_to_zero()
                    #     self.plot_no_fit(self.rawX, self.rawY, msg)
        
                    # Ensure we have a baseline corrected scan
                    #el

                    if len(yCorrected) > 1:

                        if max(self.peakModel) < 0:
                            msg = "\nMax < 0"
                            msg_wrapper("warning", self.log.warning, msg)
                            self.flag = 12
                            self.set_fit_params_to_zero()
                            self.plot_no_fit(self.rawX, self.rawY, msg)

                        elif self.peakRms > 1.:
                            msg = "\nPeak rms > 1"
                            msg_wrapper("warning", self.log.warning, msg)
                            self.flag = 13
                            self.set_fit_params_to_zero()
                            self.plot_no_fit(self.rawX, self.rawY, msg)

                        elif np.isinf(self.peakRms):
                            msg = "\nRMS is +- inf"
                            msg_wrapper("warning", self.log.warning, msg)
                            self.flag = 14
                            self.set_fit_params_to_zero()
                            self.plot_no_fit(self.rawX, self.rawY, msg)
                            sys.exit()

                        else:

                            # =============================================
                            # Estimate the signal to noise ratio
                            # =============================================
                            msg="Peak = {:.3f} +- {:.3f} [K]".format(self.peakFit, self.peakRms)
                            msg_wrapper("info", self.log.info, msg)
                            self.s2n = sig_to_noise(
                                        max(yCorrected), self.driftRes, self.log)
                            msg2="S/N: {:.2f}".format(self.s2n)
                            msg_wrapper("info", self.log.info, msg2)

                            if self.s2n < 3.0:
                                msg=("signal to noise ratio < 3")
                                self.flag = 15
                                msg_wrapper("warning", self.log.warning, msg)
                            else:
                                pass

                            #print("hey")
                            lbl=[]
                            rbl=[]
                            [lbl.append(float(f'{xCleanedRFI[xx]:.3f}')) for xx in self.lb]
                            [rbl.append(float(f'{xCleanedRFI[xx]:.3f}')) for xx in self.rb]

                            datadict={}
                            datadict['name']=self.data['FILENAME'][:18]
                            datadict['scan']=self.tag
                            datadict['leftBaselinePts']=lbl
                            datadict['rightBaselinePts']=rbl
                            datadict['baselineRms']=self.driftRms
                            #datadict['baselineSlope']=self.driftCoeffs[0]
                            #print(datadict)
                            #sys.exit()
                            
                            try:
                                datadict['baselineSlope']=self.driftCoeffs[0]
                                datadict['baselineIntercept']=self.driftCoeffs[1]
                                datadict['peakPts']= [float(f'{xCleanedRFI[peakPts[0]]:.3f}'), float(f'{xCleanedRFI[peakPts[-1]]:.3f}')]
                            except:
                                datadict['baselineSlope'] = np.nan 
                                datadict['baselineIntercept'] = np.nan      
                                datadict['peakPts']= np.nan                
                            
                            datadict['yMax']= self.peakFit
                            datadict['yMaxErr']= self.peakRms
                            
                            #print("\nRaw Data ")
                            #print(self.autoFit)
                            #print("\nProcessed Data ")
                            #print(datadict,"\n")

                            if self.saveLocs=="y" and self.fitTheoretical!="y":
                                msg_wrapper("debug", self.log.debug,"Saving ffree fitting locs")
                                with open('plot_locs.txt','a') as fl:
                                    fl.write(('{};{};{};{};{:.3f};{:.3f};{:.3f};{};{:.3f};{:.3f}\n').format(
                                        datadict['name'], datadict['scan'], datadict['leftBaselinePts'],datadict['rightBaselinePts'], 
                                        datadict['baselineSlope'], datadict['baselineIntercept'], datadict['baselineRms'],
                                        datadict['peakPts'],datadict['yMax'] ,datadict['yMaxErr']))

                            elif self.saveLocs=="y" and self.fitTheoretical=="y":
                                msg_wrapper("debug", self.log.debug,"Saving theoretical locs")
                                with open('plot_locs.txt','a') as fl:
                                    fl.write(('{};{};{};{};{:.3f};{:.3f};{:.3f};{};{:.3f};{:.3f}\n').format(
                                        datadict['name'], datadict['scan'], datadict['leftBaselinePts'],datadict['rightBaselinePts'], 
                                        datadict['baselineSlope'], datadict['baselineIntercept'], datadict['baselineRms'],
                                        datadict['peakPts'],datadict['yMax'] ,datadict['yMaxErr']))
                            
                            elif(self.saveLocs!="y"):
                                pass
                            
                            # Plot the corrected drift scan
                            self.plot_result(xCleanedRFI, yCorrected, peakPts)
                            

                    else:
                        #self.flag = 1
                        #msg = "Found nans"
                        msg_wrapper("warning", self.log.warning,
                                        msg)
                        self.set_fit_params_to_zero()
                        self.plot_no_fit(self.rawX, self.rawY, msg)

        pl.clf()
            
            
    def set_fit_params_to_zero(self):
        """ Set fit parameters to zero/nan. """

        msg_wrapper("debug", self.log.debug,
                    "Setting data to zero for encountered error")

        if "D" in self.data["BEAMTYPE"]:
            # for dual beam data
            self.yMaxAbeam = np.nan
            self.erryMaxAbeam = np.nan
            self.s2na = np.nan
            self.yMinBbeam = np.nan
            self.erryMinBbeam = np.nan
            self.s2nb = np.nan
            self.rmsBeforeClean = np.nan
            self.rmsAfterClean = np.nan
            self.driftRms = np.nan
            self.peakLoca = np.nan
            self.peakLocb = np.nan
            self.driftSlope = np.nan

        else:
            # for single beam data
            self.peakFit = np.nan
            self.peakRms = np.nan
            self.s2n = np.nan
            self.rmsBeforeClean = np.nan
            self.rmsAfterClean = np.nan
            self.driftRms = np.nan
            self.driftSlope = np.nan
            self.peakLoc = np.nan

    def plot_no_fit(self, x=[], y=[], label="", xlabel="", ylabel="",  title=""):
        """
        Plot corrupted data.
        """

        PLOT_PATH = self.set_plot_path()

        if title == "":
            plotTitle = "Plot " + self.name[:18] + \
                " of " + self.data["SOURCEDIR"]
        else:
            plotTitle = title

        pl.title(plotTitle)

        if xlabel == "":
            pl.xlabel("Scandist [deg]")
        else:
            pl.xlabel(xlabel)

        if ylabel == "":
            pl.ylabel("Ta [K]")
        else:
            pl.ylabel(ylabel)

        pl.plot(x, y, 'r', label=label)
        pl.legend(loc="best")
        pl.savefig(PLOT_PATH)
        pl.close('all')

    def set_plot_path(self, ext=".png"):
        """ Set path where plot will be saved. """

        plotPath = f"{self.scanSaveFolder}/{self.name}_{self.tag+ext}"
        
        # print(plotPath)
        # print(self.scanSaveFolder)
        # sys.exit()

        return plotPath

    def plot_beam(self, x, y, xlab, ylab, title,  saveas, label="",col="k"):
        """ make a plot of the beam"""


        pl.title(title)
        # pl.xlabel(xlab+" [Deg]")
        # pl.ylabel(ylab+" antenna temp [K]")
        pl.xlabel("Offset [Deg]")
        pl.ylabel("Ta [K]")
        if col == "k":
            if label != "":
                pl.plot(x, y, col, label)
            else:
                pl.plot(x, y, col, label=title)
        else:
            if label != "":
                pl.plot(x, y, label=label)
            else:
                pl.plot(x, y, label=title)
        
        pl.legend(loc="best")
        pl.savefig(saveas)
        pl.close('all')

    def plot_raw_beam(self, x, y, title, saveas):
        """ make a plot of the raw beam"""

        pl.title(title)
        pl.xlabel("Offset [Deg]")
        pl.ylabel("Ta [K]")
        pl.plot(x, y, 'k', label="raw data")
        pl.legend(loc="best")
        pl.savefig(saveas)
        pl.close('all')
        
    def overplot_raw_data(self, x, y, xlabel, ylabel, title, saveas, col="k"):
        """ make two plots overlayed on each other """

        pl.title("Raw vs "+title)
        pl.xlabel("Offset [Deg]")
        pl.ylabel("Ta [K]")
        pl.plot(self.rawX, self.rawY, "C0", label="Raw data")
        pl.plot(x, y, col, label=title)
        pl.legend(loc="best")
        pl.savefig(saveas)
        #pl.show()
        pl.close('all')

    def plot_result(self, x, y, peakPts, pt=""):
        """
        Plot the result of the corrected data and save to file.

        Parameters
        ----------

            x : float array of size N
                data for the x-axis
            y : float array of size N
                data for the y-axis
            peakPts : locations where peak was fit
        """

        loc = 1  # legend location: upper right corner
        PLOT_PATH = self.set_plot_path()

        title="Plot of " + self.data['OBJECT']+" observation "+self.name[:18]+" at ( " + str(self.data['CENTFREQ'])+" MHz)"
        xlabel="Scandist [deg]"
        ylabel="Ta [K]"

        if self.keep == "y":
            saveloc='rawPlots'+os.path.dirname(PLOT_PATH[5:])
            try:
                os.makedirs('rawPlots'+os.path.dirname(PLOT_PATH[5:]))
            except:
                pass
            
            plotPath = 'rawPlots'+PLOT_PATH[5:]
            self.plot_raw_beam(self.rawX, self.rawY, title,  plotPath)
        else:
            pass

        # create y=0 line
        zero = np.zeros_like(x)

        # create plot layout
        gridsize = (5, 2)
        fig = pl.figure(figsize=(12, 8))
        ax1 = pl.subplot2grid(gridsize, (0, 0), colspan=3, rowspan=3)

        if pt != "":
            ax1.set_title(
                "Plot of " + self.name[:18]+", deleted "+str(pt)+" pts")
        else:
            #ax1.set_title("Plot of " + self.name[:18])
            ax1.set_title("Plot of " + self.data['OBJECT']+" observation "+self.name[:18]+" at ( " + str(self.data['CENTFREQ'])+" MHz)")


        ax1.set_ylabel("Ta [K]")
        ax1.set_xlabel("Scandist [deg]")
        col = 'k'#'b'  # color of fit locations

        # main plot
        ax1.plot(x, y, 'k',label="data")  # cleaned data
        ax1.plot(x[peakPts], y[peakPts], col, label="peak fit data")
        ax1.plot(x[peakPts], self.peakModel, 'r', label="Ta [K] = %.3f +- %.3f" %(max(self.peakModel), self.peakRms))

        if self.saveLocs=="y":
            ax1.plot(x[self.baseLeft],    y[self.baseLeft], col+".",label="baseline fit locs")
            ax1.plot(x[self.baseRight],  y[self.baseRight], col+".")
        ax1.plot(x, zero, 'gray')
        lim = pl.axis('tight')
        ax1.legend(loc=loc)

        # plot 2
        ax2 = pl.subplot2grid(gridsize, (4, 0))
        self.plot_residuals(ax2, self.driftRes, "Residual of baseline fit", loc)

        # ax21=pl.subplot2grid(gridsize, (4, 1))
        # ax21.hist(self.driftRes,bins=50, orientation="horizontal",density=True)
        # ax21.set_xlabel('Distribution')

        # plot 3
        ax3 = pl.subplot2grid(gridsize, (4, 1))
        self.plot_residuals(ax3, self.fitRes, "Residual of peak fit", loc)

        pl.savefig(PLOT_PATH)
        pl.close('all') #fig
        #sys.exit()

    def plot_residuals(self, axis, data, label, loc):
        """ Data plotting configuration for residuals """

        x=np.zeros(len(data))

        axis.set_title(label)
        pl.plot(data, 'k', label="data")
        # pl.ylim((-0.5,0.5))
        pl.ylim((-.1-max(data),max(data)+.1))
        pl.plot(x,color='k',alpha=0.3)
        #pl.show()
        #print(np.zeros(len(data)))

        # print(min(data),max(data), abs(min(data)/max(data)), abs(max(data)/min(data)) )

        # if abs(min(data)) > ((abs(max(data))) + 0.5*abs(max(data))):
        #     sys.exit()
        # elif abs(max(data)) > ((abs(min(data))) + 0.5*abs(min(data))):
        #     sys.exit()
        # else:
        #     pass

        # coeffs=np.polyfit(x, data, 1)
        # model = np.polyval(coeffs, x)
        # print(coeffs)
        # sys.exit()
        axis.set_ylabel("res [K]")
        axis.set_xlabel("N")
        axis.legend(loc=loc)

    def plot_basic_db(self, x, y):
        """
        Plot results of dual beam data fitting.
        """

        # setup plot basics
        loc = 1  # legend location: upper right corner
        PLOT_PATH = self.set_plot_path()
        title="Plot of " + self.data['OBJECT']+" observation "+self.name[:18]+" at ( " + str(self.data['CENTFREQ'])+" MHz)"
        #print(title)
        #sys.exit()
        xlabel="Scandist [deg]"
        ylabel="Ta [K]"

        if self.keep == "y":
            saveloc='rawPlots'+os.path.dirname(PLOT_PATH[5:])
            try:
                os.makedirs('rawPlots'+os.path.dirname(PLOT_PATH[5:]))
            except:
                pass
            
            plotPath = 'rawPlots'+PLOT_PATH[5:]
            self.plot_raw_beam(self.rawX, self.rawY, title,  plotPath)

        #sys.exit()
        col = 'r'

        # create y=0 line
        zero = np.zeros_like(x)

        # create plot layout
        gridsize = (7, 2)
        fig = pl.figure(figsize=(12, 8))
        ax1 = pl.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=3)
        zero = np.zeros_like(x) 
        ax1.set_ylabel(ylabel)
        ax1.set_xlabel(xlabel)
        ax1.set_title(title)

        # split baselocs
        baseLeft = np.where(x[self.baseLocs] < 0)[0]
        baseRight = self.baseLocs[baseLeft[-1]+1:]

        # main plot
        ax1.plot(x, y, "k", label="raw data")

        ax1.plot(self.xPeakDataAbeam, self.yPeakDataAbeam, col,
                 label="Ta [K] = %.3f +- %.3f" % (self.yMaxAbeam, self.erryMaxAbeam))
        ax1.plot(self.xPeakDataBbeam, self.yPeakDataBbeam, col,
                 label="Ta [K] = %.3f +- %.3f" % (self.yMinBbeam, self.erryMinBbeam))
        if self.saveLocs=="y":
            ax1.plot(x[baseLeft], y[baseLeft], col+".")
            ax1.plot(x[baseRight], y[baseRight], col+".")
        ax1.plot(x, zero, 'gray')

        lim = pl.axis('tight')

        ax1.legend(loc=loc)

        # residual of baseline block
        ax2 = pl.subplot2grid(gridsize, (4, 0), colspan=2, rowspan=1)
        #ax21=
        self.plot_residuals(ax2, self.driftRes, "Residual of base fit", loc)

        # residual of left peak
        ax3 = pl.subplot2grid(gridsize, (6, 0))
        self.plot_residuals(ax3, self.resAbeam, "Residual of peak A", loc)

        # residual of right peak
        ax4 = pl.subplot2grid(gridsize, (6, 1))
        self.plot_residuals(ax4, self.resBbeam, "Residual of peak B", loc)

        #pl.show()
        pl.savefig(PLOT_PATH)
        pl.close('all')#fig
        #sys.exit()
