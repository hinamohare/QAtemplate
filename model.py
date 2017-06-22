from pymongo import MongoClient
from bson.json_util import dumps
import json

client = MongoClient()
def getMongoDB():
    return client


class DataProcess:
    def __init__(self):
        self.client = getMongoDB()
        # Select appropriate database
        self.db = self.client.qaplatformdb
        # Select appropriate collection
        self.coll = self.db.wqprocess

    def getDataFromProcess(self):
        print("getting processing data from collection")
        data = list(self.coll.find({"_id":0}))
        if data is not None:
            return data
        else:
            print "unable to extract processing data from db"


class RegionData:
    """
    The stationdata collection stores the regions and the stations information in each region
    The data is represented as:
    {RegionName:"San Francisco Bay, CA",RegionId:1,Stations:[{StationName:"China Camp",StationCode:"sfbccwq",Lat:38.0012,Lon:122.4604}]}
    """

    def __init__(self):
        self.client = getMongoDB()  # setting connection with the mongoclient
        self.db = self.client.qaplatformdb  # getting database
        self.collection = self.db.stationdata


    def getAllRegionInfo(self):
        """
        This function fetches all the records from the collection "stationdata"
        :return: all the region records
        """
        regions = []
        # client = MongoClient()  # setting connection with the mongoclient
        # db = client.qaplatformdb  # getting database
        # collection = db.stationdata #getting stationdata collection
        data = self.collection.find()
        if data.count() != 0:
            for item in data:
                #field ={}

                #field["RegionName"] = item["stationname"]

                regions.append(item)
                #print item
            return regions
        else:
            print ("no records found in the database")
            return None

    def getAllStationInfo(self):
        stations = []
        # client = MongoClient()  # setting connection with the mongoclient
        # db = client.qaplatformdb  # getting database
        # collection = db.stationdata  # getting stationdata collection
        data = self.collection.find()
        if data.count() != 0:
            for item in data:
                for station in item["Stations"]:
                    stations.append(station)
                # print item
            return stations
        else:
            print ("no records found in the database")
            return None


    def getSingleRegionInfo(self, region):
        """
        This function reads the record for one region from the collection "stationdata"
        :return:
        """

        # client = MongoClient()  # setting connection with the mongoclient
        # db = client.qaplatformdb  # getting database
        # collection = db.stationdata #getting stationdata collection
        data = self.collection.find_one({"RegionName":region})
        if data!= {}:
            return {'data':data}
        else:
            print ("no record for the given region found in the database")
            return None

    def getSingleStationInfo(self,region, station_name):
        """
        This function fetches single records from the collection "stationdata" whose name matches to the input station
        :return: single record for the station in the region
        """
        # client = MongoClient()  # setting connection with the mongoclient
        # db = client.qaplatformdb  # getting database
        # collection = db.stationdata #getting stationdata collection
        result = self.collection.find_one({"RegionName": region})
        if result.count() != 0:
            stations = result['Stations']
            for station in stations:
                if station["StationName"] == station_name:
                    return station
        else:
            print ("no record for the given station found in the database")
            return None

    def getStaionCode(self, region, station):
        """
        :param region:
        :param station:
        :return: code of the input station
        """
        # client = MongoClient()  # setting connection with the mongoclient
        # db = client.qaplatformdb  # getting database
        # collection = db.stationdata  # getting stationdata collection
        result = self.collection.find_one({"RegionName": region})
        if result != {}:
            stations = result["Stations"]
            for s in stations:
                if s["StationName"]== station:
                    print ("The station found in the given region")
                    code = s["StationCode"]
                    return code
        else :
            print ("This station doesnt exist in the given region")
            return None


    def insertRegionInfoIntoDB(self, post_data):
        """
        database name: "qaplatformdb"
        collection name: "stationdata"
        This method is used to insert stations information into the collection
        The input format is
        post_data =[
                    {RegionId: regionId,
                    RegionName: regionname,
                    Stations: [{StationName: staitonname, 
                                StationCode: stationcode,
                                 Lat: lattitude, 
                                 Lon: longitude}
                                 ,.....]
                    }...]
        :return: 
        """

        # client = MongoClient()  # setting connection with the mongoclient
        # db = client.qaplatformdb  # getting database
        # collection = db.stationdata #getting stationdata collection
        # inserting document to mongodb
        result = self.collection.insert(post_data)
        print ("The station information inserted successfully into the stationdata collection")
        #print('One post: {0}'.format(result.inserted_id))


