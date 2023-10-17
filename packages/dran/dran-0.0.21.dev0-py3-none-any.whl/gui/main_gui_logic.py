# ============================================================================#
# File: main_gui_logic.py                                                     #
# Author: Pfesesani V. van Zyl                                                #
# ============================================================================#

# Standard library imports
# --------------------------------------------------------------------------- #
from ast import Pass
from datetime import datetime
# from PyQt5 import QtWidgets
from PyQt6 import QtWidgets
import numpy as np
import sys
import os
import matplotlib.pyplot as pl
# import shutil
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import pandas as pd
import webbrowser
from astropy.time import Time
import glob
#from sqlalchemy import create_engine
#engine = create_engine('sqlite://', echo=False)

# Local imports
# --------------------------------------------------------------------------- #
# sys.path.append("src/")
from common.messaging import msg_wrapper
from common.sqlite_db import SQLiteDB
from common.fits_file_reader import FitsFileReader
import common.fitting as fit
from gui.main_window import Ui_MainWindow
from gui.edit_driftscan_window import Ui_DriftscanWindow
from gui.edit_timeseries_window import Ui_TimeSeriesWindow
from gui.view_plots_window import Ui_PlotViewer
from common.file_handler import FileHandler
import common.calc_pss as cp
from gui.canvas_manager import CanvasManager
from gui.secondary_canvas_manager import SecondaryCanvasManager
from gui.timeseries_canvas import TimeCanvas
from common.fitting import f as fx
# =========================================================================== #


