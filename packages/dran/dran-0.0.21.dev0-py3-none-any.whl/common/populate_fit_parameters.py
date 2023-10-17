# =========================================================================== #
# File    : populate_fit_parameters.py                                        #
# Author  : Pfesesani V. van Zyl                                              #
# =========================================================================== #

# Standard library imports
# --------------------------------------------------------------------------- #
import numpy as np
import sys

# Local imports
# --------------------------------------------------------------------------- #
#sys.path.append("src/")
from common.messaging import msg_wrapper
import common.calc_pss as cp
# =========================================================================== #

class PopulateFitParameters:
    """ 
    Populate the fitted parameters.
    """

    def __init__(self, scanNum, srcData, plot,log):
        self.srcData = srcData
        self.plot = plot
        self.scanNum = scanNum
        self.log=log

        
        msg_wrapper("debug", self.log.debug, "Populating data from fit")

    def calc_wb_parms(self):
        """
        Populate the wide beam parameters.
        """

        if self.scanNum == 0:

            self.srcData['OLTA'] = self.plot.peakFit
            self.srcData['OLDTA'] = self.plot.peakRms
            self.srcData['OLS2N'] = self.plot.s2n
            self.srcData['OLTAPEAKLOC'] = self.plot.peakLoc

            if self.srcData['OBJECTTYPE'] == 'CAL':

                # CALCULATE PSS
                PSS, dPSS, appEff = cp.calc_pss(
                    self.srcData['FLUX'], self.plot.peakFit, self.plot.peakRms)
                self.srcData['OLPSS'] = PSS
                self.srcData['OLDPSS'] = dPSS
                self.srcData["OLAPPEFF"] = appEff
                self.srcData['OLFLAG'] = self.plot.flag

                self.srcData['OLRMSB'] = self.plot.rmsBeforeClean
                self.srcData['OLRMSA'] = self.plot.rmsAfterClean

                #self.plot.driftCoeffs[0]

                try:
                    self.srcData['OLBSLOPE']=self.plot.driftCoeffs[0]
                    self.srcData['OLBSRMS']=self.plot.driftCoeffs[1]

                    #self.srcData['OLBSLOPE'] = self.plot.driftCoeffs[0]
                    # On LCP Base Slope Rms
                    #self.srcData['OLBSRMS'] = self.plot.driftRms
                    #self.srcData["OLBSLOPEL"] = self.plot.slopel
                    #self.srcData["OLBSLOPER"] = self.plot.sloper

                except Exception:
                    self.srcData['OLBSLOPE'] = np.nan
                    #self.srcData["OLBSLOPEL"] = np.nan
                    #self.srcData["OLBSLOPER"] = np.nan
                    self.srcData['OLBSRMS'] = np.nan
                    #self.srcData['OLFLAG'] = 6
            else:
                self.srcData['OLRMSB'] = self.plot.rmsBeforeClean
                self.srcData['OLRMSA'] = self.plot.rmsAfterClean
                self.srcData['OLFLAG'] = self.plot.flag

                try:
                    self.srcData['OLBSLOPE']=self.plot.driftCoeffs[0]
                    self.srcData['OLBSRMS']=self.plot.driftCoeffs[1]

                    #self.srcData['OLBSLOPE'] = self.plot.driftCoeffs[0]
                    #self.srcData["OLBSLOPEL"] = self.plot.slopel
                    #self.srcData["OLBSLOPER"] = self.plot.sloper
                    # On LCP Base Slope Rms
                    #self.srcData['OLBSRMS'] = self.plot.driftRms

                except Exception:
                    self.srcData['OLBSLOPE'] = np.nan
                    #self.srcData["OLBSLOPEL"] = np.nan
                    #self.srcData["OLBSLOPER"] = np.nan
                    self.srcData['OLBSRMS'] = np.nan
                    #self.srcData['OLFLAG'] = 6

        else:

            self.srcData['ORTA'] = self.plot.peakFit
            self.srcData['ORDTA'] = self.plot.peakRms
            self.srcData['ORS2N'] = self.plot.s2n
            self.srcData['ORTAPEAKLOC'] = self.plot.peakLoc

            if self.srcData['OBJECTTYPE'] == 'CAL':

                # CALCULATE PSS
                PSS, dPSS, appEff = cp.calc_pss(
                    self.srcData['FLUX'], self.plot.peakFit, self.plot.peakRms)
                self.srcData['ORPSS'] = PSS
                self.srcData['ORDPSS'] = dPSS
                self.srcData["ORAPPEFF"] = appEff
                self.srcData['ORFLAG'] = self.plot.flag
                self.srcData['ORRMSB'] = self.plot.rmsBeforeClean
                self.srcData['ORRMSA'] = self.plot.rmsAfterClean

                try:
                    self.srcData['ORBSLOPE']=self.plot.driftCoeffs[0]
                    self.srcData['ORBSRMS']=self.plot.driftCoeffs[1]

                    #self.srcData['ORBSLOPE'] = self.plot.driftCoeffs[0]
                    #self.srcData["ORBSLOPEL"] = self.plot.slopel
                    #self.srcData["ORBSLOPER"] = self.plot.sloper

                    # On LCP Base Slope Rms
                    #self.srcData['ORBSRMS'] = self.plot.driftRms
                except Exception:
                    self.srcData['ORBSLOPE'] = np.nan
                    #self.srcData["ORBSLOPEL"] = np.nan
                    #self.srcData["ORBSLOPER"] = np.nan
                    self.srcData['ORBSRMS'] = np.nan
            else:
                self.srcData['ORRMSB'] = self.plot.rmsBeforeClean
                self.srcData['ORRMSA'] = self.plot.rmsAfterClean
                self.srcData['ORFLAG'] = self.plot.flag

                try:
                    self.srcData['ORBSLOPE']=self.plot.driftCoeffs[0]
                    self.srcData['ORBSRMS']=self.plot.driftCoeffs[1]
                    
                    #self.srcData['ORBSLOPE'] = self.plot.driftCoeffs[0]
                    #self.srcData["ORBSLOPEL"] = self.plot.slopel
                    #self.srcData["ORBSLOPER"] = self.plot.sloper

                    # On LCP Base Slope Rms
                    #self.srcData['ORBSRMS'] = self.plot.driftRms

                except Exception:
                    self.srcData['ORBSLOPE'] = np.nan
                    #self.srcData["OLBSLOPEL"] = np.nan
                    #self.srcData["OLBSLOPER"] = np.nan
                    self.srcData['ORBSRMS'] = np.nan

    def calc_nb_parms(self):
        """
        Populate the narrow beam parameters.
        """

        #self.srcData["PLOT_URL"] = self.plot.PLOT_URL

        if self.scanNum == 0:
            self.srcData['SLTA'] = self.plot.peakFit
            self.srcData['SLDTA'] = self.plot.peakRms
            self.srcData['SLS2N'] = self.plot.s2n
            self.srcData['SLFLAG'] = self.plot.flag
            self.srcData['SLTAPEAKLOC'] = self.plot.peakLoc
            self.add_hpslcp_parameters()

        elif self.scanNum == 1:
            self.srcData['NLTA'] = self.plot.peakFit
            self.srcData['NLDTA'] = self.plot.peakRms
            self.srcData['NLS2N'] = self.plot.s2n
            self.srcData['NLFLAG'] = self.plot.flag
            self.srcData['NLTAPEAKLOC'] = self.plot.peakLoc
            self.add_hpnlcp_parameters()

        elif self.scanNum == 2:
            self.srcData['OLTA'] = self.plot.peakFit
            self.srcData['OLDTA'] = self.plot.peakRms
            self.srcData['OLS2N'] = self.plot.s2n
            self.srcData['OLFLAG'] = self.plot.flag
            self.srcData['OLTAPEAKLOC'] = self.plot.peakLoc
            self.add_onlcp_parameters()

            if self.srcData['OBJECTTYPE'] == 'CAL':

                # CALCULATE PSS

                if self.srcData["BEAMTYPE"] == "01.3S":
                    try:
                        PSS, dPSS, PC, TA, DTA, appEff = cp.calc_pc_pss(self.scanNum, self.srcData['SLTA'], self.srcData['SLDTA'], self.srcData[
                        'NLTA'], self.srcData['NLDTA'], self.srcData['OLTA'], self.srcData['OLDTA'], self.srcData['TOTAL_PLANET_FLUX_D'], self.srcData)
                    except:
                        PSS=np.nan
                        dPSS=np.nan
                        PC=np.nan
                        TA=np.nan
                        DTA=np.nan
                        appEff=np.nan

                elif self.srcData['BEAMTYPE'] == "02.5S":

                    #print(self.srcData)
                    #sys.exit()
                    # Force jupiter 12.178GHz to use jupiter 22 ghz process
                    if self.srcData['SOURCEDIR']== 'Jupiter_12.178GHz':
                        PSS, dPSS, PC, TA, DTA, appEff = cp.calc_pc_pss(self.scanNum, self.srcData['SLTA'], self.srcData['SLDTA'], self.srcData[
                        'NLTA'], self.srcData['NLDTA'], self.srcData['OLTA'], self.srcData['OLDTA'], self.srcData['TOTAL_PLANET_FLUX_D'], self.srcData)
                    else:
                        PSS, dPSS, PC, TA, DTA, appEff = cp.calc_pc_pss(self.scanNum, self.srcData['SLTA'], self.srcData['SLDTA'], self.srcData[
                            'NLTA'], self.srcData['NLDTA'], self.srcData['OLTA'], self.srcData['OLDTA'], self.srcData['FLUX'], self.srcData)

                else:
                    PSS, dPSS, PC, TA, DTA, appEff = cp.calc_pc_pss(self.scanNum, self.srcData['SLTA'], self.srcData['SLDTA'], self.srcData[
                        'NLTA'], self.srcData['NLDTA'], self.srcData['OLTA'], self.srcData['OLDTA'], self.srcData['FLUX'], self.srcData)

                self.srcData['OLPC'] = PC
                self.srcData['COLTA'] = TA
                self.srcData['COLDTA'] = DTA
                self.srcData['OLPSS'] = PSS
                self.srcData['OLDPSS'] = dPSS
                self.srcData["OLAPPEFF"] = appEff

            else:
                # CALCULATE POINTING CORRECTION
                PC, TA, DTA = cp.calc_pc(self.scanNum,
                                        self.srcData['SLTA'], self.srcData['SLDTA'], self.srcData['NLTA'], self.srcData['NLDTA'], self.srcData['OLTA'], self.srcData['OLDTA'], self.srcData)
                self.srcData['OLPC'] = PC
                self.srcData['COLTA'] = TA
                self.srcData['COLDTA'] = DTA

        elif self.scanNum == 3:
            self.srcData['SRTA'] = self.plot.peakFit
            self.srcData['SRDTA'] = self.plot.peakRms
            self.srcData['SRS2N'] = self.plot.s2n
            self.srcData['SRFLAG'] = self.plot.flag
            self.srcData['SRTAPEAKLOC'] = self.plot.peakLoc
            self.add_hpsrcp_parameters()

        elif self.scanNum == 4:
            self.srcData['NRTA'] = self.plot.peakFit
            self.srcData['NRDTA'] = self.plot.peakRms
            self.srcData['NRS2N'] = self.plot.s2n
            self.srcData['NRFLAG'] = self.plot.flag
            self.srcData['NRTAPEAKLOC'] = self.plot.peakLoc
            self.add_hpnrcp_parameters()

        elif self.scanNum == 5:
            self.srcData['ORTA'] = self.plot.peakFit
            self.srcData['ORDTA'] = self.plot.peakRms
            self.srcData['ORS2N'] = self.plot.s2n
            self.srcData['ORFLAG'] = self.plot.flag
            self.srcData['ORTAPEAKLOC'] = self.plot.peakLoc
            self.add_onrcp_parameters()

            if self.srcData['OBJECTTYPE'] == 'CAL':
                # CALCULATE PSS

                if self.srcData["BEAMTYPE"] == "01.3S":
                    try:
                        PSS, dPSS, PC, TA, DTA, appEff = cp.calc_pc_pss(self.scanNum, self.srcData['SRTA'], self.srcData['SRDTA'], self.srcData['NRTA'],
                                                                    self.srcData['NRDTA'], self.srcData['ORTA'], self.srcData['ORDTA'], self.srcData['TOTAL_PLANET_FLUX_D'], self.srcData)
                    except:
                        PSS=np.nan
                        dPSS=np.nan
                        PC=np.nan
                        TA=np.nan
                        DTA=np.nan
                        appEff=np.nan
                        
                elif self.srcData['BEAMTYPE'] == "02.5S":
                    # Force jupiter 12.178GHz to use jupiter 22 ghz process
                    if self.srcData['SOURCEDIR']== 'Jupiter_12.178GHz':
                        PSS, dPSS, PC, TA, DTA, appEff = cp.calc_pc_pss(self.scanNum, self.srcData['SRTA'], self.srcData['SRDTA'], self.srcData[
                        'NRTA'], self.srcData['NRDTA'], self.srcData['ORTA'], self.srcData['ORDTA'], self.srcData['TOTAL_PLANET_FLUX_D'], self.srcData)
                    else:
                        PSS, dPSS, PC, TA, DTA, appEff = cp.calc_pc_pss(self.scanNum, self.srcData['SRTA'], self.srcData['SRDTA'], self.srcData[
                            'NRTA'], self.srcData['NRDTA'], self.srcData['ORTA'], self.srcData['ORDTA'], self.srcData['FLUX'], self.srcData)

                else:
                    PSS, dPSS, PC, TA, DTA, appEff = cp.calc_pc_pss(
                        self.scanNum, self.srcData['SRTA'], self.srcData['SRDTA'], self.srcData['NRTA'], self.srcData['NRDTA'], self.srcData['ORTA'], self.srcData['ORDTA'], self.srcData['FLUX'], self.srcData)

                self.srcData['ORPC'] = PC
                self.srcData['CORTA'] = TA
                self.srcData['CORDTA'] = DTA
                self.srcData['ORPSS'] = PSS
                self.srcData['ORDPSS'] = dPSS
                self.srcData['ORAPPEFF'] = appEff

            else:
                # CALCULATE POINTING CORRECTION
                PC, TA, DTA = cp.calc_pc(self.scanNum,
                                        self.srcData['SRTA'], self.srcData['SRDTA'], self.srcData['NRTA'], self.srcData['NRDTA'], self.srcData['ORTA'], self.srcData['ORDTA'], self.srcData)
                self.srcData['ORPC'] = PC
                self.srcData['CORTA'] = TA
                self.srcData['CORDTA'] = DTA

    def calc_db_parms(self):
        """
        Calculate dual beam parameters.
        """

        #self.srcData["PLOT_URL"] = self.plot.PLOT_URL
        

        if self.scanNum == 0:
            self.srcData['ASLTA'] = self.plot.yMaxAbeam
            self.srcData['ASLDTA'] = self.plot.erryMaxAbeam
            self.srcData['ASLS2N'] = self.plot.s2na
            self.srcData['BSLTA'] = self.plot.yMinBbeam
            self.srcData['BSLDTA'] = self.plot.erryMinBbeam
            self.srcData['BSLS2N'] = self.plot.s2nb
            self.srcData['SLFLAG'] = self.plot.flag
            #self.srcData['SLBSLOPE'] = self.plot.driftSlope
            #self.srcData['SLBSRMS'] = self.plot.driftRms
            self.srcData['ASLTAPEAKLOC'] = self.plot.peakLoca
            self.srcData['BSLTAPEAKLOC'] = self.plot.peakLocb
            
            self.add_hpslcp_parameters()
            

        elif self.scanNum == 1:
            self.srcData['ANLTA'] = self.plot.yMaxAbeam
            self.srcData['ANLDTA'] = self.plot.erryMaxAbeam
            self.srcData['ANLS2N'] = self.plot.s2na
            self.srcData['BNLTA'] = self.plot.yMinBbeam
            self.srcData['BNLDTA'] = self.plot.erryMinBbeam
            self.srcData['BNLS2N'] = self.plot.s2nb
            self.srcData['NLFLAG'] = self.plot.flag
            self.srcData['ANLTAPEAKLOC'] = self.plot.peakLoca
            self.srcData['BNLTAPEAKLOC'] = self.plot.peakLocb
            #self.srcData['NLBSLOPE'] = self.plot.driftSlope
            #self.srcData['NLBSRMS'] = self.plot.driftRms
            self.add_hpnlcp_parameters()

        elif self.scanNum == 2:
            self.srcData['AOLTA'] = self.plot.yMaxAbeam
            self.srcData['AOLDTA'] = self.plot.erryMaxAbeam
            self.srcData['AOLS2N'] = self.plot.s2na
            self.srcData['BOLTA'] = self.plot.yMinBbeam
            self.srcData['BOLDTA'] = self.plot.erryMinBbeam
            self.srcData['BOLS2N'] = self.plot.s2nb
            self.srcData['OLFLAG'] = self.plot.flag
            self.srcData['AOLTAPEAKLOC'] = self.plot.peakLoca
            self.srcData['BOLTAPEAKLOC'] = self.plot.peakLocb
            #self.srcData['OLBSLOPE'] = self.plot.driftCoeffs[0]
            #self.srcData['OLBSRMS'] = self.plot.driftRms
            self.add_onlcp_parameters()

            if self.srcData['OBJECTTYPE'] == 'CAL':

                # CALCULATE PSS
                ALPSS, ALdPSS, ALPC, ALTA, ALDTA, aAppEff = cp.calc_pc_pss(
                    self.scanNum, self.srcData['ASLTA'], self.srcData['ASLDTA'], self.srcData['ANLTA'], self.srcData['ANLDTA'], self.srcData['AOLTA'], self.srcData['AOLDTA'], self.srcData['FLUX'], self.srcData)
                BLPSS, BLdPSS, BLPC, BLTA, BLDTA, bAppEff = cp.calc_pc_pss(
                    self.scanNum, self.srcData['BSLTA'], self.srcData['BSLDTA'], self.srcData['BNLTA'], self.srcData['BNLDTA'], self.srcData['BOLTA'], self.srcData['BOLDTA'], self.srcData['FLUX'], self.srcData)

                self.srcData['AOLPC'] = ALPC
                self.srcData['ACOLTA'] = ALTA
                self.srcData['ACOLDTA'] = ALDTA
                self.srcData['AOLPSS'] = ALPSS
                self.srcData['AOLDPSS'] = ALdPSS
                self.srcData["AOLAPPEFF"] = aAppEff

                self.srcData['BOLPC'] = BLPC
                self.srcData['BCOLTA'] = BLTA
                self.srcData['BCOLDTA'] = BLDTA
                self.srcData['BOLPSS'] = BLPSS
                self.srcData['BOLDPSS'] = BLdPSS
                self.srcData["BOLAPPEFF"] = bAppEff

            else:
                # CALCULATE POINTING CORRECTION
                ALPC, ALTA, ALDTA = cp.calc_pc(self.scanNum, self.srcData['ASLTA'], self.srcData['ASLDTA'], self.srcData['ANLTA'],
                                              self.srcData['ANLDTA'], self.srcData['AOLTA'], self.srcData['AOLDTA'], self.srcData)
                BLPC, BLTA, BLDTA = cp.calc_pc(self.scanNum, self.srcData['BSLTA'], self.srcData['BSLDTA'], self.srcData['BNLTA'],
                                              self.srcData['BNLDTA'], self.srcData['BOLTA'], self.srcData['BOLDTA'], self.srcData)

                self.srcData['AOLPC'] = ALPC
                self.srcData['ACOLTA'] = ALTA
                self.srcData['ACOLDTA'] = ALDTA

                self.srcData['BOLPC'] = BLPC
                self.srcData['BCOLTA'] = BLTA
                self.srcData['BCOLDTA'] = BLDTA

        elif self.scanNum == 3:
            self.srcData['ASRTA'] = self.plot.yMaxAbeam
            self.srcData['ASRDTA'] = self.plot.erryMaxAbeam
            self.srcData['ASRS2N'] = self.plot.s2na
            self.srcData['BSRTA'] = self.plot.yMinBbeam
            self.srcData['BSRDTA'] = self.plot.erryMinBbeam
            self.srcData['BSRS2N'] = self.plot.s2nb
            self.srcData['SRFLAG'] = self.plot.flag
            self.srcData['ASRTAPEAKLOC'] = self.plot.peakLoca
            self.srcData['BSRTAPEAKLOC'] = self.plot.peakLocb
            #self.srcData['SRBSLOPE'] = self.plot.driftCoeffs[0]
            #self.srcData['SRBSRMS'] = self.plot.driftRms
            self.add_hpsrcp_parameters()

        elif self.scanNum == 4:
            self.srcData['ANRTA'] = self.plot.yMaxAbeam
            self.srcData['ANRDTA'] = self.plot.erryMaxAbeam
            self.srcData['ANRS2N'] = self.plot.s2na
            self.srcData['BNRTA'] = self.plot.yMinBbeam
            self.srcData['BNRDTA'] = self.plot.erryMinBbeam
            self.srcData['BNRS2N'] = self.plot.s2nb
            self.srcData['NRFLAG'] = self.plot.flag
            self.srcData['ANRTAPEAKLOC'] = self.plot.peakLoca
            self.srcData['BNRTAPEAKLOC'] = self.plot.peakLocb
            #self.srcData['NRBSLOPE'] = self.plot.driftCoeffs[0]
            #self.srcData['NRBSRMS'] = self.plot.driftRms
            self.add_hpnrcp_parameters()

        elif self.scanNum == 5:
            self.srcData['AORTA'] = self.plot.yMaxAbeam
            self.srcData['AORDTA'] = self.plot.erryMaxAbeam
            self.srcData['AORS2N'] = self.plot.s2na
            self.srcData['BORTA'] = self.plot.yMinBbeam
            self.srcData['BORDTA'] = self.plot.erryMinBbeam
            self.srcData['BORS2N'] = self.plot.s2nb
            self.srcData['ORFLAG'] = self.plot.flag
            self.srcData['AORTAPEAKLOC'] = self.plot.peakLoca
            self.srcData['BORTAPEAKLOC'] = self.plot.peakLocb
            #self.srcData['ORBSLOPE'] = self.plot.driftCoeffs[0]
            #self.srcData['ORBSRMS'] = self.plot.driftRms
            self.add_onrcp_parameters()

            if self.srcData['OBJECTTYPE'] == 'CAL':

                # CALCULATE PSS
                ARPSS, ARdPSS, ARPC, ARTA, ARDTA, aAppEff = cp.calc_pc_pss(
                    self.scanNum, self.srcData['ASRTA'], self.srcData['ASRDTA'], self.srcData['ANRTA'], self.srcData['ANRDTA'], self.srcData['AORTA'], self.srcData['BORDTA'], self.srcData['FLUX'], self.srcData)
                BRPSS, BRdPSS, BRPC, BRTA, BRDTA, bAppEff = cp.calc_pc_pss(
                    self.scanNum, self.srcData['BSRTA'], self.srcData['BSRDTA'], self.srcData['BNRTA'], self.srcData['BNRDTA'], self.srcData['BORTA'], self.srcData['BORDTA'], self.srcData['FLUX'], self.srcData)

                self.srcData['AORPC'] = ARPC
                self.srcData['ACORTA'] = ARTA
                self.srcData['ACORDTA'] = ARDTA
                self.srcData['AORPSS'] = ARPSS
                self.srcData['AORDPSS'] = ARdPSS
                self.srcData["AORAPPEFF"] = aAppEff

                self.srcData['BORPC'] = BRPC
                self.srcData['BCORTA'] = BRTA
                self.srcData['BCORDTA'] = BRDTA
                self.srcData['BORPSS'] = BRPSS
                self.srcData['BORDPSS'] = BRdPSS
                self.srcData["BORAPPEFF"] = bAppEff

            else:
                # CALCULATE POINTING CORRECTION
                ARPC, ARTA, ARDTA = cp.calc_pc(self.scanNum,
                                              self.srcData['ASRTA'], self.srcData['ASRDTA'], self.srcData['ANRTA'], self.srcData['ANRDTA'], self.srcData['AORTA'], self.srcData['AORDTA'], self.srcData)
                BRPC, BRTA, BRDTA = cp.calc_pc(self.scanNum,
                                              self.srcData['BSRTA'], self.srcData['BSRDTA'], self.srcData['BNRTA'], self.srcData['BNRDTA'], self.srcData['BORTA'], self.srcData['BORDTA'], self.srcData)

                self.srcData['AORPC'] = ARPC
                self.srcData['ACORTA'] = ARTA
                self.srcData['ACORDTA'] = ARDTA

                self.srcData['BORPC'] = BRPC
                self.srcData['BCORTA'] = BRTA
                self.srcData['BCORDTA'] = BRDTA

    def add_hpslcp_parameters(self):

        self.srcData['SLRMSB'] = self.plot.rmsBeforeClean
        self.srcData['SLRMSA'] = self.plot.rmsAfterClean

        #print(self.plot.driftCoeffs[0],self.plot.driftRms)
        #sys.exit()

        try:
            self.srcData['SLBSLOPE'] = self.plot.driftCoeffs[0]
            # On LCP Base Slope Rms
            self.srcData['SLBSRMS'] = self.plot.driftRms

        except Exception:
            try:
                self.srcData['SLBSLOPE'] = self.plot.driftSlope
                self.srcData['SLBSRMS'] = self.plot.driftRms
            except:
                self.srcData['SLBSLOPE'] = np.nan
                self.srcData['SLBSRMS'] = np.nan

           
        
        #print(self.plot.data)
        #sys.exit()

    def add_hpnlcp_parameters(self):

        self.srcData['NLRMSB'] = self.plot.rmsBeforeClean
        self.srcData['NLRMSA'] = self.plot.rmsAfterClean
        try:
            self.srcData['NLBSLOPE'] = self.plot.driftCoeffs[0]
            # On LCP Base Slope Rms
            self.srcData['NLBSRMS'] = self.plot.driftRms

        except Exception:
            try:
                self.srcData['NLBSLOPE'] = self.plot.driftSlope
                self.srcData['NLBSRMS'] = self.plot.driftRms
            except:
                self.srcData['NLBSLOPE'] = np.nan
                self.srcData['NLBSRMS'] = np.nan
                #self.srcData['NLFLAG'] = 4

    def add_onlcp_parameters(self):

        self.srcData['OLRMSB'] = self.plot.rmsBeforeClean
        self.srcData['OLRMSA'] = self.plot.rmsAfterClean

        try:
            self.srcData['OLBSLOPE'] = self.plot.driftCoeffs[0]
            # On LCP Base Slope Rms
            self.srcData['OLBSRMS'] = self.plot.driftRms

        except Exception:
            try:
                self.srcData['OLBSLOPE'] = self.plot.driftSlope
                self.srcData['OLBSRMS'] = self.plot.driftRms
            except:
                self.srcData['OLBSLOPE'] = np.nan
                self.srcData['OLBSRMS'] = np.nan
            #self.srcData['OLFLAG'] = 6

    def add_hpsrcp_parameters(self):

        self.srcData['SRRMSB'] = self.plot.rmsBeforeClean
        self.srcData['SRRMSA'] = self.plot.rmsAfterClean
        try:
            self.srcData['SRBSLOPE'] = self.plot.driftCoeffs[0]
            # On LCP Base Slope Rms
            self.srcData['SRBSRMS'] = self.plot.driftRms

        except Exception:
            try:
                self.srcData['SRBSLOPE'] = self.plot.driftSlope
                self.srcData['SRBSRMS'] = self.plot.driftRms
            except:
                self.srcData['SRBSLOPE'] = np.nan
                self.srcData['SRBSRMS'] = np.nan
            #self.srcData['SRFLAG'] = 10

    def add_hpnrcp_parameters(self):

        self.srcData['NRRMSB'] = self.plot.rmsBeforeClean
        self.srcData['NRRMSA'] = self.plot.rmsAfterClean
        try:
            self.srcData['NRBSLOPE'] = self.plot.driftCoeffs[0]
            # On LCP Base Slope Rms
            self.srcData['NRBSRMS'] = self.plot.driftRms

        except Exception:
            try:
                self.srcData['NRBSLOPE'] = self.plot.driftSlope
                self.srcData['NRBSRMS'] = self.plot.driftRms
            except:
                self.srcData['NRBSLOPE'] = np.nan
                self.srcData['NRBSRMS'] = np.nan
            #self.srcData['NRFLAG'] = 3

    def add_onrcp_parameters(self):
        """
            Add ON LCP SCAN fits to the data list.
        """

        # Add the rms before and after the removal ofigh rms values
        self.srcData['ORRMSB'] = self.plot.rmsBeforeClean
        self.srcData['ORRMSA'] = self.plot.rmsAfterClean

        try:
            # Add the rms before and after the removal of high rms values
            self.srcData['ORBSLOPE'] = self.plot.driftCoeffs[0]
            self.srcData['ORBSRMS'] = self.plot.driftRms

        except Exception:
            try:
                self.srcData['ORBSLOPE'] = self.plot.driftSlope
                self.srcData['ORBSRMS'] = self.plot.driftRms
            except:
                self.srcData['ORBSLOPE'] = np.nan
                self.srcData['ORBSRMS'] = np.nan
