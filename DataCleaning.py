from pandas.io.json import json_normalize
import pandas as pd
from pprint import pprint # to pretty print the cursor result.
import pandas as pd
import pymongo
"""
1. remove the station codes and flags if any
2. remove duplicate rows
3. correct timestamp
"""
class DataCleaning :
    def __init__(self):
        self.client = pymongo.MongoClient()
        #db and collection for testing purpose
        #self.db = self.client.currentTest
        self.db = self.client.qaplatformdb
        self.collection = self.db.wqprocess
        pass

    def cleanCSVData(self,filename):
        """
        take input as a csv file, clean data and store it into database for further parameter calculation
        :param filename: 
        :return: 
        """
        # set DateTimeStamp as index for the table
        df = pd.read_csv(filename,encoding='latin1')
        # remove columns
        columnSet = ['Station_Code', 'isSWMP', 'Historical', 'ProvisionalPlus', 'F_Record', 'F_Temp', 'F_SpCond',
                     'F_Sal', 'F_DO_pct',
                     'F_DO_mgl', 'F_Depth', 'F_cDepth', 'F_pH', 'F_Turb', 'ChlFluor', 'EC_ChlFluor', 'EC_DO_mgl',
                     'EC_DO_pct', 'EC_Depth',
                     'EC_Level', 'EC_Sal', 'EC_SpCond', 'EC_SpCond', 'EC_Temp', 'EC_Turb', 'EC_cDepth', 'EC_cLevel',
                     'EC_pH', 'F_ChlFluor',
                     'F_Level', 'F_cLevel', 'F_cLevel', 'ID', 'Level', 'MarkAsDeleted', 'Vented', '_id', 'cLevel']
        for column in columnSet:
            if column in df:
                df.drop(column, axis=1, inplace=True)

        #remove duplicate rows
        df.drop_duplicates(keep='first')
        #insert dataframe into mondodb for processing
        self.collection.remove()
        self.collection.insert_many(df.to_dict('records'))
        #pprint(list(self.collection.find()))

    def cleanJSONData(self, jsonList):
        """
        take inpput as a json List, clean data and store it into database for further parameter calculation
        :return: 
        """
        df = pd.read_json(jsonList)
        columnSet = ['Station_Code', 'isSWMP', 'Historical', 'ProvisionalPlus', 'F_Record', 'F_Temp', 'F_SpCond','F_Sal','F_DO_pct',
                     'F_DO_mgl', 'F_Depth', 'F_cDepth', 'F_pH', 'F_Turb', 'ChlFluor', 'EC_ChlFluor','EC_DO_mgl','EC_DO_pct', 'EC_Depth',
                     'EC_Level', 'EC_Sal', 'EC_SpCond', 'EC_SpCond', 'EC_Temp', 'EC_Turb','EC_cDepth', 'EC_cLevel','EC_pH', 'F_ChlFluor',
                     'F_Level', 'F_cLevel', 'F_cLevel', 'ID', 'Level', 'MarkAsDeleted', 'Vented','_id', 'cLevel']
        for column in columnSet:
            if column in df:
                df.drop(column, axis=1, inplace=True)

        # remove duplicate rows
        df.drop_duplicates(keep='first')
        # insert dataframe into mondodb for processing
        self.collection.remove()
        self.collection.insert_many(df.to_dict('records'))
        #pprint(list(self.collection.find()))

#obj =  DataCleaning()
#obj.cleanCSVData('./data/csv/sample.csv')