# --------------------------------- Querying the validated data sets ------------------------------------------------
class ValidatedData:
    """
    The validateddata collection consists of validated data for each station
    """
    def __init__(self):
        self.client = getMongoDB()  # setting connection with the mongoclient

        # db = client.test # test database

        self.db = self.client.qaplatformdb  # getting database
        self.collection = self.db.validateddata


    def insertResult(self, result, data):
        """       
        :param result: result = {'Region':region,'Station':station, 'FromDate':start_date, 'EndDate': end_date,\
                  'IsCleaned':isCleaningRequired,'DefaultQualityParameters': '', 'YearlyQualityParameters':'', 
                  'MonthlyQualityParameters':''}
        :return: 
        """
        # region = result['Region']
        # station = result['Station']
        # start_date = result['FromDate']
        # end_date = result['EndDate']
        # isCleaned = result['IsCleaned']
        # defaultQualityParameters = result['DefaultQualityParameters']
        # yearlyQualityParameters = result['YearlyQualityParameters']
        # monthlyQualityParameters = result['MonthlyQualityParameters']
        # self.insertValidatedStationData(region, station, start_date, end_date, isCleaned,
        #         defaultQualityParameters, yearlyQualityParameters, monthlyQualityParameters, data)
        print("insert validated data into db function called")

        newresult = dict(result.items())
        newresult["Data"] = data
        # client = MongoClient()  # setting connection with the mongoclient
        #
        # #db = client.test  # test database
        #
        # db = client.qaplatformdb  # getting database
        # collection = db.validateddata  # getting validateddata collections

        self.collection.insert_one(newresult)

        print ('inserted validated data into the database')



    def insertValidatedStationData(self, region, station, start_date, end_date, isCleaned,
                defaultQualityParameters, yearlyQualityParameters, monthlyQualityParameters, data):
        """
        result = {'Region':region,'Station':station, 'FromDate':start_date, 'EndDate': end_date,\
                  'IsCleaned':isCleaningRequired,'DefaultQualityParameters': '', 'YearlyQualityParameters':'', 
                  'MonthlyQualityParameters':'', "Data":data}
        :param region: 
        :param station: 
        :param start_date: 
        :param end_date: 
        :param isCleaned: 
        :param defaultQualityParameters: 
        :param yearlyQualityParameters: 
        :param monthlyQualityParameters: 
        :param data: 
        :return: 
        """
        # client = MongoClient()  # setting connection with the mongoclient
        #
        # #db = client.test # test database
        #
        # db = client.qaplatformdb  # getting database
        # collection = db.validateddata #getting validateddata collections


        post_data = {'Region': region, 'Station': station, 'FromDate': start_date,'EndDate': end_date,'IsCleaned': isCleaned,
                     "DefaultQualityParameters": defaultQualityParameters,
                     'YearlyQualityParameters': yearlyQualityParameters,
                     'MonthlyQualityParameters': monthlyQualityParameters,
                     'Data': data}
        result = self.collection.insert_one(post_data)

        print ('inserted validated data into the database')

    def searchAllValidatedDataForRegion(self,region):
        """
                This function searches for all the records for the given region in the validated database
                :param region:
                :param station:
                :return: returns the region record without data field
                """
        records = []  # list to store all the records of the stations in a region
        # client = MongoClient()  # setting connection with the mongoclient
        # db = client.qaplatformdb  # getting database
        #
        # #db = client.test  # test data collection
        #
        # collection = db.validateddata  # getting validateddata collections
        result = self.collection.find({"Region": region}, {"Data": 0})
        #print "result: "+ dumps(result)
        print (result.count())
        if result.count() is not 0:
            print ("validated data for the region is found in the database")
            for record in result:
                records.append(record)

            #print records
            return records
        else:
            print ("raw data for the region is not found in the database")
            return None


    def searchAllValidatedDataForStation(self, region, station):
        """
        This function reads all station data for all the dates from validateddata collection
        :param region:
        :param station:
        :return: returns the station record without data field
        """
        records =[] # list to store all the records of the stations in a region
        # client = MongoClient()  # setting connection with the mongoclient
        #
        # #db = client.test  # test data collection
        #
        # db = client.qaplatformdb  # getting database
        # collection = db.validateddata  # getting validateddata collections
        result = self.collection.find({"Region": region, "Station": station},{"Data":0})

        if result.count()!= 0:
            print ("validated data for the station is found in the database")
            for record in result:
                records.append(record)
            #print records
            return records
        else:
            print ("raw data for the station is not found in the database")
            return None

    def searchValidatedDataForStation(self, region, station, start_date, end_date):
        """
        This function searches the record of the station between start and end date into collection of validated dataset
        validatedcollection stores data in following format
        { region: 'regionname' , station: 'stationname', from: 'startdate', to: 'enddate', type: "water quality",
        'TotalWaterQuality':totalquality, data: "data",
        qualityparameters: {completeness: '', accuracy:'',timeliness:'',uniqueness:'',validity:'',consistency:'', reliability:'', usability:''}
        }
        :param region:
        :param station:
        :param start_date:
        :param end_date:
        :return: returns record without data field if found, else return empty body
        """
        records = []
        # client = MongoClient()  # setting connection with the mongoclient
        #
        # #db = client.test  # test data collection
        #
        # db = client.qaplatformdb  # getting database
        # collection = db.validateddata #getting validateddata collection
        result = self.collection.find({'$and': [{"Region": region}, {"Station":station}, {"FromDate":start_date}, {"EndDate": end_date}]},{"Data":0})
        if result.count() != 0:
            print ("The record of the station for the given dates is present in the validated database")
            for record in result:
                records.append(record)
            #print records
            return records
        else:
            print ("The record of the station is not present in the validated database")
            return None


