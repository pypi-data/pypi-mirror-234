# =========================================================================== #
# File    : sqlite_db.py                                                      #
# Author  : Pfesesani V. van Zyl                                              #
# =========================================================================== #

# Standard library imports
# --------------------------------------------------------------------------- #
import os
import sys
import sqlite3
import numpy as np

# Local imports
# --------------------------------------------------------------------------- #
sys.path.append("src/")
from common.messaging import msg_wrapper
import common.exceptions as ex
import common.calc_pss as cp
# =========================================================================== #

class SQLiteDB:
    """
    The SQLite database used for storing calibration or target data.
    
    Args:
        objectType (str): Type of object (e.g., CALIBRATOR or TARGET source).
        objectFolder (str): Name of the containing folder.
        database_name (str): Name of the database.
        log (object): Logging object.

    Attributes:
        objectType (str): Type of object.
        objectFolder (str): Name of the containing folder.
        database_name (str): Name of the database.
        log (object): Logging object.
        conn (sqlite3.Connection): SQLite database connection.
        cursor (sqlite3.Cursor): SQLite database cursor.

    Methods:
        - `db_exists(dbname)`: Check if a database exists.
        - `create_db()`: Create a new database.
        - `setup_database()`: Set up the database for use.
        - `save_to_database(data, source_folder)`: Save data to the database.
        - `read_data_from_database(field_name)`: Read data from the database.
        - `close_db()`: Close the database connection.
        - `validate_table_name(table_name)`: Validate a table name according to SQLite standards.
        - `get_table_name(table_name)`: Validate and get the table name for the database.
        - `get_table_names(db)`: Get table names from the database.
        - `get_table_columns(table_name)`: Get column details for a table.
        - `delete_row(table, key)`: Delete a row from the table.
        - `select_row(table, key)`: Select a row from the table.

    Usage:
        The `SQLiteDB` class provides functionality for managing SQLite databases, 
        including creation, setup, data saving, and retrieval.
    """

    def __init__(self, objectType="", objectFolder="", databaseName="",log=""):

        self.objectType = objectType
        self.objectFolder = objectFolder
        self.log = log
        self.conn=None
        self.c=None

        if databaseName:
            self.set_database_name(databaseName)
        else:
            self.databaseName = databaseName
        
        msg_wrapper("debug",self.log.debug,"SQLite database initiated")
      
    def set_database_name(self, databaseName):
        """ Set the name of the database. """

        msg_wrapper("debug", self.log.debug, "Setup database name")

       
        if ".db" in databaseName:
            self.databaseName = databaseName
        else:
            self.databaseName = databaseName+".db"

    def db_exists(self,dbname):
        """check if database exists. """

        if os.path.exists(dbname) == True:
            msg_wrapper("debug",self.log.debug,f'{dbname} exists')
            return True
        else:
            msg_wrapper("debug",self.log.debug,f'{dbname} does not exists')
            return False

    def create_db(self):
        """ Create a new database. """

        self.conn = sqlite3.connect(self.databaseName)
        self.c = self.conn.cursor()

    def setup_database(self):
        """ Setup the database that will be used to store our data. """

        if(self.objectType == "CAL"):
            self.set_database_name("CALDB")
        else:
            self.set_database_name("TARDB")
        self.create_db()
        self.get_table_name()

    def close_db(self):
        """ Close the database connection."""

        if self.c:
            self.conn.close()



    def validate_table_name(self, tableName=""):
        """Validate that the table name adheres to SQLite standards.

            SQLite does not support names that contain the "- and ." characters.
            This method checks if a folder name has the "-/." character.
            If found, the character is changed to an underscore ("_").

            Args:
                table_name (str): The name of the table

            Returns:
                table_name (str): Validated name of the table
        """

        msg_wrapper("debug", self.log.debug,
                    "Validating table name adheres to naming standards.")

        if not tableName:
            msg_wrapper("debug", self.log.debug, "Table name not provided, setting it to the object folder name.")
            tableName = self.objectFolder
        else:
            pass

        invalidChars = ['.', '-','+']

        for char in invalidChars:
            if char == "+":
                tableName = tableName.replace(char, "plus")
            else:
                if tableName.startswith(char):
                    tableName = "_"+tableName
                    tableName = tableName.replace(char, "_")
                tableName = tableName.replace(char, "_")
        return tableName

    def get_table_name(self, tableName=""):
        """Get a valid table name."""

        msg_wrapper("debug", self.log.debug, "Getting table name ")

        # create or fetch table and set lower case
        if not tableName:
            tableName = (self.validate_table_name(self.objectFolder)).lower()
            self.set_table_name(tableName)
        else:
            tableName = (self.validate_table_name(tableName)).lower()

        return tableName

    def get_table_names(self,db):
        """Get table names from the database.

        Args:
            db (str): The name of the database

        Returns:
            table_names (list): List of table names
        """

        print("\nGetting tables from: ", db, "\n")
        self.set_database_name(db)
        
        table_names = []
        sql_stmt = "SELECT name FROM sqlite_master WHERE type = 'table';"
        # tables = self.c.execute(sql_stmt).fetchall()
        
        try:
            tables = self.c.execute(sql_stmt).fetchall()
        except sqlite3.OperationalError:
            print("Failed to fetch data from the server")
            sys.exit()

        #print("Tables: ",tables)
        for i in range(len(tables)):
            if tables[i][0].startswith("data"):
                table_names.append(tables[i][0])
        for i in range(len(tables)):
            if tables[i][0].startswith("sqlite_sequence"):
                pass
            else:
                table_names.append(tables[i][0])
        #print(table_names)
        return table_names

    def get_table_coloumns(self, table_name):
        """Get columns of the table.

        Args:
            table_name (str): The name of the table

        Returns:
            col_indices (list): List of column indices
            col_names (list): List of column names
            col_types (list): List of column types
        """

        col_ind = []
        col_name = []
        col_type = []

        try:
            res = self.c.execute("PRAGMA table_info('%s') " %
                             table_name).fetchall()
        except sqlite3.OperationalError:
            print("Failed to fetch table columns from the database")
            sys.exit()

        #print(res)
        #sys.exit()
        for i in range(len(res)):
            #print(res[i][1])
            if res[i][1] == "OBSDATE" or res[i][1]=='FILENAME':
                col_ind.append(res[i][0])
                col_name.append(res[i][1])
                col_type.append(res[i][2])

            if res[i][2] == "TEXT":
                pass
            else:
                col_ind.append(res[i][0])
                col_name.append(res[i][1])
                col_type.append(res[i][2])

        return col_ind, col_name, col_type

    def get_table_coloumns2(self, table_name):
        """
            Get coloumns of table
            return index, coloumn name and coloumn type
        """

        col_ind = []
        col_name = []
        col_type = []

        try:
            res = self.c.execute("PRAGMA table_info('%s') " %
                             table_name).fetchall()
        except sqlite3.OperationalError:
            print("Failed to fetch table columns from the database")
            sys.exit()

        #print(res)
        #sys.exit()
        for i in range(len(res)):
            #print(res[i][1])
            # if res[i][1] == "OBSDATE" or res[i][1]=='FILENAME':
            #     col_ind.append(res[i][0])
            #     col_name.append(res[i][1])
            #     col_type.append(res[i][2])

            # if res[i][2] == "TEXT":
            #     pass
            # else:
            col_ind.append(res[i][0])
            col_name.append(res[i][1])
            col_type.append(res[i][2])

        return col_ind, col_name, col_type

    def get_all_table_coloumns(self, table_name):
        """
            Get coloumns of table
            return index, coloumn name and coloumn type
        """

        col_ind = []
        col_name = []
        col_type = []

        res = self.c.execute("PRAGMA table_info('%s') " %
                             table_name).fetchall()

        # print(res)
        # sys.exit()
        for i in range(len(res)):
            col_ind.append(res[i][0])
            col_name.append(res[i][1])
            col_type.append(res[i][2])

        return col_ind, col_name, col_type

    def delete_row(self,table,key):
        """Delete a row from the table.

        Args:
            table (str): The name of the table
            key (str): The key to identify the row to be deleted
        """

        stmt = "DELETE FROM "+table+" WHERE FILENAME = '"+key+"';"
        self.c.execute(stmt)
        self.commit_changes()
        msg_wrapper("info",self.log.info,f'{key} entry deleted from {table} database.\n' )
    
    def select_row(self,table,key):
        """Select a row from the table.

        Args:
            table (str): The name of the table
            key (str): The key to identify the row to be selected

        Returns:
            rows (list): List of rows matching the selection criteria
        """

        stmt = "SELECT * FROM "+table+" WHERE FILENAME = '"+key+"';"
        self.c.execute(stmt)
        data = self.c.fetchall()

        rows = []
        [rows.append(row) for row in data]
        return rows

    def commit_changes(self):
        """ Commit/save changes you have implemented to the database. """
        self.conn.commit()



    def select_row2(self,table,key,cmd="=",value="100"):
        '''Select row from table'''
        stmt = f"SELECT * FROM {table} WHERE {key} {cmd} {value};"
        print(stmt)
        self.c.execute(stmt)
        data = self.c.fetchall()

        rows = []
        [rows.append(row) for row in data]

        return rows

    def select_row3(self,table,key,cmd="=",value="100"):
        '''Select row from table'''
        stmt = f"SELECT * FROM {table} WHERE {key} {cmd} '{value}';"
        print(stmt)
        self.c.execute(stmt)
        data = self.c.fetchall()

        rows = []
        [rows.append(row) for row in data]

        return rows

    def get_rows(self, tbname):
        """ Get the rows in the database table.

            Parameters
            ----------
                tbname : str
                    table name

            Returns
            -------
                rows: str
                    table row list
        """

        # print(tbname)
        # open the database
        self.create_db()

        # read from selected table
        stmt = f"SELECT * FROM '{tbname}' ORDER BY FILENAME ASC;"
        # print(stmt)
        self.c.execute(stmt)
        data = self.c.fetchall()

        # get filenames and return them
        rows = []
        for row in data:
            rows.append(row)

        return rows

    def get_rows_of_cols(self, tbname,cols):
        """ Get the rows in the database table.

            Parameters
            ----------
                tbname : str
                    table name

            Returns
            -------
                rows: str
                    table row list
        """

        #tbname=tbname.split("/")[-1]
        #print(tbname,cols)
        #sys.exit()
        # open the database
        self.create_db()

        colNames=""
        for i in range(len(cols)):
                if i == len(cols)-1:
                    colNames = colNames + cols[i]+" "
                else:
                    colNames = colNames + cols[i]+", "
     
        # read from selected table
        stmt = "SELECT "+colNames[:-1]+"  FROM '"+tbname+"' ORDER BY FILENAME ASC;"

        # print(stmt)
        # print('\nExecuting: ',stmt,'\n')
        self.c.execute(stmt)
        data = self.c.fetchall()

        # get filenames and return them
        rows = []
        for row in data:
            rows.append(row)

        return rows

    def set_table_name(self,tableName):
        msg_wrapper("debug", self.log.debug, "Setting table name to: "+tableName)
        self.tableName=tableName

    def read_data_from_database(self, colName):
        """
        Read column data from from table.
        """

        sqlStmt = "SELECT "+colName+" FROM "+self.tableName+";"
        #self.c.execute(sqlStmt)
        try:
            self.c.execute(sqlStmt)
        except Exception as e:
           msg_wrapper("warning", self.log.warning, "Failed to read {} column from table '{}', \nthe table either doesn't exists or is corrupted. \nAttempting to create a new table\n".format(colName,self.tableName))

        data = self.c.fetchall()

        readData = []
        for row in data:
            readData.append(row[0])

        return readData 


    def save_to_database(self, data, tableName):
        """ Save data to database """

        #print('\nData: ',data)
        try:
            data['NLTAPEAKLOC']=data['NLTAPEAKLOC'][0]
        except:
            pass

        try:
            data['SLTAPEAKLOC']=data['SLTAPEAKLOC'][0]
        except:
            pass

        try:
            data['OLTAPEAKLOC']=data['OLTAPEAKLOC'][0]
        except:
            pass
        
        try:
            data['SRTAPEAKLOC']=data['SRTAPEAKLOC'][0]
        except:
            pass

        try:
            data['NRTAPEAKLOC']=data['NRTAPEAKLOC'][0]
        except:
            pass
        
        try:
            data['ORTAPEAKLOC']=data['ORTAPEAKLOC'][0]
        except:
            pass
        # for k,v in data.items():
        #     if "TAPEAK" in k:
        #         print(k,v, )
        # sys.exit()

        table = self.get_table_name(tableName) 
        self.set_table_name(table)
        self.create_table(data, table)
        self.populate_table(data, table)
        try:
            msg_wrapper("debug", self.log.debug,
                        "Captured data to database")
        except Exception:
            msg_wrapper("debug", self.log.debug,
                        "Values already captured to database")

    def create_table(self, data, tableName):
        """ Create an sql statement to create a table."""

        try:
            self.create_db()
        except Exception:
            pass

        #print(data)
        #sys.exit()
        sqlStmt = self.create_table_stmt(data, tableName)
        self.c.execute(sqlStmt)

    def create_table_stmt(self, data, tableName):
        """ Create table from dictionary. """

        sqlStmt = ""
       
        #print(data.items())
        #sys.exit()
        for key, value in data.items():
            # Make the filename a foreign key
            if key == "FILENAME":
                sqlStmt +=f'CREATE TABLE IF NOT EXISTS {tableName} ('
                idKey = sqlStmt + "id INTEGER PRIMARY KEY AUTOINCREMENT" + ", "
                sqlStmt = idKey + key + " " + "TEXT" + " UNIQUE , "
            elif isinstance(value, float):
                sqlStmt = sqlStmt + key + " " + "REAL" + " , "
            elif type(value).__name__ == "float64":
                sqlStmt = sqlStmt + key + " " + "REAL" + " , "
            elif isinstance(value, int):
                sqlStmt = sqlStmt + key + " " + "INTEGER" + " , "
            elif isinstance(value, str):
                sqlStmt = sqlStmt + key + " " + "TEXT" + " , "
        return sqlStmt[:-2] + ")"
      
        

    def insert_into_table_stmt_with_pk(self, data, tableName):
        """ Insert values into table and create a primary key."""

        sqlStmt = ""

        dataListKey = list(data.keys())
        dataListKeyString = ""
        dataListValues = list(data.values())
        dataListValueString = ""

        for i in range(len(dataListValues)):
            if i == 0:
                dataListKeyString = dataListKeyString + dataListKey[i]
            else:
                dataListKeyString = dataListKeyString + ", " + dataListKey[i]

        placeHolders = "?,"*len(data)

        sqlStmt = "INSERT INTO " + tableName + \
            " (" + dataListKeyString + ") VALUES (" + placeHolders[:-1] + ")"

        return sqlStmt, dataListValues

    def populate_table(self, data, tableName, key=""):
        """ populate a database table with values. """

        try:
            self.create_db()
        except Exception:
            pass

        #print('data: ',data)

        sqlStmt, values = self.insert_into_table_stmt_with_pk(data, tableName)
       
        #print(sqlStmt)

        try:
            self.c.execute(sqlStmt, values)
        except Exception as e:
            print("issue: ", e)

        self.commit_changes()

    def get_update_query_wb(self, data, status, beams, keys, values):
        """Get the values and keys which will be 
        updated in the database, this is for wide 
        beam data."""

        dbKeys = ["OLTA", "ORTA"]
        queryItems = ""
        queryDict = {}

        if (1 in status) or (2 in status):
            if len(beams) == 2:
                for i in range(len(beams)):
                    if beams[i] == "ONLCP":
                        if status[i] == 1 or status[i] == 2:
                            start = int(keys.index(dbKeys[0]))
                            end = int(keys.index(dbKeys[1]))
                            for t in range(start, end, 1):
                                queryItems = queryItems + \
                                    keys[t] + " = '" + str(values[t]) + "',"
                                queryDict[keys[t]] = values[t]
                        else:
                            pass
                    elif beams[i] == "ONRCP":
                        if status[i] == 1 or status[i] == 2:
                            start = int(keys.index(dbKeys[1]))
                            for t in range(start, len(data)):
                                queryItems = queryItems + \
                                    keys[t] + " = '" + str(values[t]) + "',"
                                queryDict[keys[t]] = values[t]
                        else:
                            pass
            else:
                pass
        else:
            msg_wrapper("debug",self.log.debug,"\nSaving everything as nans\n")

            if beams[0] == "ONLCP":
                start = int(keys.index(dbKeys[0]))
                for t in range(start, len(data)):
                    if "FLAG" in keys[t]:
                        queryItems = queryItems + \
                            keys[t] + " = '" + str(values[t]) + "',"
                        queryDict[keys[t]] = values[t]
                    else:
                        queryItems = queryItems + \
                            keys[t] + " = '" + str(np.nan) + "',"
                        queryDict[keys[t]] = values[t]

        return queryItems[:-1], queryDict


    def populate_queries(self, i, status, keys, values, dbKeys, ind1, ind2, queryItems, queryDict):
        """ Populate the query dictionary and query items. """
      
        if status[i] == 1 or status[i] == 2:
            start = int(keys.index(dbKeys[ind1]))
            end = int(keys.index(dbKeys[ind2]))

            for t in range(start, end, 1):
                queryItems = queryItems + \
                    keys[t] + " = '" + \
                    str(values[t]) + "',"
                queryDict[keys[t]] = values[t]
        
      
        return queryItems, queryDict

    def get_update_query_nb(self, data, status, beams, keys, values):
        """ Get the values and keys which will be 
        updated in the database, this is for narrow 
        beam data.
        """

        #print(keys)
        if "SLTA" in keys:
            dbKeys = ["SLTA", "NLTA", "OLTA", "SRTA", "NRTA", "ORTA"]
        elif "ASLTA" in keys:
            dbKeys = ["ASLTA", "BSLTA", "ANLTA", "BNLTA", "AOLTA", "BOLTA",
                       "ASRTA", "BSRTA", "ANRTA", "BNRTA", "AORTA", "BORTA"]

        queryItems = ""
        queryDict = {}

        if (1 in status) or (2 in status):

            if len(beams) == 6:

                if "SLTA" in keys:
                    for i in range(len(beams)):
                        if beams[i] == "HPSLCP":
                            queryItems, queryDict = self.populate_queries(
                                i, status, keys, values, dbKeys, 0, 1, queryItems, queryDict)

                        elif beams[i] == "HPNLCP":
                            queryItems, queryDict = self.populate_queries(i, status, keys, values, dbKeys, 1,2, queryItems, queryDict)

                        elif beams[i] == "ONLCP":
                            queryItems, queryDict = self.populate_queries(i, status, keys, values, dbKeys, 2,3, queryItems, queryDict)

                        elif beams[i] == "HPSRCP":
                            queryItems, queryDict = self.populate_queries(i, status, keys, values, dbKeys, 3,4, queryItems, queryDict)

                        elif beams[i] == "HPNRCP":
                            queryItems, queryDict = self.populate_queries(
                                i, status, keys, values, dbKeys, 4, 5, queryItems, queryDict)

                        elif beams[i] == "ONRCP":
                            if status[i] == 1 or status[i] == 2:
                                start = int(keys.index(dbKeys[5]))
                                for t in range(start, len(data)):
                                    queryItems = queryItems + \
                                        keys[t] + " = '" + \
                                        str(values[t]) + "',"
                                    queryDict[keys[t]] = values[t]

                elif "ASLTA" in keys:

                    for i in range(len(beams)):

                        if beams[i] == "HPSLCP":
                            queryItems, queryDict = self.populate_queries(i, status, keys, values, dbKeys, 0,2, queryItems, queryDict)
                            
                        elif beams[i] == "HPNLCP":
                            queryItems, queryDict = self.populate_queries(i, status, keys, values, dbKeys, 2,4, queryItems, queryDict)

                        elif beams[i] == "ONLCP":
                            queryItems, queryDict = self.populate_queries(i, status, keys, values, dbKeys, 4,6, queryItems, queryDict)

                        elif beams[i] == "HPSRCP":
                            queryItems, queryDict = self.populate_queries(
                                i, status, keys, values, dbKeys, 6, 8, queryItems, queryDict)

                        elif beams[i] == "HPNRCP":
                            if status[i] == 1 or status[i] == 2:
                                queryItems, queryDict = self.populate_queries(
                                    i, status, keys, values, dbKeys, 8, 10, queryItems, queryDict)

                        elif beams[i] == "ONRCP":
                            if status[i] == 1 or status[i] == 2:
                                start = int(keys.index(dbKeys[10]))
                                for t in range(start, len(data)):
                                    queryItems = queryItems + \
                                        keys[t] + " = '" + \
                                        str(values[t]) + "',"
                                    queryDict[keys[t]] = values[t]

        else:

            if dbKeys[0] == "SLTA" or dbKeys[0] == "ASLTA":

                start = int(keys.index(dbKeys[0]))
                for t in range(start, len(data)):
                    if "FLAG" in keys[t]:  
                        queryItems = queryItems + \
                            keys[t] + " = '" + str(100) + "',"
                        queryDict[keys[t]] = values[t]
                    else:
                        queryItems = queryItems + \
                            keys[t] + " = '" + str(np.nan) + "',"
                        queryDict[keys[t]] = values[t]

        return queryItems[:-1], queryDict

    def update_row_in_db(self, table, filename, data, status, beams):
        """ Update a row in a table. """

        #print(table, filename)
        keys = list((data).keys())
        values = list((data).values())

        if len(beams) == 2:

            queryItems, queryDict = self.get_update_query_wb(
                data, status, beams, keys, values)

            #print('\nqueryDict: ', queryDict)
            #print('\nqueryItems: ', queryItems)

            queryKeys = list(queryDict.keys())
            queryValues = list(queryDict.values())

            print('\nquery keys: ',queryKeys)

            dbKeysList=""
            for key in queryKeys:
                if "TA" in key:
                    dbKeysList = dbKeysList + key+","
   
            print("\nList of keys from database: ", dbKeysList)
       
            if 1 in status:

                # get data from database
                if data["OBJECTTYPE"] == "CAL":
                    stmt = "SELECT FLUX,"+dbKeysList[:-1]+" FROM "+table + \
                        ' WHERE FILENAME = "' + filename+'" ;'
                
                    self.c.execute(stmt)
                    databaseData = self.c.fetchall()

                    flux = databaseData[0][0]

                    # update pss
                    if 'OLTA' in queryKeys:
                        print("updating lcp pss")

                        psslcp, dpsslcp, appEfflcp = cp.calc_pss(
                            flux, queryDict["OLTA"], queryDict["OLDTA"])
                        queryDict['OLPSS'] = psslcp
                        queryDict['OLDPSS']= dpsslcp
                        queryDict['OLAPPEFF'] = appEfflcp
                      
                    if 'ORTA' in queryKeys:
                        print('updating rcp pss')

                        pssrcp, dpssrcp, appEffrcp = cp.calc_pss(
                            flux, queryDict["ORTA"], queryDict["ORDTA"])
                        queryDict['ORPSS'] = pssrcp
                        queryDict['ORDPSS']= dpssrcp
                        queryDict['ORAPPEFF'] = appEffrcp

                else:
                    stmt = "SELECT "+dbKeysList+" FROM "+table + \
                        ' WHERE FILENAME = "' + filename+'" ;' 

            elif 2 in status:

                # get data from database
                if data["OBJECTTYPE"] == "CAL":
                    stmt = "SELECT FLUX,"+dbKeysList[:-1]+" FROM "+table + \
                        ' WHERE FILENAME = "' + filename+'" ;'

                    if 'OLTA' in queryKeys:
                        print('setting lcp pss to None')
                        queryDict['OLPSS'] = str(np.nan)
                        queryDict['OLDPSS'] = str(np.nan)
                        queryDict['OLAPPEFF'] = str(np.nan)

                    if 'ORTA' in queryKeys:
                        print('setting rcp pss to None')
                        queryDict['ORPSS'] = str(np.nan)
                        queryDict['ORDPSS']= str(np.nan)
                        queryDict['ORAPPEFF'] = str(np.nan)

                else:
                    stmt = "SELECT "+dbKeysList+" FROM "+table + \
                        ' WHERE FILENAME = "' + filename+'" ;'

            else:
                print("\n-> Setting everything to nans")

        elif len(beams) == 6:
            queryItems, queryDict = self.get_update_query_nb(
                data, status, beams, keys, values)
            
            queryKeys = list(queryDict.keys())
            queryValues = list(queryDict.values())

            dbKeysList = ""
            for d in range(len(queryKeys)):
                if "TA" in queryKeys[d]:
                    dbKeysList = dbKeysList + queryKeys[d]+","
                elif "PSS" in queryKeys[d]:
                    dbKeysList = dbKeysList + queryKeys[d]+","

            print("\nUpdating: ", dbKeysList[:-1])
      
            if "SLTA" in keys:
                dbKeys = "SLTA,SLDTA,NLTA,NLDTA,OLTA,OLDTA,SRTA,SRDTA,NRTA,NRDTA,ORTA,ORDTA"

            elif "ASLTA" in keys:
                dbKeys = "ASLTA, ASLDTA, BSLTA, BSLDTA, ANLTA, ANLDTA, BNLTA, BNLDTA, AOLTA, AOLDTA, BOLTA, BOLDTA, ASRTA, ASRDTA, BSRTA, BSRDTA , ANRTA, ANRDTA, BNRTA, BNRDTA, AORTA, AORDTA, BORTA, BORDTA"

            if 1 in status or 2 in status:

                # get data from database
                if "TAR" in data['OBJECTTYPE']:
                    print('')
                    stmt = "SELECT "+dbKeys+" FROM "+table + \
                        ' WHERE FILENAME = "' + filename+'" ;'

                    self.c.execute(stmt)
                    databaseData = self.c.fetchall()

                    if "S" in data['BEAMTYPE']:
                        flux = databaseData[0][0]
                        slta = databaseData[0][1]
                        sldta = databaseData[0][2]
                        nlta = databaseData[0][3]
                        nldta = databaseData[0][4]
                        olta = databaseData[0][5]
                        oldta = databaseData[0][6]
                        srta = databaseData[0][7]
                        srdta = databaseData[0][8]
                        nrta = databaseData[0][9]
                        nrdta = databaseData[0][10]
                        orta = databaseData[0][11]
                        ordta = databaseData[0][12]

                        # FOR LCP
                        if 'SLTA' in queryKeys and 'NLTA' in queryKeys and 'OLTA' in queryKeys:

                            print('recalculate pss for all lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2, 
                            queryDict["SLTA"], queryDict["SLDTA"], queryDict["NLTA"], 
                            queryDict["NLDTA"], queryDict["OLTA"], queryDict["OLDTA"], flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        if 'SLTA' in queryKeys and 'NLTA' in queryKeys and 'OLTA' not in queryKeys:

                            print('recalculate pss for hps and hpn lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                queryDict["SLTA"], queryDict["SLDTA"], queryDict["NLTA"], 
                                queryDict["NLDTA"], olta, oldta, flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        if 'SLTA' in queryKeys and 'NLTA' not in queryKeys and 'OLTA' in queryKeys:

                            print('recalculate pss for s and o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2, 
                            queryDict["SLTA"], queryDict["SLDTA"], nlta, nldta, queryDict["OLTA"], 
                            queryDict["OLDTA"], flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        if 'SLTA' in queryKeys and 'NLTA' not in queryKeys and 'OLTA' not in queryKeys:

                            print('recalculate pss for s lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                queryDict["SLTA"], queryDict["SLDTA"], nlta, nldta, olta, oldta, 
                                flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff
                            
                        if 'SLTA' not in queryKeys and 'NLTA' in queryKeys and 'OLTA' in queryKeys:

                            print('recalculate pss for n lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                slta, sldta, queryDict["NLTA"], queryDict["NLDTA"], queryDict["OLTA"], 
                                queryDict["OLDTA"], flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        if 'SLTA' not in queryKeys and 'NLTA' not in queryKeys and 'OLTA' in queryKeys:

                            print('recalculate pss for o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                slta, sldta, nlta, nldta, queryDict["OLTA"], queryDict["OLDTA"], 
                                flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        if 'SLTA' not in queryKeys and 'NLTA' in queryKeys and 'OLTA' not in queryKeys:

                            print('recalculate pss for s and o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                slta, sldta, queryDict["NLTA"], queryDict["NLDTA"], olta, oldta, 
                                flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        # FOR RCP
                        if 'SRTA' in queryKeys and 'NRTA' in queryKeys and 'ORTA' in queryKeys:

                            print('recalculate pss for all rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5,
                                queryDict["SRTA"], queryDict["SRDTA"], queryDict["NRTA"], 
                                queryDict["NRDTA"], queryDict["ORTA"], queryDict["ORDTA"], 
                                flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' in queryKeys and 'NRTA' in queryKeys and 'ORTA' not in queryKeys:

                            print('recalculate pss for s and n rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5, 
                            queryDict["SRTA"], queryDict["SRDTA"], queryDict["NRTA"], 
                            queryDict["NRDTA"], orta, ordta, flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' in queryKeys and 'NRTA' not in queryKeys and 'ORTA' in queryKeys:

                            print('recalculate pss for s and o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5, 
                            queryDict["SRTA"], queryDict["SRDTA"], nrta, nrdta, queryDict["ORTA"], 
                            queryDict["ORDTA"], flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' in queryKeys and 'NRTA' not in queryKeys and 'ORTA' not in queryKeys:

                            print('recalculate pss for s rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5, 
                            queryDict["SRTA"], queryDict["SRDTA"], nrta, nrdta, orta, ordta, 
                            flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' not in queryKeys and 'NRTA' in queryKeys and 'ORTA' in queryKeys:

                            print('recalculate pss for n and o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5,
                                srta, srdta, queryDict["NRTA"], queryDict["NRDTA"], queryDict["ORTA"], 
                                queryDict["ORDTA"], flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' not in queryKeys and 'NRTA' not in queryKeys and 'ORTA' in queryKeys:

                            print('recalculate pss for o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(
                                5, srta, srdta, nrta, nrdta,  queryDict["ORTA"], queryDict["ORDTA"], 
                                flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' not in queryKeys and 'NRTA' in queryKeys and 'ORTA' not in queryKeys:

                            print('recalculate pss for n rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5,
                                srta, srdta, queryDict["NRTA"], queryDict["NRDTA"], orta, ordta, 
                                flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                    elif "D" in data["BEAMTYPE"]:
                        
                        aslta = databaseData[0][0]
                        asldta = databaseData[0][1]
                        bslta = databaseData[0][2]
                        bsldta = databaseData[0][3]

                        anlta = databaseData[0][4]
                        anldta = databaseData[0][5]
                        bnlta = databaseData[0][6]
                        bnldta = databaseData[0][7]
                        
                        aolta = databaseData[0][8]
                        aoldta = databaseData[0][9]
                        bolta = databaseData[0][10]
                        boldta = databaseData[0][11]

                        asrta = databaseData[0][12]
                        asrdta = databaseData[0][13]
                        bsrta = databaseData[0][14]
                        bsrdta = databaseData[0][15]
                        
                        anrta = databaseData[0][16]
                        anrdta = databaseData[0][17]
                        bnrta = databaseData[0][18]
                        bnrdta = databaseData[0][19]
                        
                        aorta = databaseData[0][20]
                        aordta = databaseData[0][21]
                        borta = databaseData[0][22]
                        bordta = databaseData[0][23]

                        # FOR LCP
                        if 'ASLTA' in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' in queryKeys:

                            #print('recalculate ONTA for all A BEAM lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2, 
                            queryDict["ASLTA"], queryDict["ASLDTA"], queryDict["ANLTA"], 
                            queryDict["ANLDTA"], queryDict["AOLTA"], queryDict["AOLDTA"], data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr

                        if 'BSLTA' in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' in queryKeys:

                            #print('recalculate pss for all B BEAM lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2, queryDict["BSLTA"], queryDict["BSLDTA"], 
                            Dict["BNLTA"], queryDict["BNLDTA"], queryDict["BOLTA"], queryDict["BOLDTA"], 
                            data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr


                        if 'ASLTA' in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' not in queryKeys:

                            #print('recalculate pss for A BEAM hps and hpn lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc( 2, 
                            queryDict["ASLTA"], queryDict["ASLDTA"], queryDict["ANLTA"], 
                            queryDict["ANLDTA"], aolta, aoldta,  data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr

                        if 'BSLTA' in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' not in queryKeys:

                            #print('recalculate pss for B BEAM hps and hpn lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(
                                2, queryDict["BSLTA"], queryDict["BSLDTA"], queryDict["BNLTA"], 
                                queryDict["BNLDTA"], bolta, boldta, data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr


                        if 'ASLTA' in queryKeys and 'ANLTA' not in queryKeys and 'AOLTA' in queryKeys:

                            #print('recalculate pss for A BEAM s and o lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(
                                2, queryDict["ASLTA"], queryDict["ASLDTA"], anlta, anldta, 
                                queryDict["AOLTA"], queryDict["AOLDTA"], data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr

                        if 'BSLTA' in queryKeys and 'BNLTA' not in queryKeys and 'BOLTA' in queryKeys:

                            #print('recalculate pss for B BEAM s and o lcp')
                            pc, Tcorr, Tcorerr= cp.calc_pc(
                                2, queryDict["BSLTA"], queryDict["BSLDTA"], bnlta, bnldta, 
                                queryDict["BOLTA"], queryDict["BOLDTA"], data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr


                        if 'ASLTA' in queryKeys and 'ANLTA' not in queryKeys and 'AOLTA' not in queryKeys:

                            #print('recalculate pss for A BEAM s lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2, 
                            queryDict["ASLTA"], queryDict["ASLDTA"], anlta, anldta, 
                            aolta, aoldta,  data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr

                        if 'BSLTA' in queryKeys and 'BNLTA' not in queryKeys and 'BOLTA' not in queryKeys:

                            #print('recalculate pss for B BEAM s lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2, 
                            queryDict["BSLTA"], queryDict["BSLDTA"], bnlta, bnldta, 
                            bolta, boldta, data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr


                        if 'ASLTA' not in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' in queryKeys:

                            #print('recalculate A BEAM pss for n lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2,
                            aslta, asldta, queryDict["ANLTA"], queryDict["ANLDTA"], 
                            queryDict["AOLTA"], queryDict["AOLDTA"],  data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr

                        if 'BSLTA' not in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' in queryKeys:

                            #print('recalculate B BEAM pss for n lcp')
                            pc, Tcorr, Tcorerr= cp.calc_pc(2,
                            bslta, bsldta, queryDict["BNLTA"], queryDict["BNLDTA"], 
                            queryDict["BOLTA"], queryDict["BOLDTA"], data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr


                        if 'ASLTA' not in queryKeys and 'ANLTA' not in queryKeys and 'AOLTA' in queryKeys:

                            #print('recalculate A BEAM pss for o lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2,
                            aslta, asldta, anlta, anldta, queryDict["AOLTA"], queryDict["AOLDTA"], 
                            data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr

                        if 'BSLTA' not in queryKeys and 'BNLTA' not in queryKeys and 'BOLTA' in queryKeys:

                            #print('recalculate pss for o lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2,
                            bslta, bsldta, bnlta, bnldta, queryDict["BOLTA"], queryDict["BOLDTA"], 
                            data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr


                        if 'ASLTA' not in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' not in queryKeys:

                            #print('recalculate A BEAM pss for s and o lcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2,
                            aslta, asldta, queryDict["ANLTA"], queryDict["ANLDTA"], 
                            aolta, aoldta, data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr

                        if 'BSLTA' not in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' not in queryKeys:

                            #print('recalculate B BEAM pss for s and o lcp')
                            pc, Tcorr, Tcorerr= cp.calc_pc(2,
                            bslta, bsldta, queryDict["BNLTA"], queryDict["BNLDTA"], 
                            bolta, boldta, data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr


                        # FOR RCP
                        if 'ASRTA' in queryKeys and 'ANRTA' in queryKeys and 'AORTA' in queryKeys:

                            print('recalculate pss for all A BEAM rcp')
                            pc, Tcorr, Tcorerr= cp.calc_pc(
                                2, queryDict["ASRTA"], queryDict["ASRDTA"], queryDict["ANRTA"], 
                                queryDict["ANRDTA"], queryDict["AORTA"], queryDict["AORDTA"], 
                                 data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr

                        if 'BSRTA' in queryKeys and 'BNRTA' in queryKeys and 'BORTA' in queryKeys:

                            print('recalculate pss for all B BEAM rcp')
                            pc, Tcorr, Tcorerr= cp.calc_pc(
                                2, queryDict["BSRTA"], queryDict["BSRDTA"], queryDict["BNRTA"], 
                                queryDict["BNRDTA"], queryDict["BORTA"], queryDict["BORDTA"], 
                                data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr

                        
                        if 'ASRTA' in queryKeys and 'ANRTA' in queryKeys and 'AORTA' not in queryKeys:

                            print('recalculate pss for A BEAM hps and hpn rcp')
                            pc, Tcorr, Tcorerr, appEff = cp.calc_pc(2,
                            queryDict["ASRTA"], queryDict["ASRDTA"], queryDict["ANRTA"],
                            queryDict["ANRDTA"], aorta, aordta,data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr

                        if 'BSRTA' in queryKeys and 'BNRTA' in queryKeys and 'BORTA' not in queryKeys:

                            print('recalculate pss for B BEAM hps and hpn rcp')
                            pc, Tcorr, Tcorerr, appEff = cp.calc_pc(
                                2, queryDict["BSRTA"], queryDict["BSRDTA"], 
                                queryDict["BNRTA"], queryDict["BNRDTA"], borta, bordta,  data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr

                        
                        if 'ASRTA' in queryKeys and 'ANRTA' not in queryKeys and 'AORTA' in queryKeys:

                            #print('recalculate pss for A BEAM s and o rcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(
                                2, queryDict["ASRTA"], queryDict["ASRDTA"], anrta, anrdta,
                                queryDict["AORTA"], queryDict["AORDTA"], data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr

                        if 'BSRTA' in queryKeys and 'BNRTA' not in queryKeys and 'BORTA' in queryKeys:

                            print('recalculate pss for B BEAM s and o rcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(
                                2, queryDict["BSRTA"], queryDict["BSRDTA"], bnrta, bnrdta,
                                queryDict["BORTA"], queryDict["BORDTA"], data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr


                        if 'ASRTA' in queryKeys and 'ANRTA' not in queryKeys and 'AORTA' not in queryKeys:

                            print('recalculate pss for A BEAM s rcp')
                            pc, Tcorr, Tcorerr= cp.calc_pc(2,
                                queryDict["ASRTA"], queryDict["ASRDTA"], anrta, anrdta,
                                aorta, aordta,  data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr

                        if 'BSRTA' in queryKeys and 'BNRTA' not in queryKeys and 'BORTA' not in queryKeys:

                            print('recalculate pss for B BEAM s rcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2,
                                queryDict["BSRTA"], queryDict["BSRDTA"], bnrta, bnrdta,
                                borta, bordta, data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr


                        if 'ASRTA' not in queryKeys and 'ANRTA' in queryKeys and 'AORTA' in queryKeys:

                            print('recalculate A BEAM pss for n rcp')
                            pc, Tcorr, Tcorerr= cp.calc_pc(2,
                                asrta, asrdta, queryDict["ANRTA"], queryDict["ANRDTA"],
                                queryDict["AORTA"], queryDict["AORDTA"], data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr

                        if 'BSRTA' not in queryKeys and 'BNRTA' in queryKeys and 'BORTA' in queryKeys:

                            #print('recalculate B BEAM pss for n rcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2,
                                bsrta, bsrdta, queryDict["BNRTA"], queryDict["BNRDTA"],
                                queryDict["BORTA"], queryDict["BORDTA"],  data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr


                        if 'ASRTA' not in queryKeys and 'ANRTA' not in queryKeys and 'AORTA' in queryKeys:

                            #print('recalculate A BEAM pss for o rcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2,
                                asrta, asrdta, anrta, anrdta, queryDict["AORTA"], queryDict["AORDTA"],
                                data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr

                        if 'BSRTA' not in queryKeys and 'BNRTA' not in queryKeys and 'BORTA' in queryKeys:

                            print('recalculate pss for B BEAM o rcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2,
                                bsrta, bsrdta, bnrta, bnrdta, queryDict["BORTA"], queryDict["BORDTA"],
                                data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr


                        if 'ASRTA' not in queryKeys and 'ANRTA' in queryKeys and 'AORTA' not in queryKeys:

                            #print('recalculate A BEAM pss for s and o rcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2,
                                asrta, asrdta, queryDict["ANRTA"], queryDict["ANRDTA"],
                                aorta, aordta, data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr

                        if 'BSRTA' not in queryKeys and 'BNRTA' in queryKeys and 'BORTA' not in queryKeys:

                            #print('recalculate B BEAM pss for s and o rcp')
                            pc, Tcorr, Tcorerr = cp.calc_pc(2,
                                bsrta, bsrdta, queryDict["BNRTA"], queryDict["BNRDTA"],
                                borta, bordta,  data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr

                else:

                    if "CAL" in data['OBJECTTYPE'] and data["OBJECT"] == "JUPITER":
                        stmt = "SELECT TOTAL_PLANET_FLUX_D,"+dbKeys+" FROM "+table + \
                            ' WHERE FILENAME = "' + filename+'" ;'
                    else:
                        stmt = "SELECT FLUX,"+dbKeys+" FROM "+table + \
                            ' WHERE FILENAME = "' + filename+'" ;'

                    self.c.execute(stmt)
                    databaseData = self.c.fetchall()

                    if "S" in data['BEAMTYPE']:
                        flux = databaseData[0][0]
                        slta = databaseData[0][1]
                        sldta = databaseData[0][2]
                        nlta = databaseData[0][3]
                        nldta = databaseData[0][4]
                        olta = databaseData[0][5]
                        oldta = databaseData[0][6]
                        srta = databaseData[0][7]
                        srdta = databaseData[0][8]
                        nrta = databaseData[0][9]
                        nrdta = databaseData[0][10]
                        orta = databaseData[0][11]
                        ordta = databaseData[0][12]

                        # FOR LCP
                        if 'SLTA' in queryKeys and 'NLTA' in queryKeys and 'OLTA' in queryKeys:

                            print('recalculate pss for all lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2, 
                            queryDict["SLTA"], queryDict["SLDTA"], queryDict["NLTA"], 
                            queryDict["NLDTA"], queryDict["OLTA"], queryDict["OLDTA"], flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        if 'SLTA' in queryKeys and 'NLTA' in queryKeys and 'OLTA' not in queryKeys:

                            print('recalculate pss for hps and hpn lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                queryDict["SLTA"], queryDict["SLDTA"], queryDict["NLTA"], 
                                queryDict["NLDTA"], olta, oldta, flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        if 'SLTA' in queryKeys and 'NLTA' not in queryKeys and 'OLTA' in queryKeys:

                            print('recalculate pss for s and o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2, 
                            queryDict["SLTA"], queryDict["SLDTA"], nlta, nldta, queryDict["OLTA"], 
                            queryDict["OLDTA"], flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        if 'SLTA' in queryKeys and 'NLTA' not in queryKeys and 'OLTA' not in queryKeys:

                            print('recalculate pss for s lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                queryDict["SLTA"], queryDict["SLDTA"], nlta, nldta, olta, oldta, 
                                flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff
                            
                        if 'SLTA' not in queryKeys and 'NLTA' in queryKeys and 'OLTA' in queryKeys:

                            print('recalculate pss for n lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                slta, sldta, queryDict["NLTA"], queryDict["NLDTA"], queryDict["OLTA"], 
                                queryDict["OLDTA"], flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        if 'SLTA' not in queryKeys and 'NLTA' not in queryKeys and 'OLTA' in queryKeys:

                            print('recalculate pss for o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                slta, sldta, nlta, nldta, queryDict["OLTA"], queryDict["OLDTA"], 
                                flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        if 'SLTA' not in queryKeys and 'NLTA' in queryKeys and 'OLTA' not in queryKeys:

                            print('recalculate pss for s and o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                slta, sldta, queryDict["NLTA"], queryDict["NLDTA"], olta, oldta, 
                                flux, data)

                            queryDict['OLPC'] = pc
                            queryDict['COLTA'] = Tcorr
                            queryDict['COLDTA'] = Tcorerr
                            queryDict['OLPSS'] = pss
                            queryDict['OLDPSS'] = psserr
                            queryDict['OLAPPEFF'] = appEff

                        # FOR RCP
                        if 'SRTA' in queryKeys and 'NRTA' in queryKeys and 'ORTA' in queryKeys:

                            print('recalculate pss for all rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5,
                                queryDict["SRTA"], queryDict["SRDTA"], queryDict["NRTA"], 
                                queryDict["NRDTA"], queryDict["ORTA"], queryDict["ORDTA"], 
                                flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' in queryKeys and 'NRTA' in queryKeys and 'ORTA' not in queryKeys:

                            print('recalculate pss for s and n rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5, 
                            queryDict["SRTA"], queryDict["SRDTA"], queryDict["NRTA"], 
                            queryDict["NRDTA"], orta, ordta, flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' in queryKeys and 'NRTA' not in queryKeys and 'ORTA' in queryKeys:

                            print('recalculate pss for s and o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5, 
                            queryDict["SRTA"], queryDict["SRDTA"], nrta, nrdta, queryDict["ORTA"], 
                            queryDict["ORDTA"], flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' in queryKeys and 'NRTA' not in queryKeys and 'ORTA' not in queryKeys:

                            print('recalculate pss for s rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5, 
                            queryDict["SRTA"], queryDict["SRDTA"], nrta, nrdta, orta, ordta, 
                            flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' not in queryKeys and 'NRTA' in queryKeys and 'ORTA' in queryKeys:

                            print('recalculate pss for n and o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5,
                                srta, srdta, queryDict["NRTA"], queryDict["NRDTA"], queryDict["ORTA"], 
                                queryDict["ORDTA"], flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' not in queryKeys and 'NRTA' not in queryKeys and 'ORTA' in queryKeys:

                            print('recalculate pss for o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(
                                5, srta, srdta, nrta, nrdta,  queryDict["ORTA"], queryDict["ORDTA"], 
                                flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                        if 'SRTA' not in queryKeys and 'NRTA' in queryKeys and 'ORTA' not in queryKeys:

                            print('recalculate pss for n rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(5,
                                srta, srdta, queryDict["NRTA"], queryDict["NRDTA"], orta, ordta, 
                                flux, data)

                            queryDict['ORPC'] = pc
                            queryDict['CORTA'] = Tcorr
                            queryDict['CORDTA'] = Tcorerr
                            queryDict['ORPSS'] = pss
                            queryDict['ORDPSS'] = psserr
                            queryDict['ORAPPEFF'] = appEff

                    elif "D" in data["BEAMTYPE"]:
                        
                        flux = databaseData[0][0]
                        aslta = databaseData[0][1]
                        asldta = databaseData[0][2]
                        bslta = databaseData[0][3]
                        bsldta = databaseData[0][4]
                        anlta = databaseData[0][5]
                        anldta = databaseData[0][6]
                        bnlta = databaseData[0][7]
                        bnldta = databaseData[0][8]
                        aolta = databaseData[0][9]
                        aoldta = databaseData[0][10]
                        bolta = databaseData[0][11]
                        boldta = databaseData[0][12]

                        asrta = databaseData[0][13]
                        asrdta = databaseData[0][14]
                        bsrta = databaseData[0][15]
                        bsrdta = databaseData[0][16]
                        anrta = databaseData[0][17]
                        anrdta = databaseData[0][18]
                        bnrta = databaseData[0][19]
                        bnrdta = databaseData[0][20]
                        aorta = databaseData[0][21]
                        aordta = databaseData[0][22]
                        borta = databaseData[0][23]
                        bordta = databaseData[0][24]

                        # FOR LCP
                        if 'ASLTA' in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' in queryKeys:

                            print('recalculate pss for all A BEAM lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2, 
                            queryDict["ASLTA"], queryDict["ASLDTA"], queryDict["ANLTA"], 
                            queryDict["ANLDTA"], queryDict["AOLTA"], queryDict["AOLDTA"], 
                            flux, data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr
                            queryDict['AOLPSS'] = pss
                            queryDict['AOLDPSS'] = psserr
                            queryDict['AOLAPPEFF'] = appEff

                        if 'BSLTA' in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' in queryKeys:

                            print('recalculate pss for all B BEAM lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2, queryDict["BSLTA"], queryDict["BSLDTA"], queryDict["BNLTA"], queryDict["BNLDTA"], queryDict["BOLTA"], queryDict["BOLDTA"], flux, data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr
                            queryDict['BOLPSS'] = pss
                            queryDict['BOLDPSS'] = psserr
                            queryDict['BOLAPPEFF'] = appEff


                        if 'ASLTA' in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' not in queryKeys:

                            print('recalculate pss for A BEAM hps and hpn lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss( 2, 
                            queryDict["ASLTA"], queryDict["ASLDTA"], queryDict["ANLTA"], 
                            queryDict["ANLDTA"], aolta, aoldta, flux, data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr
                            queryDict['AOLPSS'] = pss
                            queryDict['AOLDPSS'] = psserr
                            queryDict['AOLAPPEFF'] = appEff

                        if 'BSLTA' in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' not in queryKeys:

                            print('recalculate pss for B BEAM hps and hpn lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(
                                2, queryDict["BSLTA"], queryDict["BSLDTA"], queryDict["BNLTA"], queryDict["BNLDTA"], bolta, boldta, flux, data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr
                            queryDict['BOLPSS'] = pss
                            queryDict['BOLDPSS'] = psserr
                            queryDict['BOLAPPEFF'] = appEff


                        if 'ASLTA' in queryKeys and 'ANLTA' not in queryKeys and 'AOLTA' in queryKeys:

                            print('recalculate pss for A BEAM s and o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(
                                2, queryDict["ASLTA"], queryDict["ASLDTA"], anlta, anldta, 
                                queryDict["AOLTA"], queryDict["AOLDTA"], flux, data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr
                            queryDict['AOLPSS'] = pss
                            queryDict['AOLDPSS'] = psserr
                            queryDict['AOLAPPEFF'] = appEff

                        if 'BSLTA' in queryKeys and 'BNLTA' not in queryKeys and 'BOLTA' in queryKeys:

                            print('recalculate pss for B BEAM s and o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(
                                2, queryDict["BSLTA"], queryDict["BSLDTA"], bnlta, bnldta, 
                                queryDict["BOLTA"], queryDict["BOLDTA"], flux, data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr
                            queryDict['BOLPSS'] = pss
                            queryDict['BOLDPSS'] = psserr
                            queryDict['BOLAPPEFF'] = appEff


                        if 'ASLTA' in queryKeys and 'ANLTA' not in queryKeys and 'AOLTA' not in queryKeys:

                            print('recalculate pss for A BEAM s lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2, 
                            queryDict["ASLTA"], queryDict["ASLDTA"], anlta, anldta, 
                            aolta, aoldta, flux, data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr
                            queryDict['AOLPSS'] = pss
                            queryDict['AOLDPSS'] = psserr
                            queryDict['AOLAPPEFF'] = appEff

                        if 'BSLTA' in queryKeys and 'BNLTA' not in queryKeys and 'BOLTA' not in queryKeys:

                            print('recalculate pss for B BEAM s lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2, 
                            queryDict["BSLTA"], queryDict["BSLDTA"], bnlta, bnldta, 
                            bolta, boldta, flux, data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr
                            queryDict['BOLPSS'] = pss
                            queryDict['BOLDPSS'] = psserr
                            queryDict['BOLAPPEFF'] = appEff


                        if 'ASLTA' not in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' in queryKeys:

                            print('recalculate A BEAM pss for n lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                            aslta, asldta, queryDict["ANLTA"], queryDict["ANLDTA"], 
                            queryDict["AOLTA"], queryDict["AOLDTA"], flux, data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr
                            queryDict['AOLPSS'] = pss
                            queryDict['AOLDPSS'] = psserr
                            queryDict['AOLAPPEFF'] = appEff

                        if 'BSLTA' not in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' in queryKeys:

                            print('recalculate B BEAM pss for n lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                            bslta, bsldta, queryDict["BNLTA"], queryDict["BNLDTA"], 
                            queryDict["BOLTA"], queryDict["BOLDTA"], flux, data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr
                            queryDict['BOLPSS'] = pss
                            queryDict['BOLDPSS'] = psserr
                            queryDict['BOLAPPEFF'] = appEff


                        if 'ASLTA' not in queryKeys and 'ANLTA' not in queryKeys and 'AOLTA' in queryKeys:

                            print('recalculate A BEAM pss for o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                            aslta, asldta, anlta, anldta, queryDict["AOLTA"], queryDict["AOLDTA"], 
                            flux, data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr
                            queryDict['AOLPSS'] = pss
                            queryDict['AOLDPSS'] = psserr
                            queryDict['AOLAPPEFF'] = appEff

                        if 'BSLTA' not in queryKeys and 'BNLTA' not in queryKeys and 'BOLTA' in queryKeys:

                            print('recalculate pss for o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                            bslta, bsldta, bnlta, bnldta, queryDict["BOLTA"], queryDict["BOLDTA"], 
                            flux, data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr
                            queryDict['BOLPSS'] = pss
                            queryDict['BOLDPSS'] = psserr
                            queryDict['BOLAPPEFF'] = appEff


                        if 'ASLTA' not in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' not in queryKeys:

                            print('recalculate A BEAM pss for s and o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                            aslta, asldta, queryDict["ANLTA"], queryDict["ANLDTA"], 
                            aolta, aoldta, flux, data)

                            queryDict['AOLPC'] = pc
                            queryDict['ACOLTA'] = Tcorr
                            queryDict['ACOLDTA'] = Tcorerr
                            queryDict['AOLPSS'] = pss
                            queryDict['AOLDPSS'] = psserr
                            queryDict['AOLAPPEFF'] = appEff

                        if 'BSLTA' not in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' not in queryKeys:

                            print('recalculate B BEAM pss for s and o lcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                            bslta, bsldta, queryDict["BNLTA"], queryDict["BNLDTA"], 
                            bolta, boldta, flux, data)

                            queryDict['BOLPC'] = pc
                            queryDict['BCOLTA'] = Tcorr
                            queryDict['BCOLDTA'] = Tcorerr
                            queryDict['BOLPSS'] = pss
                            queryDict['BOLDPSS'] = psserr
                            queryDict['BOLAPPEFF'] = appEff


                        # FOR RCP
                        if 'ASRTA' in queryKeys and 'ANRTA' in queryKeys and 'AORTA' in queryKeys:

                            print('recalculate pss for all A BEAM rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(
                                2, queryDict["ASRTA"], queryDict["ASRDTA"], queryDict["ANRTA"], 
                                queryDict["ANRDTA"], queryDict["AORTA"], queryDict["AORDTA"], 
                                flux, data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr
                            queryDict['AORPSS'] = pss
                            queryDict['AORDPSS'] = psserr
                            queryDict['AORAPPEFF'] = appEff

                        if 'BSRTA' in queryKeys and 'BNRTA' in queryKeys and 'BORTA' in queryKeys:

                            print('recalculate pss for all B BEAM rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(
                                2, queryDict["BSRTA"], queryDict["BSRDTA"], queryDict["BNRTA"], 
                                queryDict["BNRDTA"], queryDict["BORTA"], queryDict["BORDTA"], 
                                flux, data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr
                            queryDict['BORPSS'] = pss
                            queryDict['BORDPSS'] = psserr
                            queryDict['BORAPPEFF'] = appEff

                        
                        if 'ASRTA' in queryKeys and 'ANRTA' in queryKeys and 'AORTA' not in queryKeys:

                            print('recalculate pss for A BEAM hps and hpn rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                            queryDict["ASRTA"], queryDict["ASRDTA"], queryDict["ANRTA"],
                            queryDict["ANRDTA"], aorta, aordta, flux, data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr
                            queryDict['AORPSS'] = pss
                            queryDict['AORDPSS'] = psserr
                            queryDict['AORAPPEFF'] = appEff

                        if 'BSRTA' in queryKeys and 'BNRTA' in queryKeys and 'BORTA' not in queryKeys:

                            print('recalculate pss for B BEAM hps and hpn rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(
                                2, queryDict["BSRTA"], queryDict["BSRDTA"], 
                                queryDict["BNRTA"], queryDict["BNRDTA"], borta, bordta, flux, data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr
                            queryDict['BORPSS'] = pss
                            queryDict['BORDPSS'] = psserr
                            queryDict['BORAPPEFF'] = appEff

                        
                        if 'ASRTA' in queryKeys and 'ANRTA' not in queryKeys and 'AORTA' in queryKeys:

                            print('recalculate pss for A BEAM s and o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(
                                2, queryDict["ASRTA"], queryDict["ASRDTA"], anrta, anrdta,
                                queryDict["AORTA"], queryDict["AORDTA"], flux, data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr
                            queryDict['AORPSS'] = pss
                            queryDict['AORDPSS'] = psserr
                            queryDict['AORAPPEFF'] = appEff

                        if 'BSRTA' in queryKeys and 'BNRTA' not in queryKeys and 'BORTA' in queryKeys:

                            print('recalculate pss for B BEAM s and o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(
                                2, queryDict["BSRTA"], queryDict["BSRDTA"], bnrta, bnrdta,
                                queryDict["BORTA"], queryDict["BORDTA"], flux, data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr
                            queryDict['BORPSS'] = pss
                            queryDict['BORDPSS'] = psserr
                            queryDict['BORAPPEFF'] = appEff


                        if 'ASRTA' in queryKeys and 'ANRTA' not in queryKeys and 'AORTA' not in queryKeys:

                            print('recalculate pss for A BEAM s rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                queryDict["ASRTA"], queryDict["ASRDTA"], anrta, anrdta,
                                aorta, aordta, flux, data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr
                            queryDict['AORPSS'] = pss
                            queryDict['AORDPSS'] = psserr
                            queryDict['AORAPPEFF'] = appEff

                        if 'BSRTA' in queryKeys and 'BNRTA' not in queryKeys and 'BORTA' not in queryKeys:

                            print('recalculate pss for B BEAM s rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                queryDict["BSRTA"], queryDict["BSRDTA"], bnrta, bnrdta,
                                borta, bordta, flux, data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr
                            queryDict['BORPSS'] = pss
                            queryDict['BORDPSS'] = psserr
                            queryDict['BORAPPEFF'] = appEff


                        if 'ASRTA' not in queryKeys and 'ANRTA' in queryKeys and 'AORTA' in queryKeys:

                            print('recalculate A BEAM pss for n rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                asrta, asrdta, queryDict["ANRTA"], queryDict["ANRDTA"],
                                queryDict["AORTA"], queryDict["AORDTA"], flux, data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr
                            queryDict['AORPSS'] = pss
                            queryDict['AORDPSS'] = psserr
                            queryDict['AORAPPEFF'] = appEff

                        if 'BSRTA' not in queryKeys and 'BNRTA' in queryKeys and 'BORTA' in queryKeys:

                            print('recalculate B BEAM pss for n rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                bsrta, bsrdta, queryDict["BNRTA"], queryDict["BNRDTA"],
                                queryDict["BORTA"], queryDict["BORDTA"], flux, data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr
                            queryDict['BORPSS'] = pss
                            queryDict['BORDPSS'] = psserr
                            queryDict['BORAPPEFF'] = appEff


                        if 'ASRTA' not in queryKeys and 'ANRTA' not in queryKeys and 'AORTA' in queryKeys:

                            print('recalculate A BEAM pss for o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                asrta, asrdta, anrta, anrdta, queryDict["AORTA"], queryDict["AORDTA"],
                                flux, data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr
                            queryDict['AORPSS'] = pss
                            queryDict['AORDPSS'] = psserr
                            queryDict['AORAPPEFF'] = appEff

                        if 'BSRTA' not in queryKeys and 'BNRTA' not in queryKeys and 'BORTA' in queryKeys:

                            print('recalculate pss for B BEAM o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                bsrta, bsrdta, bnrta, bnrdta, queryDict["BORTA"], queryDict["BORDTA"],
                                flux, data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr
                            queryDict['BORPSS'] = pss
                            queryDict['BORDPSS'] = psserr
                            queryDict['BORAPPEFF'] = appEff


                        if 'ASRTA' not in queryKeys and 'ANRTA' in queryKeys and 'AORTA' not in queryKeys:

                            print('recalculate A BEAM pss for s and o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                asrta, asrdta, queryDict["ANRTA"], queryDict["ANRDTA"],
                                aorta, aordta, flux, data)

                            queryDict['AORPC'] = pc
                            queryDict['ACORTA'] = Tcorr
                            queryDict['ACORDTA'] = Tcorerr
                            queryDict['AORPSS'] = pss
                            queryDict['AORDPSS'] = psserr
                            queryDict['AORAPPEFF'] = appEff

                        if 'BSRTA' not in queryKeys and 'BNRTA' in queryKeys and 'BORTA' not in queryKeys:

                            print('recalculate B BEAM pss for s and o rcp')
                            pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
                                bsrta, bsrdta, queryDict["BNRTA"], queryDict["BNRDTA"],
                                borta, bordta, flux, data)

                            queryDict['BORPC'] = pc
                            queryDict['BCORTA'] = Tcorr
                            queryDict['BCORDTA'] = Tcorerr
                            queryDict['BORPSS'] = pss
                            queryDict['BORDPSS'] = psserr
                            queryDict['BORAPPEFF'] = appEff

            # elif 2 in status:

            #     if "TAR" in data['OBJECTTYPE']:
            #         stmt = "SELECT "+dbKeysList[:-1]+" FROM "+table + \
            #             ' WHERE FILENAME = "' + filename+'" ;'
            #     else:
            #         if "CAL" in data['OBJECTTYPE'] and data["OBJECT"] == "JUPITER":
            #             stmt = "SELECT TOTAL_PLANET_FLUX_D,"+dbKeys+" FROM "+table + \
            #                 ' WHERE FILENAME = "' + filename+'" ;'
            #         else:
            #             stmt = "SELECT FLUX,"+dbKeys+" FROM "+table + \
            #                 ' WHERE FILENAME = "' + filename+'" ;'

            #         self.c.execute(stmt)
            #         databaseData = self.c.fetchall()

            #         if "S" in data['BEAMTYPE']:
            #             flux = databaseData[0][0]
            #             slta = databaseData[0][1]
            #             sldta = databaseData[0][2]
            #             nlta = databaseData[0][3]
            #             nldta = databaseData[0][4]
            #             olta = databaseData[0][5]
            #             oldta = databaseData[0][6]
            #             srta = databaseData[0][7]
            #             srdta = databaseData[0][8]
            #             nrta = databaseData[0][9]
            #             nrdta = databaseData[0][10]
            #             orta = databaseData[0][11]
            #             ordta = databaseData[0][12]

            #             # FOR LCP
            #             if 'SLTA' in queryKeys and 'NLTA' in queryKeys and 'OLTA' in queryKeys:
            #                 # recalculate pss
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_lcp_stats(queryDict)

            #             if 'SLTA' in queryKeys and 'NLTA' in queryKeys and 'OLTA' not in queryKeys:
            #                 print('setting lcp pss to None')
            #                 #queryDict = self.set_lcp_stats(queryDict)

            #                 print('recalculate pss for hps and hpn lcp')
            #                 pss, psserr, pc, Tcorr, Tcorerr, appEff = cp.calc_pc_pss(2,
            #                     queryDict["SLTA"], queryDict["SLDTA"], queryDict["NLTA"], 
            #                     queryDict["NLDTA"], olta, oldta, flux, data)

            #                 queryDict['OLPC'] = pc
            #                 queryDict['COLTA'] = Tcorr
            #                 queryDict['COLDTA'] = Tcorerr
            #                 queryDict['OLPSS'] = pss
            #                 queryDict['OLDPSS'] = psserr
            #                 queryDict['OLAPPEFF'] = appEff

            #             if 'SLTA' in queryKeys and 'NLTA' not in queryKeys and 'OLTA' in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_lcp_stats(queryDict)

            #             if 'SLTA' in queryKeys and 'NLTA' not in queryKeys and 'OLTA' not in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_lcp_stats(queryDict)
                            
            #             if 'SLTA' not in queryKeys and 'NLTA' in queryKeys and 'OLTA' in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_lcp_stats(queryDict)

            #             if 'SLTA' not in queryKeys and 'NLTA' not in queryKeys and 'OLTA' in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_lcp_stats(queryDict)

            #             if 'SLTA' not in queryKeys and 'NLTA' in queryKeys and 'OLTA' not in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_lcp_stats(queryDict)

            #             # FOR RCP

            #             if 'SRTA' in queryKeys and 'NRTA' in queryKeys and 'ORTA' in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_rcp_stats(queryDict)

            #             if 'SRTA' in queryKeys and 'NRTA' in queryKeys and 'ORTA' not in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_rcp_stats(queryDict)

            #             if 'SRTA' in queryKeys and 'NRTA' not in queryKeys and 'ORTA' in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_rcp_stats(queryDict)

            #             if 'SRTA' in queryKeys and 'NRTA' not in queryKeys and 'ORTA' not in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_rcp_stats(queryDict)

            #             if 'SRTA' not in queryKeys and 'NRTA' in queryKeys and 'ORTA' in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_rcp_stats(queryDict)

            #             if 'SRTA' not in queryKeys and 'NRTA' not in queryKeys and 'ORTA' in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_rcp_stats(queryDict)

            #             if 'SRTA' not in queryKeys and 'NRTA' in queryKeys and 'ORTA' not in queryKeys:
            #                 print('setting lcp pss to None')
            #                 queryDict = self.set_rcp_stats(queryDict)

            #         elif "D" in data["BEAMTYPE"]:

            #             # FOR LCP
            #             if 'ASLTA' in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' in queryKeys:

            #                 print('recalculate pss for all A BEAM lcp')
            #                 queryDict = self.set_a_lcp_stats(queryDict)

            #             if 'BSLTA' in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' in queryKeys:

            #                 print('recalculate pss for all B BEAM lcp')
            #                 queryDict = self.set_b_lcp_stats(queryDict)

            #             if 'ASLTA' in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' not in queryKeys:

            #                 print('recalculate pss for A BEAM hps and hpn lcp')
            #                 queryDict = self.set_a_lcp_stats(queryDict)

            #             if 'BSLTA' in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' not in queryKeys:

            #                 print('recalculate pss for B BEAM hps and hpn lcp')
            #                 queryDict = self.set_b_lcp_stats(queryDict)

            #             if 'ASLTA' in queryKeys and 'ANLTA' not in queryKeys and 'AOLTA' in queryKeys:

            #                 print('recalculate pss for A BEAM s and o lcp')
            #                 queryDict = self.set_a_lcp_stats(queryDict)

            #             if 'BSLTA' in queryKeys and 'BNLTA' not in queryKeys and 'BOLTA' in queryKeys:

            #                 print('recalculate pss for B BEAM s and o lcp')
            #                 queryDict = self.set_b_lcp_stats(queryDict)

            #             if 'ASLTA' in queryKeys and 'ANLTA' not in queryKeys and 'AOLTA' not in queryKeys:

            #                 print('recalculate pss for A BEAM s lcp')
            #                 queryDict = self.set_a_lcp_stats(queryDict)

            #             if 'BSLTA' in queryKeys and 'BNLTA' not in queryKeys and 'BOLTA' not in queryKeys:

            #                 print('recalculate pss for B BEAM s lcp')
            #                 queryDict = self.set_b_lcp_stats(queryDict)

            #             if 'ASLTA' not in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' in queryKeys:

            #                 print('recalculate A BEAM pss for n lcp')
            #                 queryDict = self.set_a_lcp_stats(queryDict)

            #             if 'BSLTA' not in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' in queryKeys:

            #                 print('recalculate B BEAM pss for n lcp')
            #                 queryDict = self.set_b_lcp_stats(queryDict)

            #             if 'ASLTA' not in queryKeys and 'ANLTA' not in queryKeys and 'AOLTA' in queryKeys:

            #                 print('recalculate A BEAM pss for o lcp')
            #                 queryDict = self.set_a_lcp_stats(queryDict)

            #             if 'BSLTA' not in queryKeys and 'BNLTA' not in queryKeys and 'BOLTA' in queryKeys:

            #                 print('recalculate pss for o lcp')
            #                 queryDict = self.set_b_lcp_stats(queryDict)

            #             if 'ASLTA' not in queryKeys and 'ANLTA' in queryKeys and 'AOLTA' not in queryKeys:

            #                 print('recalculate A BEAM pss for s and o lcp')
            #                 queryDict = self.set_a_lcp_stats(queryDict)

            #             if 'BSLTA' not in queryKeys and 'BNLTA' in queryKeys and 'BOLTA' not in queryKeys:

            #                 print('recalculate B BEAM pss for s and o lcp')
            #                 queryDict = self.set_b_lcp_stats(queryDict)

            #             # FOR RCP
            #             if 'ASRTA' in queryKeys and 'ANRTA' in queryKeys and 'AORTA' in queryKeys:

            #                 print('recalculate pss for all A BEAM rcp')
            #                 queryDict = self.set_a_rcp_stats(queryDict)

            #             if 'BSRTA' in queryKeys and 'BNRTA' in queryKeys and 'BORTA' in queryKeys:

            #                 print('recalculate pss for all B BEAM rcp')
            #                 queryDict = self.set_b_rcp_stats(queryDict)

            #             if 'ASRTA' in queryKeys and 'ANRTA' in queryKeys and 'AORTA' not in queryKeys:

            #                 print('recalculate pss for A BEAM hps and hpn rcp')
            #                 queryDict = self.set_a_rcp_stats(queryDict)

            #             if 'BSRTA' in queryKeys and 'BNRTA' in queryKeys and 'BORTA' not in queryKeys:

            #                 print('recalculate pss for B BEAM hps and hpn rcp')
            #                 queryDict = self.set_b_rcp_stats(queryDict)


            #             if 'ASRTA' in queryKeys and 'ANRTA' not in queryKeys and 'AORTA' in queryKeys:

            #                 print('recalculate pss for A BEAM s and o rcp')
            #                 queryDict = self.set_a_rcp_stats(queryDict)

            #             if 'BSRTA' in queryKeys and 'BNRTA' not in queryKeys and 'BORTA' in queryKeys:

            #                 print('recalculate pss for B BEAM s and o rcp')
            #                 queryDict = self.set_b_rcp_stats(queryDict)


            #             if 'ASRTA' in queryKeys and 'ANRTA' not in queryKeys and 'AORTA' not in queryKeys:

            #                 print('recalculate pss for A BEAM s rcp')
            #                 queryDict = self.set_a_rcp_stats(queryDict)

            #             if 'BSRTA' in queryKeys and 'BNRTA' not in queryKeys and 'BORTA' not in queryKeys:

            #                 print('recalculate pss for B BEAM s rcp')
            #                 queryDict = self.set_b_rcp_stats(queryDict)


            #             if 'ASRTA' not in queryKeys and 'ANRTA' in queryKeys and 'AORTA' in queryKeys:

            #                 print('recalculate A BEAM pss for n rcp')
            #                 queryDict = self.set_a_rcp_stats(queryDict)

            #             if 'BSRTA' not in queryKeys and 'BNRTA' in queryKeys and 'BORTA' in queryKeys:

            #                 print('recalculate B BEAM pss for n rcp')
            #                 queryDict = self.set_b_rcp_stats(queryDict)


            #             if 'ASRTA' not in queryKeys and 'ANRTA' not in queryKeys and 'AORTA' in queryKeys:

            #                 print('recalculate A BEAM pss for o rcp')
            #                 queryDict = self.set_a_rcp_stats(queryDict)

            #             if 'BSRTA' not in queryKeys and 'BNRTA' not in queryKeys and 'BORTA' in queryKeys:

            #                 print('recalculate pss for B BEAM o rcp')
            #                 queryDict = self.set_b_rcp_stats(queryDict)


            #             if 'ASRTA' not in queryKeys and 'ANRTA' in queryKeys and 'AORTA' not in queryKeys:

            #                 print('recalculate A BEAM pss for s and o rcp')
            #                 queryDict = self.set_a_rcp_stats(queryDict)

            #             if 'BSRTA' not in queryKeys and 'BNRTA' in queryKeys and 'BORTA' not in queryKeys:

            #                 print('recalculate B BEAM pss for s and o rcp')
            #                 queryDict = self.set_b_rcp_stats(queryDict)

            else:
                print("setting everything to nans")

        else:
            print("Beam length out of range")
            sys.exit()

        queryList = ', '.join(key +"='"+ str(val)+"'" for key, val in queryDict.items())
        #print(queryList)
        #print(queryDict)
        #sys.exit()
        query = "UPDATE "+table+" SET "+queryList + \
            ' WHERE FILENAME = "' + filename+'" ;'
        print("\nUpdate query: \n", query, "\n")
      
        self.c.execute(query)
        self.commit_changes()

    def set_lcp_stats(self, queryDict):
        """ Set the pss entries for LCP """
        
        queryDict.update({
            'OLPC': str(np.nan),
            'COLTA': str(np.nan),
            'COLDTA': str(np.nan),
            'OLPSS': str(np.nan),
            'OLDPSS': str(np.nan),
            'OLAPPEFF': str(np.nan)
        })
        return queryDict

    def set_rcp_stats(self, queryDict):
        """set the pss entries for lcp"""       
        queryDict['ORPC'] = str(np.nan)
        queryDict['CORTA'] = str(np.nan)
        queryDict['CORDTA'] = str(np.nan)
        queryDict['ORPSS'] = str(np.nan)
        queryDict['ORDPSS'] = str(np.nan)
        queryDict['ORAPPEFF'] = str(np.nan)
        return queryDict

    def set_a_lcp_stats(self, queryDict):
        
        """ set the pss entries for lcp"""
        queryDict['AOLPC'] = str(np.nan)
        queryDict['ACOLTA'] = str(np.nan)
        queryDict['ACOLDTA'] = str(np.nan)
        queryDict['AOLPSS'] = str(np.nan)
        queryDict['AOLDPSS'] = str(np.nan)
        queryDict['AOLAPPEFF'] = str(np.nan)
        return queryDict

    def set_b_lcp_stats(self, queryDict):

        """ set the pss entries for lcp"""
        queryDict['BOLPC'] = str(np.nan)
        queryDict['BCOLTA'] = str(np.nan)
        queryDict['BCOLDTA'] = str(np.nan)
        queryDict['BOLPSS'] = str(np.nan)
        queryDict['BOLDPSS'] = str(np.nan)
        queryDict['BOLAPPEFF'] = str(np.nan)
        return queryDict

    def set_a_rcp_stats(self, queryDict):

        """ set the pss entries for lcp"""
        queryDict['AORPC'] = str(np.nan)
        queryDict['ACORTA'] = str(np.nan)
        queryDict['ACORDTA'] = str(np.nan)
        queryDict['AORPSS'] = str(np.nan)
        queryDict['AORDPSS'] = str(np.nan)
        queryDict['AORAPPEFF'] = str(np.nan)
        return queryDict

    def set_b_rcp_stats(self, queryDict):

        """ set the pss entries for lcp"""
        queryDict['BORPC'] = str(np.nan)
        queryDict['BCORTA'] = str(np.nan)
        queryDict['BCORDTA'] = str(np.nan)
        queryDict['BORPSS'] = str(np.nan)
        queryDict['BORDPSS'] = str(np.nan)
        queryDict['BORAPPEFF'] = str(np.nan)
        return queryDict
