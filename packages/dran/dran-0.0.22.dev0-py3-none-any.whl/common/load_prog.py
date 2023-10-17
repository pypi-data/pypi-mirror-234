
import sys
import pandas as pd

# Local imports
# --------------------------------------------------------------------------- #
from common.messaging import msg_wrapper, print_start, load_prog
from common.quick_reader import QuickReader
from common.log_conf import configure_logging
from common.sqlite_db import SQLiteDB
from common.file_handler import FileHandler

class LoadProg():
    """Run common initialization processes depending on user input"""

    def __init__(self,args,log):
        # print(args)

        
        if args.quickview:
            if args.f:
                quick = QuickReader(args.f)
            else:
                msg_wrapper("error",log.error,"quickview requires a file fo view")
                sys.exit()
        else:
            pass
        
        if args.conv== "CALDB.db" or args.conv == "TARDB.db":

            msg_wrapper("info",log.info,f'Converting {args.conv} tables to csv files')
            try:
                db=SQLiteDB(databaseName=args.conv,log=log)
            except:
                msg_wrapper("error",log.error,"Please enter a valid SQLite database name")
                sys.exit()
            db.create_db()
            dbTables = db.get_table_names(args.conv)
            
            for i in range(len(dbTables)):
                ind, col_names, col_type = db.get_table_coloumns(dbTables[i])
                rows = db.get_rows(dbTables[i])
    
                msg_wrapper("info",log.info,f'Converting table {dbTables[i]} to csv file.')
                
                #Get rows from specified table
                ind, col_names, col_type = db.get_all_table_coloumns(dbTables[i])
                rows = db.get_rows_of_cols(dbTables[i],col_names)

                # create dataframe
                df = pd.DataFrame(list(rows), columns = col_names)
                df.to_csv(dbTables[i]+".csv")
        elif args.conv==None:
            pass        
        else:
            print("\nPlease enter a valid SQLite database name\n")
            sys.exit()

        if args.delete_db:
            if ".db" in args.delete_db:
                fh = FileHandler(log,args.delete_db)

                # delete given database name
                msg_wrapper("debug", log.debug,
                            f"Deleting {args.delete_db} database.")
                fh.delete_file(args.delete_db)
            else:
                print(f"The database '{args.delete_db}' does not exists")
                print("Check the name and try again\n")

        # if args.deleteFrom:
        # Delete an observation from the dtabase
        #     if (args.deleteFrom != None) and (args.f != None):
        #         msg_wrapper("debug",log.debug,f"Deleting row from {args.deleteFrom} database")

        #         # Delete row from database given the database name and filename
        #         dbName = args.deleteFrom 
        #         filePath  = args.f

        #         # get file and table to process
        #         fh = FileHandler(log,filePath)
        #         table=(fh.folderName).lower()
        #         file=fh.fileName

        #         # check if database exists
        #         db = SQLiteDB(databaseName=dbName,log=log)
        #         isDB=db.db_exists(db.databaseName)
        #         if isDB == True:
        #             db.create_db()
        #         else:
        #             print(f'The database {dbName} does not exists.\n')
        #             sys.exit()

        #         # Get all tables in database
        #         dbTables = db.get_table_names(dbName)
        #         if table in dbTables:
        #             # Get rows from specified table
        #             data = db.select_row(table,file)
            
        #             if len(data) >= 1:
        #                 db.delete_row(table,file)
        #             else:
        #                 print(f'The entry for file {file} does not exist in table {table}.\n')
        #                 sys.exit()
        #         else:
        #             print(f'{table} table does not exist. \n')
        #             sys.exit()
        #         sys.exit()
        #     else:
        #         if args.f == None:
        #             msg_wrapper("debug", log.debug,f"No file name given to delete.")


        