class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    """ The main class that handles all gui operations."""

    def __init__(self, log): #,filePath=""):

        super(Main, self).__init__()
        # changing the background color to yellow
        # self.setStyleSheet("background-color: #36648B; color: white")
        # self.setWindowTitle("GUI APP")
        self.log = log
        self.filePath="" #filePath
        msg_wrapper("debug", self.log.debug,"GUI initiated")

        # Setup the user interface
        self.setupUi(self)
        self.statusbar.showMessage("Ready.")

        # initiate file handling
        self.file=FileHandler(self.log)

        # setup holder for deleted values
        self.deleted=[]#{}

        if self.filePath=="":

            btnCol='white'
            btnTextCol='black'
            # Connect buttons to window
            self.btn_edit_driftscan.clicked.connect(self.open_drift_window)
            self.btn_edit_timeseries.clicked.connect(self.open_timeseries_window)
            self.btn_view_plots.clicked.connect(self.open_plots_window)
            self.btn_edit_driftscan.setStyleSheet(f'QPushButton {{background-color: {btnCol}; color: {btnTextCol};}}')
            self.btn_edit_timeseries.setStyleSheet(f'QPushButton {{background-color: {btnCol}; color: {btnTextCol};}}')
            self.btn_view_plots.setStyleSheet(f'QPushButton {{background-color: {btnCol}; color: {btnTextCol};}}')

        else:
            self.open_drift_window()
            self.open_file()

    # === Windows setup   ===
    def open_drift_window(self):
        """ Connect the edit drift scan window to the main window. """

        msg_wrapper("debug", self.log.debug, "Initiating drift scan editing window")

        # Initiate Canvas
        self.Canvas = CanvasManager(log=self.log)
        self.ntb = NavigationToolbar(self.Canvas, self)
        self.drift_window = QtWidgets.QMainWindow()
        self.drift_ui = Ui_DriftscanWindow()
        self.drift_ui.setupUi(self.drift_window)

        # initiate Secondary canvas
        self.secondaryCanvas = SecondaryCanvasManager(log=self.log)

        # Layouts
        plotLayout = self.drift_ui.PlotLayout
        otherPlotLayout = self.drift_ui.otherPlotsLayout

        # Add Canvas/es to the gui
        plotLayout.addWidget(self.ntb)
        plotLayout.addWidget(self.Canvas)
        otherPlotLayout.addWidget(self.secondaryCanvas)

        # Connect buttons to actions performed by user
        self.connect_buttons()

        # Print welcome message
        self.write("DRAN GUI loaded successfully.",'info')
        self.write("Open a file to get started.",'info')

        # Set status, indicates whether fit/plot has been modified/not
        self.status = [0, 0, 0, 0, 0, 0]

        self.drift_window.show()

    def open_timeseries_window(self):
        """ Connect the edit timeseries window. """

        msg_wrapper("debug", self.log.debug, "Initiating timeseries editing window")

        # Initiate Canvas
        self.Canvas = TimeCanvas(log=self.log)
        self.ntb = NavigationToolbar(self.Canvas,self) # add nav toolbar
        self.time_window = QtWidgets.QMainWindow()
        self.time_ui = Ui_TimeSeriesWindow()
        self.time_ui.setupUi(self.time_window)

        # Layouts
        plotLayout = self.time_ui.PlotLayout

        # Add canvas to the gui
        plotLayout.addWidget(self.ntb)
        plotLayout.addWidget(self.Canvas)
        
        # connect buttons to actions performed by users
        self.time_ui.BtnReset.setVisible(False)
        self.time_ui.BtnResetPoint.setVisible(False)
        self.time_ui.BtnFit.setVisible(True)
        self.time_ui.BtnQuit.setVisible(False)
        self.time_ui.BtnQuit.setText("Update db")
        self.time_ui.EdtSplKnots.setVisible(False)
        self.time_ui.LblSplKnots.setVisible(False)
        self.time_ui.BtnUpdateDB.setVisible(False)
        self.time_ui.BtnOpenDB.clicked.connect(self.open_db)
        self.time_ui.comboBoxColsYerr.setVisible(True)
        # self.time_ui.errorCheckBox.setVisible(False)
        self.time_ui.Lblxlim.setVisible(False)
        self.time_ui.Lblylim.setVisible(False)
        self.time_ui.EdtxlimMin.setVisible(False)
        self.time_ui.EdtxlimMax.setVisible(False)
        self.time_ui.EdtylimMax.setVisible(False)
        self.time_ui.EdtylimMin.setVisible(False)
        # self.time_ui.comboBoxTables.setEnabled(True)
        # self.time_ui.comboBoxColsX.setEnabled(True)
        # self.time_ui.comboBoxColsY.setEnabled(False)
        # self.time_ui.comboBoxFilters.setEnabled(False)
        # self.time_ui.BtnFilter.setEnabled(False)
        self.time_ui.BtnRefreshDB.setVisible(True)
        # self.time_ui.BtnSavePlot.setVisible(False)
        self.time_ui.BtnSaveDB.setVisible(False)
        self.time_ui.EdtFilter.setEnabled(False)

        self.time_ui.EdtEndDate.setVisible(False)
        self.time_ui.EdtStartDate.setVisible(False)
        self.time_ui.LblEndDate.setVisible(False)
        self.time_ui.LblStartDate.setVisible(False)

        # Setup index change options for combo boxes
        self.time_ui.comboBoxTables.currentIndexChanged.connect(self.on_table_name_changed)
        self.time_ui.comboBoxFitTypes.currentIndexChanged.connect(self.on_fit_changed)

        # connect buttons
        self.time_ui.BtnRefreshDB.clicked.connect(self.refresh_list)
        self.time_window.show()

    def f(self,x):
        """ convert values to floats """

        try:
            return np.float(x)
        except:
            return np.nan

    def update_db(self):
                    # update db on change

                    # check last selected points
                    fit_points= self.Canvas.fit_points
                    click_index = self.Canvas.click_index

                    print('\n',"+"*30)
                    print(f"\nDeleting \n-point: {fit_points} \n-at index {click_index}")

                    print('\ndf length Before deleting: ',len(self.df))

                    xCol = self.Canvas.xlab
                    yCol = self.Canvas.ylab

                    print('\n','-'*30)
                    try:
                        t = Time(fit_points[0][0])
                    except:
                        print('An error occurred, please ensure you click on a point')
                        sys.exit()

                    doy = t.strftime('%j')

                    xp=self.df[xCol]
                    yp=self.df[yCol]

                    date_str=f'{str(fit_points[0][0])[:4]}d{str(doy)}'
                    
                    ii=int(click_index[0]) # point index to delete

                    print('Deleting: ')

                    try:
                        self.df=self.df.replace(None,np.nan)
                    except:
                        pass

                    try:
                        self.df=self.df.replace("nan",np.nan)
                    except:
                        pass

                    # find what i is in the db
                    id=self.df['id'].iloc[ii]

                    i=ii#d
                    FN=self.df['FILENAME'].iloc[i]
 

                    print('\n-date: ',date_str,'\n-file: ',FN)

                    print(f"\n-id: {self.df['id'].iloc[i]}, \n-index: {ii}")
                    # print('match: ', self.df['id'].iloc[i])#, self.df.iloc[i])
                    
                    #self.df.drop(id,inplace=True)
                    
                    print(f'\n> Setting {yCol}: {self.df.iloc[i][yCol]}, to np.nan')

                    self.df.at[i,yCol]=np.nan

                    print(f'\n+ New {yCol}: {self.df.iloc[i][yCol]}')

                    tablename = self.time_ui.comboBoxTables.currentText()
                  
                    xcol=self.time_ui.comboBoxColsX.currentText()
                    ycol=self.time_ui.comboBoxColsY.currentText()

                    db = self.db#SQLiteDB(databaseName="CALDB.db", log=self.log)
                    db.create_db()
                    srcType=self.df['OBJECTTYPE'].iloc[i]

                    if srcType == "CAL":
                        
                        self.write(f"Updating {self.dbFile} table: {tablename}, type: {srcType}",'info')
                        
                        print('\n-BEAMTYPE: ',self.df['BEAMTYPE'][i],'\n-srcType: ',srcType)

                        # update the database
                        if 'S' in  str(self.df['BEAMTYPE'].iloc[i]):

                            print(self.df['BEAMTYPE'].iloc[i])
                            
                            if "13.0S" == self.df['BEAMTYPE'].iloc[i]:
                                if "TSYS1" in ycol or "TSYS2" in ycol:
                                    if 'TSYS1' in ycol:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLTA='{np.nan}',  OLDTA='{np.nan}', OLFLAG=200, OLPSS='{pss}', OLDPSS={errpss},  OLAPPEFF={appeff}, WHERE FILENAME = '{FN}' ;"

                                    if 'TSYS2' in ycol:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORTA='{np.nan}', ORDTA='{np.nan}', ORFLAG=200, ORPSS='{pss}', ORDPSS={errpss}, ORAPPEFF={appeff}, WHERE FILENAME = '{FN}' ;"

                                elif "OLTA" in ycol :
                                    pss,errpss,appeff = np.nan,np.nan,np.nan
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}',OLDTA='{np.nan}', OLFLAG=201, OLPSS='{pss}', OLDPSS='{errpss}', OLAPPEFF='{appeff}' WHERE FILENAME = '{FN}' ;"

                                elif "ORTA" in ycol :
                                    pss,errpss,appeff = np.nan,np.nan,np.nan
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}',ORDTA='{np.nan}', ORFLAG=202, ORPSS='{pss}', ORDPSS='{errpss}', ORAPPEFF='{appeff}' WHERE FILENAME = '{FN}' ;"

                                elif "OLPSS" in ycol:
                                        print('\nprint updating OLPSS')
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLDPSS='{np.nan}', OLFLAG=201, OLAPPEFF='{np.nan}' WHERE FILENAME = '{FN}' ;"

                                elif "ORPSS" in ycol:
                                        print('\nprint updating ORPSS')
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=202, ORDPSS='{np.nan}', ORAPPEFF='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                       
                                print(stmt)
                                db.c.execute(stmt)
                                db.commit_changes()
                                db.close_db()
                                print(f"updated {self.dbFile}")
                                print(tablename,xcol,ycol)
                                print('\nDONE')
                                print("+"*30,"\n")

                            else:
                    
                                if "TSYS1" in ycol or "TSYS2" in ycol or 'LS2N' in ycol or 'RS2N' in ycol or 'PC' in ycol :# or "SLTA" in ycol:
                                    if 'TSYS1' in ycol :
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLTA='{np.nan}', SLTA='{np.nan}', \
                                            NLTA='{np.nan}', OLDTA='{np.nan}', SLDTA='{np.nan}', NLDTA='{np.nan}', OLFLAG=200, \
                                                OLS2N='{np.nan}',OLPSS='{np.nan}', OLDPSS='{np.nan}', OLPC='{np.nan}', \
                                                    OLAPPEFF='{np.nan}', COLTA='{np.nan}', COLDTA='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                        print("\n",stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                    if 'OLPC' in ycol :
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLTA='{np.nan}', SLTA='{np.nan}', \
                                            NLTA='{np.nan}', OLDTA='{np.nan}', SLDTA='{np.nan}', NLDTA='{np.nan}', OLFLAG=200, \
                                                OLS2N='{np.nan}',OLPSS='{np.nan}', OLDPSS='{np.nan}', OLPC='{np.nan}', \
                                                    OLAPPEFF='{np.nan}', TSYS1='{np.nan}',COLTA='{np.nan}', COLDTA='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                        print("\n",stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                    if 'ORPC' in ycol :
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLTA='{np.nan}', SLTA='{np.nan}', \
                                            NLTA='{np.nan}', OLDTA='{np.nan}', SLDTA='{np.nan}', NLDTA='{np.nan}', OLFLAG=200, \
                                                OLS2N='{np.nan}',OLPSS='{np.nan}', OLDPSS='{np.nan}', OLPC='{np.nan}', \
                                                    OLAPPEFF='{np.nan}', TSYS2='{np.nan}',COLTA='{np.nan}', COLDTA='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                        print("\n",stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                    if 'TSYS2' in ycol :
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORTA='{np.nan}', SRTA='{np.nan}', NRTA='{np.nan}', \
                                            ORDTA='{np.nan}', SRDTA='{np.nan}', NRDTA='{np.nan}', ORFLAG=200, ORS2N='{np.nan}',ORPSS='{np.nan}', \
                                                ORDPSS='{np.nan}', ORPC='{np.nan}', ORAPPEFF='{np.nan}', CORTA='{np.nan}', CORDTA={np.nan}  WHERE FILENAME = '{FN}' ;"
                                        print("\n",stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                    if 'SLS2N' in ycol:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLS2N='{np.nan}',NLS2N='{np.nan}',OLTA='{np.nan}', SLTA='{np.nan}', NLTA='{np.nan}', OLDTA='{np.nan}', SLDTA='{np.nan}', NLDTA='{np.nan}', OLFLAG=200, TSYS1='{np.nan}', OLPSS='{np.nan}', OLDPSS='{np.nan}', OLPC='{np.nan}', OLAPPEFF='{np.nan}', COLTA='{np.nan}', COLDTA='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                        print("\n",stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                    if 'NLS2N' in ycol:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLS2N='{np.nan}',SLS2N='{np.nan}',OLTA='{np.nan}', SLTA='{np.nan}', NLTA='{np.nan}', OLDTA='{np.nan}', SLDTA='{np.nan}', NLDTA='{np.nan}', OLFLAG=200, TSYS1='{np.nan}', OLPSS='{np.nan}', OLDPSS='{np.nan}', OLPC='{np.nan}', OLAPPEFF='{np.nan}', COLTA='{np.nan}', COLDTA='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                        print("\n",stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                    if 'OLS2N' in ycol:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', SLS2N='{np.nan}',NLS2N='{np.nan}',OLTA='{np.nan}', SLTA='{np.nan}', NLTA='{np.nan}', OLDTA='{np.nan}', SLDTA='{np.nan}', NLDTA='{np.nan}', OLFLAG=200, TSYS1='{np.nan}', OLPSS='{np.nan}', OLDPSS='{np.nan}', OLPC='{np.nan}', OLAPPEFF='{np.nan}', COLTA='{np.nan}', COLDTA='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                        print("\n",stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                    if 'SRS2N' in ycol:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORS2N='{np.nan}',NRS2N='{np.nan}',ORTA='{np.nan}', SRTA='{np.nan}', NRTA='{np.nan}', ORDTA='{np.nan}', SRDTA='{np.nan}', NRDTA='{np.nan}', ORFLAG=200, TSYS2='{np.nan}', ORPSS='{np.nan}', ORDPSS='{np.nan}', ORPC='{np.nan}', ORAPPEFF='{np.nan}', CORTA='{np.nan}', CORDTA={np.nan}  WHERE FILENAME = '{FN}' ;"
                                        print("\n",stmt)
                                       
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                    if 'NRS2N' in ycol:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORS2N='{np.nan}',SRS2N='{np.nan}',ORTA='{np.nan}', SRTA='{np.nan}', NRTA='{np.nan}', ORDTA='{np.nan}', SRDTA='{np.nan}', NRDTA='{np.nan}', ORFLAG=200, TSYS2='{np.nan}', ORPSS='{np.nan}', ORDPSS='{np.nan}', ORPC='{np.nan}', ORAPPEFF='{np.nan}', CORTA='{np.nan}', CORDTA={np.nan}  WHERE FILENAME = '{FN}' ;"
                                        print("\n",stmt)
                                       
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                    if 'ORS2N' in ycol:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', SRS2N='{np.nan}',NRS2N='{np.nan}',ORTA='{np.nan}', SRTA='{np.nan}', NRTA='{np.nan}', ORDTA='{np.nan}', SRDTA='{np.nan}', NRDTA='{np.nan}', ORFLAG=200, TSYS2='{np.nan}', ORPSS='{np.nan}', ORDPSS='{np.nan}', ORPC='{np.nan}', ORAPPEFF='{np.nan}', CORTA='{np.nan}', CORDTA={np.nan}  WHERE FILENAME = '{FN}' ;"
                                        print("\n",stmt)
                                       
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                elif "OLTA" in ycol or "NLTA" in ycol or "SLTA" in ycol:
                                        
                                        if 'NLTA' in ycol:
                                            if "13.0S" not in str(self.df['BEAMTYPE'].iloc[i]):
                                                onta=self.df['OLTA'].iloc[i]
                                                ontaerr=self.df['OLDTA'].iloc[i]
                                                sta=self.df['SLTA'].iloc[i]
                                                staerr=self.df['SLDTA'].iloc[i]

                                                if "01.3S" in str(self.df['BEAMTYPE'].iloc[i]):
                                              
                                                    print('\nupdating 22ghz olpss - nlta')
                                                    pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df['TOTAL_PLANET_FLUX_D'].iloc[i],self.df)

                                                elif "02.5S" in str(self.df['BEAMTYPE'].iloc[i]):
                                                    print('\nupdating 12ghz olpss - nlta')
                                                    pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                                    
                                                
                                                #print(str(self.df['BEAMTYPE'].iloc[i]),"0.25S","0.25S"==str(self.df['BEAMTYPE'].iloc[i]))
                                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', NLDTA='{np.nan}', OLFLAG=200, OLPSS='{pss}', OLDPSS={errpss}, OLPC={pc}, OLAPPEFF={appeff}, COLTA={ota}, COLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"
                                                print("\n",stmt)

                                        elif 'SLTA' in ycol:
                                            if "13.0S" not in str(self.df['BEAMTYPE'].iloc[i]):
                                                onta=self.df['OLTA'].iloc[i]
                                                ontaerr=self.df['OLDTA'].iloc[i]
                                                nta=self.df['NLTA'].iloc[i]
                                                ntaerr=self.df['NLDTA'].iloc[i]

                                                if "01.3S" in str(self.df['BEAMTYPE'].iloc[i]):
                                                    print('\nupdating 22ghz olpss - slta')
                                                    pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,0.0,0.0,nta,ntaerr,onta,ontaerr,self.df['TOTAL_PLANET_FLUX_D'].iloc[i],self.df)

                                                elif "02.5S" in str(self.df['BEAMTYPE'].iloc[i]):
                                                    print('\nupdating 12ghz olpss - slta')
                                                    pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,0.0,0.0,nta,ntaerr,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                                
                                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}',SLDTA='{np.nan}', OLFLAG=200, OLPSS='{pss}', OLDPSS={errpss}, OLPC={pc}, OLAPPEFF={appeff},COLTA={ota},COLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"
                                                print(stmt)

                                        else:
                                            print('print updating OLTA')
                                            try:
                                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLDTA='{np.nan}', OLPC='{np.nan}', OLFLAG=200, OLPSS='{np.nan}', OLDPSS='{np.nan}', COLTA='{np.nan}', COLDTA='{np.nan}',OLAPPEFF='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                            except:
                                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}',OLDTA='{np.nan}',OLFLAG=200, OLPSS='{np.nan}',OLDPSS='{np.nan}',OLAPPEFF='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                            print(stmt)
                                
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"\nupdated {self.dbFile} ")
                                        print(tablename,xcol,ycol)
                                        print('\nDONE')
                                        print("+"*30,"\n")

                                elif "ORTA" in ycol or "NRTA" in ycol or "SRTA" in ycol:
                                    if 'NRTA' in ycol:
                                            if "13.0S" not in str(self.df['BEAMTYPE'].iloc[i]):
                                                onta=self.df['ORTA'].iloc[i]
                                                ontaerr=self.df['ORDTA'].iloc[i]
                                                sta=self.df['SRTA'].iloc[i]
                                                staerr=self.df['SRDTA'].iloc[i]

                                                if "01.3S" in str(self.df['BEAMTYPE'].iloc[i]):
                                                    print('updating 22ghz orpss - nrta')
                                                    pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df['TOTAL_PLANET_FLUX_D'].iloc[i],self.df)

                                                elif "02.5S" in str(self.df['BEAMTYPE'].iloc[i]):
                                                    print('updating 12ghz orpss - nrta')
                                                    pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                                
                                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORDTA='{np.nan}',ORFLAG=200, ORPSS='{pss}', ORDPSS={errpss}, ORPC={pc}, ORAPPEFF={appeff},CORTA={ota},CORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"
                                                print(stmt)
                                                db.c.execute(stmt)
                                                db.commit_changes()
                                                db.close_db()
                                                print("updated CALDB")
                                                print(tablename,xcol,ycol)
                                                print('DONE')

                                    elif 'SRTA' in ycol:
                                            if "13.0S" not in str(self.df['BEAMTYPE'].iloc[i]):
                                                onta=self.df['ORTA'].iloc[i]
                                                ontaerr=self.df['ORDTA'].iloc[i]
                                                nta=self.df['NRTA'].iloc[i]
                                                ntaerr=self.df['NRDTA'].iloc[i]

                                                if "01.3S" in str(self.df['BEAMTYPE'].iloc[i]):
                                                    print('updating 22ghz orpss - srta')
                                                    pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,0.0,0.0,nta,ntaerr,onta,ontaerr,self.df['TOTAL_PLANET_FLUX_D'].iloc[i],self.df)

                                                elif "02.5S" in str(self.df['BEAMTYPE'].iloc[i]):
                                                    print('updating 12ghz orpss - srta')
                                                    pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,0.0,0.0,nta,ntaerr,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                                
                                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', SRDTA='{np.nan}', ORFLAG=200, ORPSS='{pss}', ORDPSS={errpss}, ORPC={pc}, ORAPPEFF={appeff},CORTA={ota},CORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"
                                                print(stmt)
                                                db.c.execute(stmt)
                                                db.commit_changes()
                                                db.close_db()
                                                print("updated CALDB")
                                                print(tablename,xcol,ycol)
                                                print('DONE')

                                    else:
                                        print('\nprint updating ORTA')
                                        try:
                                            stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORDTA='{np.nan}', ORFLAG=200, ORPC='{np.nan}', ORPSS='{np.nan}', ORDPSS='{np.nan}', CORTA='{np.nan}', CORDTA='{np.nan}', ORAPPEFF={appeff} WHERE FILENAME = '{FN}' ;"
                                        except:
                                            stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, ORPSS='{np.nan}', ORDPSS='{np.nan}' WHERE FILENAME = '{FN}' ;"

                                        print(stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print("updated CALDB")
                                        print(tablename,xcol,ycol)

                                elif "OLPSS" in ycol:
                                        print('\nprint updating OLPSS')
                                        # try:
                                        #     stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, COLTA='{np.nan}', COLDTA='{np.nan}', OLAPPEFF='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                        # except:
                                        #     stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, OLTA='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                        
                                        # try:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLDPSS='{np.nan}', OLFLAG=201, OLAPPEFF='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                        # except:
                                        #     stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}',OLDTA='{np.nan}',OLFLAG=200, OLPSS='{np.nan}',OLDPSS='{np.nan}',OLAPPEFF='{np.nan}' WHERE FILENAME = '{FN}' ;"

                                        print(stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                elif "ORPSS" in ycol:
                                        print('\nprint updating ORPSS')
                                        # try:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, ORDPSS='{np.nan}', ORAPPEFF='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                        # except:
                                        #     stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, ORTA='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                        print(stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                               
                                else:
                                    print('No update')#MISSED: ',ycol)
                                    #sys.exit()

                        elif 'D' in str(self.df['BEAMTYPE'].iloc[0]):
                            print("D in beamtype")

                            if "TSYS1" in ycol or "TSYS2" in ycol:# or "SLTA" in ycol:
                                if 'TSYS1' in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', AOLTA='{np.nan}', ASLTA='{np.nan}', ANLTA='{np.nan}', AOLDTA='{np.nan}', ASLDTA='{np.nan}', ANLDTA='{np.nan}', AOLFLAG=200, AOLPSS='{pss}', AOLDPSS={errpss}, AOLPC={pc}, AOLAPPEFF={appeff}, ACOLTA={ota}, ACOLDTA={otaerr} \
                                         BOLTA='{np.nan}', BSLTA='{np.nan}', BNLTA='{np.nan}', BOLDTA='{np.nan}', BSLDTA='{np.nan}', BNLDTA='{np.nan}', BOLFLAG=200, BOLPSS='{pss}', BOLDPSS={errpss}, BOLPC={pc}, BOLAPPEFF={appeff}, BCOLTA={ota}, BCOLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"
                                    print("\n",stmt)
                                if 'TSYS2' in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', AORTA='{np.nan}', ASRTA='{np.nan}', ANRTA='{np.nan}', AORDTA='{np.nan}', ASRDTA='{np.nan}', ANRDTA='{np.nan}', AORFLAG=200, AORPSS='{pss}', AORDPSS={errpss}, AORPC={pc}, AORAPPEFF={appeff}, ACORTA={ota}, ACORDTA={otaerr}  \
                                         BORTA='{np.nan}', BSRTA='{np.nan}', BNRTA='{np.nan}', BORDTA='{np.nan}', BSRDTA='{np.nan}', BNRDTA='{np.nan}', BORFLAG=200, BORPSS='{pss}', BORDPSS={errpss}, BORPC={pc}, BORAPPEFF={appeff}, BCORTA={ota}, BCORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"
                                    
                                    print("\n",stmt)

                            elif "AOLTA" in ycol:
                                
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', AOLDTA='{np.nan}', OLFLAG=200, AOLPSS='{np.nan}',AOLDPSS='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                    print(stmt)

                            elif "AORTA" in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', AORDTA='{np.nan}',ORFLAG=200, AORPSS='{np.nan}' ,AORDPSS='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                    print(stmt)

                            elif "BOLTA" in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', BOLDTA='{np.nan}', OLFLAG=200, BOLPSS='{np.nan}' ,BOLDPSS='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                    print(stmt)

                            elif "BORTA" in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', BORDTA='{np.nan}',ORFLAG=200, BORPSS='{np.nan}' ,BORDPSS='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                    print(stmt)

                            elif "AOLPSS" in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', AOLDPSS='{np.nan}', OLFLAG=200  WHERE FILENAME = '{FN}' ;"
                                    print(stmt)

                            elif "AORPSS" in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, AORDPSS='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                    print(stmt)

                            elif "BOLPSS" in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, BOLDPSS='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                    print(stmt)

                            elif "BORPSS" in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, BORDPSS='{np.nan}'  WHERE FILENAME = '{FN}' ;"
                                    print(stmt)

                            elif "ASLTA" in ycol or "BSLTA" in ycol:
                                    
                                    if "ASLTA" in ycol:
                                        onta=self.df['AOLTA'].iloc[i]
                                        ontaerr=self.df['AOLDTA'].iloc[i]
                                        nta=self.df['ANLTA'].iloc[i]
                                        ntaerr=self.df['ANLDTA'].iloc[i]

                                        print('updating dual aolpss - aSlta')
                                        pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,0.0,0.0, nta,ntaerr,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, AOLPSS='{pss}', AOLDPSS={errpss}, AOLPC={pc}, AOLAPPEFF={appeff},ACOLTA={ota},ACOLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    elif "BSLTA" in ycol:
                                        onta=self.df['BOLTA'].iloc[i]
                                        ontaerr=self.df['BOLDTA'].iloc[i]
                                        nta=self.df['BNLTA'].iloc[i]
                                        ntaerr=self.df['BNLDTA'].iloc[i]

                                        print('updating dual aolpss - bSlta')
                                        pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,0.0,0.0, nta,ntaerr,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, BOLPSS='{pss}', BOLDPSS={errpss}, BOLPC={pc}, BOLAPPEFF={appeff},BCOLTA={ota},BCOLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    print(stmt)

                            elif "ANLTA" in ycol or "BNLTA" in ycol:
                                    
                                    if "ANLTA" in ycol:
                                        onta=self.df['AOLTA'].iloc[i]
                                        ontaerr=self.df['AOLDTA'].iloc[i]
                                        sta=self.df['ASLTA'].iloc[i]
                                        staerr=self.df['ASLDTA'].iloc[i]

                                        print('updating dual aolpss - aSlta')
                                        pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, AOLPSS='{pss}', AOLDPSS={errpss}, AOLPC={pc}, AOLAPPEFF={appeff},ACOLTA={ota},ACOLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    elif "BNLTA" in ycol:
                                        onta=self.df['BOLTA'].iloc[i]
                                        ontaerr=self.df['BOLDTA'].iloc[i]
                                        sta=self.df['BSLTA'].iloc[i]
                                        staerr=self.df['BSLDTA'].iloc[i]

                                        print('updating dual aolpss - bSlta')
                                        pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, BOLPSS='{pss}', BOLDPSS={errpss}, BOLPC={pc}, BOLAPPEFF={appeff},BCOLTA={ota},BCOLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    print(stmt)

                            elif "AOLTA" in ycol or "BOLTA" in ycol:
                                    
                                    if "AOLTA" in ycol:

                                        print('updating dual aolpss - aSlta')
                                        pss,errpss,pc,ota,otaerr,appeff = np.nan,np.nan,np.nan,np.nan,np.nan,np.nan
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, AOLPSS='{pss}', AOLDPSS={errpss}, AOLPC={pc}, AOLAPPEFF={appeff},ACOLTA={ota},ACOLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    elif "BOLTA" in ycol:

                                        print('updating dual aolpss - bSlta')
                                        pss,errpss,pc,ota,otaerr,appeff =np.nan,np.nan,np.nan,np.nan,np.nan,np.nan
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, BOLPSS='{pss}', BOLDPSS={errpss}, BOLPC={pc}, BOLAPPEFF={appeff},BCOLTA={ota},BCOLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    print(stmt)

                            elif "ASRTA" in ycol or "BSRTA" in ycol:
                                    
                                    if "ASRTA" in ycol:
                                        onta=self.df['AORTA'].iloc[i]
                                        ontaerr=self.df['AORDTA'].iloc[i]
                                        nta=self.df['ANRTA'].iloc[i]
                                        ntaerr=self.df['ANRDTA'].iloc[i]

                                        print('updating dual aoRpss - aSRta')
                                        pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,0.0,0.0, nta,ntaerr,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, AORPSS={pss}, AORDPSS={errpss}, AORPC={pc}, AORAPPEFF={appeff},ACORTA={ota},ACORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    elif "BSRTA" in ycol:
                                        onta=self.df['BORTA'].iloc[i]
                                        ontaerr=self.df['BORDTA'].iloc[i]
                                        nta=self.df['BNRTA'].iloc[i]
                                        ntaerr=self.df['BNRDTA'].iloc[i]

                                        print('updating dual aoRpss - bSRta')
                                        pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,0.0,0.0, nta,ntaerr,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, BORPSS={pss}, BORDPSS={errpss}, BORPC={pc}, BORAPPEFF={appeff},BCORTA={ota},BCORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    print(stmt)

                            elif "ANRTA" in ycol or "BNRTA" in ycol:
                                    
                                    if "ANRTA" in ycol:
                                        onta=self.df['AORTA'].iloc[i]
                                        ontaerr=self.df['AORDTA'].iloc[i]
                                        sta=self.df['ASRTA'].iloc[i]
                                        staerr=self.df['ASRDTA'].iloc[i]

                                        print('updating dual aoRpss - aSRta')
                                        pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, AORPSS={pss}, AORDPSS={errpss}, AORPC={pc}, AORAPPEFF={appeff},ACORTA={ota},ACORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    elif "BNRTA" in ycol:
                                        onta=self.df['BORTA'].iloc[i]
                                        ontaerr=self.df['BORDTA'].iloc[i]
                                        sta=self.df['BSRTA'].iloc[i]
                                        staerr=self.df['BSRDTA'].iloc[i]

                                        print('updating dual aoRpss - bSlta')
                                        pss,errpss,pc,ota,otaerr,appeff = cp.calc_pc_pss(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df['FLUX'].iloc[i],self.df)
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, BORPSS={pss}, BORDPSS={errpss}, BORPC={pc}, BORAPPEFF={appeff},BCORTA={ota},BCORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    print(stmt)

                            elif "AORTA" in ycol or "BORTA" in ycol:
                                    
                                    if "AORTA" in ycol:

                                        print('updating dual aoRpss - aSRta')
                                        pss,errpss,pc,ota,otaerr,appeff = np.nan,np.nan,np.nan,np.nan,np.nan,np.nan
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, AORPSS={pss}, AORDPSS={errpss}, AORPC={pc}, AORAPPEFF={appeff},ACORTA={ota},ACORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    elif "BORTA" in ycol:

                                        print('updating dual aoRPss - bSRta')
                                        pss,errpss,pc,ota,otaerr,appeff =np.nan,np.nan,np.nan,np.nan,np.nan,np.nan
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, BORPSS={pss}, BORDPSS={errpss}, BORPC={pc}, BORAPPEFF={appeff},BCORTA={ota},BCORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    print(stmt)

                            db.c.execute(stmt)
                            db.commit_changes()
                            db.close_db()
                            print("updated CALDB")
                            print(tablename,xcol,ycol)
                    
                            # complete the code here
                            # for the rest of them.
                    else:
                        self.write(f"Updating {self.dbFile} table: {tablename}, type: {srcType}",'info')
                        
                        print('\n-BEAMTYPE: ',self.df['BEAMTYPE'].iloc[i],'\n-srcType: ',srcType)

                        # update the database
                        if 'S' in  str(self.df['BEAMTYPE'].iloc[i]):

                            print(self.df['BEAMTYPE'].iloc[i])
                            
                            if "13.0S" == self.df['BEAMTYPE'].iloc[i]:
                                
                                if "TSYS1" in ycol or "TSYS2" in ycol:

                                    if 'TSYS1' in ycol:
                                        stot=self.df['SRCP'].iloc[i]
                                        stoterr=np.sqrt(self.df['SRCPERR'].iloc[i]**2)
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLTA='{np.nan}',  OLDTA='{np.nan}', OLFLAG=200, SLCP='{np.nan}', SLCPERR='{np.nan}',  STOT='{stot}', STOTERR='{stoterr}' WHERE FILENAME = '{FN}' ;"

                                    if 'TSYS2' in ycol:
                                        stot=self.df['SLCP'].iloc[i]
                                        stoterr=np.sqrt(self.df['SLCPERR'].iloc[i]**2)
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORTA='{np.nan}', ORDTA='{np.nan}', ORFLAG=200, SRCP='{np.nan}', SRCPERR='{np.nan}',  STOT='{stot}', STOTERR='{stoterr}' WHERE FILENAME = '{FN}' ;"

                                elif "OLTA" in ycol or "SLCP" in ycol :
                                    stot=self.df['SRCP'].iloc[i]
                                    stoterr=np.sqrt(self.df['SRCPERR'].iloc[i]**2)
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}',OLDTA='{np.nan}', OLFLAG=201, TSYS1='{np.nan}', SLCP='{np.nan}', SLCPERR='{np.nan}', STOT='{stot}', STOTERR='{stoterr}' WHERE FILENAME = '{FN}' ;"

                                elif "ORTA" in ycol or "SRCP" in ycol:
                                    stot=self.df['SLCP'].iloc[i]
                                    stoterr=np.sqrt(self.df['SLCPERR'].iloc[i]**2)
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}',ORDTA='{np.nan}', ORFLAG=201, TSYS2='{np.nan}', SRCP='{np.nan}', SRCPERR='{np.nan}',  STOT='{stot}', STOTERR='{stoterr}' WHERE FILENAME = '{FN}' ;"

                                # elif "SLCP" in ycol:
                                #     print('\nprint updating SLCP')
                                #     stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', SLCPERR='{np.nan}', OLFLAG=202, OLAPPEFF='{np.nan}' WHERE FILENAME = '{FN}' ;"

                                # elif "SRCP" in ycol:
                                #     print('\nprint updating SRCP')
                                #     stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=202, ORDPSS='{np.nan}', ORAPPEFF='{np.nan}' WHERE FILENAME = '{FN}' ;"
                                       
                                print(stmt)
                                db.c.execute(stmt)
                                db.commit_changes()
                                db.close_db()
                                print(f"updated {self.dbFile}")
                                print(tablename,xcol,ycol)
                                print('\nDONE')
                                print("+"*30,"\n")

                            else:

                                if "TSYS1" in ycol or "TSYS2" in ycol:

                                    if 'TSYS1' in ycol:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLTA='{np.nan}', OLDTA='{np.nan}', COLTA='{np.nan}', COLDTA='{np.nan}',  OLPC='{np.nan}', OLS2N=200,  \
                                            SLTA='{np.nan}', SLDTA='{np.nan}', SLS2N='{np.nan}',\
                                            NLTA='{np.nan}', NLDTA='{np.nan}', NLS2N='{np.nan}',\
                                            SLCP='{np.nan}', SLCPERR='{np.nan}',\
                                            SLCPPSS='{np.nan}', SLCPPSSERR='{np.nan}',\
                                            STOT='{np.nan}', STOTERR='{np.nan}' \
                                            WHERE FILENAME = '{FN}' ;"
                                        
                                    if 'TSYS2' in ycol:
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORTA='{np.nan}', ORDTA='{np.nan}', CORTA='{np.nan}', CORDTA='{np.nan}',  ORPC='{np.nan}', ORS2N=200,  \
                                            SRTA='{np.nan}', SRDTA='{np.nan}', SRS2N='{np.nan}',\
                                            NRTA='{np.nan}', NRDTA='{np.nan}', NRS2N='{np.nan}',\
                                            SRCP='{np.nan}', SRCPERR='{np.nan}',\
                                            SRCPPSS='{np.nan}', SRCPPSSERR='{np.nan}',\
                                            STOT='{np.nan}', STOTERR='{np.nan}' \
                                            WHERE FILENAME = '{FN}' ;"

                                elif "OLTA" in ycol or "NLTA" in ycol or "SLTA" in ycol:

                                        srcp=self.df['SRCP'].iloc[i]
                                        srcperr=self.df['SRCPERR'].iloc[i]

                                        
                                        if 'NLTA' in ycol:

                                                hpsTa=self.df['SLTA'].iloc[i]
                                                errHpsTa=self.df['SLDTA'].iloc[i]
                                                onTa=self.df['OLTA'].iloc[i]
                                                errOnTa=self.df['OLDTA'].iloc[i]
                                                pss=self.df['SLCPPSS'].iloc[i]
                                                errpss=self.df['SLCPPSSERR'].iloc[i]

                                                pc,corrta,errta=cp.calc_pc(0,  hpsTa, errHpsTa, 0, 0, onTa, errOnTa, self.df)

                                                slcp=corrta*pss
                                                slcperr=np.sqrt((corrta/errta)**2 + (pss/errpss)**2)*slcp

                                                stot = (slcp+srcp)/2.
                                                stoterr=0.5*((slcperr)**2 + (srcperr)**2)

                                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', NLDTA='{np.nan}', OLFLAG=200, OLPC={pc}, COLTA={corrta}, COLDTA={errta}, SLCP={slcp}, SLCPERR={slcperr},STOT={stot}, STOTERR={stoterr}  WHERE FILENAME = '{FN}' ;"
                                               
                                        elif 'SLTA' in ycol:

                                                hpnTa=self.df['NLTA'].iloc[i]
                                                errHpnTa=self.df['NLDTA'].iloc[i]
                                                onTa=self.df['OLTA'].iloc[i]
                                                errOnTa=self.df['OLDTA'].iloc[i]
                                                pss=self.df['SLCPPSS'].iloc[i]
                                                errpss=self.df['SLCPPSSERR'].iloc[i]

                                                pc,corrta,errta=cp.calc_pc(0,  0, 0, hpnTa, errHpnTa, onTa, errOnTa, self.df)

                                                slcp=corrta*pss
                                                slcperr=np.sqrt((corrta/errta)**2 + (pss/errpss)**2)*slcp

                                                stot = (slcp+srcp)/2.
                                                stoterr=0.5*((slcperr)**2 + (srcperr)**2)

                                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', SLDTA='{np.nan}', OLFLAG=200, OLPC={pc}, COLTA={corrta}, COLDTA={errta}, SLCP={slcp}, SLCPERR={slcperr},STOT={stot}, STOTERR={stoterr}  WHERE FILENAME = '{FN}' ;"
                                              
                                        else:
                                            # print('print updating OLTA')
                                            stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLDTA='{np.nan}', SLTA='{np.nan}',SLDTA='{np.nan}',NLTA='{np.nan}',\
                                                NLDTA'{np.nan}',OLPC='{np.nan}', OLFLAG=200, COLTA='{np.nan}', COLDTA='{np.nan}',OLAPPEFF='{np.nan}',SLCP='{np.nan}', \
                                                SLCPERR='{np.nan}',STOT={srcp},STOTERR={srcperr} WHERE FILENAME = '{FN}' ;"
                                         
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"\nupdated {self.dbFile} ")
                                        print(tablename,xcol,ycol)
                                        print('\nDONE')
                                        print("+"*30,"\n")

                                elif "ORTA" in ycol or "NRTA" in ycol or "SRTA" in ycol:

                                        slcp=self.df['SLCP'].iloc[i]
                                        slcperr=self.df['SLCPERR'].iloc[i]

                                        if 'NRTA' in ycol:

                                                hpsTa=self.df['SRTA'].iloc[i]
                                                errHpsTa=self.df['SRDTA'].iloc[i]
                                                onTa=self.df['ORTA'].iloc[i]
                                                errOnTa=self.df['ORDTA'].iloc[i]
                                                pss=self.df['SRCPPSS'].iloc[i]
                                                errpss=self.df['SRCPPSSERR'].iloc[i]

                                                pc,corrta,errta=cp.calc_pc(0,  hpsTa, errHpsTa, 0, 0, onTa, errOnTa, self.df)

                                                srcp=corrta*pss
                                                srcperr=np.sqrt((corrta/errta)**2 + (pss/errpss)**2)*slcp

                                                stot = (slcp+srcp)/2.
                                                stoterr=0.5*((slcperr)**2 + (srcperr)**2)

                                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', NRDTA='{np.nan}', ORFLAG=200, ORPC={pc}, CORTA={corrta}, CORDTA={errta}, SRCP={slcp}, SRCPERR={slcperr},STOT={stot}, STOTERR={stoterr}  WHERE FILENAME = '{FN}' ;"
                                               
                                        elif 'SRTA' in ycol:

                                                hpnTa=self.df['NLTA'].iloc[i]
                                                errHpnTa=self.df['NLDTA'].iloc[i]
                                                onTa=self.df['OLTA'].iloc[i]
                                                errOnTa=self.df['OLDTA'].iloc[i]
                                                pss=self.df['SRCPPSS'].iloc[i]
                                                errpss=self.df['SRCPPSSERR'].iloc[i]

                                                pc,corrta,errta=cp.calc_pc(0,  0, 0, hpnTa, errHpnTa, onTa, errOnTa, self.df)

                                                srcp=corrta*pss
                                                srcperr=np.sqrt((corrta/errta)**2 + (pss/errpss)**2)*slcp

                                                stot = (slcp+srcp)/2.
                                                stoterr=0.5*((slcperr)**2 + (srcperr)**2)

                                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', SRDTA='{np.nan}', ORFLAG=200, ORPC={pc}, CORTA={corrta}, CORDTA={errta}, SRCP={slcp}, SRCPERR={slcperr},STOT={stot}, STOTERR={stoterr}  WHERE FILENAME = '{FN}' ;"
                                              
                                        else:
                                            # print('print updating OLTA')
                                            stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORDTA='{np.nan}', SRTA='{np.nan}',SRDTA='{np.nan}',NRTA='{np.nan}',NRDTA'{np.nan}',\
                                                ORPC='{np.nan}', ORFLAG=200, CORTA='{np.nan}', CORDTA='{np.nan}',ORAPPEFF='{np.nan}',SRCP='{np.nan}', SRCPERR='{np.nan}',\
                                                STOT={slcp},STOTERR={slcperr} WHERE FILENAME = '{FN}' ;"
                                         
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"\nupdated {self.dbFile} ")
                                        print(tablename,xcol,ycol)
                                        print('\nDONE')
                                        print("+"*30,"\n")

                                elif "SLCP" in ycol:

                                        # print('\nprint updating OLPSS')
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', SLCPERR='{np.nan}', OLFLAG=201, \
                                            SLTA='{np.nan}', SLDTA='{np.nan}', SLS2N='{np.nan}',\
                                            NLTA='{np.nan}', NLDTA='{np.nan}', NLS2N='{np.nan}',\
                                            OLTA='{np.nan}', OLDTA='{np.nan}', COLTA='{np.nan}', COLDTA='{np.nan}', OLPC='{np.nan}', OLS2N=202,  \
                                            STOT={srcp}, STOTERR={srcperr}\
                                        WHERE FILENAME = '{FN}' ;"

                                        print(stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                elif "SRCP" in ycol:

                                        # print('\nprint updating ORPSS')
                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', SRCPERR='{np.nan}', ORFLAG=202, \
                                            SRTA='{np.nan}', SRDTA='{np.nan}', SRS2N='{np.nan}',\
                                            NRTA='{np.nan}', NRDTA='{np.nan}', NRS2N='{np.nan}',\
                                            ORTA='{np.nan}', ORDTA='{np.nan}', CORTA='{np.nan}', CORDTA='{np.nan}', ORPC='{np.nan}', ORS2N=202,  \
                                            STOT={srcp}, STOTERR={srcperr}\
                                        WHERE FILENAME = '{FN}' ;"

                                        print(stmt)
                                        db.c.execute(stmt)
                                        db.commit_changes()
                                        db.close_db()
                                        print(f"updated {self.dbFile}")
                                        print(tablename,xcol,ycol)

                                else:
                                    print('No update algorithm setup yet\n')

                        elif 'D' in str(self.df['BEAMTYPE'].iloc[0]):
                            # print("D in beamtype")1
                            aslcp=self.df['ASLCP'].iloc[i]
                            bslcp=self.df['BSLCP'].iloc[i]
                            asrcp=self.df['ASRCP'].iloc[i]
                            bsrcp=self.df['BSRCP'].iloc[i]
                            aslcperr=self.df['ASLCPERR'].iloc[i]
                            bslcperr=self.df['BSLCPERR'].iloc[i]
                            asrcperr=self.df['ASRCPERR'].iloc[i]
                            bsrcperr=self.df['BSRCPERR'].iloc[i]

                            if "TSYS1" in ycol or "TSYS2" in ycol:

                                if 'TSYS1' in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', \
                                        AOLTA='{np.nan}', AOLDTA='{np.nan}', OLFLAG=200, AOLPC='{np.nan}',  ACOLTA='{np.nan}', ACOLDTA='{np.nan}', \
                                        ASLTA='{np.nan}', ASLDTA='{np.nan}', SLFLAG=200, ANLTA='{np.nan}', ANLDTA='{np.nan}' \
                                        BSLTA='{np.nan}', BSLDTA='{np.nan}', NLFLAG=200, BNLTA='{np.nan}', BNLDTA='{np.nan}', \
                                        BOLTA='{np.nan}', BOLDTA='{np.nan}', BOLPC='{np.nan}',  BCOLTA='{np.nan}', BCOLDTA='{np.nan}', \
                                        ASLCP='{np.nan}', ASLCPERR='{np.nan}',BSLCP='{np.nan}', BSLCPERR='{np.nan}'  WHERE FILENAME = '{FN}' ;"

                                if 'TSYS2' in ycol:
                                    stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', \
                                        AORTA='{np.nan}', AORDTA='{np.nan}', ORFLAG=200, AORPC='{np.nan}', ACORTA='{np.nan}', ACORDTA='{np.nan}', \
                                        ASRTA='{np.nan}', ASRDTA='{np.nan}', SRFLAG=200, ANRTA='{np.nan}', ANRDTA='{np.nan}', \
                                        BSRTA='{np.nan}', BSRDTA='{np.nan}', NRFLAG=200, BNRTA='{np.nan}', BNRDTA='{np.nan}', \
                                        BORTA='{np.nan}', BORDTA='{np.nan}', BORFLAG=200, BORPC='{np.nan}', BCORTA='{np.nan}', BCORDTA='{np.nan}', \
                                        ASRCP='{np.nan}', ASRCPERR='{np.nan}', BSRCP='{np.nan}', BSRCPERR='{np.nan}'  WHERE FILENAME = '{FN}' ;"

                            elif "ASLCP" in ycol:
                                s=[bslcp,asrcp,bsrcp]
                                er=[bslcperr,asrcperr,bsrcperr]
                                ss=[]
                                se=[]
                                       
                                for i in range(len(s)):
                                    if "nan" in str(s[i]):
                                        pass
                                    else:
                                        ss.append(s[i])
                                        se.append(er[i])
                                                
                                stot = (sum(ss))/len(ss)
                                stoterr=(1/len(se))*np.sqrt(sum([w**2 for w in se]))

                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ASLCPERR='{np.nan}',  OLFLAG=200, \
                                    STOT={stot},  STOTERR={stoterr} \
                                    WHERE FILENAME = '{FN}' ;"

                            elif "BSLCP" in ycol:
                                s=[aslcp,asrcp,bsrcp]
                                er=[aslcperr,asrcperr,bsrcperr]
                                ss=[]
                                se=[]
                                       
                                for i in range(len(s)):
                                    if "nan" in str(s[i]):
                                        pass
                                    else:
                                        ss.append(s[i])
                                        se.append(er[i])
                                                
                                stot = (sum(ss))/len(ss)
                                stoterr=(1/len(se))*np.sqrt(sum([w**2 for w in se]))

                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', BSLCPERR='{np.nan}',  OLFLAG=200, \
                                    STOT={stot},  STOTERR={stoterr} \
                                    WHERE FILENAME = '{FN}' ;"

                            elif "ASRCP" in ycol:
                                s=[bslcp,asrcp,bsrcp]
                                er=[bslcperr,asrcperr,bsrcperr]
                                ss=[]
                                se=[]
                                       
                                for i in range(len(s)):
                                    if "nan" in str(s[i]):
                                        pass
                                    else:
                                        ss.append(s[i])
                                        se.append(er[i])
                                                
                                stot = (sum(ss))/len(ss)
                                stoterr=(1/len(se))*np.sqrt(sum([w**2 for w in se]))

                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ASRCPERR='{np.nan}',  ORFLAG=200, \
                                    STOT={stot},  STOTERR={stoterr} \
                                    WHERE FILENAME = '{FN}' ;"

                            elif "BSRCP" in ycol:
                                s=[aslcp,asrcp,bsrcp]
                                er=[aslcperr,asrcperr,bsrcperr]
                                ss=[]
                                se=[]
                                       
                                for i in range(len(s)):
                                    if "nan" in str(s[i]):
                                        pass
                                    else:
                                        ss.append(s[i])
                                        se.append(er[i])
                                                
                                stot = (sum(ss))/len(ss)
                                stoterr=(1/len(se))*np.sqrt(sum([w**2 for w in se]))

                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', BSRCPERR='{np.nan}',  ORFLAG=200, \
                                    STOT={stot},  STOTERR={stoterr} \
                                    WHERE FILENAME = '{FN}' ;"

                            elif "AOLTA" in ycol:
                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', AOLDTA='{np.nan}',  OLFLAG=200, AOLPC='{np.nan}',  ACOLTA='{np.nan}', ACOLDTA='{np.nan}', \
                                    ASLTA='{np.nan}', ASLDTA='{np.nan}', SLFLAG=200, \
                                    ANLTA='{np.nan}', ANLDTA='{np.nan}', NLFLAG=200 \
                                    WHERE FILENAME = '{FN}' ;"

                            elif "AORTA" in ycol:
                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', AORDTA='{np.nan}', ORFLAG=200, AORPC='{np.nan}', ACORTA='{np.nan}', ACORDTA='{np.nan}', \
                                    ASRTA='{np.nan}', ASRDTA='{np.nan}', SRFLAG=200, \
                                    ANRTA='{np.nan}', ANRDTA='{np.nan}', NRFLAG=200 \
                                    WHERE FILENAME = '{FN}' ;"

                            elif "BOLTA" in ycol:
                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', BOLDTA='{np.nan}', OLFLAG=200, BOLPC='{np.nan}',  BCOLTA='{np.nan}', BCOLDTA='{np.nan}', \
                                    BSLTA='{np.nan}', BSLDTA='{np.nan}', SLFLAG=200, \
                                    BNLTA='{np.nan}', BNLDTA='{np.nan}', NLFLAG=200 \
                                    WHERE FILENAME = '{FN}' ;"

                            elif "BORTA" in ycol:
                                stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', BORDTA='{np.nan}', ORFLAG=200, BORPC='{np.nan}',  BCORTA='{np.nan}', BCORDTA='{np.nan}', \
                                    BSRTA='{np.nan}', BSRDTA='{np.nan}', SRFLAG=200, \
                                    BNRTA='{np.nan}', BNRDTA='{np.nan}', NRFLAG=200 \
                                    WHERE FILENAME = '{FN}' ;"

                            elif "ASLTA" in ycol or "BSLTA" in ycol:

                                    if "ASLTA" in ycol:

                                        # recalculate tot flux
                                        hpnTa=self.df['ANLTA'].iloc[i]
                                        errHpnTa=self.df['ANLDTA'].iloc[i]
                                        onTa=self.df['AOLTA'].iloc[i]
                                        errOnTa=self.df['AOLDTA'].iloc[i]
                                        pss=self.df['ALCPPSS'].iloc[i]
                                        errpss=self.df['ALCPPSSERR'].iloc[i]

                                        pc,corrta,errta=cp.calc_pc(0, 0, 0, hpnTa, errHpnTa, onTa, errOnTa, self.df)

                                        slcp=corrta*pss
                                        slcperr=np.sqrt((corrta/errta)**2 + (pss/errpss)**2)*slcp

                                        s=[slcp,bslcp,asrcp,bsrcp]
                                        er=[slcperr,bslcperr,asrcperr,bsrcperr]
                                        ss=[]
                                        se=[]
                                       
                                        for i in range(len(s)):
                                            if "nan" in str(s[i]):
                                                pass
                                            else:
                                                ss.append(s[i])
                                                se.append(er[i])
                                                
                                        stot = (sum(ss))/len(ss)
                                        stoterr=(1/len(se))*np.sqrt(sum([w**2 for w in se]))

                                        print('updating dual ASLTA')

                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, \
                                            ASLTA='{np.nan}', ASLDTA='{np.nan}', \
                                            AOLPC={pc}, ACOLTA={corrta},ACOLDTA={errta}, \
                                            ASLCP={slcp}, ASLCPERR={slcperr}, STOT={stot}, STOTERR={stoterr}  WHERE FILENAME = '{FN}' ;"

                                    elif "BSLTA" in ycol:
                                        # recalculate tot flux
                                        hpnTa=self.df['BNLTA'].iloc[i]
                                        errHpnTa=self.df['BNLDTA'].iloc[i]
                                        onTa=self.df['BOLTA'].iloc[i]
                                        errOnTa=self.df['BOLDTA'].iloc[i]
                                        pss=self.df['BLCPPSS'].iloc[i]
                                        errpss=self.df['BLCPPSSERR'].iloc[i]

                                        pc,corrta,errta=cp.calc_pc(0, 0, 0, hpnTa, errHpnTa, onTa, errOnTa, self.df)

                                        slcp=corrta*pss
                                        slcperr=np.sqrt((corrta/errta)**2 + (pss/errpss)**2)*slcp

                                        s=[aslcp,slcp,asrcp,bsrcp]
                                        er=[aslcperr,slcperr,asrcperr,bsrcperr]
                                        ss=[]
                                        se=[]
                                       
                                        for i in range(len(s)):
                                            if "nan" in str(s[i]):
                                                pass
                                            else:
                                                ss.append(s[i])
                                                se.append(er[i])
                                                
                                        stot = (sum(ss))/len(ss)
                                        stoterr=(1/len(se))*np.sqrt(sum([w**2 for w in se]))

                                        print('updating dual ASLTA')

                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, \
                                            BSLTA='{np.nan}', BSLDTA='{np.nan}', \
                                            BOLPC={pc}, BCOLTA={corrta},BCOLDTA={errta}, \
                                            BSLCP={slcp}, BSLCPERR={slcperr}, STOT={stot}, STOTERR={stoterr}  WHERE FILENAME = '{FN}' ;"

                            elif "ANLTA" in ycol or "BNLTA" in ycol:
                                    
                                    if "ANLTA" in ycol:
                                        # recalculate tot flux
                                        hpsTa=self.df['ASLTA'].iloc[i]
                                        errHpsTa=self.df['ASLDTA'].iloc[i]
                                        onTa=self.df['AOLTA'].iloc[i]
                                        errOnTa=self.df['AOLDTA'].iloc[i]
                                        pss=self.df['ALCPPSS'].iloc[i]
                                        errpss=self.df['ALCPPSSERR'].iloc[i]

                                        pc,corrta,errta=cp.calc_pc(0, hpsTa, errHpsTa, 0, 0, onTa, errOnTa, self.df)

                                        slcp=corrta*pss
                                        slcperr=np.sqrt((corrta/errta)**2 + (pss/errpss)**2)*slcp

                                        s=[slcp,bslcp,asrcp,bsrcp]
                                        er=[slcperr,bslcperr,asrcperr,bsrcperr]
                                        ss=[]
                                        se=[]
                                       
                                        for i in range(len(s)):
                                            if "nan" in str(s[i]):
                                                pass
                                            else:
                                                ss.append(s[i])
                                                se.append(er[i])
                                                
                                        stot = (sum(ss))/len(ss)
                                        stoterr=(1/len(se))*np.sqrt(sum([w**2 for w in se]))

                                        print('updating dual ANLTA')

                                        stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, \
                                            ANLTA='{np.nan}', ANLDTA='{np.nan}', \
                                            AOLPC={pc}, ACOLTA={corrta},ACOLDTA={errta}, \
                                            ASLCP={slcp}, ASLCPERR={slcperr}, STOT={stot}, STOTERR={stoterr}  WHERE FILENAME = '{FN}' ;"
                                    
                                    # elif "BNLTA" in ycol:
                                    #     onta=self.df['BOLTA'].iloc[i]
                                    #     ontaerr=self.df['BOLDTA'].iloc[i]
                                    #     sta=self.df['BSLTA'].iloc[i]
                                    #     staerr=self.df['BSLDTA'].iloc[i]

                                    #     print('updating dual BNLTA')
                                    #     pc,ota,otaerr= cp.calc_pc(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df)
                                    #     stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, BOLPC={pc}, BCOLTA={ota},BCOLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                                    # print(stmt)

                            # elif "AOLTA" in ycol or "BOLTA" in ycol:
                                    
                            #         if "AOLTA" in ycol:

                            #             print('updating dual AOLTA')
                            #             pc,ota,otaerr = np.nan,np.nan,np.nan
                            #             stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, AOLPC={pc}, ACOLTA={ota},ACOLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                            #         elif "BOLTA" in ycol:

                            #             print('updating dual BOLTA')
                            #             pc,ota,otaerr=np.nan,np.nan,np.nan
                            #             stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', OLFLAG=200, BOLPC={pc}, BCOLTA={ota},BCOLDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                            #         print(stmt)

                            # elif "ASRTA" in ycol or "BSRTA" in ycol:
                                    
                            #         if "ASRTA" in ycol:
                            #             onta=self.df['AORTA'].iloc[i]
                            #             ontaerr=self.df['AORDTA'].iloc[i]
                            #             nta=self.df['ANRTA'].iloc[i]
                            #             ntaerr=self.df['ANRDTA'].iloc[i]

                            #             print('updating dual ASRTA')
                            #             pc,ota,otaerr = cp.calc_pc(0,0.0,0.0, nta, ntaerr, onta, ontaerr,self.df)
                            #             stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200,  AORPC={pc},ACORTA={ota},ACORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                            #         elif "BSRTA" in ycol:
                            #             onta=self.df['BORTA'].iloc[i]
                            #             ontaerr=self.df['BORDTA'].iloc[i]
                            #             nta=self.df['BNRTA'].iloc[i]
                            #             ntaerr=self.df['BNRDTA'].iloc[i]

                            #             print('updating dual BSRTA')
                            #             pc,ota,otaerr = cp.calc_pc(0,0.0,0.0, nta,ntaerr,onta,ontaerr,self.df)
                            #             stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, BORPC={pc}, BCORTA={ota},BCORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                            #         print(stmt)

                            # elif "ANRTA" in ycol or "BNRTA" in ycol:
                                    
                            #         if "ANRTA" in ycol:
                            #             onta=self.df['AORTA'].iloc[i]
                            #             ontaerr=self.df['AORDTA'].iloc[i]
                            #             sta=self.df['ASRTA'].iloc[i]
                            #             staerr=self.df['ASRDTA'].iloc[i]

                            #             print('updating dual ANRTA')
                            #             pc,ota,otaerr = cp.calc_pc(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df)
                            #             stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, AORPC={pc},ACORTA={ota},ACORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                            #         elif "BNRTA" in ycol:
                            #             onta=self.df['BORTA'].iloc[i]
                            #             ontaerr=self.df['BORDTA'].iloc[i]
                            #             sta=self.df['BSRTA'].iloc[i]
                            #             staerr=self.df['BSRDTA'].iloc[i]

                            #             print('updating dual BNRTA')
                            #             pc,ota,otaerr = cp.calc_pc(0,sta,staerr, 0.0,0.0,onta,ontaerr,self.df)
                            #             stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200, BORPC={pc}, BCORTA={ota},BCORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                            #         print(stmt)

                            # elif "AORTA" in ycol or "BORTA" in ycol:
                                    
                            #         if "AORTA" in ycol:

                            #             print('updating dual AORTA')
                            #             pc,ota,otaerr = np.nan, np.nan, np.nan
                            #             stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200,  AORPC={pc}, ACORTA={ota},ACORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                            #         elif "BORTA" in ycol:

                            #             print('updating dual BORTA')
                            #             pc,ota,otaerr =np.nan, np.nan, np.nan
                            #             stmt = f"UPDATE {tablename} SET {ycol}='{np.nan}', ORFLAG=200,  BORPC={pc}, BCORTA={ota},BCORDTA={otaerr}  WHERE FILENAME = '{FN}' ;"

                            #         

                            print(stmt)
                            db.c.execute(stmt)
                            db.commit_changes()
                            db.close_db()
                            print("updated CALDB")
                            print(tablename,xcol,ycol)
                    
                            # complete the code here
                            # for the rest of them.

                    print('After deleting: ',len(self.df))
                    print(self.df.iloc[i][yCol])
                    self.Canvas.clear_figure()
                    self.plot_cols_df()

    def getdata(self,df,pol,ind):
        """get data for flux calculation"""

        antennaTemp=abs(df[f'O{pol}TA'].iloc[ind])
        errAntennaTemp=abs(df[f'O{pol}DTA'].iloc[ind])
        
        return antennaTemp,errAntennaTemp
    
    def getdata_nb(df,pol,ind):
        s=abs(df[f'S{pol}TA'].iloc[ind])
        se=abs(df[f'S{pol}DTA'].iloc[ind])
        n=abs(df[f'N{pol}TA'].iloc[ind])
        ne=abs(df[f'N{pol}DTA'].iloc[ind])
        o=abs(df[f'O{pol}TA'].iloc[ind])
        oe=abs(df[f'O{pol}DTA'].iloc[ind])
        return s,se,n,ne,o,oe

    def get_params(self,mydf,ind):
        """get params for flux calc"""
        fn = mydf['FILENAME'].iloc[ind]#[:18]
        sd = mydf['SOURCEDIR'].iloc[ind]
        idx = mydf['id'].iloc[ind]
        bt = mydf['BEAMTYPE'].iloc[ind]
        objt = mydf['OBJECTTYPE'].iloc[ind]
        date = mydf['MJD'].iloc[ind]
        d2 = mydf['OBSDATE'].iloc[ind]
        obj = mydf['OBJECT'].iloc[ind]
        frq = mydf['CENTFREQ'].iloc[ind]

        # get data
        olta,oldta = self.getdata(mydf,'L',ind)
        orta,ordta = self.getdata(mydf,'R',ind)

        try:
            data={'BEAMTYPE':mydf['BEAMTYPE'].iloc[ind],
                        'OBJECTTYPE':mydf['OBJECTTYPE'].iloc[ind],
                        'ATMOS_ABSORPTION_CORR':mydf['ATMOS_ABSORPTION_CORR'].iloc[ind],
                        'SIZE_CORRECTION_FACTOR':mydf['SIZE_CORRECTION_FACTOR'].iloc[ind]}
        except:
            data={'BEAMTYPE':mydf['BEAMTYPE'].iloc[ind],
                'OBJECTTYPE':mydf['OBJECTTYPE'].iloc[ind]}
        
        return data,fn,sd,idx,bt,objt,date,d2,obj,frq,olta,oldta,orta,ordta
                    
    def get_params_nb(self,mydf,ind):
    
        fn=mydf['FILENAME'].iloc[ind]#[:18]
        sd=mydf['SOURCEDIR'].iloc[ind]
        idx=mydf['id'].iloc[ind]
        bt=mydf['BEAMTYPE'].iloc[ind]
        objt=mydf['OBJECTTYPE'].iloc[ind]
        date = mydf['MJD'].iloc[ind]
        d2 = mydf['OBSDATE'].iloc[ind]
        obj = mydf['OBJECT'].iloc[ind]
        frq = mydf['CENTFREQ'].iloc[ind]

        # get data
        slta,sldta,nlta,nldta,olta,oldta = self.getdata_nb(mydf,'L',ind)
        srta,srdta,nrta,nrdta,orta,ordta = self.getdata_nb(mydf,'R',ind)

        try:
            data={'BEAMTYPE':mydf['BEAMTYPE'].iloc[ind],
                'OBJECTTYPE':mydf['OBJECTTYPE'].iloc[ind],
                'ATMOS_ABSORPTION_CORR':mydf['ATMOS_ABSORPTION_CORR'].iloc[ind],
                'SIZE_CORRECTION_FACTOR':mydf['SIZE_CORRECTION_FACTOR'].iloc[ind]
                }
        except:
            data={'BEAMTYPE':mydf['BEAMTYPE'].iloc[ind],
                'OBJECTTYPE':mydf['OBJECTTYPE'].iloc[ind]}
        
        return data,fn,sd,idx,bt,objt,date,d2,obj,frq,slta,sldta,srta,srdta,nlta,nldta,nrta,nrdta,olta,oldta,orta,ordta
                        
    def catch_zeroDivError(self,col,colerr):
        try:
            return (colerr/col)
        except ZeroDivisionError:
            return 0
            
    def calc_flux(self,ta,dta,pss,dpss):
        flux=ta*pss
        
        lta=self.catch_zeroDivError(ta,dta)
        lps=self.catch_zeroDivError(pss,dpss)
        errta=(lta)**2
        errpss=(lps)**2
        dflux=flux*np.sqrt(errta+errpss)
        return flux,dflux

    def calc_totFlux(self,slcp,dslcp,srcp,dsrcp):
        sumflux=np.sum([slcp,srcp])
        n=(np.array([slcp,srcp])>0).sum() 
        fluxtot=(sumflux/n)*2
        dfluxtot=(2/n)*np.sqrt(dslcp**2+dsrcp**2)
        return fluxtot,dfluxtot
        
    def update_point(self):
                    # update db on change

                    
                    # check last selected points
                    fit_points= self.Canvas.fit_points
                    click_index = self.Canvas.click_index

                    print('\n',"+"*30)
                    print(f"\nDeleting \n-point: {fit_points} \n-at index {click_index}")
                    #self.deleted[click_index].append([click_index, fit_points])

                    print('\ndf length Before deleting: ',len(self.df))
                    
                    xCol = self.Canvas.xlab
                    yCol = self.Canvas.ylab

                    print('\n','-'*30)

                    t = Time(fit_points[0][0])
                    #date=t
                    doy = t.strftime('%j')
                    #mjd=t.mjd

                    xp=self.df[xCol]
                    yp=self.df[yCol]

                    date_str=f'{str(fit_points[0][0])[:4]}d{str(doy)}'
                    
                    ii=int(click_index[0]) # point index to delete

                    print('Deleting: ')

                    # find what i is in the db
                    id=self.df['id'].iloc[ii]
                    #print(f'i: {ii}, id: {id}')
                    i=ii#d
                    FN=self.df['FILENAME'].iloc[i]

                    print('\n-date: ',date_str,'\n-file: ',FN)

                    print(f"\n-id: {self.df['id'].iloc[i]}, \n-index: {ii}")
                    # print('match: ', self.df['id'].iloc[i])#, self.df.iloc[i])
                    
                    #self.df.drop(id,inplace=True)
                    
                    print(f'\n> Setting {yCol}: {self.df.iloc[i][yCol]}, to np.nan')
                    #print(self.df.iloc[i][yCol])

                    
                    try:
                        self.df.at[i,yCol]=np.nan
                    except ValueError:
                        self.df.at[i,yCol]=0.0

                    print(f'\n+ New {yCol}: {self.df.iloc[i][yCol]}')
                    # change plot
                    tablename = self.time_ui.comboBoxTables.currentText()
                  
                    xcol=self.time_ui.comboBoxColsX.currentText()
                    ycol=self.time_ui.comboBoxColsY.currentText()

                    #self.dbFile
                    db = SQLiteDB(databaseName=self.dbFile, log=self.log)
                    db.create_db()

                    try:
                        srcType=self.df['OBJECTTYPE'].iloc[i]
                        self.write(f"Updating {self.dbFile} table: {tablename}, type: {srcType}",'info')
                        print('\n-BEAMTYPE: ',self.df['BEAMTYPE'][i],'\n-srcType: ',srcType)
                    except:
                        pass

                    # update the database
                    cols=list(self.df.columns)
                    stmt=f"UPDATE '{tablename}' SET "

                    dct={}

                    dct['BEAMTYPE']=self.df['BEAMTYPE'].iloc[i]
                    # print(list(self.df.columns))
                    dct['OBJECTTYPE']=self.df['OBJECTTYPE'].iloc[i]

                    try:
                        dct['ATMOS_ABSORPTION_CORR']=self.df['ATMOS_ABSORPTION_CORR'].iloc[i]
                        dct['SIZE_CORRECTION_FACTOR']=self.df['SIZE_CORRECTION_FACTOR'].iloc[i]
                    except:
                        pass

                    def procDual():
                        pass
                    
                    bms=['A','B']

                 
                    if "TAR" in self.df['OBJECTTYPE'].iloc[i]:
                        print('Processing target')

                        if "DTA" in ycol:
                            rep=ycol.replace("D","")
                            
                            stmt=stmt+f"{ycol}='{np.nan}', {rep}='{np.nan}', "
            
                        elif ycol == "SLTA" :#or ycol=="ASLTA" or ycol=="BSLTA":
                            # recalculate pss
                            pc, corrTa, errCorrTa=cp.calc_pc(0, 0, 0, self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i], dct)
                            stmt=stmt+f"SLTA='{np.nan}', SLDTA='{np.nan}', OLPC='{pc}', COLTA='{corrTa}', COLDTA='{errCorrTa}', "
                                
                        elif ycol == "SRTA":
                            # recalculate pss
                            #print(self.df['NRTA'].iloc[i], self.df['NRDTA'].iloc[i], self.df['ORTA'].iloc[i], self.df['ORDTA'].iloc[i])
                            pc, corrTa, errCorrTa=cp.calc_pc(0, 0, 0, self.df['NRTA'].iloc[i], self.df['NRDTA'].iloc[i], self.df['ORTA'].iloc[i], self.df['ORDTA'].iloc[i], dct)
                            stmt=stmt+f"SRTA='{np.nan}', SRDTA='{np.nan}', ORPC='{pc}', CORTA='{corrTa}', CORDTA='{errCorrTa}', "

                        elif ycol == "NLTA":
                            # recalculate pss
                            #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                            pc, corrTa, errCorrTa=cp.calc_pc(0,  self.df['SLTA'].iloc[i], self.df['SLDTA'].iloc[i],0,0, self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i], dct)
                            stmt=stmt+f"NLTA='{np.nan}', NLDTA='{np.nan}', OLPC='{pc}', COLTA='{corrTa}', COLDTA='{errCorrTa}', "
                        
                        elif ycol == "NRTA":
                            # recalculate pss
                            #print(self.df['NRTA'].iloc[i], self.df['NRDTA'].iloc[i], self.df['ORTA'].iloc[i], self.df['ORDTA'].iloc[i])
                            pc, corrTa, errCorrTa=cp.calc_pc(0, self.df['SRTA'].iloc[i], self.df['SRDTA'].iloc[i], 0, 0, self.df['ORTA'].iloc[i], self.df['ORDTA'].iloc[i], dct)
                            stmt=stmt+f"NRTA='{np.nan}', NRDTA='{np.nan}', ORPC='{pc}', CORTA='{corrTa}', CORDTA='{errCorrTa}', "

                        elif ycol == "OLTA":
                            # recalculate pss
                            frq=self.df['CENTFREQ'].iloc[i]
                            if int(frq)==2280:
                                stmt=stmt+f"{ycol}='{np.nan}', OLDTA='{np.nan}', "#TSYS1='{np.nan}', "
                            else:
                                stmt=stmt+f"{ycol}='{np.nan}', OLDTA='{np.nan}', COLDTA='{np.nan}', COLDTA='{np.nan}', SLTA='{np.nan}', SLDTA='{np.nan}', NLTA='{np.nan}', NLDTA='{np.nan}', "

                        elif ycol == "ORTA" or "RRMS" in ycol:
                            # recalculate pss
                            frq=self.df['CENTFREQ'].iloc[i]
                            if int(frq)==2280:
                                if ycol == "ORTA":
                                    stmt=stmt+f"{ycol}='{np.nan}', ORDTA='{np.nan}', "#TSYS2='{np.nan}', "
                                else:
                                    stmt=stmt+f"{ycol}='{np.nan}', ORTA='{np.nan}', ORDTA='{np.nan}', "
                            else:
                                stmt=stmt+f"{ycol}='{np.nan}', ORTA='{np.nan}', SRTA='{np.nan}', SRDTA='{np.nan}', NRTA='{np.nan}', NRDTA='{np.nan}', ORPC='{np.nan}', CORTA='{np.nan}', CORDTA='{np.nan}', "
                
                        else:
                            stmt=stmt+f"{ycol}='{np.nan}', "
                    else:

                        # print('here')
                        # sys.exit()
                        if ycol == "SLTA" or ycol=="SLS2N" or ycol=="ASLTA" or ycol=="BSLTA":
                            # recalculate pss
                            # k1="S"
                            pol="L"
                            #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                            if ycol[0]=="A":
                                k=0
                            elif ycol[0]=="B":
                                k=1
                            else:
                                k=""

                            if k=="":
                                try:
                                    pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0, 0, 0, self.df[f'N{pol}TA'].iloc[i], self.df[f'N{pol}DTA'].iloc[i], self.df[f'O{pol}TA'].iloc[i], self.df[f'O{pol}DTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                                    stmt=stmt+f"S{pol}TA='{np.nan}', S{pol}DTA='{np.nan}', S{pol}S2N='{np.nan}', O{pol}PSS='{pss}', O{pol}DPSS='{errPss}', O{pol}PC='{pc}', CO{pol}TA='{corrTa}', CO{pol}DTA='{errCorrTa}', O{pol}APPEFF='{appEff}', "
                            
                                except:
                                    pc, corrTa, errCorrTa=cp.calc_pc(0, 0, 0, self.df[f'N{pol}TA'].iloc[i], self.df[f'N{pol}DTA'].iloc[i], self.df[f'O{pol}TA'].iloc[i], self.df[f'O{pol}DTA'].iloc[i], dct)
                                    stmt=stmt+f"S{pol}TA='{np.nan}', S{pol}DTA='{np.nan}', S{pol}S2N='{np.nan}', O{pol}PC='{pc}', CO{pol}TA='{corrTa}', CO{pol}DTA='{errCorrTa} ', "
                            else:  
                                try:
                                        pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0, 0, 0, self.df[f'{bms[k]}N{pol}TA'].iloc[i], self.df[f'{bms[k]}N{pol}DTA'].iloc[i], self.df[f'{bms[k]}O{pol}TA'].iloc[i], self.df[f'{bms[k]}O{pol}DTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                                        stmt=stmt+f"{bms[k]}S{pol}TA='{np.nan}', {bms[k]}S{pol}DTA='{np.nan}', {bms[k]}S{pol}S2N='{np.nan}', {bms[k]}O{pol}PSS='{pss}', {bms[k]}O{pol}DPSS='{errPss}', {bms[k]}O{pol}PC='{pc}', {bms[k]}CO{pol}TA='{corrTa}', {bms[k]}CO{pol}DTA='{errCorrTa}', {bms[k]}O{pol}APPEFF='{appEff}', "
                                
                                except:
                                        pc, corrTa, errCorrTa=cp.calc_pc(0, 0, 0, self.df[f'{bms[k]}N{pol}TA'].iloc[i], self.df[f'{bms[k]}N{pol}DTA'].iloc[i], self.df[f'{bms[k]}O{pol}TA'].iloc[i], self.df[f'{bms[k]}O{pol}TA'].iloc[i], dct)
                                        stmt=stmt+f"{bms[k]}S{pol}TA='{np.nan}', {bms[k]}S{pol}DTA='{np.nan}', {bms[k]}S{pol}S2N='{np.nan}', {bms[k]}O{pol}PC='{pc}', {bms[k]}CO{pol}TA='{corrTa}', {bms[k]}CO{pol}DTA='{errCorrTa} ', "

                            
                            
                        elif ycol == "SRTA" or ycol=="SRS2N" or ycol=="ASRTA" or ycol=="BSRTA":
                            # recalculate pss
                            
                            #print(self.df['NRTA'].iloc[i], self.df['NRDTA'].iloc[i], self.df['ORTA'].iloc[i], self.df['ORDTA'].iloc[i])
                            # pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0, 0, 0, self.df['NRTA'].iloc[i], self.df['NRDTA'].iloc[i], self.df['ORTA'].iloc[i], self.df['ORDTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                            # stmt=stmt+f"SRTA='{np.nan}', SRDTA='{np.nan}', SRS2N='{np.nan}', ORPSS='{pss}', ORDPSS='{errPss}', ORPC='{pc}', CORTA='{corrTa}', CORDTA='{errCorrTa}', ORAPPEFF='{appEff}', "

                            pol="R"
                            #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                            if ycol[0]=="A":
                                k=0
                            elif ycol[0]=="B":
                                k=1
                            else:
                                k=""

                            if k=="":
                                try:
                                    pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0, 0, 0, self.df[f'N{pol}TA'].iloc[i], self.df[f'N{pol}DTA'].iloc[i], self.df[f'O{pol}TA'].iloc[i], self.df[f'O{pol}DTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                                    stmt=stmt+f"S{pol}TA='{np.nan}', S{pol}DTA='{np.nan}', S{pol}S2N='{np.nan}', O{pol}PSS='{pss}', O{pol}DPSS='{errPss}', O{pol}PC='{pc}', CO{pol}TA='{corrTa}', CO{pol}DTA='{errCorrTa}', O{pol}APPEFF='{appEff}', "
                            
                                except:
                                    pc, corrTa, errCorrTa=cp.calc_pc(0, 0, 0, self.df[f'N{pol}TA'].iloc[i], self.df[f'N{pol}DTA'].iloc[i], self.df[f'O{pol}TA'].iloc[i], self.df[f'O{pol}DTA'].iloc[i], dct)
                                    stmt=stmt+f"S{pol}TA='{np.nan}', S{pol}DTA='{np.nan}', S{pol}S2N='{np.nan}', O{pol}PC='{pc}', CO{pol}TA='{corrTa}', CO{pol}DTA='{errCorrTa} ', "
                            else:  
                                try:
                                        pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0, 0, 0, self.df[f'{bms[k]}N{pol}TA'].iloc[i], self.df[f'{bms[k]}N{pol}DTA'].iloc[i], self.df[f'{bms[k]}O{pol}TA'].iloc[i], self.df[f'{bms[k]}O{pol}DTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                                        stmt=stmt+f"{bms[k]}S{pol}TA='{np.nan}', {bms[k]}S{pol}DTA='{np.nan}', {bms[k]}S{pol}S2N='{np.nan}', {bms[k]}O{pol}PSS='{pss}', {bms[k]}O{pol}DPSS='{errPss}', {bms[k]}O{pol}PC='{pc}', {bms[k]}CO{pol}TA='{corrTa}', {bms[k]}CO{pol}DTA='{errCorrTa}', {bms[k]}O{pol}APPEFF='{appEff}', "
                                
                                except:
                                        pc, corrTa, errCorrTa=cp.calc_pc(0, 0, 0, self.df[f'{bms[k]}N{pol}TA'].iloc[i], self.df[f'{bms[k]}N{pol}DTA'].iloc[i], self.df[f'{bms[k]}O{pol}TA'].iloc[i], self.df[f'{bms[k]}O{pol}TA'].iloc[i], dct)
                                        stmt=stmt+f"{bms[k]}S{pol}TA='{np.nan}', {bms[k]}S{pol}DTA='{np.nan}', {bms[k]}S{pol}S2N='{np.nan}', {bms[k]}O{pol}PC='{pc}', {bms[k]}CO{pol}TA='{corrTa}', {bms[k]}CO{pol}DTA='{errCorrTa} ', "

                            

                        elif ycol == "NLTA" or ycol == "NLS2N" or ycol=="ANLTA" or ycol=="BNLTA":
                            # recalculate pss
                            
                            #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                            # pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0,  self.df['SLTA'].iloc[i], self.df['SLDTA'].iloc[i],0,0, self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                            # stmt=stmt+f"NLTA='{np.nan}', NLDTA='{np.nan}', NLS2N='{np.nan}',OLPSS='{pss}', OLDPSS='{errPss}', OLPC='{pc}', COLTA='{corrTa}', COLDTA='{errCorrTa}', OLAPPEFF='{appEff}', "
                        
                            pol="L"
                            #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                            if ycol[0]=="A":
                                k=0
                            elif ycol[0]=="B":
                                k=1
                            else:
                                k=""

                            if k=="":
                                try:
                                    pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0, self.df[f'S{pol}TA'].iloc[i], self.df[f'S{pol}DTA'].iloc[i], 0, 0, self.df[f'O{pol}TA'].iloc[i], self.df[f'O{pol}DTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                                    stmt=stmt+f"N{pol}TA='{np.nan}', N{pol}DTA='{np.nan}', N{pol}S2N='{np.nan}', O{pol}PSS='{pss}', O{pol}DPSS='{errPss}', O{pol}PC='{pc}', CO{pol}TA='{corrTa}', CO{pol}DTA='{errCorrTa}', O{pol}APPEFF='{appEff}', "
                            
                                except:
                                    pc, corrTa, errCorrTa=cp.calc_pc(0, self.df[f'S{pol}TA'].iloc[i], self.df[f'S{pol}DTA'].iloc[i], 0, 0, self.df[f'O{pol}TA'].iloc[i], self.df[f'O{pol}DTA'].iloc[i], dct)
                                    stmt=stmt+f"N{pol}TA='{np.nan}', N{pol}DTA='{np.nan}', N{pol}S2N='{np.nan}', O{pol}PC='{pc}', CO{pol}TA='{corrTa}', CO{pol}DTA='{errCorrTa} ', "
                            else:  
                                try:
                                        pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0, self.df[f'{bms[k]}S{pol}TA'].iloc[i], self.df[f'{bms[k]}S{pol}DTA'].iloc[i],0, 0, self.df[f'{bms[k]}O{pol}TA'].iloc[i], self.df[f'{bms[k]}O{pol}DTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                                        stmt=stmt+f"{bms[k]}N{pol}TA='{np.nan}', {bms[k]}N{pol}DTA='{np.nan}', {bms[k]}N{pol}S2N='{np.nan}', {bms[k]}O{pol}PSS='{pss}', {bms[k]}O{pol}DPSS='{errPss}', {bms[k]}O{pol}PC='{pc}', {bms[k]}CO{pol}TA='{corrTa}', {bms[k]}CO{pol}DTA='{errCorrTa}', {bms[k]}O{pol}APPEFF='{appEff}', "
                                
                                except:
                                        pc, corrTa, errCorrTa=cp.calc_pc(0,self.df[f'{bms[k]}S{pol}TA'].iloc[i], self.df[f'{bms[k]}S{pol}DTA'].iloc[i],0, 0,self.df[f'{bms[k]}O{pol}TA'].iloc[i], self.df[f'{bms[k]}O{pol}TA'].iloc[i], dct)
                                        stmt=stmt+f"{bms[k]}N{pol}TA='{np.nan}', {bms[k]}N{pol}DTA='{np.nan}', {bms[k]}N{pol}S2N='{np.nan}', {bms[k]}O{pol}PC='{pc}', {bms[k]}CO{pol}TA='{corrTa}', {bms[k]}CO{pol}DTA='{errCorrTa} ', "


                        elif ycol == "NRTA" or ycol=="NRS2N" or ycol=="ANRTA" or ycol=="BNRTA":
                            # recalculate pss
                            
                            #print(self.df['NRTA'].iloc[i], self.df['NRDTA'].iloc[i], self.df['ORTA'].iloc[i], self.df['ORDTA'].iloc[i])
                            # pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0, self.df['SRTA'].iloc[i], self.df['SRDTA'].iloc[i], 0, 0, self.df['ORTA'].iloc[i], self.df['ORDTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                            # stmt=stmt+f"NRTA='{np.nan}', NRDTA='{np.nan}', NRS2N='{np.nan}', ORPSS='{pss}', ORDPSS='{errPss}', ORPC='{pc}', CORTA='{corrTa}', CORDTA='{errCorrTa}', ORAPPEFF='{appEff}', "

                            pol="R"
                            #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                            if ycol[0]=="A":
                                k=0
                            elif ycol[0]=="B":
                                k=1
                            else:
                                k=""

                            if k=="":
                                try:
                                    pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0, self.df[f'S{pol}TA'].iloc[i], self.df[f'S{pol}DTA'].iloc[i], 0, 0, self.df[f'O{pol}TA'].iloc[i], self.df[f'O{pol}DTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                                    stmt=stmt+f"N{pol}TA='{np.nan}', N{pol}DTA='{np.nan}', N{pol}S2N='{np.nan}', O{pol}PSS='{pss}', O{pol}DPSS='{errPss}', O{pol}PC='{pc}', CO{pol}TA='{corrTa}', CO{pol}DTA='{errCorrTa}', O{pol}APPEFF='{appEff}', "
                            
                                except:
                                    pc, corrTa, errCorrTa=cp.calc_pc(0, self.df[f'S{pol}TA'].iloc[i], self.df[f'S{pol}DTA'].iloc[i], 0, 0, self.df[f'O{pol}TA'].iloc[i], self.df[f'O{pol}DTA'].iloc[i], dct)
                                    stmt=stmt+f"N{pol}TA='{np.nan}', N{pol}DTA='{np.nan}', N{pol}S2N='{np.nan}', O{pol}PC='{pc}', CO{pol}TA='{corrTa}', CO{pol}DTA='{errCorrTa} ', "
                            else:  
                                try:
                                        pss, errPss, pc, corrTa, errCorrTa, appEff=cp.calc_pc_pss(0, self.df[f'{bms[k]}S{pol}TA'].iloc[i], self.df[f'{bms[k]}S{pol}DTA'].iloc[i],0, 0, self.df[f'{bms[k]}O{pol}TA'].iloc[i], self.df[f'{bms[k]}O{pol}DTA'].iloc[i], self.df['FLUX'].iloc[i],dct)
                                        stmt=stmt+f"{bms[k]}N{pol}TA='{np.nan}', {bms[k]}N{pol}DTA='{np.nan}', {bms[k]}N{pol}S2N='{np.nan}', {bms[k]}O{pol}PSS='{pss}', {bms[k]}O{pol}DPSS='{errPss}', {bms[k]}O{pol}PC='{pc}', {bms[k]}CO{pol}TA='{corrTa}', {bms[k]}CO{pol}DTA='{errCorrTa}', {bms[k]}O{pol}APPEFF='{appEff}', "
                                
                                except:
                                        pc, corrTa, errCorrTa=cp.calc_pc(0,self.df[f'{bms[k]}S{pol}TA'].iloc[i], self.df[f'{bms[k]}S{pol}DTA'].iloc[i],0, 0,self.df[f'{bms[k]}O{pol}TA'].iloc[i], self.df[f'{bms[k]}O{pol}TA'].iloc[i], dct)
                                        stmt=stmt+f"{bms[k]}N{pol}TA='{np.nan}', {bms[k]}N{pol}DTA='{np.nan}', {bms[k]}N{pol}S2N='{np.nan}', {bms[k]}O{pol}PC='{pc}', {bms[k]}CO{pol}TA='{corrTa}', {bms[k]}CO{pol}DTA='{errCorrTa} ', "


                        elif ycol == "OLTA" or ycol=="OLS2N" or ycol == "AOLTA" or ycol == "BOLTA":
                            # # recalculate pss
                            # frq=self.df['CENTFREQ'].iloc[i]
                            # if int(frq)==2280:
                            #     stmt=stmt+f"{ycol}='{np.nan}', OLDTA='{np.nan}', "#TSYS1='{np.nan}', "
                            # else:
                            #     #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                            
                            #     stmt=stmt+f"{ycol}='{np.nan}', OLDTA='{np.nan}', OLS2N='{np.nan}', SLTA='{np.nan}', SLDTA='{np.nan}',  SLS2N='{np.nan}',NLTA='{np.nan}', NLDTA='{np.nan}',  NLS2N='{np.nan}',OLPSS='{np.nan}', OLDPSS='{np.nan}', OLPC='{np.nan}', COLTA='{np.nan}', COLDTA='{np.nan}', OLAPPEFF='{np.nan}', "
                            
                            pol="L"
                            #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                            if ycol[0]=="A":
                                k=0
                            elif ycol[0]=="B":
                                k=1
                            else:
                                k=""

                            if k=="":
                                frq=self.df['CENTFREQ'].iloc[i]
                                if int(frq)==2280:
                                    stmt=stmt+f"{ycol}='{np.nan}', O{pol}DTA='{np.nan}', "#TSYS1='{np.nan}', "
                                else:
                                    #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                                
                                    stmt=stmt+f"{ycol}='{np.nan}', O{pol}DTA='{np.nan}', O{pol}S2N='{np.nan}', S{pol}TA='{np.nan}', S{pol}DTA='{np.nan}',  S{pol}S2N='{np.nan}',N{pol}TA='{np.nan}', N{pol}DTA='{np.nan}',  N{pol}S2N='{np.nan}',O{pol}PSS='{np.nan}', O{pol}DPSS='{np.nan}', O{pol}PC='{np.nan}', CO{pol}TA='{np.nan}', CO{pol}DTA='{np.nan}', O{pol}APPEFF='{np.nan}', "
                                
                            else:  
                                try:
                                    stmt=stmt+f"{bms[k]}N{pol}TA='{np.nan}', {bms[k]}N{pol}DTA='{np.nan}', {bms[k]}N{pol}S2N='{np.nan}', {bms[k]}S{pol}TA='{np.nan}', {bms[k]}S{pol}DTA='{np.nan}', {bms[k]}S{pol}S2N='{np.nan}',{bms[k]}O{pol}TA='{np.nan}', {bms[k]}O{pol}DTA='{np.nan}', {bms[k]}O{pol}S2N='{np.nan}',{bms[k]}O{pol}PSS='{np.nan}', {bms[k]}O{pol}DPSS='{np.nan}', {bms[k]}O{pol}PC='{np.nan}', {bms[k]}CO{pol}TA='{np.nan}', {bms[k]}CO{pol}DTA='{np.nan}', {bms[k]}O{pol}APPEFF='{np.nan}', "
                                except:
                                    stmt=stmt+f"{bms[k]}N{pol}TA='{np.nan}', {bms[k]}N{pol}DTA='{np.nan}', {bms[k]}N{pol}S2N='{np.nan}', {bms[k]}S{pol}TA='{np.nan}', {bms[k]}S{pol}DTA='{np.nan}', {bms[k]}S{pol}S2N='{np.nan}',{bms[k]}O{pol}TA='{np.nan}', {bms[k]}O{pol}DTA='{np.nan}', {bms[k]}O{pol}S2N='{np.nan}', {bms[k]}O{pol}PC='{np.nan}', {bms[k]}CO{pol}TA='{np.nan}', {bms[k]}CO{pol}DTA='{np.nan}', "
                                
                             
                        # elif ycol == "OLTA" or "LRMS" in ycol:
                        #     # recalculate pss
                        #     frq=self.df['CENTFREQ'].iloc[i]
                        #     if int(frq)==2280:
                        #         stmt=stmt+f"{ycol}='{np.nan}', OLDTA='{np.nan}', TSYS1='{np.nan}', "
                        #     else:
                        #         #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                        #         try:
                        #             stmt=stmt+f"{ycol}='{np.nan}', OLDTA='{np.nan}', SLTA='{np.nan}', SLDTA='{np.nan}', NLTA='{np.nan}', NLDTA='{np.nan}', OLPSS='{np.nan}', OLDPSS='{np.nan}', OLPC='{np.nan}', COLTA='{np.nan}', COLDTA='{np.nan}', OLAPPEFF='{np.nan}', "
                        #         except:
                        #             stmt=stmt+f"ASLTA='{np.nan}', ASLDTA='{np.nan}', ANLTA='{np.nan}', ANLDTA='{np.nan}', AOLTA='{np.nan}', AOLDTA='{np.nan}', AOLPSS='{np.nan}', AOLDPSS='{np.nan}', AOLPC='{np.nan}', ACOLTA='{np.nan}', ACOLDTA='{np.nan}', \
                        #                         BSLTA='{np.nan}', BSLDTA='{np.nan}', BNLTA='{np.nan}', BNLDTA='{np.nan}', BOLTA='{np.nan}', BOLDTA='{np.nan}', BOLPSS='{np.nan}', BOLDPSS='{np.nan}', BOLPC='{np.nan}', BCOLTA='{np.nan}', BCOLDTA='{np.nan}', "
                                

                        elif ycol == "ORTA" or "RRMS" in ycol or ycol=="ORS2N" or ycol == "AORTA" or ycol == "BORTA":
                            # recalculate pss
                            frq=self.df['CENTFREQ'].iloc[i]
                            # if int(frq)==2280:
                            #     stmt=stmt+f"{ycol}='{np.nan}', ORDTA='{np.nan}', ORS2N='{np.nan}', "#TSYS2='{np.nan}', "
                            # else:
                            #     #print(self.df['NRTA'].iloc[i], self.df['NRDTA'].iloc[i], self.df['ORTA'].iloc[i], self.df['ORDTA'].iloc[i])
                            #     # try:
                            #     stmt=stmt+f"SRTA='{np.nan}', SRDTA='{np.nan}', SRS2N='{np.nan}', NRTA='{np.nan}', NRDTA='{np.nan}', NRS2N='{np.nan}', ORPSS='{np.nan}', ORDPSS='{np.nan}', ORS2N='{np.nan}', ORPC='{np.nan}', CORTA='{np.nan}', CORDTA='{np.nan}', ORAPPEFF='{np.nan}', "
                            #     # except:
                            #     #     stmt=stmt+f"ASRTA='{np.nan}', ASRDTA='{np.nan}', ANRTA='{np.nan}', ANRDTA='{np.nan}', AORTA='{np.nan}', AORDTA='{np.nan}', AORPSS='{np.nan}', AORDPSS='{np.nan}', AORPC='{np.nan}', ACORTA='{np.nan}', ACORDTA='{np.nan}', \
                            #     #                 BSRTA='{np.nan}', BSRDTA='{np.nan}', BNRTA='{np.nan}', BNRDTA='{np.nan}', BORTA='{np.nan}', BORDTA='{np.nan}', BORPSS='{np.nan}', BORDPSS='{np.nan}', BORPC='{np.nan}', BCORTA='{np.nan}', BCORDTA='{np.nan}', "
                                
                            pol="R"
                            #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                            if ycol[0]=="A":
                                k=0
                            elif ycol[0]=="B":
                                k=1
                            else:
                                k=""

                            if k=="":
                                frq=self.df['CENTFREQ'].iloc[i]
                                if int(frq)==2280:
                                    stmt=stmt+f"{ycol}='{np.nan}', O{pol}DTA='{np.nan}', "#TSYS1='{np.nan}', "
                                else:
                                    #print(self.df['NLTA'].iloc[i], self.df['NLDTA'].iloc[i], self.df['OLTA'].iloc[i], self.df['OLDTA'].iloc[i])
                                
                                    stmt=stmt+f"{ycol}='{np.nan}', O{pol}DTA='{np.nan}', O{pol}S2N='{np.nan}', S{pol}TA='{np.nan}', S{pol}DTA='{np.nan}',  S{pol}S2N='{np.nan}',N{pol}TA='{np.nan}', N{pol}DTA='{np.nan}',  N{pol}S2N='{np.nan}',O{pol}PSS='{np.nan}', O{pol}DPSS='{np.nan}', O{pol}PC='{np.nan}', CO{pol}TA='{np.nan}', CO{pol}DTA='{np.nan}', O{pol}APPEFF='{np.nan}', "
                                
                            else:  
                                try:
                                    stmt=stmt+f"{bms[k]}N{pol}TA='{np.nan}', {bms[k]}N{pol}DTA='{np.nan}', {bms[k]}N{pol}S2N='{np.nan}', {bms[k]}S{pol}TA='{np.nan}', {bms[k]}S{pol}DTA='{np.nan}', {bms[k]}S{pol}S2N='{np.nan}',{bms[k]}O{pol}TA='{np.nan}', {bms[k]}O{pol}DTA='{np.nan}', {bms[k]}O{pol}S2N='{np.nan}',{bms[k]}O{pol}PSS='{np.nan}', {bms[k]}O{pol}DPSS='{np.nan}', {bms[k]}O{pol}PC='{np.nan}', {bms[k]}CO{pol}TA='{np.nan}', {bms[k]}CO{pol}DTA='{np.nan}', {bms[k]}O{pol}APPEFF='{np.nan}', "
                                except:
                                    stmt=stmt+f"{bms[k]}N{pol}TA='{np.nan}', {bms[k]}N{pol}DTA='{np.nan}', {bms[k]}N{pol}S2N='{np.nan}', {bms[k]}S{pol}TA='{np.nan}', {bms[k]}S{pol}DTA='{np.nan}', {bms[k]}S{pol}S2N='{np.nan}',{bms[k]}O{pol}TA='{np.nan}', {bms[k]}O{pol}DTA='{np.nan}', {bms[k]}O{pol}S2N='{np.nan}', {bms[k]}O{pol}PC='{np.nan}', {bms[k]}CO{pol}TA='{np.nan}', {bms[k]}CO{pol}DTA='{np.nan}', "
                                

                        else:
                            stmt=stmt+f"{ycol}='{np.nan}', "

                    stmt=stmt[:-3]+f"'  WHERE FILENAME = '{FN}' ;"
                    print(stmt)   

                    db.c.execute(stmt)
                    db.commit_changes()
                    db.close_db()
                    # print("updated CALDB")
                    print(tablename,xcol,ycol)

                    print('After deleting: ',len(self.df))
                    print(self.df.iloc[i][yCol])
                    self.Canvas.clear_figure()
                    self.plot_cols_df()

    def update_db_all(self):
                    # update db on change

                    # check last selected points
                    fit_points= self.Canvas.fit_points
                    click_index = self.Canvas.click_index

                    print('\n',"+"*30)
                    print(f"\nDeleting \n-point: {fit_points} \n-at index {click_index}")
                    #self.deleted[click_index].append([click_index, fit_points])

                    print('\ndf length Before deleting: ',len(self.df))

                    xCol = self.Canvas.xlab
                    yCol = self.Canvas.ylab

                    print('\n','-'*30)
                    ii=int(click_index[0]) # point index to delete
                    # find what i is in the db
                    id=self.df['id'].iloc[ii]
                    #print(f'i: {ii}, id: {id}')
                    i=ii#d
                    FN=self.df['FILENAME'].iloc[i]

                    if 'TAR' in self.df['OBJECTTYPE'].iloc[i]:

                        t = Time(fit_points[0][0])
                        print(t)
                        # sys.exit()
                        #date=t
                        doy = t.strftime('%j')
                        #mjd=t.mjd

                        xp=self.df[xCol]
                        yp=self.df[yCol]

                        date_str=f'{str(fit_points[0][0])[:4]}d{str(doy)}'
                        

                        # for i in range(len(self.df)):
                            # if date_str in self.df['FILENAME'].iloc[i]:
                                #print(date_str, self.df['FILENAME'].iloc[i])

                        #if self.df[yCol].iloc[i]==float(fit_points[0][1]):
                        

                        print('Deleting: ')

                        

                        print('\n-date: ',date_str,'\n-file: ',FN)

                        print(f"\n-id: {self.df['id'].iloc[i]}, \n-index: {ii}")
                        # print('match: ', self.df['id'].iloc[i])#, self.df.iloc[i])
                        
                        #self.df.drop(id,inplace=True)
                        
                        print(f'\n> Setting {yCol}: {self.df.iloc[i][yCol]}, to np.nan')
                        #print(self.df.iloc[i][yCol])
                        try:
                            self.df.at[i,yCol]=np.nan
                        except ValueError:
                            self.df.at[i,yCol]=0.0
                            
                        #self.df=self.df[~(self.df['id']==id)]
                        #print(self.df.iloc[i][yCol])
                        print(f'\n+ New {yCol}: {self.df.iloc[i][yCol]}')
                        # change plot
                        tablename = self.time_ui.comboBoxTables.currentText()
                    
                        xcol=self.time_ui.comboBoxColsX.currentText()
                        ycol=self.time_ui.comboBoxColsY.currentText()

                        #self.dbFile
                        db = SQLiteDB(databaseName=self.dbFile, log=self.log)
                        db.create_db()

                        try:
                            srcType=self.df['OBJECTTYPE'].iloc[i]
                            self.write(f"Updating {self.dbFile} table: {tablename}, type: {srcType}",'info')
                            print('\n-BEAMTYPE: ',self.df['BEAMTYPE'][i],'\n-srcType: ',srcType)
                        except:
                            pass

                        # update the database
                        cols=list(self.df.columns)
                        stmt=f"UPDATE '{tablename}' SET "

                        
                        for col in cols:
                            if "FILENAME"  in col or "OBJECT" in col or "OBJECTTYPE" in col or "CURDATETIME" in col or "SOURCEDIR" in col or  "RADIOMETER" in col or "CENTFREQ" in col or "id" in col or "MJD" in col or "OBSDATE" in col:
                                pass
                            else:
                                stmt=stmt+f"{col}='{np.nan}', "
                    else:
                        t = Time(fit_points[0][0])
                        #date=t
                        doy = t.strftime('%j')
                        #mjd=t.mjd

                        xp=self.df[xCol]
                        yp=self.df[yCol]

                        date_str=f'{str(fit_points[0][0])[:4]}d{str(doy)}'
                        

                        # for i in range(len(self.df)):
                            # if date_str in self.df['FILENAME'].iloc[i]:
                                #print(date_str, self.df['FILENAME'].iloc[i])

                        #if self.df[yCol].iloc[i]==float(fit_points[0][1]):
                        ii=int(click_index[0]) # point index to delete

                        print('Deleting: ')

                        

                        print('\n-date: ',date_str,'\n-file: ',FN)

                        print(f"\n-id: {self.df['id'].iloc[i]}, \n-index: {ii}")
                        # print('match: ', self.df['id'].iloc[i])#, self.df.iloc[i])
                        
                        #self.df.drop(id,inplace=True)
                        
                        print(f'\n> Setting {yCol}: {self.df.iloc[i][yCol]}, to np.nan')
                        #print(self.df.iloc[i][yCol])
                        try:
                            self.df.at[i,yCol]=np.nan
                        except ValueError:
                            self.df.at[i,yCol]=0.0
                            
                        #self.df=self.df[~(self.df['id']==id)]
                        #print(self.df.iloc[i][yCol])
                        print(f'\n+ New {yCol}: {self.df.iloc[i][yCol]}')
                        # change plot
                        tablename = self.time_ui.comboBoxTables.currentText()
                    
                        xcol=self.time_ui.comboBoxColsX.currentText()
                        ycol=self.time_ui.comboBoxColsY.currentText()

                        #self.dbFile
                        db = SQLiteDB(databaseName=self.dbFile, log=self.log)
                        db.create_db()

                        try:
                            srcType=self.df['OBJECTTYPE'].iloc[i]
                            self.write(f"Updating {self.dbFile} table: {tablename}, type: {srcType}",'info')
                            print('\n-BEAMTYPE: ',self.df['BEAMTYPE'][i],'\n-srcType: ',srcType)
                        except:
                            pass

                        # update the database
                        cols=list(self.df.columns)
                        stmt=f"UPDATE '{tablename}' SET "

                        
                        for col in cols:
                            if "FILENAME"  in col or "OBJECT" in col or "OBJECTTYPE" in col or "CURDATETIME" in col or "SOURCEDIR" in col or  "RADIOMETER" in col or "CENTFREQ" in col or "id" in col or "MJD" in col or "OBSDATE" in col:
                                pass
                            else:
                                stmt=stmt+f"{col}='{np.nan}', "

                    stmt=stmt[:-3]+f"'  WHERE FILENAME = '{FN}' ;"
                    print(stmt)        
                 
                  

                    db.c.execute(stmt)
                    db.commit_changes()
                    db.close_db()
                    print("updated CALDB")
                    print(tablename,xcol,ycol)

                    print('After deleting: ',len(self.df))
                    print(self.df.iloc[i][yCol])
                    self.Canvas.clear_figure()
                    self.plot_cols_df()

    def on_fit_changed(self):
        """"""

        if self.time_ui.comboBoxFitTypes.currentText()=="Spline":
            self.time_ui.LblSplKnots.setVisible(True)
            self.time_ui.EdtSplKnots.setVisible(True)
            self.time_ui.EdtEndDate.setVisible(False)
            self.time_ui.EdtStartDate.setVisible(False)
            self.time_ui.LblEndDate.setVisible(False)
            self.time_ui.LblStartDate.setVisible(False)
        else:
            self.time_ui.LblSplKnots.setVisible(False)
            self.time_ui.EdtSplKnots.setVisible(False)
            self.time_ui.EdtEndDate.setVisible(True)
            self.time_ui.EdtEndDate.setEnabled(True)
            self.time_ui.EdtStartDate.setVisible(True)
            self.time_ui.EdtStartDate.setEnabled(True)
            self.time_ui.LblEndDate.setVisible(True)
            self.time_ui.LblStartDate.setVisible(True)

    def open_plots_window(self):
        """ Connect the plots window to the main window. """

        msg_wrapper("debug", self.log.debug, "Initiating plot viewer window")

        # Initiate viewer
        self.plot_window = QtWidgets.QMainWindow()
        self.plot_ui = Ui_PlotViewer()
        self.plot_ui.setupUi(self.plot_window)

        # fix all else
        self.plot_ui.btnDelete.setEnabled(False)
        self.plot_ui.btnRefreshPlotList.setEnabled(False)
        self.plot_ui.btnShow.setEnabled(False)
        self.plot_ui.comboBox.setEnabled(False)
        self.plot_ui.comboBoxFilter.setEnabled(False)
        self.plot_ui.comboBoxOptions.setEnabled(False)
        self.plot_ui.txtBoxEnd.setEnabled(False)
        self.plot_ui.txtBoxStart.setEnabled(False)

        # Enable open db only
        self.plot_ui.btnOpen.clicked.connect(self.open_db_path)

        # Setup index change options for combo boxes
        self.plot_ui.comboBox.currentIndexChanged.connect(self.on_combo_changed)
        # self.plot_ui.comboBoxOptions.currentIndexChanged.connect(
        #     self.on_options_changed)
        self.plot_ui.comboBoxFilter.currentIndexChanged.connect(self.on_filter_changed)
        
        # # Connect buttons to actions performed by user
        self.plot_ui.btnRefreshPlotList.clicked.connect(self.add_items_to_combobox)
        
        self.plot_ui.btnShow.clicked.connect(self.show_plot_browser)
        self.plot_ui.btnDelete.clicked.connect(self.delete_obs)
        # self.plot_ui.btnRefreshPlotList.clicked.connect(self.refresh_list)
        # self.plot_ui.btnRefreshPlotList.setVisible(False)

        # get names of all folders containing plots and place list in combobox
        # self.add_items_to_combobox()
        
        # # get info from db
        # self.get_info_from_db()

        # # check folder name against table name
        # plotFolderName=self.plot_ui.comboBox.currentText()
        # folderName=plotFolderName.lower().replace(".","_")
        # folderName=folderName.lower().replace("-","_")

        # if folderName in self.tables:
        #     print("\n",folderName, " found")
        #     target=folderName

        #     # get column names from db and put them in combobox
        #     self.colInd, self.colName, self.colType = self.tardb.get_all_table_coloumns(folderName)
        #     if len(self.colInd) != 0:
        #         #print(folderName)
        #         #print(self.colName)
        #         print('in tardb')
        #         #self.db="TARDB.db"
        #     else:
        #         self.colInd, self.colName, self.colType = self.caldb.get_all_table_coloumns(folderName)
        #         #print(folderName)
        #         #print(self.colName)
        #         print('in caldb')
        #         #self.db="CALDB.db"

        #     self.plot_ui.comboBoxOptions.clear()
        #     self.plot_ui.comboBoxFilter.clear()

        #     plotCols=[]
        #     for name in self.colName:
        #         if 'SOURCE' in name or 'CUR' in name or 'NOM' in name or 'TUDE' in name or 'BW' in name or 'FREQ' in name or 'FILE' in name or 'OBS' in name or 'OBJ' in name or 'id' == name or 'RAD' in name or 'TYPE' in name or 'PRO' in name or 'TELE' in name or 'UPGR' in name or 'INST' in name or 'SCAN' in name:
        #             pass
        #         else:
        #             plotCols.append(name)

        #         #print(plotCols)

        #     self.plot_ui.comboBoxFilter.addItems(['','>','>=','=','<','<=','between'])
        #     self.plot_ui.comboBoxOptions.addItems([""])
        #     self.plot_ui.comboBoxOptions.addItems(plotCols)

        #     # show comboboxes
        #     self.plot_ui.comboBoxFilter.setVisible(True)
            
        # else:
        #     print("dne")

        # #sys.exit()
        # self.toggle_range_filter('off')

        self.plot_window.show()

    def on_combo_changed(self):

        print("\nChanged obs. to: ", self.plot_ui.comboBox.currentText())

        # get data from db
        # check folder name against table name
        folderName=self.plot_ui.comboBox.currentText()

        # get column names from db and put them in combobox
        colInd, colNames, colType = self.db.get_all_table_coloumns(folderName)

        plotCols=[]
        for name in colNames:
            #or 'OBS' in name 
            if 'OBSTIME' in name or 'SOURCE' in name or 'CUR' in name or 'NOM' in name or 'TUDE' in name or 'BW' in name or 'FREQ' in name or 'FILE' in name or 'OBJ' in name or 'id' == name or 'RAD' in name or 'TYPE' in name or 'PRO' in name or 'TELE' in name or 'UPGR' in name or 'INST' in name or 'SCAN' in name:
                pass
            else:
                plotCols.append(name)

        self.plot_ui.comboBoxOptions.clear()
        self.plot_ui.comboBoxOptions.clear()
        self.plot_ui.comboBoxOptions.addItems(plotCols)

        self.plot_ui.comboBoxFilter.clear()
        self.plot_ui.comboBoxFilter.clear()
        self.plot_ui.comboBoxFilter.addItems(['','>','>=','=','<','<=','between'])

    def refresh_list(self):
        """Refresh list if database updated"""
        pass
    
    def on_options_changed(self):

        if self.plot_ui.comboBoxOptions.currentText()=="":
            print("\nOptions is empty")
            print('Filter: ', self.plot_ui.comboBoxOptions.currentText())
            self.plot_ui.txtBoxFilter.setText('')
            print('Text: ', self.plot_ui.txtBoxFilter.text())
            print("\n--- Showing all plots in folder\n")
        else:
            #print(self.plot_ui.comboBox.currentText())
            self.enable_btns()
            print("\nOptions selected")
            print('Option: ', self.plot_ui.comboBoxOptions.currentText())
            print('Filter: ', self.plot_ui.comboBoxFilter.currentText())
            self.plot_ui.txtBoxFilter.setText('')
            print('Text: ', self.plot_ui.txtBoxFilter.text())
            print("\n--- Showing all plots in folder\n")
            
    def on_filter_changed(self):
        if self.plot_ui.comboBoxFilter.currentText()=="between":
            print(self.plot_ui.comboBoxFilter.currentText())
            #Add second filter
            self.toggle_range_filter('on')
            self.plot_ui.txtBoxFilter.setVisible(False)
        else:
            print(self.plot_ui.comboBoxFilter.currentText())
            # remove second filter
            self.toggle_range_filter('off')
            self.plot_ui.txtBoxFilter.setVisible(True)

    def toggle_range_filter(self,filter):
        
        if filter=='off':
            toggle=False
        elif filter=="on":
            toggle=True

        self.plot_ui.LblRangeFilter.setVisible(toggle)
        self.plot_ui.LblStart.setVisible(toggle)
        self.plot_ui.LblStop.setVisible(toggle)
        self.plot_ui.LblFormat.setVisible(toggle)
        self.plot_ui.txtBoxEnd.setVisible(toggle)
        self.plot_ui.txtBoxStart.setVisible(toggle)

    def get_info_from_db(self):
        # read from database

        caldb='CALDB.db'
        tardb='TARDB.db'

        # check if db's exist
        print("Opening dbs: ",)
        pathToCalDB=os.path.abspath(caldb)
        pathToTarDB=os.path.abspath(tardb)
        foundCALDB=False
        foundTARDB=False

        #print(os.path.isfile(pathToCalDB))
        if os.path.isfile(pathToCalDB) == True:
            print("Found CALDB in path")
            foundCALDB=True
        else:
            print("Couldn't find CALDB in path")

        if os.path.isfile(pathToTarDB) == True:
            print("Found TARDB in path")
            foundTARDB=True
        else:
            print("Couldn't find TARDB in path")

        if foundCALDB==True:
            # open db and get names
            # open the database and get tables
            self.caldb = SQLiteDB(databaseName=caldb, log=self.log)
            self.caldb.create_db()

            # populate columns
            #self.get_table_list() or
            self.calTables = sorted(self.caldb.get_table_names(caldb))
            #print(self.calTables )
            # curTxt = self.time_ui.comboBoxTables.currentText()
            # if curTxt  not in self.tables:
            #     # force combobox to accept new items, need to investigate this issue further
            #     self.time_ui.comboBoxTables.clear()
            #     self.time_ui.comboBoxTables.clear()
            #     self.time_ui.comboBoxTables.addItems(self.tables)
            #     #self.time_ui.comboBoxTables.addItems(self.tables)     
            #     #self.time_ui.comboBoxTables.addItems(self.tables)
            # else:
            #     pass


            #self.populate_cols()

        if foundTARDB==True:
            # open db and get names
            # open the database and get tables
            self.tardb = SQLiteDB(databaseName=tardb, log=self.log)
            self.tardb.create_db()

            # populate columns
            #self.get_table_list() or
            self.tarTables = sorted(self.tardb.get_table_names(tardb))
            #print(self.tarTables )

        self.tables=(self.tarTables + self.calTables)

    # == Widget connections
    def connect_buttons(self):
        """ Connect button key presses to widgets. """

        msg_wrapper("debug", self.log.debug,"Connecting buttons to main canvas")

        # Plot parameters buttons
        self.drift_ui.BtnFilterData.clicked.connect(self.filter_data)
        self.drift_ui.BtnViewFit.clicked.connect(self.view_fit)

        # PSS values buttons
        self.drift_ui.BtnCalc.setEnabled(False)
        self.drift_ui.BtnCalc.setText("Calc PSS/Flux")
        self.drift_ui.BtnCalc.clicked.connect(self.calc)
        self.drift_ui.BtnPopulatePSS.clicked.connect(self.populate_pss_from_file)

        # beam fitting buttons
        self.drift_ui.BtnFitData.clicked.connect(self.fit_data)
        self.drift_ui.BtnClearSelection.clicked.connect(self.clear_selection)
        self.drift_ui.BtnSave.clicked.connect(self.save_fit)

        # Current plot selection
        self.drift_ui.BtnChoosePlot.clicked.connect(self.choose_plot)
        self.drift_ui.BtnOpenFile.clicked.connect(self.open_file)
        self.drift_ui.BtnResetPlot.clicked.connect(self.reset_plot)
        self.popup_msg_dict()
        self.drift_ui.BtnSaveToDb.clicked.connect(self.save_to_DB)

        # Current fit status buttons
        self.drift_ui.BtnResetStatus.clicked.connect(self.reset_status)
        self.drift_ui.BtnViewStatus.clicked.connect(self.view_status)

    def connect_time_buttons(self):
        """ connect button key press to widgets. """

        msg_wrapper("debug", self.log.debug,"Connecting buttons to main canvas")

        self.time_ui.BtnPlot.clicked.connect(self.plot_cols)
        self.time_ui.BtnFilter.clicked.connect(self.filter_timeseries_data)
        self.time_ui.BtnFit.clicked.connect(self.fit_timeseries)
        self.time_ui.BtnDelPoint.clicked.connect(self.update_point)#point)
        self.time_ui.BtnDelBoth.clicked.connect(self.update_db_all)#point)
        # self.time_ui.BtnResetPoints.clicked.connect()
        # self.time_ui.BtnSavePlot.clicked.connect()
        # self.time_ui.BtnQuit.clicked.connect()
        self.time_ui.BtnQuit.clicked.connect(self.update_db)
        self.time_ui.BtnReset.clicked.connect(self.reset_timeseries)
        #self.time_ui.BtnOpenDB.clicked.connect(self.open_db)
        self.time_ui.BtnRefreshDB.clicked.connect(self.refresh_db)
        # self.time_ui.BtnUpdateDB.clicked.connect()
        self.time_ui.BtnSaveDB.clicked.connect(self.save_time_db)
        #self.time_ui.BtnFit.clicked.connect(self.fit_timeseries)

    def delete_point(self):
        """ Delet point on canvas plot."""

        # check last selected points
        fit_points= self.Canvas.fit_points
        click_index = self.Canvas.click_index

        print(f"Deleting point: {fit_points} at index {click_index}")
        #self.deleted[click_index].append([click_index, fit_points])

        print('Before deleting: ',len(self.df))

        xCol = self.Canvas.xlab
        yCol = self.Canvas.ylab

        print('\n','-'*30)
        #print(fit_points)
        print(str(fit_points[0][0])[:10], fit_points[0][1])
        print(self.df.iloc[click_index[0]]['FILENAME'])


        #print(str(self.df.iloc[click_index[0]][xCol])[:10])
        #print(self.df.iloc[click_index[0]][yCol])

        t=Time(fit_points[0][0])
        #date=t
        doy= t.strftime('%j')
        #mjd=t.mjd

        xp=self.df[xCol]
        yp=self.df[yCol]

        date_str=f'{str(fit_points[0][0])[:4]}d{str(doy)}'
        #print(date_str)
        for i in range(len(self.df)):
            if date_str in self.df['FILENAME'].iloc[i]:
                #print(date_str, self.df['FILENAME'].iloc[i])

                if self.df[yCol].iloc[i]==float(fit_points[0][1]):
                    print('Deleting: ')
                    FN=self.df['FILENAME'].iloc[i]
                    print(f"id: {self.df['id'].iloc[i]}, filename: {FN}")
                    # print('match: ', self.df['id'].iloc[i])#, self.df.iloc[i])
                    id=self.df['id'].iloc[i]
                    #self.df.drop(id,inplace=True)
                    
                    self.df.at[id,yCol]=np.nan
                    self.df=self.df[~(self.df['id']==id)]

                    # update the database


                    # change plot
                    

                    #print(self.df['id'].iloc[i])
                    #print(list(self.df['id']))
                    #print(len(self.df))
                    break
                    # delete row
        print('\n')
        # sys.exit()
        

        #print(self.df[self.df['FILENAME']==FN])
        # pl.plot(xp,yp,'.')
        # pl.plot(self.df[xCol],self.df[yCol],'.')
        # pl.show()
        # pl.close()
        # sys.exit()
        # if (str(fit_points[0][0])[:10] == str(self.df.iloc[click_index[0]][xCol])[:10]) and (float(fit_points[0][1])==float(self.df.iloc[click_index[0]][yCol])):
        #     cond = (self.df[xCol]==str(fit_points[0][0])[:10]) & (self.df[yCol]==float(fit_points[0][1]))
        #     # cond
        #     print(cond)
        #     sys.exit()
        #     self.df.drop(cond.index,inplace=True)
        # # try:
        # #     self.df.drop(click_index[0],inplace=True)
        # # except:
        # #     print('Item already deleted from data')
        # else:
        #     print('Cant delete')

        #print('After deleting: ',len(self.df))

        self.Canvas.clear_figure()
        self.plot_cols_df()

    def refresh_db(self):
        """refresh the database entries. Check for updates."""
        
        # open the database and get tables
        self.db = SQLiteDB(databaseName=self.dbFile, log=self.log)
        self.db.create_db()

        # populate columns
        self.get_table_list()
        self.populate_cols()

        # update plot
        self.plot_cols()
        #self.db.close_db()

    def save_time_db(self,filen=""):
        """Save the analysis results to a csv file"""
        self.df.to_csv("Analysis_results.csv")
        if filen:
            self.df.to_csv(f"Analysis_of_table_{filen}.csv")
            # save db as well
            # import sqlite3
            # dbname=f'{filen}_db'
            # conn=sqlite3.connect(f'{self.dbFile}')
            # self.df.to_csv(f'{dbname}.csv',index=False)
            # self.df.to_sql(f'{dbname}',conn,if_exists='replace',index=False)
            # conn.commit()
            # conn.close
            
        #self.df.to_sql("Analysis_results.db",con=engine, if_exists='replace',index=False)

        print('saved results to Analysis_results.csv')

    def reset_timeseries(self):
        self.df=self.orig_df

        # plot
        self.Canvas.clear_figure()

        self.plot_cols()
        
    def fit_timeseries(self):

        # get fit type and fit order
        fitType = self.time_ui.comboBoxFitTypes.currentText()
        fitOrder = self.time_ui.comboBoxOrder.currentText()

        print(f"Fitting: {fitType}, order: {fitOrder}")

        if fitOrder != "Order" and fitType!="Type":

            xCol=self.Canvas.xlab
            yCol=self.Canvas.ylab

            print("col: ",xCol)
            if xCol !="MJD":
                print('Require x-axis as MJD')
            else:
                x=np.array(self.Canvas.x).astype(float)
                y=np.array(self.Canvas.y).astype(float)
                
                if fitType == "Polynomial":
                    try:
                        tstart=int(self.time_ui.EdtStartDate.text())
                    except:
                        tstart="nodate"
                    try:
                        tend=int(self.time_ui.EdtEndDate.text())
                    except:
                        tend="nodate"

                    if tstart == "nodate" and tend=="nodate":
                        print(f'\nstart; {x[0]},  end: {x[-1]}')
                        xm,model,res,rma,coeffs=fit.calc_residual_and_rms_fit(x,y,int(fitOrder))
                        ind=(np.where(model==max(model))[0])[0]
                        # print(ind)
                        # sys.exit()
                        print("\n","*"*20)
                        print(f'tstart: {x[0]}, tend: {x[-1]}')
                        print(f'ymin:{min(y):.3f}, ymax: {max(y):.3f}')
                        print('> model')
                        print(f'ymin:{min(model):.3f}, ymax: {max(model):.3f}, x @ ymax: {xm[ind]}')
                        print(f'rms of fit: {rma:.3f}')
                        print('coeffs: ',coeffs)
                        print("*"*20,"\n")

                        self.Canvas.plot_dual_fig(x,y,xm,model,'data','model','Plot of data vs polynomial model')

                    elif tstart == "nodate" and tend!="nodate":
                        print(f'start; {x[0]},  end: {tend}')
                        
                        if tend < x[0]:
                            print(f"End date ({tend}) needs to be bigger than start date ({x[0]})")
                        else:
                            v=np.where(x <= tend)[0]
                            x1=x[v]
                            y1=y[v]
                            xm,model,res,rma,coeffs=fit.calc_residual_and_rms_fit(x1,y1,int(fitOrder))
                            ind=(np.where(model==max(model))[0])[0]
                            print("\n","*"*20)
                            print(f'tstart: {x[0]}, tend: {tend}')
                            print(f'ymin:{min(y):.3f}, ymax: {max(y):.3f}')
                            print('> model')
                            print(f'ymin:{min(model):.3f}, ymax: {max(model):.3f}, x @ ymax: {xm[ind]}')
                            print(f'rms of fit: {rma:.3f}')
                            print('coeffs: ',coeffs)
                            print("*"*20,"\n")

                            self.Canvas.plot_dual_fig(x,y,xm,model,'data','model','Plot of data vs polynomial model')

                    elif tstart != "nodate" and tend=="nodate":
                        print(f'start; {tstart},  end: {x[-1]}')

                        if tstart > x[-1]:
                            print(f"Start date ({tstart}) needs to be smaller than end date ({x[-1]})")
                        else:
                            v=np.where(x >= tstart)[0]
                            x1=x[v]
                            y1=y[v]
                            xm,model,res,rma,coeffs=fit.calc_residual_and_rms_fit(x1,y1,int(fitOrder))
                            ind=(np.where(model==max(model))[0])[0]

                            print("\n","*"*20)
                            print(f'tstart: {tstart}, tend: {x[-1]}')
                            print(f'ymin:{min(y):.3f}, ymax: {max(y):.3f}')
                            print('> model')
                            print(f'ymin:{min(model):.3f}, ymax: {max(model):.3f}, x @ ymax: {xm[ind]}')
                            print(f'rms of fit: {rma:.3f}')
                            print('coeffs: ',coeffs)
                            print("*"*20,"\n")
                            
                            self.Canvas.plot_dual_fig(x,y,xm,model,'data','model','Plot of data vs polynomial model')

                    elif tstart != "nodate" and tend!="nodate":
                        print(f'start; {tstart},  end: {tend}')

                        if tstart > tend:
                            print(f"Start date ({tstart}) needs to be smaller than end date ({tend})")
                        else:
                            v=np.where((x >= tstart)&(x <= tend))[0]
                            x1=x[v]
                            y1=y[v]
                            xm,model,res,rma,coeffs=fit.calc_residual_and_rms_fit(x1,y1,int(fitOrder))
                            ind=(np.where(model==max(model))[0])[0]

                            print("\n","*"*20)
                            print(f'tstart: {tstart}, tend: {tend}')
                            print(f'ymin:{min(y):.3f}, ymax: {max(y):.3f}')
                            print('> model')
                            print(f'ymin:{min(model):.3f}, ymax: {max(model):.3f}, x @ ymax: {xm[ind]}')
                            print(f'rms of fit: {rma:.3f}')
                            print('coeffs: ',coeffs)
                            print("*"*20,"\n")

                            #print('coeffs: ',coeffs)
                            self.Canvas.plot_dual_fig(x,y,xm,model,'data','model','Plot of data vs polynomial model')
                
                elif fitType == "Spline":
                    knots=int(self.time_ui.EdtSplKnots.text())

                    if knots<9:
                        knots=9
                    xm,model=fit.spline_fit(x, y, int(knots),int(fitOrder))
                    self.Canvas.plot_dual_fig(x,y,xm,model,'data','model','Plot of data vs spline model')
                    
        elif fitOrder == "Order" and fitType!="Type":
            print("\nNo fit order selected\n")
        elif fitOrder != "Order" and fitType=="Type":
            print("\nNo fit type selected\n")
        else:
            print("\nNo fit parameters selected\n")
            
    def filter_timeseries_data(self):
        """ Filter the data"""

        # get current text  from combobox and bins
        filterText = self.time_ui.comboBoxFilters.currentText()
        filterCut = self.time_ui.EdtFilter.text()

        if filterText=="Type":
            print(f'please select a filter type\n')
        else:

            if filterText == ">" or filterText == ">=":
            
                try:
                    cut=float(filterCut)
                except:
                    print(f'{filterCut} is an invalid entry for filter {filterText}')
                    cut=""
                
                if cut=="":
                    pass
                else:
                    print(f'filter everything {filterText} {filterCut}')

                    # get x and y
                    if len(self.Canvas.x) == 0:
                        print(self.Canvas.x,self.Canvas.y)
                        print('\nYou need to plot the data first\n')
                    else:
                        x=np.array(self.Canvas.x)
                        y=np.array(self.Canvas.y).astype(float)
                        xCol=self.Canvas.xlab
                        yCol=self.Canvas.ylab

                        print(self.df[['id','FILENAME','MJD']])

                        print(f'cut: {cut}')
                        if filterText == ">":
                            cuts=np.where(y>float(cut))[0]
                        else:# filterText == ">=":
                            cuts=np.where(y>=float(cut))[0]

                        if len(cuts)>0:
                            print(cuts)
                            #df_cuts=self.df[self.df[xCol]>]
                            self.df=self.df.drop(self.df.index[cuts])
                            #print(self.df)
                            self.deleted.append(cuts)
                            print(f'deleted: {self.deleted}')

                            # re-plot
                            self.Canvas.plot_fig(self.df[xCol], self.df[yCol], xCol, yCol, data=self.df,title=f"Plot of {self.df['SOURCEDIR']} obs. {self.df['FILENAME'][:8]}")

            elif filterText == "<" or filterText == "<=":
                try:
                    cut=float(filterCut)
                except:
                    print(f'{filterCut} is an invalid entry for filter {filterText}')
                    cut=""
                
                if cut=="":
                    pass
                else:
                    print(f'filter everything {filterText} {filterCut}')

                    # get x and y
                    if len(self.Canvas.x) == 0:
                        print(self.Canvas.x,self.Canvas.y)
                        print('\nYou need to plot the data first\n')
                    else:
                        x=np.array(self.Canvas.x)
                        y=np.array(self.Canvas.y).astype(float)
                        xCol=self.Canvas.xlab
                        yCol=self.Canvas.ylab

                        print(self.df[['id','FILENAME','MJD']])

                        print(f'cut: {cut}')
                        if filterText == "<":
                            cuts=np.where(y<float(cut))[0]
                        else:
                            cuts=np.where(y<=float(cut))[0]
                        if len(cuts)>0:
                            print(cuts)
                            #df_cuts=self.df[self.df[xCol]>]
                            self.df=self.df.drop(self.df.index[cuts])
                            print(self.df)
                            self.deleted.append(cuts)
                            print(f'deleted: {self.deleted}')

                            # re-plot
                            self.Canvas.plot_fig(self.df[xCol], self.df[yCol], xCol, yCol, data=self.df,title=f"Plot of {self.df['SOURCEDIR']} obs. {self.df['FILENAME'][:8]}")
                        else:
                            print(f"No values found for condition {filterText} {filterCut} ")

            elif filterText == "rms cuts":

                print("Performing rms cuts")
                # ================================================
                # Clean the data using rms cuts
                # ================================================

                # get df
                xCol=self.Canvas.xlab
                yCol=self.Canvas.ylab

                # need to run this once else it destroys data
                self.df[yCol]=self.df[yCol].replace('nan',0)
                self.df[yCol].fillna(0,inplace=True)

                x=list(self.df[xCol])#np.array(self.Canvas.x)
                y=list(self.df[yCol])#np.array(self.Canvas.y).astype(float)
                
                scanLen = len(x)
                if self.df["CENTFREQ"][int(len(self.df)/2)] <= 3000:
                    noTotScans = 2
                else:
                    noTotScans = 6

                # spline the data
                spl = fit.spline(x, y)

                pl.plot(x,y)
                pl.plot(x,spl)
                pl.show()
                sys.exit()

                if len(spl)==0:
                    pass
                else:
                    # print('spl: ',spl)
                    # print('y: ',y)
                    #sys.exit()
                    print(self.df['FILENAME'])

                    scanResBefore, scanRmsBefore = fit.calc_residual(spl, y)
                    finX, finY, scanRmsAfter, scanResAfter, finMaxSpl, finspl, pt, names = fit.clean_data_iterative_fitting(x, y, scanLen, scanResBefore, scanRmsBefore, self.log, x2=list(self.df["FILENAME"]))

                    self.write(f'RMS before: after -> {scanRmsBefore:.3f}: {scanRmsAfter:.3f}','info')

                    self.Canvas.clear_figure()  # Update figures

                    #self.df[xCol]=""
                    self.df[yCol]=np.nan

                    #for j in range(len(list(self.df["FILENAME"]))):
                    err=self.time_ui.comboBoxColsYerr.currentText()
                    for i in range(len(names)):
                        self.df.loc[self.df['FILENAME']==names[i] ,yCol]=finY[i]
                        #self.df.loc[self.df['FILENAME']==names[i] ,err]=finY[i]
                    
                    # #self.update_plot(self.x, self.y, "After rms cuts",
                    # #                self.res, "smoothed data", "smoothed residual")    # Update plot
                    # if self.time_ui.errorCheckBox.isChecked() == True:
    
                    #     self.Canvas.plot_fig_errs(self.df[xCol], self.df[yCol], xCol, yCol, data=self.df,errs=self.df[err])
                    # else:
                    #     self.Canvas.plot_fig(self.df[xCol], self.df[yCol], xCol, yCol, data=self.df)
                                        

                    # smallestRmsFound=True
                    # self.df.fillna(0,inplace=True)
                    # self.df=self.df.replace('nan',0)
                    # for col in list(self.df.columns):
                    #     if "FILENAME" in col or "OBSDATE":# in col or ""
                    #         pass
                    #     else:
                    #         self.df[col] = pd.to_numeric(self.df[col],downcast=float)

                    
                    # out_df=self.remove_rfi(self.df,xCol,yCol)

                    # #print(out_df.columns)
                    
                    # #if (len(out_df) == len(self.df)):
                    # #    print("Failed to remove RFI, probably data length too short")
                    # #else:
                    #     # merge to original
                    # self.df= pd.merge(self.df, out_df, how='left', on=['MJD'])
                    #     #self.rename_col(self.df,"_x")
                    # self.rename_col(self.df,"_y")

                    # # re-plot
                    # self.Canvas.clear_figure()
                    # self.Canvas.plot_fig(self.df[xCol], self.df[yCol], xCol, yCol, data=self.df)
                                    

                        # rms3_ = 
                        # scanLen = len(self.Canvas.x)
                        # if self.data["CENTFREQ"] <= 3000:
                        #     noTotScans = 2
                        # else:
                        #     noTotScans = 6

                        # # spline the data
                        # spl = fit.spline(self.Canvas.x, self.Canvas.y)

                        # scanRes, self.Canvas.x, self.Canvas.y, res, finspl, rmsb, rmsa = fit.cleanRmsCuts2(
                        #     spl, self.Canvas.x, self.Canvas.y, scanLen, self.log)

                        # self.write(f'RMS before: after -> {rmsb}: {rmsa,}','info')

                        # self.Canvas.clear_figure()  # Update figures

                        # # re-plot
                        # xCol=self.Canvas.xlab
                        # yCol=self.Canvas.ylab
                        #self.Canvas.plot_fig(self.df[xCol] ,self.df[yCol], xCol, yCol, data=self.df)

                        
            elif filterText == "binning":
               
               print("Binning not implemented yet\n")

    def enable_time_buttons(self):
        """ Enable time buttons. """
        self.time_ui.comboBoxTables.setEnabled(True)
        self.time_ui.comboBoxColsX.setEnabled(True)
        self.time_ui.comboBoxColsY.setEnabled(True)
        self.time_ui.comboBoxColsYerr.setEnabled(True)
        self.time_ui.EdtSplKnots.setEnabled(True)
        self.time_ui.BtnPlot.setEnabled(True)
        self.time_ui.comboBoxFilters.setEnabled(True)
        self.time_ui.EdtFilter.setEnabled(True)
        self.time_ui.BtnFilter.setEnabled(True)
        self.time_ui.comboBoxFitTypes.setEnabled(True)
        self.time_ui.comboBoxOrder.setEnabled(True)
        self.time_ui.BtnFit.setEnabled(True)
        # self.time_ui.BtnSavePlot.setEnabled(True)
        self.time_ui.BtnDelPoint.setEnabled(True)
        self.time_ui.BtnDelBoth.setEnabled(True)
        self.time_ui.BtnResetPoint.setEnabled(True)
        self.time_ui.BtnReset.setEnabled(True)
        self.time_ui.BtnRefreshDB.setEnabled(True)
        self.time_ui.BtnUpdateDB.setEnabled(True)
        self.time_ui.BtnSaveDB.setEnabled(True)
        self.time_ui.BtnQuit.setEnabled(True)

    def add_items_to_combobox(self):

        """Refresh the list of folders containing plots to be displayed. """
        
        self.db.close_db()

        # open db and get tables
        self.db = SQLiteDB(databaseName=self.dbFilePath, log=self.log)
        self.db.create_db()
        tables = sorted(self.db.get_table_names(self.dbFilePath))

        self.plot_ui.comboBox.clear()
        self.plot_ui.comboBox.clear()
            
        self.plot_ui.comboBoxOptions.clear()
        self.plot_ui.comboBoxOptions.clear()

        self.plot_ui.comboBoxFilter.clear()
        self.plot_ui.comboBoxFilter.clear()

        self.plot_ui.comboBox.addItems(tables)

    def check_dates(self):
        # check dates given
        pass

    def disable_btns(self):
        self.plot_ui.txtBoxFilter.setEnabled(False)
        self.plot_ui.comboBoxFilter.setEnabled(False)
    
    def enable_btns(self):
        self.plot_ui.txtBoxFilter.setEnabled(True)
        self.plot_ui.comboBoxFilter.setEnabled(True)

    def delete_obs(self):
        option=self.plot_ui.comboBoxOptions.currentText()
        filter=self.plot_ui.comboBoxFilter.currentText()
        txt=self.plot_ui.txtBoxFilter.text()
        
        try:
            txt=float(txt)
        except:
            pass

        # print('-'* 5, txt)
        
        if txt!=None and type(txt).__name__ !='str':
                print('in txt')
                if option == "":
                    print("Choose an option")
                else:
                    if filter!="" and txt!="":

                        # check folder name against table name
                        folderName=self.plot_ui.comboBox.currentText() 

                        print('opt: ',option,", filt: ",filter,', table: ',folderName)

                        db = SQLiteDB(databaseName=self.dbFilePath, log=self.log)
                        db.create_db()
                        tableNames = sorted(db.get_table_names(self.dbFilePath))
                        colInd, colNames, colType = db.get_all_table_coloumns(folderName)
                        rows = self.db.get_rows_of_cols(folderName,colNames)
                        
                        # create dataframe
                        df = pd.DataFrame(list(rows), columns = colNames)
                        df = df[(df['OBSDATE']>="2008-01-01") & (df['OBSDATE']<="2018-12-31")]

                        txt=float(txt)
                        if type(txt).__name__ != "str":

                                    #txt=float(txt)
                                    df[option] = df[option].astype(float)

                                    if filter == ">":
                                        ndf = df[df[option] > txt]
                                        print(len(ndf))#,option,txt ,df[option])

                                    elif filter == ">=":
                                        ndf = df[df[option] >= txt]
                                        print(len(ndf))

                                    elif filter == "<":
                                        ndf = df[df[option] < txt]
                                        print(len(ndf))

                                    elif filter == "<=":
                                        ndf = df[df[option] <= txt]
                                        print(len(ndf))

                                    elif filter == "=":
                                        ndf = df[df[option] == txt]
                                        print(len(ndf))
                            
                                    else:
                                        ndf=df

                        cols=list(ndf.columns)
                        files=list(ndf.FILENAME)

                        print(f'cols: {len(cols)}, files: {len(files)}')
                        print(cols)
                        
                        if "FLUXTOT" in cols:
                            for j in files:
                                stmt=f"UPDATE '{folderName}' SET "

                                if "OL" in option:
                                    ols=[]
                                    for i in cols:
                                        if 'OL' in i or 'NL' in i or 'SL' in i:
                                            ols.append(i)
                                            # print(ols)

                                    for k in ols:
                                        stmt=stmt+f"{k}='{np.nan}', "
                                # elif "OR" in option:
                                #         ols=[i for i in cols if 'OR' in i]
                                #         print(ols)

                                #         for k in ols:
                                #             stmt=stmt+f"{k}='{np.nan}', "

                                # for col in cols:
                                    print(stmt)
                                    sys.exit()
                                else:
                                    # if "SL" in option:
                                    #     ols=[]
                                    #     for i in cols:
                                    #         if 'SL' in i:
                                    #             ols.append(i)
                                    #     for k in ols:
                                    stmt=stmt+f"{option}='{np.nan}', "

                                print()
                                stmt=stmt[:-2]+f" WHERE FILENAME='{j}'; \n"

                                print(stmt)
                                db.c.execute(stmt)
                                db.commit_changes()
                                print('done')
                            # sys.exit()
                        else:
                            for j in files:
                                stmt=f"UPDATE '{folderName}' SET "

                                print(option)
                                sys.exit()

                                if "DTA" in option:
                                    s = option.remove("D")
                                    print(s,option)
                                    sys.exit()
                                

                                elif "OL" in option:
                                    ols=[i for i in cols if 'OL' in i]
                                    print(ols)

                                    for k in ols:
                                        if "FLAG" in k:
                                            stmt=stmt+f"{k}=200, TSYS1='{np.nan}', "
                                        else:
                                            stmt=stmt+f"{k}='{np.nan}', "

                                elif "OR" in option:
                                    #if "OL" in option:
                                    ors=[i for i in cols if 'OR' in i]
                                    print(ors)

                                    for k in ors:
                                        if "FLAG" in k:
                                            stmt=stmt+f"{k}=200,  TSYS2='{np.nan}', "
                                        else:
                                            stmt=stmt+f"{k}='{np.nan}', "
                                else:
                                    print('else')
                                    sys.exit()
                                    for col in cols:
                                        if 'SL' in col or 'SR' in col or  'OL' in col or  'OR' in col or  'NL' in col or  'NR' in col :
                                            if "FLAG" in col:
                                                stmt=stmt+f"{col}=200, "
                                            else:
                                                stmt=stmt+f"{col}='{np.nan}', TSYS1='{np.nan}', TSYS2='{np.nan}', "
                                        else:
                                            pass
                                        #or  'OBSTIME' in col or 'MJD' in col or  'OBJECT' in col or  'OBJECTTYPE' in col or  'CENTFREQ' in col or  'LOGFREQ' in col or  'FOCUS' in col or  'TILT' in col or  'HA' in col or  'ZA' in col or  'RADIOMETER' in col or  'BANDWDTH' in col or  'TCAL1' in col or 'TCAL2' in col or  'NOMTSYS' in col or 'TSYS1', 'TSYSERR1', 'TSYS2', 'TSYSERR2', 'TAMBIENT', 'PRESSURE', 'HUMIDITY', 'WINDSPD', 'HPBW', 'FNBW', 'ELEVATION', 'LONGITUDE', 'LATITUDE', 'SCANTYPE', 'BEAMTYPE', 'OBSERVER', 'OBSLOCAL', 'PROJNAME', 'PROPOSAL', 'TELESCOPE', 'UPGRADE', 'INSTFLAG', 'SCANDIST', 'SCANTIME', 'PWV', 'SVP', 'AVP', 'DPT', 'WVD', 'MEAN_ATMOS_CORRECTION', 'TAU10', 'TAU15', 'TBATMOS10', 'TBATMOS15', 'SLTA', 'SLDTA', 'SLS2N', 'SLTAPEAKLOC', 'SLFLAG', 'SLRMSB', 'SLRMSA', 'SLBSLOPE', 'SLBSRMS', 'NLTA', 'NLDTA', 'NLS2N', 'NLTAPEAKLOC', 'NLFLAG', 'NLRMSB', 'NLRMSA', 'NLBSLOPE', 'NLBSRMS', 'OLTA', 'OLDTA', 'OLPC', 'COLTA', 'COLDTA', 'OLS2N', 'OLTAPEAKLOC', 'OLFLAG', 'OLRMSB', 'OLRMSA', 'OLBSLOPE', 'OLBSRMS', 'SRTA', 'SRDTA', 'SRS2N', 'SRTAPEAKLOC', 'SRFLAG', 'SRRMSB', 'SRRMSA', 'SRBSLOPE', 'SRBSRMS', 'NRTA', 'NRDTA', 'NRS2N', 'NRTAPEAKLOC', 'NRFLAG', 'NRRMSB', 'NRRMSA', 'NRBSLOPE', 'NRBSRMS', 'ORTA', 'ORDTA', 'ORPC', 'CORTA', 'CORDTA', 'ORS2N', 'ORTAPEAKLOC', 'ORFLAG', 'ORRMSB', 'ORRMSA', 'ORBSLOPE', 'ORBSRMS'

                                stmt=stmt[:-2]+f" WHERE FILENAME='{j}'; \n"

                                print(stmt)
                                db.c.execute(stmt)
                                db.commit_changes()
                                print('done')
                
                    else:
                        pass

        elif filter=='between':

            text1=self.plot_ui.txtBoxStart.text()
            text2=self.plot_ui.txtBoxEnd.text()

            # check folder name against table name
            folderName=self.plot_ui.comboBox.currentText() 

            print('opt: ',option,", filt: ",filter,', table: ',folderName)

            # db = SQLiteDB(databaseName=self.dbFilePath, log=self.log)
            # db.create_db()
            tableNames = sorted(self.db.get_table_names(self.dbFilePath))
            colInd, colNames, colType = self.db.get_all_table_coloumns(folderName)
            rows = self.db.get_rows_of_cols(folderName,colNames)
                        
            #print(folderName,colNames)

            # create dataframe
            df = pd.DataFrame(list(rows), columns = colNames)
            df = df[(df['OBSDATE']>="2008-01-01") & (df['OBSDATE']<="2018-12-31")]

            if folderName in self.tables: 

                try:
                    txt1=float(text1)
                except:
                    # print("\nOnly integers or floats accepted\n")
                    txt1=""

                try:
                    txt2=float(text2)
                except:
                    # print("\nOnly integers or floats accepted\n")
                    txt2=""

                print(f'start: {txt1}, end: {txt2}\n')

                if type(txt1).__name__ != "str" and type(txt2).__name__ != "str":      
                    df[option] = df[option].astype(float)
                    df = df[(df[option] >= txt1)& (df[option] <= txt2)]
                    # print(len(df))

                elif type(txt1).__name__ == "str" and type(txt2).__name__ != "str":           
                    df[option] = df[option].astype(float)
                    df = df[(df[option] <= txt2)]
                    # print(len(df))

                elif type(txt1).__name__ != "str" and type(txt2).__name__ == "str":         
                    df[option] = df[option].astype(float)
                    df = df[(df[option] >= txt1)]
                    # print(len(df))

                elif type(txt1).__name__ == "str" and type(txt2).__name__ == "str":
                    
                    if option == 'OBSDATE':
                        if text1=="" and text2!="":
                            try:
                                T2=datetime.strptime(text2, '%Y-%m-%d')
                            except:
                                print ('Invalid date format, please use "yyyy-mm-dd"')
                                sys.exit()
                            df = df[df[option] <= T2]

                        elif text1!="" and text2=="": 
                            try:
                                T1=datetime.strptime(text1, '%Y-%m-%d')
                            except:
                                print ('Invalid date format, please use "yyyy-mm-dd"')
                                sys.exit()
                            df = df[df[option] >= T1]

                        elif text1!="" and text2!="":
                            try:
                                T1=datetime.strptime(text1, '%Y-%m-%d')
                            except:
                                print ('Invalid date format, please use "yyyy-mm-dd"')
                                sys.exit()
                            try:
                                T2=datetime.strptime(text2, '%Y-%m-%d')
                            except:
                                print ('Invalid date format, please use "yyyy-mm-dd"')
                                sys.exit()
                            df = df[(df[option] >= T1)& (df[option] <= T2)]
                        else:
                            print ('Invalid date formats, please use "yyyy-mm-dd" for start and end dates')
                            sys.exit()
                    else:
                        print('showing everything may freeze yyour machine')
                        try:
                            df = df[(df[option] >= text1)& (df[option] <= text2)]
                        except:
                            print('Invalid entry/entries, check values correspond to table entries')
                            sys.exit()

                else:
                    print("Failed to find working solution")
                    sys.exit()

                cols=list(df.columns)
                files=list(df.FILENAME)

                print(f'cols: {len(cols)}, files: {len(files)}')
                
                for j in files:
                    stmt=f"UPDATE {folderName} SET "
                    if "OL" in option:
                        ols=[i for i in cols if 'OL' in i]
                        print(ols)

                        for k in ols:
                            if "FLAG" in k:
                                stmt=stmt+f"{k}=200, "
                            else:
                                stmt=stmt+f"{k}='{np.nan}', "

                    elif "OR" in option:
                        #if "OL" in option:
                        ors=[i for i in cols if 'OR' in i]
                        print(ors)

                        for k in ors:
                            if "FLAG" in k:
                                stmt=stmt+f"{k}=200, "
                            else:
                                stmt=stmt+f"{k}='{np.nan}', "
                    else:
                        for col in cols:
                            if 'SL' in col or 'SR' in col or  'OL' in col or  'OR' in col or  'NL' in col or  'NR' in col :
                                if "FLAG" in col:
                                    stmt=stmt+f"{col}=200, "
                                else:
                                    stmt=stmt+f"{col}='{np.nan}', "
                            else:
                                pass
                                    #or  'OBSTIME' in col or 'MJD' in col or  'OBJECT' in col or  'OBJECTTYPE' in col or  'CENTFREQ' in col or  'LOGFREQ' in col or  'FOCUS' in col or  'TILT' in col or  'HA' in col or  'ZA' in col or  'RADIOMETER' in col or  'BANDWDTH' in col or  'TCAL1' in col or 'TCAL2' in col or  'NOMTSYS' in col or 'TSYS1', 'TSYSERR1', 'TSYS2', 'TSYSERR2', 'TAMBIENT', 'PRESSURE', 'HUMIDITY', 'WINDSPD', 'HPBW', 'FNBW', 'ELEVATION', 'LONGITUDE', 'LATITUDE', 'SCANTYPE', 'BEAMTYPE', 'OBSERVER', 'OBSLOCAL', 'PROJNAME', 'PROPOSAL', 'TELESCOPE', 'UPGRADE', 'INSTFLAG', 'SCANDIST', 'SCANTIME', 'PWV', 'SVP', 'AVP', 'DPT', 'WVD', 'MEAN_ATMOS_CORRECTION', 'TAU10', 'TAU15', 'TBATMOS10', 'TBATMOS15', 'SLTA', 'SLDTA', 'SLS2N', 'SLTAPEAKLOC', 'SLFLAG', 'SLRMSB', 'SLRMSA', 'SLBSLOPE', 'SLBSRMS', 'NLTA', 'NLDTA', 'NLS2N', 'NLTAPEAKLOC', 'NLFLAG', 'NLRMSB', 'NLRMSA', 'NLBSLOPE', 'NLBSRMS', 'OLTA', 'OLDTA', 'OLPC', 'COLTA', 'COLDTA', 'OLS2N', 'OLTAPEAKLOC', 'OLFLAG', 'OLRMSB', 'OLRMSA', 'OLBSLOPE', 'OLBSRMS', 'SRTA', 'SRDTA', 'SRS2N', 'SRTAPEAKLOC', 'SRFLAG', 'SRRMSB', 'SRRMSA', 'SRBSLOPE', 'SRBSRMS', 'NRTA', 'NRDTA', 'NRS2N', 'NRTAPEAKLOC', 'NRFLAG', 'NRRMSB', 'NRRMSA', 'NRBSLOPE', 'NRBSRMS', 'ORTA', 'ORDTA', 'ORPC', 'CORTA', 'CORDTA', 'ORS2N', 'ORTAPEAKLOC', 'ORFLAG', 'ORRMSB', 'ORRMSA', 'ORBSLOPE', 'ORBSRMS'

                    stmt=stmt[:-2]+f" WHERE FILENAME='{j}'; \n"

                    print(stmt)
                    # db.c.execute(stmt)
                    # db.commit_changes()

                    sys.exit()

            else:
                print(f"\n{folderName} not found in {self.tables}\n")

        else:
            print("No valid entries detected for filter")
            #pass

    def fx(self,x):
        # convert values to floats
        try:
            return np.float(x)
        except:
            return np.nan

    def show_plot_browser(self):
        """Open a webrowser containg the plots to be displayed."""
        
        # NEED TO RUN A FEW CHECKS FIRST
        option=self.plot_ui.comboBoxOptions.currentText()
        filter=self.plot_ui.comboBoxFilter.currentText()

        print("\nFilter by: ", option)
        print('Key: ', filter)
        
        if filter !="between":

            # get params
            txt=self.plot_ui.txtBoxFilter.text()
            print(">>> txt: ",txt, ', name: ', type(txt).__name__)
            print('option: ',option)

            if txt!=None or type(txt).__name__ !='str':
                # print('Value: ', txt)
                # print("Option: ", option)

                if option=="":
                    print("Need to choose an option")

                else:
                    if filter=="":
                        print("Please make a valid selection")
                    else:
                        if txt=="":
                            # show everything
                            print("no value added, should show all pics, but wont")
                        else:
                            # get data from db
                            # check folder name against table name
                            folderName=self.plot_ui.comboBox.currentText()

                            print('Folder name: ',folderName)
                            print('Path to file: ',self.dbFilePath)
                            # sys.exit()

                            db = SQLiteDB(databaseName=self.dbFilePath, log=self.log)
                            db.create_db()
                            tableNames = sorted(db.get_table_names(self.dbFilePath))
                            print('Table names: ', tableNames)
                            colInd, colNames, colType = db.get_all_table_coloumns(folderName)
                            rows = self.db.get_rows_of_cols(folderName,colNames)
                            
                            # create dataframe
                            df = pd.DataFrame(list(rows), columns = colNames)
                            # df = df[(df['OBSDATE']>="2008-01-01") & (df['OBSDATE']<="2018-12-31")]
                            #df=df.apply(pd.to_numeric)  
                            # print(df[option])

                            if option == 'OBSDATE':
                                print('Showing overall stats')
                                print(f'min: {df[option].iloc[0]}')
                                print(f'max: {df[option].iloc[-1]}')
                                try:
                                    print(f'mean: {df[option].mean()}')
                                    print(f'std: {df[option].std()}')
                                except:
                                    pass
                                print("*"*30,"\n")
                            else:
                                # print(df[option].apply(fx))
                                df[option]=df[option].astype(float) #.apply(fx)
                                # df[option]=df[option].apply(fx)
                                print("\n","*"*30)
                                try:
                                    print('Showing basic stats for selection')
                                    print(f'DATE start: {df["OBSDATE"].iloc[0]}')
                                    print(f'DATE end: {df["OBSDATE"].iloc[-1]}')
                                    print(f'MJD start: {df["MJD"].iloc[0]:.1f}')
                                    print(f'MJD end: {df["MJD"].iloc[-1]:.1f}')
                                    print(f'min: {df[option].dropna().min():.3f}')
                                    print(f'max: {df[option].dropna().max():.3f}')
                                    print(f'mean: {df[option].dropna().mean():.3f}')
                                    print(f'std: {df[option].dropna().std():.3f}')
                                    print(f'3sigma upper limit: {df[option].mean() + (df[option].mean()*df[option].std()):.3f}')
                                    print(f'3sigma lower limit: {df[option].mean() - (df[option].mean()*df[option].std()):.3f}')
                                except:
                                    print('Showing overall stats')
                                    print(f'DATE start: {df["OBSDATE"].iloc[0]}')
                                    print(f'DATE end: {df["OBSDATE"].iloc[-1]}')
                                    print(f'MJD start: {df["MJD"].iloc[0]:.1f}')
                                    print(f'MJD end: {df["MJD"].iloc[-1]:.1f}')
                                    print(f'min: {df[option].dropna().min():.3f}')
                                    print(f'max: {df[option].dropna().max():.3f}')
                                    print(f'mean: {df[option].dropna().mean():.3f}')
                                    print(f'std: {df[option].dropna().std():.3f}')
                                print("*"*30,"\n")

                            print(df[option])

                            # sys.exit()
                            try:
                                txt=float(txt)
                            except:
                                pass

                            if type(txt).__name__ != "str":
                                    print('in')
                                    print(filter)
                                    print(option)
                                    print(txt,type(txt))
                                    print(df[option])
                                    txt=float(txt)
                                    df[option] = df[option].astype(float)

                                    if filter == ">":
                                        ndf = df[df[option] > txt]
                                        print(len(ndf))#,option,txt ,df[option])

                                    elif filter == ">=":
                                        ndf = df[df[option] >= int(txt)]
                                        print(len(ndf))

                                    elif filter == "<":
                                        ndf = df[df[option] < txt]
                                        print(len(ndf))

                                    elif filter == "<=":
                                        ndf = df[df[option] <= txt]
                                        print(len(ndf))

                                    elif filter == "=":
                                        ndf = df[df[option] == txt]
                                        print(len(ndf))
                            
                                    else:
                                        ndf=df

                                    if len(ndf) > 0:
                                        #print(ndf['FILENAME'])
                                        ndf['plot_tag']=ndf['FILENAME'].apply(lambda x:x[:18])

                                        plots=list(ndf['plot_tag'])
                                        # print(ndf[['plot_tag',option]])
                                        # sys.exit()

                                        # print stats
                                        print("\n--- Basic stats ---\n")
                                        print("Min: ", ndf[option].min())
                                        print("Max: ", ndf[option].max())
                                        print("Mean: ", ndf[option].mean())
                                        print("Median: ", ndf[option].median())
                                        print("-"*20,"\n")

                                        # get plot folder and plot to browser
                                        imgDir = "plots/"

                                        ls=os.listdir(imgDir)
                                     
                                        #print(sorted(ls),folderName)

                                        for fn in ls:
                                            fn=fn.strip()
                                            
                                            if ".DS_Store" in fn:
                                                pass
                                            else:
                                                f=fn.replace(".","_")
                                                # f=f.replace("-","_")
                                                
                                                #print(fn,type(f),f,folderName,len(fn),len(folderName))
                                
                                                if f.lower()== folderName.lower():
                                                    print(">>",f,folderName)
                                                    folderName=fn
                                                    break

                                       
                                        msg_wrapper("debug", self.log.debug,"Plotting folder "+folderName)

                                        # print(imgDir, folderName)
                                        
                                        if "_"==folderName[0]:
                                            foldName=folderName[1:]
                                        else:
                                            foldName=folderName
                                        
                                        src=(ndf["OBJECT"].iloc[0]).replace(" ","")
                                        s=f"{src}_{foldName.upper().split('_')[-1]}"
                                        # print(src, s)
                                        # sys.exit()

                                        # src=s#src.replace("-","_")
                                        imgPath=f'plots/{src}/{s}/'
                                        dr=sorted(os.listdir(imgPath))

                                        # print(dr)
                                        # sys.exit()
                                        # imgPath=imgDir+folderName
                                        # imgPath=fpath+dr[i]

                                        imageNames = sorted(dr)
                                        images=[]

                                        if ".DS_Store" in imageNames:
                                            imageNames.remove(".DS_Store")

                                        # print(imageNames,'\n')
                                        # print(plots)
                                        # sys.exit()

                                        # # get images for current point
                                        for i in range(len(plots)):
                                            # print(imgPath,imageNames[i])
                                            for j in range(len(imageNames)):
                                                if plots[i] in imageNames[j]: #[:18]:
                                                    if "SL" in option and "HPS_LCP" in imageNames[j]:
                                                            #print(imageNames[i],plots[j])
                                                        images.append(imgPath+imageNames[j])
                                                    elif "SR" in option and "HPS_RCP" in imageNames[j]:
                                                            #print(imageNames[i],plots[j])
                                                        images.append(imgPath+imageNames[j])
                                                    elif "NL" in option and "HPN_LCP" in imageNames[j]:
                                                            #print(imageNames[i],plots[j])
                                                        images.append(imgPath+imageNames[j])
                                                    elif "NR" in option and "HPN_RCP" in imageNames[j]:
                                                            #print(imageNames[i],plots[j])
                                                        images.append(imgPath+imageNames[j])
                                                    elif  "OL" in option and "ON_LCP" in imageNames[j]:
                                                            #print(imageNames[i],plots[j])
                                                        images.append(imgPath+imageNames[j])
                                                    elif "OR" in option and "ON_RCP" in imageNames[j]:
                                                            #print(imageNames[i],plots[j])
                                                        images.append(imgPath+imageNames[j])
                                                    else:
                                                        images.append(imgPath+imageNames[i])
                                                

                                        #print(images)
                                        # sys.exit()
                                        # html link

                                        # if len(images) == 0:

                                        htmlstart = '<html> <head>\
                                                <meta charset = "utf-8" >\
                                                <meta name = "viewport" content = "width=device-width, initial-scale=1" > <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous"> <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script> <style> img {border: 2px solid  # ddd; /* Gray border */border-radius: 4px;  /* Rounded border */padding: 5px; /* Some padding */width: 400px; /* Set a small width */}/* Add a hover effect (blue shadow) */img:hover {box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);}</style> \
                                                <title>Plots</title>\
                                                </head>\
                                                <div class="container-fluid"> \
                                                    <div class="row">\
                                                        <hr>\
                                                            <h1> Plotting folder '+foldName.upper() + '</h1> <p>'
                                                    
                                        htmlmid=''

                                        imageOptions=[]
                                        

                                        if "OL" in option or "SL" in option or "NL" in option:
                                            for img in images:
                                                if "LCP" in img:
                                                    imageOptions.append(img)
                                            images=imageOptions

                                        elif "OR" in option or "SR" in option or "NR" in option:
                                            for img in images:
                                                if "RCP" in img:
                                                    imageOptions.append(img)
                                            images=imageOptions

                                        else:
                                            images=images

                                        
                                        # print(option)
                                        # sys.exit()
                                        # add images to html page
                                        for i in range(len(images)):
                                            #print(images.split("/")[1],images.split("/")[2])
                                            pathtoimg = images[i]
                                            img = '<small class="card-title">'+images[i].split("/")[3]+'</small><br/>\
                                                    <a target="_blank" href="'+pathtoimg + \
                                                    '"><img src="'+pathtoimg + \
                                                    '" class="card-img-top" alt="image goes here"></a>'
                                            imglink ='<div class = "card" style = "width: 13rem;" >\
                                                        '+img+'\
                                                            </div>'
                                            htmlmid=htmlmid+imglink

                                        htmlmid=htmlmid+'</p></div>'
                                        htmlend = '</div></html>'
                                        html = htmlstart+htmlmid+htmlend

                                        # create the html file
                                        path = os.path.abspath('temp.html')
                                        url = 'file://' + path

                                        with open(path, 'w') as f:
                                            f.write(html)
                                        webbrowser.open(url)
                                    else:
                                        html = '<html> <head>\
                                                <meta charset = "utf-8" >\
                                                <meta name = "viewport" content = "width=device-width, initial-scale=1" > <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous"> <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script> <style> img {border: 2px solid  # ddd; /* Gray border */border-radius: 4px;  /* Rounded border */padding: 5px; /* Some padding */width: 400px; /* Set a small width */}/* Add a hover effect (blue shadow) */img:hover {box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);}</style> \
                                                <title>Plots</title>\
                                                </head>\
                                                <div class="container-fluid"> \
                                                    <div class="row">\
                                                        <hr>\
                                                            <h1> Plotting folder '+folderName.upper() + '''</h1> 
                                                            <p> No data to show</p>
                                                    </div>
                                                </div>
                                                </html>
                                        '''
                                        # create the html file
                                        path = os.path.abspath('temp.html')
                                        url = 'file://' + path

                                        with open(path, 'w') as f:
                                            f.write(html)
                                        webbrowser.open(url)
                                        
                                        print("No data to show")
                            else:

                                # if txt=="OBSDATE":
                                print(f"{txt} filter not implemented yet\n")
                              
            else:
                print('Invalid entry for filter')

        elif filter =="between":
            # get params
            text1=self.plot_ui.txtBoxStart.text()
            text2=self.plot_ui.txtBoxEnd.text()

            print(f'Values: {text1}, {text2}')

            if option=="":
                print("Need to choose an option")

            else:
                if filter=="":
                    print("Plotting everything")
                else:
                    if text1=="" and text2=="":
                        # show everything
                        print("no value added, showing all images")
                    else:
                        # run filter
                        #print("All checked")

                        # get data from db
                        # check folder name against table name
                        plotFolderName=self.plot_ui.comboBox.currentText()
                        folderName=plotFolderName.lower().replace(".","_")

                        print(folderName,self.tables)
                        if folderName in self.tables:
                            print("\n",folderName, " found")
                            #target=folderName
                            db=""

                            # get column names from db and put them in combobox
                            self.colInd, self.colName, self.colType = self.db.get_all_table_coloumns(folderName)

                            rows = self.db.get_rows(folderName)

                            # create dataframe
                            df = pd.DataFrame(list(rows), columns = self.colName)
                            # df = df[(df['OBSDATE']>="2008-01-01") & (df['OBSDATE']<="2018-12-31")]
       

                            try:
                                txt1=float(text1)
                            except:
                                print("\nOnly integers or floats accepted\n")
                                txt1=""

                            try:
                                txt2=float(text2)
                            except:
                                print("\nOnly integers or floats accepted\n")
                                txt2=""

                            print(f'start: {txt1}, end: {txt2}\n')
                            print(f'start: {type(txt1)}, end: {type(txt2)}\n')
                            print(f'start: {text1}, end: {text2}\n')

                            if type(txt1).__name__ != "str" and type(txt2).__name__ != "str":
                               
                                df[option] = df[option].astype(float)
                                ndf = df[(df[option] >= txt1)& (df[option] <= txt2)]
                                print(len(ndf))

                            elif type(txt1).__name__ == "str" and type(txt2).__name__ != "str":
                               
                                df[option] = df[option].astype(float)
                                ndf = df[(df[option] <= txt2)]
                                print(len(ndf))

                            elif type(txt1).__name__ != "str" and type(txt2).__name__ == "str":
                               
                                df[option] = df[option].astype(float)
                                ndf = df[(df[option] >= txt1)]
                                print(len(ndf))

                            elif type(txt1).__name__ == "str" and type(txt2).__name__ == "str":
                                print(option)
                                if option == 'OBSDATE':
                                    df["OBSDATE"] = pd.to_datetime(df["OBSDATE"], format="%Y-%m-%d")
                                    # T2=datetime.strptime(text2, '%Y-%m-%d')
                                    # print(T2)

                                    # print(txt1)
                                    if text1=="" and text2!="":
                                        try:
                                            T2=datetime.strptime(text2, '%Y-%m-%d')
                                        except:
                                            print ('Invalid date format, please use "yyyy-mm-dd"')
                                            sys.exit()
                                        df = df[df[option] <= T2]

                                    elif text1!="" and text2=="": 
                                        try:
                                            T1=datetime.strptime(text1, '%Y-%m-%d')
                                        except:
                                            print ('Invalid date format, please use "yyyy-mm-dd"')
                                            sys.exit()
                                        df = df[df[option] >= T1]

                                    elif text1!="" and text2!="":
                                        try:
                                            T1=datetime.strptime(text1, '%Y-%m-%d')
                                        except:
                                            print ('Invalid date format, please use "yyyy-mm-dd"')
                                            sys.exit()
                                        try:
                                            T2=datetime.strptime(text2, '%Y-%m-%d')
                                        except:
                                            print ('Invalid date format, please use "yyyy-mm-dd"')
                                            sys.exit()

                                        df = df[(df[option] >= T1)& (df[option] <= T2)]

                                    else:
                                        print()
                                        print ('Invalid date formats, please use "yyyy-mm-dd" for start and end dates')
                                        sys.exit()
                                else:
                                    print('showing everything may freeze yyour machine')
                                    try:
                                        df = df[(df[option] >= txt1)& (df[option] <= txt2)]
                                    except:
                                        print('Invalid entry/entries, check values correspond to table entries')
                                        sys.exit()
    
                            else:
                                print("Failed to find working solution")
                                sys.exit()

                            if len(ndf) > 0:
                                    # ndf=df
                                    #print(ndf['FILENAME'])
                                    ndf['plot_tag']=ndf['FILENAME'].apply(lambda x:x[:18])

                                    plots=list(ndf['plot_tag'])
                                    #print(ndf[['plot_tag',option]])

                                    # print stats
                                    print("\n--- Basic stats ---\n")
                                    print("Min: ", ndf[option].min())
                                    print("Max: ", ndf[option].max())
                                    print("Mean: ", ndf[option].mean())
                                    print("Median: ", ndf[option].median())
                                    print("-"*20,"\n")

                                    # get plot folder and plot to browser
                                    imgDir = "plots/"

                                    msg_wrapper("debug", self.log.debug,"Plotting folder "+plotFolderName)

                                    ls=os.listdir(imgDir)

                                    for fn in ls:
                                        fn=fn.strip()
                                            
                                        if ".DS_Store" in fn:
                                            pass
                                        else:
                                            f=fn.replace(".","_")
                                                # f=f.replace("-","_")
                                                
                                                #print(fn,type(f),f,folderName,len(fn),len(folderName))
                                
                                            if f.lower()== folderName.lower():
                                                print(">>",f,folderName)
                                                folderName=fn
                                                break

                                        # fld=(folder.replace(".","_")).lower()
                                        # if fld==plotFolderName:
                                        #     plotFolderName=folder
                                            # print(f'{folder} = {fld} = {plotFolderName}')

                                    if "_"==folderName[0]:
                                            foldName=folderName[1:]
                                    else:
                                            foldName=folderName

                                    
                                    src=(ndf["OBJECT"].iloc[0]).replace(" ","")
                                    s=f"{src}_{foldName.upper().split('_')[-1]}"
                                    imgPath=f'plots/{src}/{s}/'
                                    dr = os.listdir(imgPath)
                                    imageNames=sorted(dr)
                                    images=[]

                                    if ".DS_Store" in imageNames:
                                        imageNames.remove(".DS_Store")

                                    print(imageNames,'\n')
                                    # print(plots)
                                    # sys.exit()

                                    # # get images for current point
                                    for i in range(len(plots)):
                                        for j in range(len(imageNames)):
                                            if plots[i] in imageNames[j]: #[:18]:
                                                if "SL" in option and "HPS_LCP" in imageNames[j]:
                                                        #print(imageNames[i],plots[j])
                                                    images.append(imgPath+imageNames[j])
                                                elif "SR" in option and "HPS_RCP" in imageNames[j]:
                                                        #print(imageNames[i],plots[j])
                                                    images.append(imgPath+imageNames[j])
                                                elif "NL" in option and "HPN_LCP" in imageNames[j]:
                                                        #print(imageNames[i],plots[j])
                                                    images.append(imgPath+imageNames[j])
                                                elif "NR" in option and "HPN_RCP" in imageNames[j]:
                                                        #print(imageNames[i],plots[j])
                                                    images.append(imgPath+imageNames[j])
                                                elif  "OL" in option and "ON_LCP" in imageNames[j]:
                                                        #print(imageNames[i],plots[j])
                                                    images.append(imgPath+imageNames[j])
                                                elif "OR" in option and "ON_RCP" in imageNames[j]:
                                                        #print(imageNames[i],plots[j])
                                                    images.append(imgPath+imageNames[j])
                                                else:
                                                    images.append(imgPath+imageNames[i])
                                            
                                    #print(images)

                                    # html link
                                    htmlstart = '<html> <head>\
                                            <meta charset = "utf-8" >\
                                            <meta name = "viewport" content = "width=device-width, initial-scale=1" > <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous"> <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script> <style> img {border: 2px solid  # ddd; /* Gray border */border-radius: 4px;  /* Rounded border */padding: 5px; /* Some padding */width: 400px; /* Set a small width */}/* Add a hover effect (blue shadow) */img:hover {box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);}</style> \
                                            <title>Plots</title>\
                                            </head>\
                                            <div class="container-fluid"> \
                                                <div class="row">\
                                                    <hr>\
                                                        <h1> Plotting folder '+foldName.upper()  + '</h1> <p>'
                                                
                                    htmlmid=''

                                    imageOptions=[]
                                        

                                    if "OL" in option or "SL" in option or "NL" in option:
                                            for img in images:
                                                if "LCP" in img:
                                                    imageOptions.append(img)
                                            images=imageOptions

                                    elif "OR" in option or "SR" in option or "NR" in option:
                                            for img in images:
                                                if "RCP" in img:
                                                    imageOptions.append(img)
                                            images=imageOptions

                                    else:
                                            images=images

                                    # add images to html page
                                    for i in range(len(images)):
                                        # print(images.split("/")[1],images.split("/")[2])
                                        # print(images[i])
                                        pathtoimg = images[i]
                                        img = '<small class="card-title">'+images[i].split("/")[3]+'</small><br/>\
                                                <a target="_blank" href="'+pathtoimg + \
                                                '"><img src="'+pathtoimg + \
                                                '" class="card-img-top" alt="image goes here"></a>'
                                        imglink ='<div class = "card" style = "width: 10rem;" >\
                                                    '+img+'\
                                                        </div>'
                                        htmlmid=htmlmid+imglink

                                    htmlmid=htmlmid+'</p></div>'
                                    htmlend = '</div></html>'
                                    html = htmlstart+htmlmid+htmlend

                                    # create the html file
                                    path = os.path.abspath('temp.html')
                                    url = 'file://' + path

                                    with open(path, 'w') as f:
                                        f.write(html)
                                    webbrowser.open(url)
                                
                            else:
                                html = '<html> <head>\
                                                <meta charset = "utf-8" >\
                                                <meta name = "viewport" content = "width=device-width, initial-scale=1" > <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous"> <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script> <style> img {border: 2px solid  # ddd; /* Gray border */border-radius: 4px;  /* Rounded border */padding: 5px; /* Some padding */width: 400px; /* Set a small width */}/* Add a hover effect (blue shadow) */img:hover {box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);}</style> \
                                                <title>Plots</title>\
                                                </head>\
                                                <div class="container-fluid"> \
                                                    <div class="row">\
                                                        <hr>\
                                                            <h1> Plotting folder '+folderName.upper() + '''</h1> 
                                                            <p> No data to show</p>
                                                    </div>
                                                </div>
                                                </html>
                                        '''
                                        # create the html file
                                path = os.path.abspath('temp.html')
                                url = 'file://' + path

                                with open(path, 'w') as f:
                                            f.write(html)
                                webbrowser.open(url)
                                        
                                print("No data to show")
                        else:
                            print(f"\n{folderName} not found in {self.tables}\n")
 
        else:
            print('Min: ', self.plot_ui.txtBoxStart.text())
            print('Max: ', self.plot_ui.txtBoxEnd.text())

    def open_db(self):
        """ Open the database. """

        # get db file
        self.dbFile = self.open_file_name_dialog("*.db")
        
        if self.dbFile == None:
            print("No file selected")
        else:
            self.time_ui.EdtDB.setText(self.dbFile)
            self.time_ui.EdtDB.setEnabled(True)
            
            # open the database and get tables

            self.db = SQLiteDB(databaseName=self.dbFile, log=self.log)
            self.db.create_db()

            # populate columns
            self.get_table_list()
            self.populate_cols()

            #self.time_ui.comboBoxColsX.setEnabled(True)
            #self.time_ui.comboBoxColsY.setEnabled(True)
            self.enable_time_buttons()
            self.connect_time_buttons()

    def on_table_name_changed(self):
        """ update combobox when table name changes. """
        self.populate_cols()

    def get_table_list(self):
        """ get list of tables in database. """

        self.tables = sorted(self.db.get_table_names(self.dbFile))
        curTxt = self.time_ui.comboBoxTables.currentText()
        if curTxt  not in self.tables:
            # force combobox to accept new items, need to investigate this issue further
            self.time_ui.comboBoxTables.clear()
            self.time_ui.comboBoxTables.clear()
            self.time_ui.comboBoxTables.addItems(self.tables)
            #self.time_ui.comboBoxTables.addItems(self.tables)     
            #self.time_ui.comboBoxTables.addItems(self.tables)
        else:
            pass

    def populate_cols(self):
        """ Populate x and y columns with data from tables. """

        # get column names from currently selected table
        self.table = self.time_ui.comboBoxTables.currentText()
        if not self.table:
            print("Issue: ")
            # force the combobox to accept items
            #self.time_ui.comboBoxTables.addItems(self.tables)
            #self.time_ui.comboBoxTables.addItems(self.tables)
            self.time_ui.comboBoxTables.addItems(self.tables)

            lt = len(self.tables)
            lc = self.time_ui.comboBoxTables.count()
            x = [self.time_ui.comboBoxTables.itemText(i) for i in range(self.time_ui.comboBoxTables.count())]
            #print(lt,lc,x)
            #print('curtxt: ',self.time_ui.comboBoxTables.currentText())
            
        self.colInd, self.colName, self.colType = self.db.get_all_table_coloumns(self.table)
        print('table: ', self.table)
        print('cols: ',self.colName,'\n')

        # select only numerical cols with a few exceptions
        colDict={}
        self.colNames=[]
        for i in range(len(self.colInd)):
            colDict[self.colInd[i]] = self.colName[i]
            self.colNames.append(self.colName[i])

        # get rows
        self.rows = self.db.get_rows_of_cols(self.table, self.colNames)

        # sys.exit()
        self.df = pd.DataFrame(list(self.rows), columns=self.colNames)
        self.df=self.df.sort_values('FILENAME')
        # try:
        # print(len(self.df))
        # self.df.drop_duplicates(subset=['MJD'], keep='first',inplace=True)
        # print(len(self.df))
        # sys.exit()
        # except:
        #     pass
        #for col in list(self.df.columns):
        #    self.df[col] = self.df[col].replace(np.nan,0)
        #    self.df[col] = self.df[col].replace('nan',0)

        #print(self.colName)
        #sys.exit()
        self.orig_df=self.df # copy of df
        self.df["OBSDATE"]=pd.to_datetime(self.df["OBSDATE"],format="%Y-%m-%d")

        # # select only numerical cols with a few exceptions
        # colDict={}
        # self.colNames=[]
        # for i in range(len(self.colInd)):
        #     if "TEXT" == self.colType[i]:
        #         if (self.colName[i]=="FILENAME" or self.colName[i]=="OBSDATE" or self.colName[i]=="SOURCEDIR"):
        #             colDict[self.colInd[i]] = self.colName[i]
        #             # if self.colName[i]=="FILENAME" or self.colName[i]=="SOURCEDIR":
        #             #     pass
        #             # else:
        #             self.colNames.append(self.colName[i])
        #         else:
        #             pass
        #     else:
        #         if "id" in self.colName[i] or "HDULENGTH" in self.colName[i] or "MJD" in self.colName[i] or "OBSDATE" in self.colName[i] or "HA" in self.colName[i]:
        #            pass
        #         else:
        #             colDict[self.colInd[i]] = self.colName[i]
        #             self.colNames.append(self.colName[i])

        self.time_ui.comboBoxColsX.clear()
        self.time_ui.comboBoxColsY.clear()
        self.time_ui.comboBoxColsYerr.clear()
        plotCols=[]
        for name in self.colNames:
            if 'SOURCE' in name or 'FILE' in name or 'HDU' in name or 'OBSD' in name or 'MJD' in name or 'OBS' in name or 'OBJ' in name or 'id' == name or 'RAD' in name or 'TYPE' in name or 'PRO' in name or 'TELE' in name or 'UPGR' in name or 'HA' in name or 'INST' in name or 'SCAN' in name:
                #or 'ERR' in name or 'LD' in name or 'RD' in name 
                pass
            else:
                plotCols.append(name)

        errcols=[]
        for name in self.colNames:
            if  'LD' in name or 'RD' in name or 'ERR' in name or 'DS' in name or 'DN' in name or 'DO' in name or 'DF' in name or 'DC' in name:
                errcols.append(name)
            else:
                pass

        yerr=['None']
        self.time_ui.comboBoxColsX.addItems(['OBSDATE','MJD','HA'])
        self.time_ui.comboBoxColsY.addItems(plotCols)
       

        
        self.yErr=list(yerr)+list(errcols)
        self.time_ui.comboBoxColsYerr.addItems(self.yErr)

    def plot_cols_df(self):
        """ Plot database columns. """

        # get col names
        xCol = self.time_ui.comboBoxColsX.currentText()
        yCol = self.time_ui.comboBoxColsY.currentText()
        # errCol = self.time_ui.comboBoxColsYerr.currentText()

        if xCol == yCol:
            print("\nYou cannot plot the same column on X and Y\n")
        else:
            yErr = self.time_ui.comboBoxColsYerr.currentText()

            # get col data
            #self.db.set_table_name(self.table)
            #x=self.db.read_data_from_database(xCol)
            #y=self.db.read_data_from_database(yCol)

            print(f"\nPlotting {xCol} vs {yCol} in table {self.table}\n")
            #print(self.df.columns)
            #sys.exit()
            self.df[yCol]=self.df[yCol].apply(self.f)
            try:
                self.df[yErr]=self.df[yErr].apply(self.f)
                self.Canvas.plot_fig(self.df[xCol],self.df[yCol],xCol,yCol,data=self.df,yerr=self.df[yErr]) #,title=f"Plot of {self.df['SOURCEDIR']} obs. {self.df['FILENAME'][:8]}")#,data=self.)
            except:
                self.Canvas.plot_fig(self.df[xCol],self.df[yCol],xCol,yCol,data=self.df)#,title=f"Plot of {self.df['SOURCEDIR']} obs. {self.df['FILENAME'][:8]}")#,data=self.)
            #self.df['ORDPSS']=self.df['ORDPSS'].apply(f)

            #print(len(self.df[xCol]))
            # make plot
            #if len(yErr)>0:
            #    self.Canvas.plot_fig_errs(self.df[xCol],self.df[yCol],xCol,yCol,yErr,self.df)#,data=self.)
            #else:
            # pl.plot(self.df[xCol],self.df[yCol],'.')
            # pl.show()
            # pl.close()
            
            self.Canvas.draw()
            
    def plot_cols(self,col=""):
        """ Plot database columns. """

        # get col names
        xCol = self.time_ui.comboBoxColsX.currentText()
        yCol = self.time_ui.comboBoxColsY.currentText()

        if xCol == yCol:
            print("\nYou cannot plot the same column on X and Y\n")
        else:
            yErr = self.time_ui.comboBoxColsYerr.currentText()

            # get col data
            self.db.set_table_name(self.table)
            #x=self.db.read_data_from_database(xCol)
            #y=self.db.read_data_from_database(yCol)
            self.df[yCol]=self.df[yCol].apply(self.f)
            try:
                self.df[yErr]=self.df[yErr].apply(self.f)
            except:
                pass

            print(f"Plotting {xCol} vs {yCol} in table {self.table}")
            #print(self.df.columns)
            #sys.exit()
            #print(self.df[xCol])
            # make plot
            #if len(yErr)>0:
            #    self.Canvas.plot_fig_errs(self.df[xCol],self.df[yCol],xCol,yCol,yErr,self.df)#,data=self.)
            #else:
            #print(yCol)
            #print(list(self.df[yCol]))

            try:
                yerr=self.df[yErr]
            except:
                yerr=[]
            self.Canvas.plot_fig(self.df[xCol],self.df[yCol],xCol,yCol,data=self.df,yerr=yerr)#,data=self.)
            
    def open_db_path(self):
        # Open a database

        self.write("Opening DB",'info')
        self.dbFilePath = self.open_file_name_dialog("*.db")
        if self.dbFilePath == None:
            self.write("You need to select a file to open",'info')
            self.write("Please select a file",'info')
            pass
        else:

            # free all else
            free=True
            self.plot_ui.btnDelete.setEnabled(free)
            self.plot_ui.btnRefreshPlotList.setEnabled(free)
            self.plot_ui.btnShow.setEnabled(free)
            self.plot_ui.comboBox.setEnabled(free)
            self.plot_ui.comboBoxFilter.setEnabled(free)
            self.plot_ui.comboBoxOptions.setEnabled(free)
            self.plot_ui.txtBoxEnd.setEnabled(free)
            self.plot_ui.txtBoxStart.setEnabled(free)

            # open db and get tables
            self.db = SQLiteDB(databaseName=self.dbFilePath, log=self.log)
            self.db.create_db()
            self.tables = sorted(self.db.get_table_names(self.dbFilePath))

            # #print(tables)
            self.plot_ui.comboBox.clear()        
            self.plot_ui.comboBox.addItems(self.tables)
 
    def open_file(self):
        """ Open file for processing. """

        self.write("Opening file",'info')

        # hide pss's
        self.drift_ui.pss_values_groupbox.setVisible(False)

        # Initialize fit parameters
        self.set_fit_parmeters()

        self.filePath = self.open_file_name_dialog("*.fits")

        if self.filePath == None:
            self.write("You need to select a file to open",'info')
            self.write("Please select a file",'info')
            pass
        else:
            try:
                self.reset_plot()
                self.reset_peak()
            except:
                pass

            self.drift_ui.pss_values_groupbox.setVisible(False)
            # Get data from file
            fileReader = FitsFileReader(self.log, filePath=self.filePath)
            self.data = fileReader.data
            self.scans = fileReader.scans

            self.Canvas.delete_canvas()

            # set the figure layout
            if "D" in self.data["BEAMTYPE"]:
                self.Canvas.init_dual_fig_canvas()
                self.Canvas.clear_dual_canvas()
                self.secondaryCanvas.init_canvas()
                self.secondaryCanvas.clear_canvas()
            else:
                self.Canvas.init_fig_canvas()
                self.Canvas.clear_canvas()
                self.secondaryCanvas.init_canvas()
                self.secondaryCanvas.clear_canvas()

            # Setup pss and flux calculation buttons
            if (self.data["OBJECTTYPE"] == "CAL"):
                self.drift_ui.BtnCalc.setText("Calc PSS")
                self.drift_ui.BtnCalc.clicked.connect(self.calc_pss_)
                
                # remove pss estimation buttons and boxes
                self.drift_ui.pss_values_groupbox.setVisible(False)
                #self.disable_target_widgdets()

            elif self.data["OBJECTTYPE"] == "TAR":
                #self.drift_ui.BtnCalc.
                self.drift_ui.BtnCalc.setText("Calc Flux")
                self.drift_ui.BtnCalc.clicked.connect(self.calc)
                self.drift_ui.pss_values_groupbox.setVisible(False)
                #self.enable_target_buttons()
 
            self.write("Opened file: "+self.filePath,'info')
            print("\n")
            
            # Setup environment variables
            self.set_beam_names()
            self.populate_widgets()
            self.enable_widgets()

            if len(self.beamName) == 2:
                ind=0
                x=self.scans['OFFSET']
                y=self.scans[self.beamName[ind]]
                y1=self.scans[self.beamName[ind+1]]
                self.secondaryCanvas.plot_figure(x,y,y1,label1=self.beamName[ind],label2=self.beamName[ind+1])
            
            else:
                ind=1
                x=self.scans['OFFSET']
                y=self.scans[self.beamName[ind]]
                y1=self.scans[self.beamName[ind+1]]
                self.secondaryCanvas.plot_figure(x,y,y1,label1=self.beamName[ind],label2=self.beamName[ind+1])
            
            # Add items to combo boxes
            self.drift_ui.ComboBoxPlotType.clear()
            self.drift_ui.ComboBoxPlotType.addItems(self.beamName)

            allProperties = list(self.data.keys())#[3:]
            #self.drift_ui.ComboBoxScanProperty.setEnabled(True)
            #self.drift_ui.ComboBoxScanProperty.clear()
            #self.drift_ui.ComboBoxScanProperty.addItems(allProperties)
            #self.drift_ui.newPropertyValue.setEnabled(True)
            #self.drift_ui.BtnModify.setEnabled(True)

            self.fit_types = ["Polynomial"]#, "Gaussian"]
            self.drift_ui.ComboBoxFitType.clear()
            self.drift_ui.ComboBoxFitType.addItems(self.fit_types)

            self.smoothing_types = ["please select:", "rms cuts", "flat",
                              "hanning", "bartlett", "blackman"]
            self.drift_ui.ComboBoxFilterType.clear()
            self.drift_ui.ComboBoxFilterType.addItems(self.smoothing_types)

            # Setup index change options for combo boxes
            self.drift_ui.ComboBoxFitLoc.currentIndexChanged.connect(
                self.on_fit_combobox_changed)
            self.drift_ui.ComboBoxFilterType.currentIndexChanged.connect(
                self.on_filter_type_combobox_changed)
            self.drift_ui.ComboBoxFitType.currentIndexChanged.connect(
                self.on_fit_type_combobox_changed)
            self.drift_ui.checkBox.stateChanged.connect(
                self.on_checkbox_changed)

            # SET FLAGS
            self.setup_flags()

            # set x,y, plot first image
            self.reset_xy(0)
            self.Canvas.plot_figure(self.x, self.y, label=self.beamName[ind])
            if "D" in self.data["BEAMTYPE"]:
                self.Canvas.label_dual_res()
            else:
                self.Canvas.label_res()

            # Functionality to read pss values
            if ("TAR" in self.data["OBJECTTYPE"]):
             
                # Read cal file
                if "S" in self.data["BEAMTYPE"]:

                    # Check if data has been calibrated for the target.
                    val = os.path.isfile("AVE_PSS.csv")

                    if val == True:

                        # READ FILE
                        df = pd.read_csv("AVE_PSS.csv", delimiter=",")

                        # Get name, freq and PSS values
                        names = np.array(df[["NAME"]])
                        frqs = np.array(df[["FREQ_MHZ"]])
                        plcp = np.array(df[["AVE_PSS_LCP"]])
                        dplcp = np.array(df[["dAVE_PSS_LCP"]])
                        prcp = np.array(df[["AVE_PSS_RCP"]])
                        dprcp = np.array(df[["dAVE_PSS_RCP"]])

                    else:
                        msg_wrapper("debug", self.log.debug,
                                    "Setting PSS to default HartRAO values")

                        # Read in hart pps values
                        hartPars={}
                        hartVals = np.loadtxt(
                            "predefs/default_hart_pss.txt", skiprows=6, delimiter=",", usecols=(0, 1))
                        for i in range(len(hartVals)):
                            hartPars[f'{hartVals[i][0]}'] = float(hartVals[i][1])
                        
                        # Find PSS for current frequency
                        parKeys=list(hartPars.keys())
                        if self.data["BEAMTYPE"][:-1] in parKeys:
                           pssInd = self.data["BEAMTYPE"][:-1]
                        else:
                           msg_wrapper("debug", self.log.debug, "The frequency is not observed at hartrao")
                           sys.exit()

                        # Check if a calibrator has been reduced
                        if ("S" in self.data["BEAMTYPE"]):

                            # Activate labels
                            self.drift_ui.pss_values_groupbox.setVisible(True)
                            self.drift_ui.LblPSSlcpA.setText("LCP PSS")
                            self.drift_ui.EdtPSSlcpA.setText(str(hartPars[pssInd]))
                            self.drift_ui.EdtPSSlcpA.setEnabled(True)
                            self.drift_ui.LblPSSrcpA.setText("RCP PSS")
                            self.drift_ui.EdtPSSrcpA.setText(str(hartPars[pssInd]))
                            self.drift_ui.EdtPSSrcpA.setEnabled(True)
                            self.drift_ui.LblPSSlcpB.setVisible(False)#setText("")
                            self.drift_ui.EdtPSSlcpB.setVisible(False)#setText("")
                            self.drift_ui.LblPSSrcpB.setVisible(False)#setText("")
                            self.drift_ui.EdtPSSrcpB.setVisible(False)#setText("")

                            

                        elif ("D" in self.data["BEAMTYPE"]):

                            # Activate buttons
                            self.drift_ui.LblPSSlcpA.setText("A LCP PSS")
                            self.drift_ui.EdtPSSlcpA.setText(
                                str(hartPSS[pssInd]))
                            self.drift_ui.LblPSSlcpB.setText("B LCP PSS")
                            self.drift_ui.EdtPSSlcpA.setText(
                                str(hartPSS[pssInd]))
                            self.drift_ui.LblPSSrcpA.setText("A RCP PSS")
                            self.drift_ui.EdtPSSrcpA.setText(
                                str(hartPSS[pssInd]))
                            self.drift_ui.LblPSSrcpB.setText("B RCP PSS")
                            self.drift_ui.EdtPSSrcpB.setText(
                                str(hartPSS[pssInd]))

                elif "D" in self.data["BEAMTYPE"]:
                    pass

            else:
                pass

        self.write("Starting data reduction",'info')

    def fit_data(self):
        """ Fit the drift scan. """

        # Open plot manager
        plotIndex = self.get_plot_index()

        # Get order to fit
        order = self.get_fit_order()
        fit_type = self.get_fit_type()

        if fit_type == "Polynomial":

            # Get location we are fitting
            fit_loc = self.get_fit_loc()

            # Check the selected fit type
            if fit_loc == "Base":

                # Get base locations
                if len(self.Canvas.click_index) == 0:
                    self.write("No points selected yet",'info')
                    self.clear_selection()

                else:
                    self.write("Fitting the baseline",'info')

                    # ensure we have a minimum of 4 points for the base fit
                    if len(self.Canvas.click_index) < 4 or len(self.Canvas.click_index) % 2 != 0:
                        self.write("Need a minimum of 4 points or an even set to fit a baseline.\nClicked points reset, pick new points",'info')
                        self.clear_selection()
                        self.write(f"selected points: {self.Canvas.click_index}",'info')
                        self.Canvas.click_index = []

                    else:

                        # prep Canvas and perform fit
                        self.Canvas.clear_canvas()        # Update figures

                        # Perform baseline fit
                        self.write("Fitting "+fit_loc+" with order "+str(order)+" "+fit_type,'info')
                        self.reset_peak(plotIndex)
                        self.fit_base(order, plotIndex)
                        self.update_base_fit(plotIndex)    # Update plot
                        self.peak_is_fit = 0
                        
            elif fit_loc == "Peak":

                    self.write("Fitting peak with poly",'info')

                    # Get base locations
                    if len(self.Canvas.click_index) == 0:
                        self.write("No points selected yet. ","info")
                        self.peak_is_fit = 0
                        self.clear_selection()

                    else:
                        # ensure we have a minimum of 2 points for the peak fit
                        if len(self.Canvas.click_index) < 2 or len(self.Canvas.click_index) % 2 != 0:
                            self.write("Need a minimum of 2 points or an even set to fit a peak.\nClicked points reset, pick new points",'info')

                            self.peak_is_fit = 0
                            self.Canvas.click_index = []
                            self.clear_selection()

                        else:

                            # Perform peak fit
                            self.write("Fitting "+fit_loc+" with order "+str(order)+" "+fit_type, 'info')

                            #CHECK IF DUAL BEAM
                            if self.data['RADIOMETER'] == "Dicke Switched":
                                
                                # Update figures
                                self.Canvas.clear_dual_canvas()
                                self.fit_dual_peak(order, plotIndex)
                                self.update_dual_peak_fit(plotIndex)  
                            else:
                                # Update figures
                                self.Canvas.clear_canvas()
                                self.fit_peak(order, plotIndex)
                                self.update_peak_fit(plotIndex)    # Update plot
                            
                            self.peak_is_fit = 1
                            #self.view_fit()
                            self.Canvas.click_index = []
                            #self.clear_selection()

        '''elif fit_type == "Gaussian":

            msg_wrapper("info", self.log.info,
                        "Fitting peak with gaussian\n")

            # Get base locations
            if len(self.Canvas.click_index) == 0:
                msg_wrapper("info", self.log.info,
                            "No points selected yet. ")
               
                self.peak_is_fit = 0

            else:

                # ensure we have a minimum of 2 points for the peak fit
                if len(self.Canvas.click_index) < 2 or len(self.Canvas.click_index) % 2 != 0:
                    msg_wrapper("info", self.log.info,
                    "We need a minimum of 2 points or an even set to fit a baseline")
                    msg_wrapper("info", self.log.info,
                                "Clicked points reset, pick new points")
               
                    self.peak_is_fit = 0
                    self.Canvas.click_index = []

                else:

                    # Perform baseline fit
                    
                    self.fit_peak(order, plotIndex)

                    # Update figures
                    self.Canvas.clear_canvas()
                    self.update_peak_fit(plotIndex)    # Update plot
                    self.peak_is_fit = 1
                    self.view_fit()
                    self.Canvas.click_index = []
        '''

    def open_file_name_dialog(self, ext):
        """ Open file. Had to use this 
        to avoid segmentation fault: 11 error
        """

        msg_wrapper("debug", self.log.debug, "Open file name dialog")

        # options = QtWidgets.QFileDialog.Options()
        # options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", "Fits Files ("+ext+");;Fits Files ("+ext+")")#, options=options)

        if file_name:
            return file_name
        else:
            return

    # === connections for fit_data() ===
    def get_fit_type(self):
        """ Get fit type from combobox."""

        msg_wrapper("debug", self.log.debug, "Get fit type")
        return self.drift_ui.ComboBoxFitType.currentText()

    def get_fit_loc(self):
        """ Get fit location from combobox. """

        msg_wrapper("debug", self.log.debug, "Get fit location")
        return self.drift_ui.ComboBoxFitLoc.currentText()

    def get_fit_order(self):
        """ Get order for fitting polynomial."""
        
        msg_wrapper("debug", self.log.debug, "Get polynomial order")
        return int(self.drift_ui.ComboBoxFitOrder.currentText())

    def get_plot_index(self):
        """ Get the current plot index  """

        msg_wrapper("debug", self.log.debug,
                    f'Getting plot index {self.drift_ui.ComboBoxPlotType.currentIndex()}\n')
        return int(self.drift_ui.ComboBoxPlotType.currentIndex())

    def clear_selection(self):
        """ Clear selections made for current scan. """

        self.write("Clearing selections for current scan.",'info')

        # Get the plot index
        plotIndex = self.get_plot_index()

        # Set plot title
        title = self.set_title()
        
        self.Canvas.plot_figure(self.x, self.y, title, "Cleared selection")
        self.Canvas.plot_residual()
        self.set_fit_parmeters()
        self.set_flags()

    def reset_plot(self):
        """ Reset figure to default settings. """

        msg="Reset figure to default settings"
        self.write(msg,'info')
        
        # Get the plot index
        plotIndex = self.get_plot_index()

        self.fit_done = 0

        self.reset_previous_fits(plotIndex)

        # Reset x and y to factory settings of current plot
        self.reset_xy(plotIndex)

        # Set plot title
        title = self.set_title()
        
        self.Canvas.plot_figure(self.x, self.y, title, "Raw data")
        self.Canvas.plot_residual()
        self.set_fit_parmeters()
        self.set_flags()
        
       
        self.reset_peak(plotIndex)

    def reset_peak(self,plotIndex):
        """ Reset previous peak fits. """ 

        msg_wrapper("debug", self.log.debug, 'reset peak fit')

        if self.data['BEAMTYPE'] == "13.0S":
            if plotIndex == 0:
                msg_wrapper("debug", self.log.debug, "Data for LCP")
                self.reset_dict("OLTA", "")
            else:
                msg_wrapper("debug", self.log.debug, "Data for RCP")
                self.reset_dict("ORTA", "")

        elif self.data["BEAMTYPE"] == "02.5S" or self.data["BEAMTYPE"] == "01.3S":
            msg_wrapper("debug", self.log.debug, "Fit stats for " +
                        self.beamName[plotIndex]+" data")

            if plotIndex == 0:
                self.reset_dict("SLTA", "NLTA")

            elif plotIndex == 1:
                self.reset_dict("NLTA", "OLTA")

            elif plotIndex == 2:
                self.reset_dict("OLTA", "SRTA")

            elif plotIndex == 3:
                self.reset_dict("SRTA", "NRTA")

            elif plotIndex == 4:
                self.reset_dict("NRTA", "ORTA")

            elif plotIndex == 5:
                self.reset_dict("ORTA", "")

        elif "D" in self.data["BEAMTYPE"]:
            msg_wrapper("debug", self.log.debug, "Fit stats for " +
                        self.beamName[plotIndex]+" data")

            if plotIndex == 0:
                self.reset_dict("ASLTA", "ANLTA")

            elif plotIndex == 1:
                self.reset_dict("ANLTA", "AOLTA")

            elif plotIndex == 2:
                self.reset_dict("AOLTA", "ASRTA")

            elif plotIndex == 3:
                self.reset_dict("ASRTA", "ANRTA")

            elif plotIndex == 4:
                self.reset_dict("ANRTA", "AORTA")

            elif plotIndex == 5:
                self.reset_dict("AORTA", "")

    def fit_base(self, order, plotIndex):
        """ Fit the baseline. """

        self.write("Fitting baseline @ "+str(self.Canvas.click_index))
        self.write("Fit points: "+str(self.x[self.Canvas.click_index]))

        # Create tags for the plot file
        self.tag = self.create_tag(plotIndex)

        # Get baseline fitting locations
        self.xb, self.yb = fit.get_base_pts(
            self.x, self.y, self.Canvas.click_index)

        # Fit the baseline
        self.dataModel, self.driftModel, self.driftRes, self.base_rms, self.driftCoeffs = fit.correct_drift(
            self.xb, self.yb, self.x, self.log,order)

        # Set the slope,rms,x and y values
        self.baseSlope = self.driftCoeffs[0]
        self.write(
            "y = {:.3f}x + {:.3f}".format(self.baseSlope, self.driftCoeffs[1]))

        self.y = np.array(self.y - self.dataModel)
        self.x = np.array(self.x)

        # update fit parameter
        self.base_is_fit = 1

    def update_base_fit(self, plotIndex):
        """ Updates figure on Canvas """

        # Update plot
        self.write("Figure updated with fit")

        plotTitle = self.set_title()
        pi = self.Canvas.click_index
        self.update_plot(self.x, self.y, plotTitle, self.driftRes,
                         "Data: baseline corrected", label2="")
        pi = []

    def update_plot(self, x, y, title, res, label="", label2=""):
        """ Update the current figure. """

        msg_wrapper("debug", self.log.debug,
                    "Update the current figure.")

        self.Canvas.plot_figure(
            x, y, title, label)
        self.Canvas.plot_residual(res, label=label2)

    def fit_peak(self, order, plotIndex):
        """ Fit peak """

        self.write("Fitting the Peak","info")
      
        self.xp, self.yp = fit.get_base_pts(
            self.x, self.y, self.Canvas.click_index)
        self.write("locs: "+str(self.x[self.Canvas.click_index]),'info')


        if self.drift_ui.ComboBoxFitType.currentText() == "Polynomial":

            # poly fit
            self.write("Fitting a polynomial",'info')

            degree = int(self.drift_ui.ComboBoxFitOrder.currentText())

            peak_res, peakRms, peakModel  = fit.fit_poly_peak(
                self.xp, self.yp, order=degree, log=self.log)  # Fit the peak

            peakLoc = self.xp[((np.where(peakModel == max(peakModel))[0])[0])]

            self.peakFit = max(peakModel)
            self.peakRms = peakRms
            self.peakRes = peak_res
            self.peakModel = peakModel 
            self.peakLoc = peakLoc

            # Calculate s2n
            try:
                # calculate s2n using drift residual
                self.s2n = fit.sig_to_noise(self.peakFit, self.driftRes,self.log)
            except Exception:
                # else calculate s2n using peak fit residual
                # if base is not corrected first
                self.s2n = fit.sig_to_noise(self.peakFit, self.peakRes,self.log)

        '''elif self.drift_ui.ComboBoxFitType.currentText() == "Gaussian":

            # gauss fit
            msg_wrapper("info", self.log.info,
                        "Fitting a gaussian")

            p0 = [max(self.yp), self.xp[np.argmax(self.yp)],
                  self.data["HPBW"]/2]
            gaus_coeff, var_matrix, gauss_fit, err_gauss_fit, res = fit.fit_gauss(self.xp, self.yp, p0)  # Fit the peak

            peakLoc = self.x[((np.where(peakModel == max(peakModel))[0])[0])]

            self.peakFit = max(gauss_fit)
            self.peakRms = err_gauss_fit
            self.peakRes = res
            self.peakModel = gauss_fit
            self.peakLoc = peakLoc

            # Calculate s2n
            try:
                # calculate s2n using drift residual
                self.s2n = fit.sig_to_noise(self.peakFit, self.driftRes)
            except Exception:
                # else calculate s2n using peak fit residual
                # if base is not corrected first
                self.s2n = fit.sig_to_noise(self.peakFit, self.peakRes)

         '''

        # Calculate PSS
        self.update_fit_parmeters()
        self.write("Ta = {:.3f} +- {:.3f} [K]".format(self.peakFit, self.peakRms),'info')

    def fit_dual_peak(self, order, plotIndex):
        """ Fit dual peaks. """

        self.write("Fitting the Peaks",'info')

        # get values of both peak click indeces
        p1ClickIndex, p2ClickIndex = [], []
        scan_mid=int(len(self.x)/2)
        [p1ClickIndex.append(n) for n in self.Canvas.click_index if n <= scan_mid]
        [p2ClickIndex.append(n) for n in self.Canvas.click_index if n > scan_mid]

        # fit the peaks
        if len(p1ClickIndex) !=0 and len(p2ClickIndex) !=0:
            self.fit_p1(p1ClickIndex)
            self.fit_p2(p2ClickIndex)

        if len(p1ClickIndex) !=0 and len(p2ClickIndex) ==0: 
            self.fit_p1(p1ClickIndex)
            self.fit_p2([])

        if len(p1ClickIndex) ==0 and len(p2ClickIndex) !=0:
            self.fit_p1([])
            self.fit_p2(p2ClickIndex)


        # Calculate PSS
        self.update_fit_parmeters()

    def fit_p1(self,locs):
        """ Fitting peak 1. """

        # Fit peak with selected points
        if len(locs) == 0:
            # no data, skip fit
            self.write("Peak 1 not fit",'info')
            self.peakFitA = np.nan
            self.peakRmsA = np.nan
            self.peakResA = np.nan
            self.peakModelA = np.nan
            self.peakLocA = np.nan
            self.s2nA = np.nan
            self.xpA = []
            self.ypA = []

        else:
            if len(locs) % 2 != 0:
                self.write("Need a minimum of 2 points or an even set on peakA in order to fit the peak.\nClicked points reset, pick new points",'info')

                self.peak_is_fit = 0
                self.Canvas.click_index = []
                self.clear_selection()
            else:
                self.xpA, self.ypA = fit.get_base_pts(
                    self.x, self.y, locs)
                self.write("locs: "+str(self.x[locs]),'info')
        
                if self.drift_ui.ComboBoxFitType.currentText() == "Polynomial":

                    # poly fit
                    self.write("Fitting a polynomial",'info')

                    degree = int(self.drift_ui.ComboBoxFitOrder.currentText())

                    peak_resA, peakRmsA, peakModelA = fit.fit_poly_peak(
                        self.xpA, self.ypA, order=degree, log=self.log)  # Fit the peak

                    peakLocA = self.x[((np.where(peakModelA == min(peakModelA))[0])[0])]

                    self.peakFitA = min(peakModelA)
                    self.peakRmsA = peakRmsA
                    self.peakResA = peak_resA
                    self.peakModelA = peakModelA
                    self.peakLocA = peakLocA

                    # Calculate s2n
                    try:
                        # calculate s2n using drift residual
                        self.s2nA = fit.sig_to_noise(
                            self.peakFitA, self.driftResA, self.log)
                    except Exception:
                        # else calculate s2n using peak fit residual
                        # if base is not corrected first
                        self.s2nA = fit.sig_to_noise(
                        self.peakFitA, self.peakResA, self.log)

    def fit_p2(self, locs):
        """ Fitting peak 2. """

        if len(locs) == 0:
            # no data, skip fit
            self.write("Peak 2 not fit",'info')
            self.peakFitB = np.nan
            self.peakRmsB = np.nan
            self.peakResB = np.nan
            self.peakModelB = np.nan
            self.peakLocB = np.nan
            self.s2nB = np.nan
            self.xpB = []
            self.ypB = []

        else:
            # Fit peak with selected points
            if len(locs) % 2 != 0:
                self.write(
                    "Need a minimum of 2 points or an even set on peakA in order to fit the peak.\nClicked points reset, pick new points",'info')

                self.peak_is_fit = 0
                self.Canvas.click_index = []
                self.clear_selection()
            else:
                self.xpB, self.ypB = fit.get_base_pts(
                    self.x, self.y, locs)
                self.write("locs: "+str(self.x[locs]),'info')

                if self.drift_ui.ComboBoxFitType.currentText() == "Polynomial":

                    # poly fit
                    self.write("Fitting a polynomial",'info')

                    degree = int(self.drift_ui.ComboBoxFitOrder.currentText())

                    peak_resB, peakRmsB, peakModelB = fit.fit_poly_peak(
                        self.xpB, self.ypB, order=degree, log=self.log)  # Fit the peak

                    peakLocB = self.x[(
                        (np.where(peakModelB == max(peakModelB))[0])[0])]

                    self.peakFitB = max(peakModelB)
                    self.peakRmsB = peakRmsB
                    self.peakResB = peak_resB
                    self.peakModelB = peakModelB
                    self.peakLocB = peakLocB

                    # Calculate s2n
                    try:
                        # calculate s2n using drift residual
                        self.s2nB = fit.sig_to_noise(
                            self.peakFitB, self.driftResB, self.log)
                    except Exception:
                        # else calculate s2n using peak fit residual
                        # if base is not corrected first
                        self.s2nB = fit.sig_to_noise(
                            self.peakFitB, self.peakResB, self.log)

    def update_peak_fit(self, plotIndex):
        """
        Updates figure on Canvas
        """

        self.write("Update peak fit ",'info')

        plotTitle = self.set_title()

        self.drift_ui.ComboBoxFitOrder.currentText()

        self.Canvas.plot_residual(self.peakRes, label="Peak residual")
        self.Canvas.plot_peak(self.xp, self.peakModel, self.peakFit,
                              self.peakRms, self.x, self.y,  plotTitle)

    def update_dual_peak_fit(self, plotIndex):
        """
        Updates figure on Canvas
        """

        self.write("Update peak fit",'info')

        plotTitle = self.set_title()

        self.drift_ui.ComboBoxFitOrder.currentText()

        self.Canvas.plot_dual_residuals(self.peakResA, self.peakResB,label="Peak residual")

        if len(self.xpA) == 0 and len(self.xpB) != 0:
            self.Canvas.plot_dual_peaks([], [], 
                0.0, 0.0, self.xpB, self.peakModelB, 
                self.peakFitB, self.peakRmsB, self.x, self.y, plotTitle)

        elif len(self.xpA) != 0 and len(self.xpB) == 0:
            self.Canvas.plot_dual_peaks(self.xpA, self.peakModelA,
                                        self.peakFitA, self.peakRmsA, [], [],
                                        0.0, 0.0, self.x, self.y, plotTitle)

        elif len(self.xpA) != 0 and len(self.xpB) != 0:
            self.Canvas.plot_dual_peaks(self.xpA, self.peakModelA, 
                self.peakFitA, self.peakRmsA, self.xpB, self.peakModelB, 
                self.peakFitB, self.peakRmsB, self.x, self.y, plotTitle)

    def view_fit(self):
        """ View current fit info"""

        self.write("Viewing fit information...",'info')

        plotIndex = self.get_plot_index()

        if self.data['BEAMTYPE'] == "13.0S":

            if plotIndex == 0:
                msg_wrapper("debug", self.log.debug, "Data for LCP")
                self.iter_dict("OLTA", "ORTA")
            else:
                msg_wrapper("debug", self.log.debug, "Data for RCP")
                self.iter_dict("ORTA", "")

        elif self.data["BEAMTYPE"] == "02.5S" or self.data["BEAMTYPE"] == "01.3S":

            plotIndex = self.get_plot_index()
            if plotIndex == 0:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("SLTA", "NLTA")
            elif plotIndex == 1:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data", 'info')
                self.iter_dict("NLTA", "OLTA")
            elif plotIndex == 2:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("OLTA", "SRTA")
            elif plotIndex == 3:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("SRTA", "NRTA")
            elif plotIndex == 4:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("NRTA", "ORTA")
            elif plotIndex == 5:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("ORTA", "")
        
        elif "D" in self.data["BEAMTYPE"]:

            plotIndex = self.get_plot_index()

            if plotIndex == 0:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("ASLTA", "ANLTA")
            elif plotIndex == 1:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("ANLTA", "AOLTA")
            elif plotIndex == 2:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("AOLTA", "ASRTA")
            elif plotIndex == 3:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("ASRTA", "ANRTA")
            elif plotIndex == 4:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("ANRTA", "AORTA")
            elif plotIndex == 5:
                self.write("Fit stats for "+self.beamName[plotIndex]+" data",'info')
                self.iter_dict("AORTA", "")

    def reset_status(self):
        self.status=[0,0,0,0,0,0]

    def view_status(self):
        print("# Status: ",self.status)

    def save_fit(self):
        """
        Save the fit. If the data has been previously saved
        overwrite the previous fit.
        """

        # Update plot settings
        obj = self.data['OBJECTTYPE']
        beam = self.data['BEAMTYPE']

        plotIndex = self.get_plot_index()
        
        if "S" in beam:

            if self.base_is_fit == 0 and self.peak_is_fit == 0:

                
                # Set flag
                self.set_flags()

                # No fit done on figure
                reply = self.popUp(self.popup_msg["noFit"])
                if reply == "yes":
                    self.update_fit_parmeters()
                    self.plot_new_fig()
                    self.status[plotIndex] = 2
                else:
                    self.write("No fit done",'info')
                self.write("Saving fit> Fit status: %d%d%d" % (
                self.base_is_fit, self.peak_is_fit, self.plot_is_smoothed),"info")

            elif self.base_is_fit == 0 and self.peak_is_fit == 1:

                # Set flag
                self.set_flags(101)

                # Only peak fit done on figure
                reply = self.popUp(self.popup_msg["noBase"])
                if reply == "yes":
                    self.update_fit_parmeters()
                    self.plot_new_fig()
                    self.status[plotIndex] = 1
                else:
                    pass
                self.write("Saving fit> Fit status: %d%d%d" % (
                self.base_is_fit, self.peak_is_fit, self.plot_is_smoothed),"info")

            elif self.base_is_fit == 1 and self.peak_is_fit == 0:
                # Only base fit done on figure
                # Create a popup window to ask if user if sure about saving this

                # Set flag
                self.set_flags(110)
                print(self.data['OLFLAG'])
                reply = self.popUp(self.popup_msg["noPeak"])

                if reply == "yes":
                    self.update_fit_parmeters()
                    self.plot_new_fig()
                    self.status[plotIndex] =  0
                    #print(self.status, plotIndex)
                else:
                    pass
                self.write("Saving fit> Fit status: %d%d%d" % (
                self.base_is_fit, self.peak_is_fit, self.plot_is_smoothed),"info")

            elif self.base_is_fit == 1 and self.peak_is_fit == 1:
                # Both base and peak were fitted

                # Set flag
                self.set_flags(111)
                self.update_fit_parmeters()
                self.view_fit()
                self.plot_new_fig()
                self.status[plotIndex] = 1

                self.write("Saving fit> Fit status: %d%d%d" % (
                self.base_is_fit, self.peak_is_fit, self.plot_is_smoothed),"info")

        elif "D" in beam:
            # Save dual beam fits

            if self.base_is_fit == 0 and self.peak_is_fit == 0:

                # Set flag
                self.set_flags()

                # No fit done on figure
                reply = self.popUp(self.popup_msg["noFit"])
                if reply == "yes":
                    self.update_fit_parmeters()
                    self.plot_new_fig()
                    self.status[plotIndex] = 2
                else:
                    self.write("No fit done",'info')

            elif self.base_is_fit == 0 and self.peak_is_fit == 1:

                # Set flag
                self.set_flags(101)

                # Only peak fit done on figure
                reply = self.popUp(self.popup_msg["noBase"])
                if reply == "yes":
                    self.update_fit_parmeters()
                    self.plot_new_fig()
                    self.status[plotIndex] = 1
                else:
                    pass

            elif self.base_is_fit == 1 and self.peak_is_fit == 0:
                # Only base fit done on figure
                # Create a popup window to ask if user if sure about saving this

                # Set flag
                self.set_flags(110)
                reply = self.popUp(self.popup_msg["noPeak"])

                if reply == "yes":
                    self.update_fit_parmeters()
                    self.plot_new_fig()
                    self.status[plotIndex] = 0
                else:
                    pass

            elif self.base_is_fit == 1 and self.peak_is_fit == 1:
                # Both base and peak were fitted

                # Set flag
                self.set_flags(111)
                self.update_fit_parmeters()
                self.view_fit()
                self.plot_new_fig()
                self.status[plotIndex] = 1

        else:
            self.write("Cant' save data, basefit not done",'info')

        print(self.status)
        #sys.exit()

    def calc(self):
        """ Calculate PSS of Flux"""

        if (self.data["OBJECTTYPE"]) == "CAL":
            self.calc_pss_()
        else:
            self.calc_flux()

    def calc_flux(self):
        """ Estimate the flux density for a target source given a PSS. """

        # need to have already calculated or entered a pss
        print(self.data["BEAMTYPE"])
        #sys.exit()

        if (self.data["OBJECTTYPE"]) == "TAR":
            if self.data["BEAMTYPE"] == "13.0S":
                # check if peak has been fit
                if self.peak_is_fit == 1:
                    try:
                        self.pss=float(self.drift_ui.EdtPSSlcpA.text())
                        self.flux = self.peakFit*self.pss
                    except:
                        print("The entered pss is invalid\n")
                else:
                    print(f"peak hasn't been fit yet, peak_is_fit: {self.peak_is_fit}\n")

            if self.data["BEAMTYPE"] == "03.5D":

                # check if peak has been fit
                if self.peak_is_fit == 1:
                    try:
                        # Activate buttons
                            # self.drift_ui.LblPSSlcpA.setText("A LCP PSS")
                            # self.drift_ui.EdtPSSlcpA.setText(
                            #     str(hartPSS[pssInd]))
                            # self.drift_ui.LblPSSlcpB.setText("B LCP PSS")
                            # self.drift_ui.EdtPSSlcpA.setText(
                            #     str(hartPSS[pssInd]))
                            # self.drift_ui.LblPSSrcpA.setText("A RCP PSS")
                            # self.drift_ui.EdtPSSrcpA.setText(
                            #     str(hartPSS[pssInd]))
                            # self.drift_ui.LblPSSrcpB.setText("B RCP PSS")
                            # self.drift_ui.EdtPSSrcpB.setText(
                            #     str(hartPSS[pssInd]))

                        self.pssALCP=float(self.drift_ui.EdtPSSlcpA.text())
                        self.flux = self.peakFit*self.pss
                    except:
                        print("The entered pss is invalid\n")
                else:
                    print(f"peak hasn't been fit yet, peak_is_fit: {self.peak_is_fit}\n")
        else:
            self.write("invalid object type: "+ self.data["BEAMTYPE"],'warning')

    def calc_pss_(self):
        """ Calculate the PSS. """
        if (self.data["OBJECTTYPE"]) == "CAL":
            self.write("beam: "+ self.data["BEAMTYPE"],'info')

            # Calculate PSS for lcp
            if self.data["BEAMTYPE"] == "01.3S":

                plotIndex = 2
                pss, dpss, pc, tcorr, dtcorr, appEff = cp.calc_pc_pss(
                    plotIndex, self.data["SLTA"], self.data["SLDTA"], self.data["NLTA"], self.data["NLDTA"], self.data["OLTA"], self.data["OLDTA"], self.data['TOTAL_PLANET_FLUX_D'], self.data)

                self.data['OLAPPEFF'] = appEff
                self.set_lcp_pss(pss, dpss, pc, tcorr, dtcorr,appEff)

                self.write("Calculating LCP PSS",'info')
                self.write(f'PSS: {pss}, errPSS: {dpss}','info')
                self.write(f'Pointing corrected Ta: {tcorr}, err: {dtcorr}','info')

            elif self.data["BEAMTYPE"] == "02.5S":

                plotIndex = 2
                pss, dpss, pc, tcorr, dtcorr, appEff = cp.calc_pc_pss(
                    plotIndex, self.data["SLTA"], self.data["SLDTA"], self.data["NLTA"], self.data["NLDTA"], self.data["OLTA"], self.data["OLDTA"], self.data['FLUX'], self.data)

                self.data['OLAPPEFF'] = appEff
                self.set_lcp_pss(pss, dpss, pc, tcorr, dtcorr,appEff)

                self.write("Calculating LCP PSS",'info')
                self.write(f'PSS: {pss}, errPSS: {dpss}','info')
                self.write(f'Pointing corrected Ta: {tcorr}, err: {dtcorr}','info')

            elif self.data["BEAMTYPE"] == "13.0S":

                # calculate 2280 PSS
                try:
                    self.set_pss(self.peakFit, self.peakRms)
                except:
                    print("Peak has not been fit yet")

            elif "D" in self.data["BEAMTYPE"]:
                # calculate dual beam PSS @ 4800 or 8280 MHz
                self.set_db_pss()

            # calculate pss for rcp
            if self.data["BEAMTYPE"] == "01.3S":
                plotIndex = 5
                pss, dpss, pc, tcorr, dtcorr , appEff= cp.calc_pc_pss(
                    plotIndex, self.data["SRTA"], self.data["SRDTA"], self.data["NRTA"], self.data["NRDTA"], self.data["ORTA"], self.data["ORDTA"],  self.data['TOTAL_PLANET_FLUX_D'], self.data)
                self.data['ORAPPEFF'] = appEff
                self.set_rcp_pss(pss, dpss, pc, tcorr, dtcorr,appEff)

                self.write("Calculating RCP PSS",'info')
                self.write(f'PSS: {pss}, errPSS: {dpss}','info')
                self.write(f'Pointing corrected Ta: {tcorr}, err: {dtcorr}','info')
            
            elif self.data["BEAMTYPE"] == "02.5S":
                plotIndex = 5
                pss, dpss, pc, tcorr, dtcorr, appEff = cp.calc_pc_pss(
                    plotIndex, self.data["SRTA"], self.data["SRDTA"], self.data["NRTA"], self.data["NRDTA"], self.data["ORTA"], self.data["ORDTA"],  self.data['FLUX'], self.data)
                self.data['ORAPPEFF'] = appEff
                self.set_rcp_pss(pss, dpss, pc, tcorr, dtcorr,appEff)

                self.write("Calculating RCP PSS",'info')
                self.write(f'PSS: {pss}, errPSS: {dpss}','info')
                self.write(f'Pointing corrected Ta: {tcorr}, err: {dtcorr}','info')

            elif self.data["BEAMTYPE"] == "13.0S":
                # calculate 2280 PSS
                try:
                    self.set_pss(self.peakFit, self.peakRms)
                except:
                    print("Peak has not been fit yet")
        else:
            pass

    def set_lcp_pss(self, pss, dpss, pc, ta, dta,appEff):
        """ Set the PSS for the LCP drift scan """
        self.data["OLPSS"] = pss
        self.data["OLDPSS"] = dpss
        self.data["OLPC"] = pc
        self.data["COLTA"] = ta
        self.data["COLDTA"] = dta
        self.data["OLAPPEFF"] = appEff

    def set_rcp_pss(self, pss, dpss, pc, ta, dta,appEff):
        """ Set the PSS for the RCP drift scan """
        self.data["ORPSS"] = pss
        self.data["ORDPSS"] = dpss
        self.data["ORPC"] = pc
        self.data["CORTA"] = ta
        self.data["CORDTA"] = dta
        self.data["ORAPPEFF"] = appEff

    def filter_data(self):
        """ Filter/smooth the data """

        if self.drift_ui.ComboBoxFilterType.currentText() == "rms cuts":

            self.write("Performing rms cuts",'info')
            # ================================================
            # Clean the data using rms cuts
            # ================================================

            scanLen = len(self.x)
            if self.data["CENTFREQ"] <= 3000:
                noTotScans = 2
            else:
                noTotScans = 6

            # spline the data
            spl = fit.spline(self.x, self.y)

            scanRes, self.x, self.y, self.res, finspl, self.rmsb, self.rmsa = fit.cleanRmsCuts2(
                spl, self.x, self.y, scanLen,self.log)

            self.write(f'RMS before: after -> {self.rmsb}: {self.rmsa,}','info')

            self.Canvas.clear_canvas()  # Update figures
            self.update_plot(self.x, self.y, "After rms cuts",
                             self.res, "smoothed data", "smoothed residual")    # Update plot

            #update rms before and after
            self.update_smoothing_params()
            self.plot_is_smoothed = 1

        else:
            msg_wrapper("debug", self.log.debug, "Smoothing window")

            smooth_type = self.drift_ui.ComboBoxFilterType.currentText()

            if smooth_type == "":

                self.write("Please select a filter.")
                self.plot_is_smoothed = 0

            else:
                # TODO: Select a better smoothing algorithm

                # Get value from smoothing window
                window = self.drift_ui.EdtFilteringWindow.text()

                try:
                    window = int(window)
                except Exception as e:
                    self.write("You need to enter a window width")

                if type(window).__name__ == "int":

                    smoothed = fit.filter_scans(self.y, window, smooth_type)

                    self.x = np.arange(0, len(smoothed), 1)
                    self.y = smoothed
                    self.Canvas.clear_canvas()            
                    self.update_plot(self.x, self.y, "After " +
                                    smooth_type+" smoothing", [])

                    self.plot_is_smoothed = 1

    def write(self,msg,logType=""):
        """ Write to screen and gui """

        if logType=="info":
            msg_wrapper("info", self.log.info, msg)
        else:
            msg_wrapper("debug", self.log.debug, msg)
     
    def choose_plot(self):
        """ Select the plot to work with. """

        msg_wrapper("debug", self.log.debug, "Choose plot")

        self.fit_done = 0

        plotIndex = self.get_plot_index()

        self.reset_previous_fits(plotIndex)

        # Set default to base fit type
        if self.drift_ui.ComboBoxFitLoc.currentText() != "Base":
            self.drift_ui.ComboBoxFitLoc.setCurrentIndex(0)

        if len(self.beamName) == 2:

            # Clear the Canvas
            self.Canvas.clear_canvas()

            # Plot figure
            self.x = self.scans["OFFSET"]
            scanName = self.beamName[plotIndex]
            self.y = self.scans[scanName]

            self.Canvas.plot_figure(self.x, self.y, label="data")
            self.Canvas.plot_residual()
            self.set_fit_parmeters()

        elif len(self.beamName) == 6:

            # Clear the Canvas
            self.Canvas.clear_canvas()

            # Plot figure
            self.write("Plotting: " +
                     self.drift_ui.ComboBoxPlotType.currentText(),'info')
            self.x = self.scans["OFFSET"]
            scanName = self.beamName[plotIndex]
            print(scanName.strip("_"), plotIndex, self.scans.keys())
            self.y = self.scans[scanName]

            self.Canvas.plot_figure(self.x, self.y,label="data")
            self.Canvas.plot_residual()
            self.set_fit_parmeters()

            if plotIndex == 0:
                # plot 1,2
                ind=1
                ind2=2
                x=self.scans['OFFSET']
                y=self.scans[self.beamName[ind]]
                y1=self.scans[self.beamName[ind2]]
                self.secondaryCanvas.plot_figure(x,y,y1,label1=self.beamName[ind],label2=self.beamName[ind2])
            
            elif plotIndex == 1:
                # plot 0,2
                ind=0
                ind2=2
                x=self.scans['OFFSET']
                y=self.scans[self.beamName[ind]]
                y1=self.scans[self.beamName[ind2]]
                self.secondaryCanvas.plot_figure(x,y,y1,label1=self.beamName[ind],label2=self.beamName[ind2])
            
            elif plotIndex == 2:
                # plot 0,1
                ind=0
                ind2=1
                x=self.scans['OFFSET']
                y=self.scans[self.beamName[ind]]
                y1=self.scans[self.beamName[ind2]]
                self.secondaryCanvas.plot_figure(x,y,y1,label1=self.beamName[ind],label2=self.beamName[ind2])
            
            elif plotIndex == 3:
                # plot 4,5
                ind=4
                ind2=5
                x=self.scans['OFFSET']
                y=self.scans[self.beamName[ind]]
                y1=self.scans[self.beamName[ind2]]
                self.secondaryCanvas.plot_figure(x,y,y1,label1=self.beamName[ind],label2=self.beamName[ind2])
            
            elif plotIndex == 4:
                # plot 3,5
                ind=3
                ind2=5
                x=self.scans['OFFSET']
                y=self.scans[self.beamName[ind]]
                y1=self.scans[self.beamName[ind2]]
                self.secondaryCanvas.plot_figure(x,y,y1,label1=self.beamName[ind],label2=self.beamName[ind2])
            
            elif plotIndex == 5:
                # plot 3,4
                ind=3
                ind2=4
                x=self.scans['OFFSET']
                y=self.scans[self.beamName[ind]]
                y1=self.scans[self.beamName[ind2]]
                self.secondaryCanvas.plot_figure(x,y,y1,label1=self.beamName[ind],label2=self.beamName[ind2])
            
        else:
            self.write("There are no scans provided. ",'info')

    def update_fit_parmeters(self):
        """ Update fit parameters. """

        msg_wrapper("debug", self.log.debug, "Update fit parameters.")

        plotIndex = self.get_plot_index()

        if len(self.beamName) == 2:

            if "13.0S" in self.data["BEAMTYPE"]:
                if self.beamName[plotIndex] == "ONLCP":
                    data_update = ["OLTA", "OLDTA", "OLS2N",
                                   "OLRMSB", "OLRMSA", "OLBSLOPE", "OLBSRMS", "OLTAPEAKLOC", "OLAPPEFF", "OLPSS", "OLDPSS"]
                    self.set_data(data_update)

                else:
                    data_update = ["ORTA", "ORDTA", "ORS2N",
                                   "ORRMSB", "ORRMSA", "ORBSLOPE", "ORBSRMS", "ORTAPEAKLOC", "ORAPPEFF", "ORPSS", "ORDPSS"]
                    self.set_data(data_update)
            else:
                pass
        else:
            if "S" in self.data["BEAMTYPE"]:

                if self.beamName[plotIndex] == "HPSLCP":
                    data_update = ["SLTA", "SLDTA", "SLS2N",
                                   "SLRMSB", "SLRMSA", "SLBSLOPE", "SLBSRMS", "SLTAPEAKLOC"]
                    self.set_nb_data(data_update)

                elif self.beamName[plotIndex] == "HPNLCP":
                    data_update = ["NLTA", "NLDTA", "NLS2N",
                                   "NLRMSB", "NLRMSA", "NLBSLOPE", "NLBSRMS", "NLTAPEAKLOC"]
                    self.set_nb_data(data_update)

                elif self.beamName[plotIndex] == "ONLCP":
                    data_update = ["OLTA", "OLDTA", "OLS2N",
                                   "OLRMSB", "OLRMSA", "OLBSLOPE", "OLBSRMS", "OLTAPEAKLOC"]

                    self.set_nb_data(data_update)
                    if self.data["OBJECTTYPE"] == "CAL":
                        self.calc_pss_()
                    else:
                        pass

                elif self.beamName[plotIndex] == "HPSRCP":
                    data_update = ["SRTA", "SRDTA", "SRS2N",
                                   "SRRMSB", "SRRMSA", "SRBSLOPE", "SRBSRMS", "SRTAPEAKLOC"]
                    self.set_nb_data(data_update)

                elif self.beamName[plotIndex] == "HPNRCP":
                    data_update = ["NRTA", "NRDTA", "NRS2N",
                                   "NRRMSB", "NRRMSA", "NRBSLOPE", "NRBSRMS", "NRTAPEAKLOC"]
                    self.set_nb_data(data_update)

                else:
                    data_update = ["ORTA", "ORDTA", "ORS2N",
                                   "ORRMSB", "ORRMSA", "ORBSLOPE", "ORBSRMS", "ORTAPEAKLOC"]
                    self.set_nb_data(data_update)
                    if self.data["OBJECTTYPE"] == "CAL":
                        self.calc_pss_()
                    else:
                        pass

            if "D" in self.data["BEAMTYPE"]:
                

                if self.beamName[plotIndex] == "HPSLCP":
                    data_update = ["ASLTA", "ASLDTA", "ASLS2N","ASLTAPEAKLOC", "BSLTA", "BSLDTA", "BSLS2N","BSLTAPEAKLOC",
                                   "SLRMSB", "SLRMSA", "SLBSLOPE", "SLBSRMS"]
                    self.set_dual_data(data_update)

                elif self.beamName[plotIndex] == "HPNLCP":
                    data_update = ["ANLTA", "ANLDTA", "ANLS2N", "ANLTAPEAKLOC", "BNLTA", "BNLDTA", "BNLS2N", "BNLTAPEAKLOC",
                                   "NLRMSB", "NLRMSA", "NLBSLOPE", "NLBSRMS"]
                    self.set_dual_data(data_update)

                elif self.beamName[plotIndex] == "ONLCP":

                    data_update = ["AOLTA", "AOLDTA", "AOLS2N","AOLTAPEAKLOC", "BOLTA", "BOLDTA", "BOLS2N","BOLTAPEAKLOC", 
                                   "OLRMSB", "OLRMSA", "OLBSLOPE", "OLBSRMS"]

                    self.set_dual_data(data_update)

                    if self.data["OBJECTTYPE"] == "CAL":
                        self.set_db_pss()
                    else:
                        pass 

                elif self.beamName[plotIndex] == "HPSRCP":
                    data_update = ["ASRTA", "ASRDTA", "ASRS2N", "ASRTAPEAKLOC", "BSRTA", "BSRDTA", "BSRS2N", "BSRTAPEAKLOC",
                                   "SRRMSB", "SRRMSA", "SRBSLOPE", "SRBSRMS"]
                    self.set_dual_data(data_update)

                elif self.beamName[plotIndex] == "HPNRCP":
                    data_update = ["ANRTA", "ANRDTA", "ANRS2N", "ANRTAPEAKLOC", "BNRTA", "BNRDTA", "BNRS2N", "BNRTAPEAKLOC",
                                   "NRRMSB", "NRRMSA", "NRBSLOPE", "NRBSRMS"]
                    self.set_dual_data(data_update)

                else:
                    data_update = ["AORTA", "AORDTA", "AORS2N", "AORTAPEAKLOC", "BORTA", "BORDTA", "BORS2N", "BORTAPEAKLOC",
                                   "ORRMSB", "ORRMSA", "ORBSLOPE", "ORBSRMS"]

                    self.set_dual_data(data_update)

                    if self.data["OBJECTTYPE"] == "CAL":
                        self.set_db_pss()
                    else:
                        pass 

    def update_smoothing_params(self):
        """ Update that plot has been smoothed"""

        plotIndex = self.get_plot_index()

        if "13.0S" == self.data["BEAMTYPE"]:

            if plotIndex == 0:
                self.data["OLRMSB"] = self.rmsb
                self.data["OLRMSA"] = self.rmsa

            elif plotIndex == 1:
                self.data["ORRMSB"] = self.rmsb
                self.data["ORRMSA"] = self.rmsa

        elif "01.3S" == self.data["BEAMTYPE"] or "02.5S" == self.data["BEAMTYPE"]:

            if plotIndex == 0:
                self.data["SLRMSB"] = self.rmsb
                self.data["SLRMSA"] = self.rmsa

            elif plotIndex == 1:
                self.data["NLRMSB"] = self.rmsb
                self.data["NLRMSA"] = self.rmsa

            elif plotIndex == 2:
                self.data["OLRMSB"] = self.rmsb
                self.data["OLRMSA"] = self.rmsa

            elif plotIndex == 3:
                self.data["SRRMSB"] = self.rmsb
                self.data["SRRMSA"] = self.rmsa

            elif plotIndex == 4:
                self.data["NRRMSB"] = self.rmsb
                self.data["NRRMSA"] = self.rmsa

            elif plotIndex == 5:
                self.data["ORRMSB"] = self.rmsb
                self.data["ORRMSA"] = self.rmsa

            else:
                pass

        else:
            pass

    def iter_dict(self, filter_key1, filter_key2=""):
        """
        Dictionary iterator to extract current fit information
        """

        ld = list((self.data).items())
        keys = list((self.data).keys())
        values = list((self.data).values())

        idx_of_key1 = int(keys.index(filter_key1))
        try:
            idx_of_key2 = int(keys.index(filter_key2))
        except:
            idx_of_key2 = len(ld)

        self.write("Fit stats: \n"+"-"*30,'info')

        if self.data["BEAMTYPE"] == "02.5S" or self.data["BEAMTYPE"] == "01.3S":

            if filter_key1 == "SLTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass
            elif filter_key1 == "NLTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass
            elif filter_key1 == "OLTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass
            elif filter_key1 == "SRTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass
            elif filter_key1 == "NRTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass
            elif filter_key1 == "ORTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass

        elif self.data["BEAMTYPE"] == "13.0S":
            if filter_key1 == "OLTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2 and idx_of_key2 != "":
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
            else:
                for i in range(len(ld)):
                    if i >= idx_of_key1:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
            

        elif "D" in self.data["BEAMTYPE"]:

            if filter_key1 == "ASLTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass
            elif filter_key1 == "ANLTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass
            elif filter_key1 == "AOLTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass
            elif filter_key1 == "ASRTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass
            elif filter_key1 == "ANRTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass
            elif filter_key1 == "AORTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1:
                        self.write(str(keys[i]) + ": " + str(values[i]),'info')
                    else:
                        pass

    def plot_new_fig(self):
        """
        Plot a new figure from the recently fit data.
        """

        self.write("plotting New Fig",'info')

        fig = self.Canvas.ax.get_figure()

        plot_tag = self.create_tag(len(self.plotBeamName))
        print(f'plot tag: {plot_tag}')
        fig_name = "plots/" + self.data["SOURCEDIR"] + \
            "/" + self.data["FILENAME"][:18] + "_" + plot_tag + ".png"

        self.file.create_folder("plots/" + self.data["SOURCEDIR"])
        fig.savefig(fig_name)

    # === setups ===
    def set_beam_names(self):
        """ Get the drift scan beam """

        msg_wrapper("debug", self.log.debug, "Setting beam names")

        if self.data['BEAMTYPE'] == "13.0S":
            self.beamName = ["ONLCP", "ONRCP"]
            self.plotBeamName = ["ON_LCP", "ON_RCP"]
        else:
            self.beamName = ["HPSLCP", "HPNLCP", "ONLCP",
                              "HPSRCP", "HPNRCP", "ONRCP"]
            self.plotBeamName = ["HPS_LCP", "HPN_LCP", "ON_LCP",
                              "HPS_RCP", "HPN_RCP", "ON_RCP"]

    def setup_flags(self):
        """ Setup flag parameters, default =100. These
        flags tell us whether a scan has been fit manually
        or not. see set_flags()
        """

        msg_wrapper("debug", self.log.debug,"Setting flags")

        if ("13.0S" in self.data["BEAMTYPE"]):
            self.data["OLFLAG"] = 100
            self.data["ORFLAG"] = 100

        else:
            self.data["SLFLAG"] = 100
            self.data["NLFLAG"] = 100
            self.data["OLFLAG"] = 100
            self.data["SRFLAG"] = 100
            self.data["NRFLAG"] = 100
            self.data["ORFLAG"] = 100
 
    def set_fit_parmeters(self,bf=0,pf=0,ps=0):
        """
        Initialize fit status parameters. These are parameters that tell us
        wether a certain part of the scan has been fit or not. The status of 
        the fit can be either 0 (data not fit yet) or 1 (data fitting has 
        been done) for the current scan. A smoothing parameter is also included
        to let us know if smoothing has been done on the original data.

        By default, all the parameters are set to zero.
        """

        msg_wrapper("debug", self.log.debug, "Setting fit status")

        self.base_is_fit = bf        # Baseline has not been corrected
        self.peak_is_fit = pf        # Peak fit has not been done
        self.plot_is_smoothed = ps   # rmscut/smoothing has not been done

    def reset_xy(self, ind):
        """ Set X and Y values to current plot. """

        msg_wrapper("debug", self.log.debug, "Setting X and Y")

        try:
            self.x = self.scans["OFFSET"]
        except Exception as e:
            print(e)
            self.x = np.zeros_like(1000)

        try:
            keys = list(self.scans.keys())
            ind=ind+2

            for i in range(2, len(keys)):
                if ind == i:
                    self.y = self.scans[keys[ind]]
        except Exception:
            self.y = np.zeros_like(1000)

    def reset_previous_fits(self, plotIndex):
        """ Reset previous fits. """

        msg_wrapper("debug", self.log.debug, "Reset previous fits")
        
        if "D" in self.data["BEAMTYPE"]:
            self.reset_dual_plot_fit_a()
            self.reset_dual_plot_fit_b()
            self.reset_dual_pss_a()
            self.reset_dual_pss_b()

        if "S" in self.data["BEAMTYPE"]:
            self.reset_plot_fit()
            self.reset_pss()

    def reset_dual_plot_fit_a(self):
        """ Reset all previously fit parameters to zero. """

        self.peakFitA = 0
        self.peakRmsA =0
        self.s2nA = 0
        self.rmsbA = 0
        self.rmsaA = 0
        self.base_slopeA = 0
        self.base_rmsA = 0
        self.peakLocA=np.nan
        
    def reset_dual_plot_fit_b(self):
        """ Reset all previously fit parameters to zero. """

        self.peakFitB = 0
        self.peakRmsB =0
        self.s2nB = 0
        self.rmsbB = 0
        self.rmsaB = 0
        self.base_slopeB = 0
        self.base_rmsB = 0
        self.peakLocB=np.nan

    def reset_plot_fit(self):
        """ Reset all previously fit parameters to zero. """

        self.peakFit = 0
        self.peakRms = 0
        self.s2n = 0
        self.baseSlope = 0
        self.base_rms = 0
        self.peakLoc = np.nan

    def reset_pss(self):
        self.PSS=0.
        self.errPSS=0.
        self.appEff=0.

    def reset_dual_pss_a(self):
        self.PSSA=0. 
        self.errPSSA=0. 
        self.pcA=0. 
        self.corrTaA=0. 
        self.errCorrTaA=0. 
        self.appEffA=0.

    def reset_dual_pss_b(self):
        self.PSSB=0. 
        self.errPSSB=0. 
        self.pcB=0. 
        self.corrTaB=0. 
        self.errCorrTaB=0. 
        self.appEffB=0.

    def set_title(self):
        """ Set the plot title. """

        plotTitle = "Plot of " + \
            self.data['OBJECT']+" @ " + \
            str(self.data['CENTFREQ'])+" MHz"
        return plotTitle

    def set_flags(self, flag=100):
        """ Set base flags.
            FLAGS = 100  # Source was manually edited/reduced by user
            This becomes the default for all flags if you save to DB
            while using the GUI.
        """

        msg_wrapper("debug", self.log.debug, "set flags")

        plotIndex = self.get_plot_index()
        beam = self.data['BEAMTYPE']

        if beam == "13.0S":
            if (self.beamName[plotIndex]) == "ONLCP":
                self.data['OLFLAG'] = flag

            if (self.beamName[plotIndex]) == "ONRCP":
                self.data['ORFLAG'] = flag

        else:

            if (self.beamName[plotIndex]) == "HPSLCP":
                try:
                    self.data["SLFLAG"] = flag
                except:
                    pass

            elif (self.beamName[plotIndex]) == "HPNLCP":
                try:
                    self.data["NLFLAG"] = flag
                except:
                    pass

            elif (self.beamName[plotIndex]) == "ONLCP":
                try:
                    self.data["OLFLAG"] = flag
                except:
                    pass

            elif (self.beamName[plotIndex]) == "HPSRCP":
                try:
                    self.data["SRFLAG"] = flag
                except:
                    pass

            elif (self.beamName[plotIndex]) == "HPNRCP":
                try:
                    self.data["NRFLAG"] = flag
                except:
                    pass

            elif (self.beamName[plotIndex]) == "ONRCP":
                try:
                    self.data["ORFLAG"] = flag
                except:
                    pass

    def set_pss(self, ta=0, dta=0):
        """
        Calculate the PSS
        """

        msg_wrapper("debug", self.log.debug, "Set PSS")

        plotIndex = self.get_plot_index()

        self.PSS, self.errPSS, self.appEff = cp.calc_pss(
            self.data['FLUX'], ta, dta)

        self.write(f'PSS: {self.PSS}, err PSS: {self.errPSS}','info')

        if self.data["BEAMTYPE"] == "13.0S":
            if plotIndex == 0:
                self.data["OLPSS"] = self.PSS
                self.data["OLDPSS"] = self.errPSS
                self.data["OLAPPEFF"] = self.appEff
            else:
                self.data["ORPSS"] = self.PSS
                self.data["ORDPSS"] = self.errPSS
                self.data["ORAPPEFF"] = self.appEff

    def set_db_pss(self):
        """ Calculate the dual beam PSS. """

        msg_wrapper("debug", self.log.debug, "Set dual beam PSS")

        plotIndex = self.get_plot_index()

        #if self.data["BEAMTYPE"] == "13.0S":
        if plotIndex == 2:

            self.PSSA, self.errPSSA, self.pcA, self.corrTaA, self.errCorrTaA, self.appEffA= cp.calc_pc_pss(
                0, self.data["ASLTA"], self.data["ASLDTA"], self.data["ANLTA"], self.data["ANLDTA"], self.data["AOLTA"], self.data["AOLDTA"], self.data['FLUX'], self.data)

            self.PSSB, self.errPSSB, self.pcB, self.corrTaB, self.errCorrTaB, self.appEffB= cp.calc_pc_pss(
                0, self.data["BSLTA"], self.data["BSLDTA"], self.data["BNLTA"], self.data["BNLDTA"], self.data["BOLTA"], self.data["BOLDTA"], self.data['FLUX'], self.data)

            self.write(f'A beam LCP PSS: {self.PSSA}, err PSS: {self.errPSSA}','info')
            self.write(
                f'A beam LCP pointing corrected Ta: {self.corrTaA}, err: {self.errCorrTaA}','info')

            self.write(f'B beam LCP PSS: {self.PSSB}, err PSS: {self.errPSSB}','info')
            self.write(
                f'B beam LCP pointing corrected Ta: {self.corrTaB}, err: {self.errCorrTaB}','info')

            self.data["AOLPC"] = self.pcA
            self.data["ACOLTA"] = self.corrTaA
            self.data["ACOLDTA"] = self.errCorrTaA
            self.data["AOLPSS"] = self.PSSA
            self.data["AOLDPSS"] = self.errPSSA
            self.data["AOLAPPEFF"] = self.appEffA
            self.data["BOLPC"] = self.pcB
            self.data["BCOLTA"] = self.corrTaB
            self.data["BCOLDTA"] = self.errCorrTaB
            self.data["BOLPSS"] = self.PSSB
            self.data["BOLDPSS"] = self.errPSSB
            self.data["BOLAPPEFF"] = self.appEffB

        elif plotIndex == 5:

            self.PSSA, self.errPSSA, self.pcA, self.corrTaA, self.errCorrTaA, self.appEffA= cp.calc_pc_pss(
                0, self.data["ASRTA"], self.data["ASRDTA"], self.data["ANRTA"], self.data["ANRDTA"], self.data["AORTA"], self.data["AORDTA"], self.data['FLUX'], self.data)

            self.PSSB, self.errPSSB, self.pcB, self.corrTaB, self.errCorrTaB, self.appEffB= cp.calc_pc_pss(
                0, self.data["BSRTA"], self.data["BSRDTA"], self.data["BNRTA"], self.data["BNRDTA"], self.data["BORTA"], self.data["BORDTA"], self.data['FLUX'], self.data)
                
            self.write(f'A beam RCP PSS: {self.PSSA}, err PSS: {self.errPSSA}','info')
            self.write(
                f'A beam RCP pointing corrected Ta: {self.corrTaA}, err: {self.errCorrTaA}','info')

            self.write(f'B beam RCP PSS: {self.PSSB}, err PSS: {self.errPSSB}','info')
            self.write(
                f'B beam RCP pointing corrected Ta: {self.corrTaB}, err: {self.errCorrTaB}','info')

            self.data["AOLPC"] = self.pcA
            self.data["ACORTA"] = self.corrTaA
            self.data["ACORDTA"] = self.errCorrTaA
            self.data["AORPSS"] = self.PSSA
            self.data["AORDPSS"] = self.errPSSA
            self.data["AORAPPEFF"] = self.appEffA
            self.data["BORPC"] = self.pcB
            self.data["BCORTA"] = self.corrTaB
            self.data["BCORDTA"] = self.errCorrTaB
            self.data["BORPSS"] = self.PSSB
            self.data["BORDPSS"] = self.errPSSB
            self.data["BORAPPEFF"] = self.appEffB

    def reset_dict(self, filter_key1, filter_key2=""):
        """ Reset the data dictionary containing the 
            driftscan keys
        """

        ld = list((self.data).items())
        keys = list((self.data).keys())
        values = list((self.data).values())
        idx_of_key1 = int(keys.index(filter_key1))

        try:
            idx_of_key2 = int(keys.index(filter_key2))

        except:
            idx_of_key2 = len(ld)

        if self.data["BEAMTYPE"] == "02.5S" or self.data["BEAMTYPE"] == "01.3S" or "D" in self.data["BEAMTYPE"]:

            if filter_key1 == "SLTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        if "FLAG" in keys[i]:
                            self.data[keys[i]] = 100
                        else:
                            self.data[keys[i]] = 0
                    else:
                        pass

            elif filter_key1 == "NLTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        if "FLAG" in keys[i]:
                            self.data[keys[i]] = 100
                        else:
                            self.data[keys[i]] = 0
                    else:
                        pass

            elif filter_key1 == "OLTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        if "FLAG" in keys[i]:
                            self.data[keys[i]] = 100
                        else:
                            self.data[keys[i]] = 0
                    else:
                        pass

            elif filter_key1 == "SRTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        if "FLAG" in keys[i]:
                            self.data[keys[i]] = 100
                        else:
                            self.data[keys[i]] = 0
                    else:
                        pass

            elif filter_key1 == "NRTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1 and i < idx_of_key2:
                        if "FLAG" in keys[i]:
                            self.data[keys[i]] = 100
                        else:
                            self.data[keys[i]] = 0
                    else:
                        pass

            elif filter_key1 == "ORTA":
                for i in range(len(ld)):
                    if i >= idx_of_key1:
                        if "FLAG" in keys[i]:
                            self.data[keys[i]] = 100
                        else:
                            self.data[keys[i]] = 0
                    else:
                        pass

        else:
            for i in range(len(ld)):
                if i >= idx_of_key1:
                    if "FLAG" in keys[i]:
                        self.data[keys[i]] = 100
                    else:
                        self.data[keys[i]] = 0

    def create_tag(self, ind):
        """ Create a tag for the plots according to the current scan being processed. e.g. ONRCP
        """

        msg_wrapper("debug", self.log.debug, "Setting up naming tags")
        #print(f'index: {ind}')
        if int(ind) > 2:
            tag = self._set_file_tag_nb()
        else:
            tag = self._set_file_tag_wb()

        return tag

    def _set_file_tag_wb(self):
        """
            A naming tag for wide beam data.
        """

        msg_wrapper("debug", self.log.debug, "Setting tag for wide beam data")

        plotIndex = self.get_plot_index()
        tagId = int(plotIndex)

        if tagId == 0:
            #self.write("Processing: ONLCP\n")
            return "ON_LCP"
        else:
            #self.write("rocessing: ONRCP\n")
            return "ON_RCP"

    def _set_file_tag_nb(self):
        """ A naming tag for narrow beam data.
        """

        msg_wrapper("debug", self.log.debug,
                    "Setting tag for narrow beam data")

        plotIndex = self.get_plot_index()
        tagId = int(plotIndex)

        #print(f'plot ind: {plotIndex}, tag id: {tagId}')
        if tagId == 0:
            #self.write("Processing: HPSLCP\n")
            return "HPS_LCP"

        elif tagId == 1:
            #self.write("Processing: HPNLCP\n")
            return "HPN_LCP"

        elif tagId == 2:
            #self.write("Processing: ONLCP\n")
            return "ON_LCP"

        elif tagId == 3:
            #self.write("Processing: HPSRCP\n")
            return "HPS_RCP"

        elif tagId == 4:
            #self.write("Processing: HPNRCP\n")
            return "HPN_RCP"

        elif tagId == 5:
            #self.write("Processing: ONRCP\n")
            return "ON_RCP"

    def set_data(self, data_update):
        """ Set the estimated values in the data dictionary.
        """

        if self.data["OBJECTTYPE"] == "CAL":
            try:
                self.data[data_update[8]] = self.appEff
            except:
                pass
            try:
                self.data[data_update[9]] = self.PSS
            except:
                pass
            try:
                self.data[data_update[10]] = self.errPSS
            except:
                pass
        else:
            pass

        try:
            self.data[data_update[0]] = self.peakFit
        except:
            pass

        try:
            self.data[data_update[1]] = self.peakRms
        except:
            pass

        try:
            self.data[data_update[2]] = self.s2n
        except:
            pass

        try:
            self.data[data_update[3]] = self.rmsb
        except:
            pass

        try:
            self.data[data_update[4]] = self.rmsa
        except:
            pass

        try:
            self.data[data_update[5]] = self.baseSlope
        except:
            pass

        try:
            self.data[data_update[6]] = self.base_rms
        except:
            pass
        
        try:
            self.data[data_update[7]] = self.peakLoc
        except:
            pass

    def set_dual_data(self, data_update):
        """ Set the estimated values in the data dictionary.
        """

        try:
            self.data[data_update[0]] = self.peakFitA
        except:
            pass

        try:
            self.data[data_update[1]] = self.peakRmsA
        except:
            pass

        try:
            self.data[data_update[2]] = self.s2nA
        except:
            pass

        try:
            self.data[data_update[3]] = self.peakLocA
        except:
            pass

        try:
            self.data[data_update[4]] = self.peakFitB
        except:
            pass

        try:
            self.data[data_update[5]] = self.peakRmsB
        except:
            pass

        try:
            self.data[data_update[6]] = self.s2nB
        except:
            pass

        try:
            self.data[data_update[7]] = self.peakLocB
        except:
            pass

        try:
            self.data[data_update[8]] = self.rmsb
        except:
            pass

        try:
            self.data[data_update[9]] = self.rmsa
        except:
            pass

        try:
            self.data[data_update[10]] = self.baseSlope
        except:
            pass

        try:
            self.data[data_update[11]] = self.base_rms
        except:
            pass

    def set_nb_data(self, data_update):
        """ Set the estimated values in the data dictionary. """

        try:
            self.data[data_update[0]] = self.peakFit
        except:
            pass

        try:
            self.data[data_update[1]] = self.peakRms
        except:
            pass

        try:
            self.data[data_update[2]] = self.s2n
        except:
            pass

        try:
            self.data[data_update[3]] = self.rmsb
        except:
            pass

        try:
            self.data[data_update[4]] = self.rmsa
        except:
            pass

        try:
            self.data[data_update[5]] = self.baseSlope
        except:
            pass

        try:
            self.data[data_update[6]] = self.base_rms
        except:
            pass

        try:
            self.data[data_update[7]] = self.peakLoc
        except:
            pass

    # ===  Combobox change setup ===
    def on_fit_combobox_changed(self):
        """ Handle events related to the combobox option change. """

        msg_wrapper("debug", self.log.debug, "Fitting ComboBox option changed")

        # Check the selected fit type
        #self.write("Now fitting: " +
        #         self.drift_ui.ComboBoxFitLoc.currentText(),'info')

        # Set the fit type
        if self.drift_ui.ComboBoxFitLoc.currentText() == "Base":
            self.drift_ui.ComboBoxFitOrder.setCurrentIndex(0)

        elif self.drift_ui.ComboBoxFitLoc.currentText() == "Peak":
            self.drift_ui.ComboBoxFitOrder.setCurrentIndex(1)

    def on_filter_type_combobox_changed(self):
        """
        Handle events related to the filter type combobox option change.
        """

        msg_wrapper("debug", self.log.debug, "Combo Box Filter Type Changed")

        if self.drift_ui.ComboBoxFilterType.currentText() == "Please select:":
            #self.write("Smoothing the data ",'info')

            # Enable filtering window
            self.drift_ui.EdtFilteringWindow.setEnabled(False)
            self.drift_ui.BtnFilterData.setEnabled(False)

        elif self.drift_ui.ComboBoxFilterType.currentText() == "rms cuts":
            #self.write("Performing Rms cuts",'info')

            # Enable filtering window
            self.drift_ui.EdtFilteringWindow.setEnabled(False)
            self.drift_ui.BtnFilterData.setEnabled(True)

        else:
            self.drift_ui.EdtFilteringWindow.setEnabled(True)
            self.drift_ui.BtnFilterData.setEnabled(True)

    def on_fit_type_combobox_changed(self):
        """ Handle events related to the combobox option change. """

        msg_wrapper("debug", self.log.debug,
                    "Fitting ComboBox option changed ")

        fit_type = self.get_fit_type()

        # Check the selected fit type
        #self.write(" Now fitting: " + fit_type,'info')

        # Set the fit type
        if fit_type == "Polynomial":

            # Enable peak fitting buttons
            self.drift_ui.ComboBoxFitOrder.setEnabled(True)
            self.drift_ui.ComboBoxFitLoc.setEnabled(True)

    def on_checkbox_changed(self):
        """ Update the cursor depending on checkbox status (on/off)"""

        # Check state of checkbox
        if self.drift_ui.checkBox.isChecked() == True:
            self.write("Checked",'info')
            self.Canvas.cursorState = "on"
        else:
            self.write("Not checked",'info')
            self.Canvas.cursorState = "off"

    # === Enabling, disabling and populating widgets ===
    def disable_single_peak_fit_widgets(self):
        """ Disable single beam peak fitting buttons/widgets. """
        self.drift_ui.BtnFitData.setEnabled(False)
        self.drift_ui.BtnClearSelection.setEnabled(False)
        self.drift_ui.BtnResetPlot.setEnabled(False)
        
    def disable_target_widgdets(self):
        """ Disable target object buttons/widgets."""
        self.drift_ui.EdtPSSlcpA.setVisible(False)
        self.drift_ui.EdtPSSrcpA.setVisible(False)
        self.drift_ui.EdtPSSlcpB.setVisible(False)
        self.drift_ui.EdtPSSrcpB.setVisible(False)
        self.drift_ui.LblPSSlcpA.setVisible(False)
        self.drift_ui.LblPSSrcpA.setVisible(False)
        self.drift_ui.LblPSSlcpB.setVisible(False)
        self.drift_ui.LblPSSrcpB.setVisible(False)
        self.drift_ui.BtnPopulatePSS.setVisible(False)
        self.drift_ui.BtnResetPSS.setVisible(False)

    def enable_single_peak_fit_widgets(self):
        """ Enable single beam peak fitting buttons/widgets. """
        self.drift_ui.BtnFitData.setEnabled(True)
        self.drift_ui.BtnClearSelection.setEnabled(True)
        self.drift_ui.BtnResetPlot.setEnabled(True)

    def enable_target_widgdets(self):
        """ Enable target object buttons/widgets."""
        self.drift_ui.EdtPSSlcpA.setVisible(True)
        self.drift_ui.EdtPSSrcpA.setVisible(True)
        self.drift_ui.EdtPSSlcpB.setVisible(True)
        self.drift_ui.EdtPSSrcpB.setVisible(True)
        self.drift_ui.LblPSSlcpA.setVisible(True)
        self.drift_ui.LblPSSrcpA.setVisible(True)
        self.drift_ui.LblPSSlcpB.setVisible(True)
        self.drift_ui.LblPSSrcpB.setVisible(True)
        self.drift_ui.BtnPopulatePSS.setVisible(True)
        self.drift_ui.BtnResetPSS.setVisible(True)

    def enable_widgets(self):
        """ Enable the widgets """

        msg_wrapper("debug", self.log.debug,"Enabling widgets")

        self.drift_ui.ComboBoxPlotType.setEnabled(True)
        self.drift_ui.ComboBoxFitLoc.setEnabled(True)
        self.drift_ui.ComboBoxFitOrder.setEnabled(True)
        self.drift_ui.ComboBoxFitType.setEnabled(True)
        self.drift_ui.ComboBoxFilterType.setEnabled(True)
        self.drift_ui.EdtFilteringWindow.setEnabled(True)

        # Enable buttons
        self.drift_ui.BtnChoosePlot.setEnabled(True)
        self.drift_ui.BtnViewFit.setEnabled(True)
        self.drift_ui.BtnFitData.setEnabled(True)
        self.drift_ui.BtnClearSelection.setEnabled(True)
        self.drift_ui.BtnResetPlot.setEnabled(True)
        self.drift_ui.BtnSave.setEnabled(True)
        #self.drift_ui.BtnResetFit.setEnabled(True)
        self.drift_ui.BtnSaveToDb.setEnabled(True)
        self.drift_ui.BtnFilterData.setEnabled(True)
        self.drift_ui.BtnCalc.setEnabled(True)

        # enable target buttons
        self.drift_ui.BtnPopulatePSS.setEnabled(True)
        self.drift_ui.BtnSavePSS.setVisible(False)
        self.drift_ui.BtnResetPSS.setVisible(False)

        # Enable checkboxes
        self.drift_ui.checkBox.setEnabled(True)
        self.cursor_state = "off"
      
    def populate_widgets(self):
        """ Populate the gui widgets. """

        msg_wrapper("debug", self.log.debug,"Populate widgets")

        self.drift_ui.EdtFilename.setText(self.data["FILENAME"])
        self.drift_ui.EdtCurDate.setText(self.data["CURDATETIME"])
        self.drift_ui.EdtObsDate.setText(self.data["OBSDATE"])
        self.drift_ui.EdtObsTime.setText(self.data["OBSTIME"])

        self.drift_ui.EdtObjectType.setText(self.data["OBJECTTYPE"])
        self.drift_ui.EdtObjectName.setText(self.data["OBJECT"])
        self.drift_ui.EdtMjd.setText(str(f'{self.data["MJD"]:.1f}'))

        self.drift_ui.EdtFreq.setText(str(self.data["CENTFREQ"]))
        self.drift_ui.EdtTsysL.setText(str(f'{self.data["TSYS1"]:.1f}'))
        self.drift_ui.EdtTsysR.setText(str(f'{self.data["TSYS2"]:.1f}'))

        self.drift_ui.EdtTemp.setText(str(f'{self.data["TAMBIENT"]:.1f}'))
        self.drift_ui.EdtPres.setText(str(f'{self.data["PRESSURE"]:.1f}'))
        self.drift_ui.EdtHum.setText(str(f'{self.data["HUMIDITY"]:.1f}'))

        self.drift_ui.EdtFnbw.setText(str(f'{self.data["FNBW"]:.2f}'))
        self.drift_ui.EdtHa.setText(str(f'{self.data["HA"]:.1f}'))
        self.drift_ui.EdtZa.setText(str(f'{self.data["ZA"]:.1f}'))
        self.drift_ui.EdtHpbw.setText(str(f'{self.data["HPBW"]:.2f}'))

    def popUp(self, question):
        """ Create a popup and get user answer for processing. """

        msg_wrapper("debug", self.log.debug, "popUp initiated")

        msgbox = QtWidgets.QMessageBox

        reply = msgbox.question(
            self, "Title", question, msgbox.Yes | msgbox.No, msgbox.No)

        if reply == msgbox.Yes:
            self.write("Yes clicked.",'info')
            return "yes"
        else:
            self.write("No clicked.",'info')
            return "no"

        self.show()

    def popup_msg_dict(self):
        """ Message dictionary for popups."""

        self.popup_msg = {
            "noBase": "Are you sure you want to save data without fitting the baseline ?",
            "noPeak": "Are you sure you want to save data without fitting the peak ?",
            "noFit": "Are you sure you want to save data without fitting the plot ?"
        }

    def update_bad_fits(self, files, dbFile,data,status= [0,0,0,0,0,0]):
        # update database for bad scan fit data

        # GET TABLE FROM DATABASE
        db = SQLiteDB(databaseName=dbFile, log=self.log)
        db.create_db()

        table = db.get_table_name(data['SOURCEDIR'])
        db.set_table_name(table)

        self.write("Updating table: {}\n".format(table),'info')

        # Update db entry
        db.update_row_in_db(
                    table, self.data['FILENAME'], data,status, self.beamName)
        self.write('Updated row in table','info')

    def save_to_DB(self):
        """ Save fit to database. """

        self.write("Saving data to database.")

        plotIndex = self.get_plot_index()

        if self.data['OBJECTTYPE'] == 'CAL':

            # make a copy of the current working db
            analDb = "CALDB.db"
            
            # GET TABLE FROM DATABASE
            db = SQLiteDB(databaseName=analDb, log=self.log)
            db.create_db()
        else:
            # make a copy of the current working db
            analDb = "TARDB.db"
            db = SQLiteDB(databaseName=analDb, log=self.log)
            db.create_db()

        table = db.get_table_name(self.data['SOURCEDIR'])
        db.set_table_name(table)

        self.write("Updating table: {}\n".format(table),'info')

        # Check if file has been processed
        try:
            files = db.read_data_from_database("FILENAME")
        except Exception:
            db.create_table(self.data, table)
            files = []

        # File in DB
        # print("File in db: ", self.data['FILENAME'] in files, self.data['FILENAME'])

        if self.data['FILENAME'] in files:

            self.write("already processed: ".format(self.data['FILENAME']),'info')

            question = "Are you sure you want to overwrite the database entry for this source ?"
            result = self.popUp(question)

            if result == "yes":

                self.write("Status: "+ str(self.status),'info')
                #print(self.beamName)
                #sys.exit()
                      
                # Update db entry
                db.update_row_in_db(
                    table, self.data['FILENAME'], self.data, self.status, self.beamName)

                self.write('Updated row in table','info')

                # Save the figure
                self.plot_new_fig()

                if 1 in self.status or 2 in self.status:

                    # update corresponding plots
                    for i in range(len(self.beamName)):
                        x = self.x # Data
                        y = self.y#scans[i]

                        if str(self.status[i]) == '2' :
                            pl.plot(x, y, "r", label="raw data")
                            pl.suptitle(
                                "Plot "+self.data["FILENAME"][:18]+" of "+self.data["OBJECT"])
                            pl.title(
                                self.beamName[i]+" scan at "+str(self.data["CENTFREQ"])+" MHz", fontsize=10)
                            pl.xlabel("Scandist [deg]")
                            pl.ylabel("Ta [K]")
                            pl.legend(loc=2)
                            pl.savefig(
                                "plots/"+self.data["SOURCEDIR"]+"/"+self.data["FILENAME"][:18]+"_"+self.plotBeamName[i]+".png")
                            pl.close()
                            
                        elif str(self.status[i]) == '1' :
                            pl.plot(x, y, "C0", label="raw data")
                            pl.suptitle(
                                "Plot "+self.data["FILENAME"][:18]+" of "+self.data["OBJECT"])
                            pl.title(
                                self.beamName[i]+" scan at "+str(self.data["CENTFREQ"])+" MHz", fontsize=10)
                            pl.xlabel("Scandist [deg]")
                            pl.ylabel("Ta [K]")
                            pl.legend(loc=2)
                            pl.savefig(
                                "plots/"+self.data["SOURCEDIR"]+"/"+self.data["FILENAME"][:18]+"_"+self.plotBeamName[i]+".png")
                            pl.close()
                        else:
                            pass
                    
  

                else:
                    # In the case where drift scans were fit but the
                    # fit for all the scans are unsatisfactory.
                    # If there is no data to fit and you want to save
                    # the raw data to the database, plot raw fits for all
                    # data and save data as nan in the database

                    print(self.status)
                    # sys.exit()
                    
                    # update corresponding plots
                    #print(self.scans)
                    
                    for i in range(len(self.beamName)):
                        
                        x = self.x#Data
                        y = self.scans[self.beamName[i]]

                        pl.plot(x, y, "r", label="raw data")
                        pl.suptitle(
                            "Plot "+self.data["FILENAME"][:18]+" of "+self.data["OBJECT"])
                        pl.title(
                            self.beamName[i]+" scan at "+str(self.data["CENTFREQ"])+" MHz", fontsize=10)
                        pl.xlabel("Scandist [deg]")
                        pl.ylabel("Ta [K]")
                        pl.legend(loc=2)
                        pl.savefig(
                            "plots/"+self.data["SOURCEDIR"]+"/"+self.data["FILENAME"][:18]+"_"+self.plotBeamName[i]+".png")
                        pl.close()

            else:
                self.write("Entry not updated in database",'info')
                self.write("SELECT POINTS TO FIT",'info')

        else:

            self.write("Processing new source: " +
                     self.data['FILENAME'],'info')

            question = "Are you sure you want create a new entry for this source in the database ?"
            result = self.popUp(question)

            if result == "yes":
                self.write(
                    "Saving new entry to database",'info')
                # Update db

                # If source is a calibrator and is 2280-MHz
                # and int(self.data["CENTFREQ"]) == 2280:
                if self.data["OBJECTTYPE"] == "CAL":

                    # Save the figure
                    self.plot_new_fig()

                    db.create_table(self.data, table)
                    tbname = db.validate_table_name(table)
                    db.populate_table(self.data, tbname)

                # and int(self.data["CENTFREQ"]) == 2280:
                elif self.data["OBJECTTYPE"] == "TAR":

                    # Save the figure
                    self.plot_new_fig()
                
                    db.create_table(self.data, table)
                    tbname = db.validate_table_name(table)
                    db.populate_table(self.data, tbname)

                    self.write(
                    "Added new row to table",'info')
            else:
                self.write(
                    "Entry not added to database",'info')
                self.write(
                    "SELECT POINTS TO FIT",'info')

    def populate_pss_from_file(self):
        """ populate the pss from file. """

        print('populating pss from file\n')