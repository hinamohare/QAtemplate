from pymongo import MongoClient
from bson.json_util import dumps
import json
class RegionData:
    """
    The stationdata collection stores the regions and the stations information in each region
    The data is represented as:
    {RegionName:"San Francisco Bay, CA",RegionId:1,Stations:[{StationName:"China Camp",StationCode:"sfbccwq",Lat:38.0012,Lon:122.4604}]}
    """

    def __init__(self):
        pass

    def getAllRegionInfo(self):
        """
        This function fetches all the records from the collection "stationdata"
        :return: all the region records
        """
        regions = []
        client = MongoClient()  # setting connection with the mongoclient
        db = client.qaplatformdb  # getting database
        collection = db.stationdata #getting stationdata collection
        data = collection.find()
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

    def getSingleRegionInfo(self, region):
        """
        This function reads the record for one region from the collection "stationdata"
        :return:
        """

        client = MongoClient()  # setting connection with the mongoclient
        db = client.qaplatformdb  # getting database
        collection = db.stationdata #getting stationdata collection
        data = collection.find_one({"RegionName":region})
        if data.count()!= 0:
            return {'data':data}
        else:
            print ("no record for the given region found in the database")
            return None

    def getSingleStationInfo(self,region, station_name):
        """
        This function fetches single records from the collection "stationdata" whose name matches to the input station
        :return: single record for the station in the region
        """
        client = MongoClient()  # setting connection with the mongoclient
        db = client.qaplatformdb  # getting database
        collection = db.stationdata #getting stationdata collection
        result = collection.find_one({"RegionName": region})
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
        client = MongoClient()  # setting connection with the mongoclient
        db = client.qaplatformdb  # getting database
        collection = db.stationdata  # getting stationdata collection
        result = collection.find_one({"RegionName": region})
        if result.count() != 0:
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

        client = MongoClient()  # setting connection with the mongoclient
        db = client.qaplatformdb  # getting database
        collection = db.stationdata #getting stationdata collection
        # inserting document to mongodb
        result = collection.insert_one(post_data)
        print ("The station information inserted successfully into the stationdata collection")
        print('One post: {0}'.format(result.inserted_id))


# --------------------------------- Querying the validated data sets ------------------------------------------------
class ValidatedData:
    """
    The validateddata collection consists of validated data for each station
    """
    def __init__(self):
        pass

    def insertValidatedStationData(self, region, station, start_date, end_date,isCleaned,overallQuality, diamension, data, parameters):
        """
        This function inserts the validated dataset into the database
        {'Region':"Padilla Bay, WA", 'Station':"Bayview Channel", 'From':"2017-01-01",
					'To':"2017-01-01",'IsCleaned': "true", "Diamension": 'Region/Station',OverallQuality':80,'Parameters':{'Completeness':75 , 'Accuracy':75,'Timeliness':75,'Uniqueness':75,'Validity':75,'Consistency':75,
         Reliability:75, Usability:75}}
        :param region:
        :param station:
        :param start_date:
        :param end_date:
        :return:
        """
        client = MongoClient()  # setting connection with the mongoclient

        db = client.test # test database

        #db = client.qaplatformdb  # getting database
        collection = db.validateddata #getting validateddata collections

        post_data = {'Region': region, 'Station': station, 'From': start_date,'To': end_date,'IsCleaned': isCleaned,"Diamension":diamension,
                     'OverallQuality': overallQuality, 'Parameters': parameters, 'Data': data}
        result = collection.insert_one(post_data)

        print ('inserted validated data into the database')

    def searchAllValidatedDataForRegion(self,region):
        """
                This function searches for all the records for the given region in the validated database
                :param region:
                :param station:
                :return: returns the region record without data field
                """
        records = []  # list to store all the records of the stations in a region
        client = MongoClient()  # setting connection with the mongoclient
        #db = client.qaplatformdb  # getting database

        db = client.test  # test data collection

        collection = db.validateddata  # getting validateddata collections
        result = collection.find({"Region": region}, {"Data": 0})
        #print "result: "+ dumps(result)
        print (result.count())
        if result.count() is not 0:
            print ("validated data for the region is found in the database")
            for record in result:
                records.append(record)
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
        client = MongoClient()  # setting connection with the mongoclient

        db = client.test  # test data collection

        #db = client.qaplatformdb  # getting database
        collection = db.validateddata  # getting validateddata collections
        result = collection.find({"Region": region, "Station": station},{"data":0})

        if result.count()!= 0:
            print ("validated data for the station is found in the database")
            for record in result:
                records.append(record)
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
        client = MongoClient()  # setting connection with the mongoclient

        db = client.test  # test data collection

        #db = client.qaplatformdb  # getting database
        collection = db.validateddata #getting validateddata collection
        result = collection.find({'$and': [{"Region": region}, {"Station":station}, {"From":start_date}, {"To": end_date}]},{"Data":0})
        if result.count() != 0:
            print ("The record of the station for the given dates is present in the validated database")
            records.append(result)
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