# --------------------------------- Querying the raw data sets ------------------------------------------------

class RawData:
    """
    The rawdata collection stores the raw data obtained from the webservices
    """
    def __init__(self):
        pass

    def insertRawStationData(self, region, station, start_date, end_date, data):
        """
        This function inserts the validated dataset into the database
        { Region: 'regionname' , Station: 'stationname', From: 'startdate', To: 'enddate', Data: "data",
         }
        :param region:
        :param station:
        :param start_date:
        :param end_date:
        :return:
        """
        client = MongoClient()  # setting connection with the mongoclient
        db = client.qaplatformdb  # getting database
        collection = db.rawdata # getting rawdata collection

        post_data = {'RegionName': region, 'StationName': station, 'From': start_date, 'To': end_date,'Data': data}
        result = collection.insert_one(post_data)
        print ("inserted record id: " + result.inserted_id)
        print ('inserted validated data into the database')

    def getRawData(self,region, station, start_date, end_date):
        """
        This function reads station data from raw database
        :param region:
        :param station:
        :param start_date:
        :param end_date:
        :return: returns the station record
        """
        client = MongoClient()  # setting connection with the mongoclient
        db = client.qaplatformdb  # getting database
        collection = db.rawdata  # getting rawdata collection
        result = collection.find({'$and': [{"Region": region}, {"Station": station}, {"From": start_date}, {"To": end_date}]})
        if result.count() !=0:
            print ("raw data for the station is found in the database")
            return result
        else:
            print( "raw data for the station is not found in the database")
            return None


"""self, region, station, start_date, end_date,isCleaned,overallQuality, diamension, data, parameters
obj = ValidatedData()

obj.insertValidatedStationData("Padilla Bay, WA","Bayview Channel",'2014-12-30', '2014-12-31',
                                 True, 95,"Station Based",'data',
            {'Completeness':75 , 'Accuracy':75,'Timeliness':75,'Uniqueness':75,'Validity':75,'Consistency':75,'Reliability':75, 'Usability':75})
obj.insertValidatedStationData("Padilla Bay, WA","Ploeg Channel",'2014-12-30', '2014-12-31',
                                 True, 95,"Station Based",'data',
            {'Completeness':75 , 'Accuracy':75,'Timeliness':75,'Uniqueness':75,'Validity':75,'Consistency':75,'Reliability':75, 'Usability':75})

obj.insertValidatedStationData("Padilla Bay, WA","Joe Leary Estary",'2014-12-30', '2014-12-31',
                                 True, 95,"Station Based",'data',
            {'Completeness':75 , 'Accuracy':75,'Timeliness':75,'Uniqueness':75,'Validity':75,'Consistency':75,'Reliability':75, 'Usability':75})

"""

result = {	'Region': u'Padilla Bay, WA',
	'Station': u'China Camp',
	'IsCleaned': True,
	'DefaultQPFlag': True,
	'EndDate': u'12/31/2015',
	'FromDate': u'1/1/2014',
	'DefaultQualityParameters':	{	'Overall Data Quality': '57.30',
									'Completeness': '69.79',
									'Timeliness': '2.85',
									'Correctness': '69.79',
									'Validity': '100.00',
									'Uniqueness': '100.00',
									'Usability': '1.39'
								},


	'YearlyQPFlag': True,
	'YearlyLabel' : [2014,2015],
	'YearlyQualityParameters': {'Completeness': [80,90], 'Timeliness': [50,95], 'Correctness': [65,82], 'Validity': [84,96], 'Uniqueness': [80,65], 'Usability':[96,76]},
	'MonthlyQPFlag': True,
	'MonthlyLabel' : ['Jan 2016', 'Feb 2017', 'Mar 2016', 'Apr 2017', 'May 2017', 'June 2016', 'July 2016', 'August 2016', 'September 2016','October 2016', 'November 2016', 'December 2016'],
	'MonthlyQualityParameters': {'Completeness': [30,40,50,60,70,90,50,80,60,70,80,90],
									'Timeliness': [40,64,85,89,74,90,50,80,60,70,80,90],
									'Correctness': [50,40,50,64,85,89,74,80,60,70,80,90],
									'Validity': [38,46,50,60,70,80,50,80,60,70,80,90],
									'Uniqueness': [40,70,50,60,70,64,85,89,74,71,81,90],
									'Usability': [86,64,85,89,74,90,50,80,60,70,80,90],
								}

}
