import os
from pprint import pprint
#from pymongo import MongoClient
import json
#from model import RegionData
import SOAPpy
import pandas as pd
import pymongo
"""
data = {'region':"Padilla Bay, WA", 'stations':[
                    {'station':"Bayview Channel", 'code': "pdbbywq", 'lat':"48.496139",'lng':"122.502114"},
                    {'station':"Ploeg Channel", 'code': "pdbbpwq", 'lat':"48.556322",'lng':"122.530894"},
                    {'station':"Joe Leary Estuary", 'code': "pdbjewq", 'lat':"48.518264",'lng':"122.474189"},
                    ]}

obj = RegionData()
"""

"""
WEB API

server = SOAPpy.SOAPProxy("http://cdmo.baruch.sc.edu/webservices2/requests.cfc?wsdl")
responsedata =  server.exportAllParamsDateRangeXMLNew('acegpwq', '2014-12-30', '2014-12-31','*')

pythonObject = SOAPpy.Types.simplify(responsedata)
#print responsedata
dataArray =  pythonObject["returnData"]["data"]
print(dataArray)

"""
"""
client = pymongo.MongoClient()
#db and collection for testing purpose
db = client.currentTest
#self.db = self.client.qaplatformdb
collection = db.wqprocess
#df = pd.read_json(dataArray)
df = pd.DataFrame.from_records(dataArray)
columnSet = ['Station_Code', 'isSWMP', 'Historical', 'ProvisionalPlus', 'F_Record', 'F_Temp', 'F_SpCond', 'F_Sal',
         'F_DO_pct', 'F_DO_mgl', 'F_Depth', 'F_cDepth', 'F_pH', 'F_Turb','ChlFluor', 'EC_ChlFluor', 'EC_DO_mgl',
         'EC_DO_pct', 'EC_Depth', 'EC_Level', 'EC_Sal', 'EC_SpCond', 'EC_SpCond', 'EC_Temp', 'EC_Turb', 'EC_cDepth', 'EC_cLevel',
         'EC_pH', 'F_ChlFluor', 'F_Level', 'F_cLevel', 'F_cLevel', 'ID', 'Level', 'MarkAsDeleted', 'Vented', '_id', 'cLevel']
for column in columnSet:
    if column in df:
        df.drop(column, axis=1, inplace=True)
# remove duplicate rows
df.drop_duplicates(keep='first')
# insert dataframe into mondodb for processing

collection.remove()
collection.insert_many(df.to_dict('records'))
pprint(list(collection.find()))
 code to import data from file to mongodb0
with open('ElkhornSlough,CA_SouthMarch_20141230_20141231.json') as data_file:
    data = json.load(data_file)
client = MongoClient()  # setting connection with the mongoclient
db = client.test  # getting database
collection = db.test #getting validateddata collection
db.test.insert(data)
print db.test.find().pretty()
"""
"""
import sys
import pandas as pd
import pymongo
import json

def import_content(filename):
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['test'] # Replace mongo db name
    collection_name = 'processing' # Replace mongo db collection name
    db_cm = mng_db[collection_name]
    #cdir = os.path.dirname(__file__)
    #file_res = os.path.join(cdir, filepath)

    data = pd.read_csv('./data/csv/'+filename)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json)
    print "data inserted succesfully"

import_content('sample.csv')
"""

startYear = '2011'
endYear = '2017'
_years = []
for year in range(int(startYear),int(endYear)+1):
    _years.append(year)

print _years
