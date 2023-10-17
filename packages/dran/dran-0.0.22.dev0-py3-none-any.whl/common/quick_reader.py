
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits as pyfits
import os
from scipy.optimize import curve_fit
import sys
from astropy.time import Time

class QuickReader:
    """ Give a quick display of the source file drift scans
    saved to a png file in the current working directory.
    
    """

    def __init__(self,fileName):
        self.fileName = fileName

        # check file type    
        lcp,rcp = self.load_drift_scan()
        self.make_plots(lcp,rcp)
        
        sys.exit()

    def load_drift_scan(self):

        """
        Open a fits file, assuming it is in HartRAO continuum driftscan format.
        Return a dict for each polarisation containing the scans and necessary metadata.
        From Sharmila's code.
        """    
        hdulist = pyfits.open(self.fileName)
        
        if len(hdulist)==5:

            noise_cal = hdulist[2]
            drift1 = hdulist[3]

            date = hdulist[0].header['DATE']
            #Conversion factor from noise diode firing - counts per Kelvin
            count_K1 = noise_cal.header['HZPERK1']
            count_K2 = noise_cal.header['HZPERK2']
            hpbw = hdulist[1].header['HPBW']    #half power beamwidth
            hfnbw = hdulist[1].header['FNBW']/2.0     #half beamwidth to first nulls
            nu =  drift1.header['CENTFREQ']
            source = hdulist[0].header['OBJECT']

            #construct an array for the x-axis in terms of scan offset from the centre
            scandist = hdulist[0].header['SCANDIST']
            offset = np.linspace(-scandist/2.0, scandist/2.0, len(drift1.data['MJD']))
            #(self.onLcp/lcpHzPerK)-(self.onLcp[0]/lcpHzPerK)
            #north_scan_LCP = drift1.data['Count1']/count_K1 - drift1.data['Count1'][0]/count_K1
            #north_scan_RCP = drift1.data['Count2']/count_K2 - drift1.data['Count2'][0]/count_K2
            centre_scan_LCP = drift1.data['Count1']/count_K1 - drift1.data['Count1'][0]/count_K1
            centre_scan_RCP = drift1.data['Count2']/count_K2 - drift1.data['Count2'][0]/count_K2
            #south_scan_LCP = drift3.data['Count1']/count_K1 - drift3.data['Count1'][0]/count_K1
            #south_scan_RCP = drift3.data['Count2']/count_K2 - drift3.data['Count2'][0]/count_K2

            #Create dict objects
            LCP = {'date' : date,
                'file':self.fileName.split("/")[-1][:18],
                'source' : source,
                'offset' : offset, 
                'hpbw' : hpbw,
                'hfnbw' : hfnbw,
                'nu' : nu,
                #'north_scan' : north_scan_LCP,
                'centre_scan' : centre_scan_LCP,
                #'south_scan' : south_scan_LCP,
                }

            RCP = {'date' : date,
                'source' : source,
                'offset' : offset, 
                'hpbw' : hpbw,
                'hfnbw' : hfnbw, 
                'nu' : nu,
                #'north_scan' : north_scan_RCP,
                'centre_scan' : centre_scan_RCP,
                #'south_scan' : south_scan_RCP,
                }

            #print(LCP)
            #sys.exit()

        elif len(hdulist)==7:
            noise_cal = hdulist[2]
            drift1 = hdulist[3]
            drift2 = hdulist[4]
            drift3 = hdulist[5]

            date = hdulist[0].header['DATE']
            #Conversion factor from noise diode firing - counts per Kelvin
            count_K1 = noise_cal.header['HZPERK1']
            count_K2 = noise_cal.header['HZPERK2']
            hpbw = hdulist[1].header['HPBW']    #half power beamwidth
            hfnbw = hdulist[1].header['FNBW']/2.0     #half beamwidth to first nulls
            nu =  drift1.header['CENTFREQ']
            source = hdulist[0].header['OBJECT']

            #construct an array for the x-axis in terms of scan offset from the centre
            scandist = hdulist[0].header['SCANDIST']
            offset = np.linspace(-scandist/2.0, scandist/2.0, len(drift1.data['MJD']))
            #(self.onLcp/lcpHzPerK)-(self.onLcp[0]/lcpHzPerK)
            north_scan_LCP = drift1.data['Count1']/count_K1 - drift1.data['Count1'][0]/count_K1
            north_scan_RCP = drift1.data['Count2']/count_K2 - drift1.data['Count2'][0]/count_K2
            centre_scan_LCP = drift2.data['Count1']/count_K1 - drift2.data['Count1'][0]/count_K1
            centre_scan_RCP = drift2.data['Count2']/count_K2 - drift2.data['Count2'][0]/count_K2
            south_scan_LCP = drift3.data['Count1']/count_K1 - drift3.data['Count1'][0]/count_K1
            south_scan_RCP = drift3.data['Count2']/count_K2 - drift3.data['Count2'][0]/count_K2

            #Create dict objects
            LCP = {'date' : date,
                'file':self.fileName.split("/")[-1][:18],
                'source' : source,
                'offset' : offset, 
                'hpbw' : hpbw,
                'hfnbw' : hfnbw,
                'nu' : nu,
                'north_scan' : north_scan_LCP,
                'centre_scan' : centre_scan_LCP,
                'south_scan' : south_scan_LCP,
                }

            RCP = {'date' : date,
                'source' : source,
                'offset' : offset, 
                'hpbw' : hpbw,
                'hfnbw' : hfnbw, 
                'nu' : nu,
                'north_scan' : north_scan_RCP,
                'centre_scan' : centre_scan_RCP,
                'south_scan' : south_scan_RCP,
                }

        return LCP, RCP

    def make_plots(self,lcp,rcp):

        # make plots of all scans

        if "north_scan" in list(lcp.keys()):
            scans=[lcp['offset'],rcp['offset'],lcp['north_scan'],lcp['centre_scan'],lcp['south_scan'],rcp['north_scan'],rcp['centre_scan'],rcp['south_scan']]
            scanNames=['lcp offset','rcp offset','LCP North scan','LCP Center scan','LCP South scan','RCP North scan','RCP Center scan','RCP South scan']
            
            plt.figure(figsize=(20,10))

            for i in range(1,7):
                plt.subplot(2,3,i)
                plt.ylabel('Ta [K]')
                plt.xlabel('Offset [deg]')
                if 'LCP' in scanNames[i+1]:
                    plt.plot(scans[0],scans[i+1])
                else:
                    plt.plot(scans[1],scans[i+1])
                plt.title(f'plot of {scanNames[i+1]}')
            plt.tight_layout()
            plt.savefig(f'quickview_{lcp["source"]}_{int(lcp["nu"])}-{lcp["file"]}.png')
            #plt.show()
            plt.close()
        else:
            scans=[lcp['offset'],rcp['offset'],lcp['centre_scan'],rcp['centre_scan']]
            scanNames=['lcp offset','rcp offset','LCP Center scan','RCP Center scan']
            
            plt.figure(figsize=(10,3))
            for i in range(1,3):
                plt.subplot(1,2,i)
                plt.ylabel('Ta [K]')
                plt.xlabel('Offset [deg]')
                if 'LCP' in scanNames[i+1]:
                    plt.plot(scans[0],scans[i+1])
                else:
                    plt.plot(scans[1],scans[i+1])
                plt.title(f'plot of {scanNames[i+1]}')
            plt.tight_layout()
            plt.savefig(f'quickview_{lcp["source"]}_{int(lcp["nu"])}-{lcp["file"]}.png')
            plt.show()
            plt.close()