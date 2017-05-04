import DataCleaning
from DataCleaning import DataCleaning
import sys
import pandas as pd
import pymongo
import json
import os
from calculateQP import QPCalculation
from calculate_yearly_QP import YearlyQPCalculation
from calculate_monthly_QP import MonthlyQPCalculation

from datacollect import DataCollectionFromWebService
from model import ValidatedData, RegionData, DataProcess

class FileInputProcess:
    """
    file processing is always performed for single station based model
    """
    def __init__(self):
        pass

    def import_content(self, filename):
        """
        
        :param filename: 
        :return: 
        """
        print("imprting csv file content into db without cleaning")
        mng_client = pymongo.MongoClient('localhost', 27017)
        mng_db = mng_client['qaplatformdb']  # Replace mongo db name
        collection_name = 'wqprocess'  # Replace mongo db collection name
        db_cm = mng_db[collection_name]
        # cdir = os.path.dirname(__file__)
        # file_res = os.path.join(cdir, filepath)

        data = pd.read_csv('./data/csv/' + filename)
        data_json = json.loads(data.to_json(orient='records'))
        db_cm.remove()
        db_cm.insert(data_json)
        print ("data inserted succesfully")

    def process(self, region, station, start_date, end_date, filename,
                isCleaningRequired, parameters, monthly,monthStartDate,monthEndDate, yearly, startYear, endYear):
        """'Parameters': 
                    
        :param region: regionName
        :param station:  stationName
        :param start_date: starting date
        :param end_date: ending date
        :param filename: filename
        :param isCleaningRequired: cleaning required or not
        :param parameters: {  'Completeness': 'true', 'Timeliness': 'true', 'Correctness': 'true','Validity': 'true', 
                            'Uniqueness': 'true','Usability': 'true'}
        :param monthly: 
        :param yearly: 
        :return: {'Overall Data Quality': '91.22', 'Completeness': '98.05', 'Timeliness': '95.00', 
        'Correctness': '80.00', 'Validity': '100.00', 'Uniqueness': '99.73', 'Usability': '74.52'}
        """
        print("This is stationbased qp calculation for csv file")
        results =[]

        # result = {'Region':region,'Station':station, 'FromDate':start_date, 'EndDate': end_date,
        #           'IsCleaned':isCleaningRequired,'DefaultQualityParameters': '', 'YearlyQualityParameters':'',
        #           'MonthlyQualityParameters':''}
        result = {'Region': region, 'Station': station, 'FromDate': start_date, 'EndDate': end_date, 'IsCleaned':isCleaningRequired}

        if isCleaningRequired:
            # perform clenaing
            print("performing cleaning")
            dataCleaner = DataCleaning()
            dataCleaner.cleanCSVData(filename)

        else :
            #read file and insert data into processing collection
            print("importing file without cleaning")
            self.import_content(filename)

        #now data is in processing collection (cleaned or uncleaned) db = qaplatformdb and collection = wqprocess contains the cleaned data
        #defaultQAParameters = {}
        qpDefaultObj = QPCalculation()
        print ("calculating default qp parameters")
        result["DefaultQPFlag"] = True
        result['DefaultQualityParameters'] = qpDefaultObj.calculate_parameters(parameters,366)
        #{'Overall Data Quality': '91.22', 'Completeness': '98.05', 'Timeliness': '95.00',
        #'Correctness': '80.00', 'Validity': '100.00', 'Uniqueness': '99.73', 'Usability': '74.52'}

        result["YearlyQPFlag"] = False
        if yearly :
            print ("calculating yearly qp parameters")
            _years =[]
            for year in range(int(startYear), int(endYear)+1):
                _years.append(year)
            qpYearlyObj = YearlyQPCalculation()
            result["YearlyQPFlag"] = True
            result['YearlyQualityParameters'] = qpYearlyObj.calculate_yearly_parameters(_years, parameters,366)
            result["YearlyLabel"] = _years

        result["MonthlyQPFlag"] = False
        if monthly :
            print ("calculating monthly qp parameters")
            _yearsForMonthly = []
            for year in range(int(monthStartDate), int(monthEndDate)+1):
                _yearsForMonthly.append(year)
            qpMonthlyObj = MonthlyQPCalculation()
            result["MonthlyQPFlag"] = True
            result['MonthlyQualityParameters'] = qpMonthlyObj.calculate_monthly_parameters(parameters,_yearsForMonthly,366)
            # generating label for months
            monthlabel = []

            month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            for y in _yearsForMonthly:
                for m in month:
                    monthlabel.append(m + str(y))
            result['MonthlyLabel'] = monthlabel

        #get data from the processing collection to insert into validated data set
        processObj = DataProcess()
        data = processObj.getDataFromProcess()
        #insert the result into validated dataset
        dbObj = ValidatedData()
        dbObj.insertResult(result, data)

        results.append(result)
        print ({'ModelBasedSubType': 'StationBased', 'Result': results})
        return {'ModelBasedSubType': 'StationBased', 'Result': results}


class WebAPIInputProcess:
    def __init__(self):
        pass

    def processStationBased(self, region, station, start_date, end_date,
                            isCleaningRequired, parameters, monthly, monthStartDate, monthEndDate, yearly, startYear, endYear):
        """
        
        :param region: 
        :param station: 
        :param start_date: 
        :param end_date: 
        :param isCleaningRequired: 
        :param parameters: 
        :param monthly: 
        :param monthStartDate: 
        :param monthEndDate: 
        :param yearly: 
        :param startYear: 
        :param endYear: 
        :return: 
        """
        print("This is stationbased qp calculation for web file")
        results =[]
        # result = {'Region': region, 'Station': station, 'FromDate': start_date, 'EndDate': end_date,
        #           'IsCleaned': isCleaningRequired, 'DefaultQualityParameters': '', 'YearlyQualityParameters': '',
        #           'MonthlyQualityParameters': ''}

        result = {'Region': region, 'Station': station, 'FromDate': start_date, 'EndDate': end_date,'IsCleaned': isCleaningRequired}

        #call web api to get data
        apiDataObj = DataCollectionFromWebService()
        jsonList = apiDataObj.getDatafromWebService(region, station, start_date, end_date)

        dataCleaner = DataCleaning()

        if isCleaningRequired:                                   #if cleaning required, clean data
            dataCleaner.cleanJSONData(jsonList)
        else:                                                   # else perform default cleaning
            dataCleaner.defaultCleanJSONData(jsonList)

        qpDefaultObj = QPCalculation()
        print ("calculating default qp parameters")
        result["DefaultQPFlag"] = True
        result['DefaultQualityParameters'] = qpDefaultObj.calculate_parameters(parameters,366)
        # {'Overall Data Quality': '91.22', 'Completeness': '98.05', 'Timeliness': '95.00',
        # 'Correctness': '80.00', 'Validity': '100.00', 'Uniqueness': '99.73', 'Usability': '74.52'}
        print("Successfully calculated default parameters")
        print (result['DefaultQualityParameters'])

        result["YearlyQPFlag"] = False
        if yearly:
            _years = []
            print ("calculating yearly qp parameters")
            for year in range(int(startYear), int(endYear) + 1):
                _years.append(year)
            qpYearlyObj = YearlyQPCalculation()
            result["YearlyQPFlag"] = True
            result['YearlyQualityParameters'] = qpYearlyObj.calculate_yearly_parameters(_years, parameters,366)
            result["YearlyLabel"] = _years
            print("Successfully calculated yearly parameters")
            #print(result['YearlyQualityParameters'])

        result["MonthlyQPFlag"] = True
        if monthly:
            print ("calculating monthly qp parameters")
            _yearsForMonthly = []

            #print ("monthStartDate: ",monthStartDate)
            #print ("monthEndDate: ",monthEndDate)
            for year in range(int(monthStartDate), int(monthEndDate) + 1):
                _yearsForMonthly.append(year)
            qpMonthlyObj = MonthlyQPCalculation()
            result["MonthlyQPFlag"] = True
            result['MonthlyQualityParameters'] = qpMonthlyObj.calculate_monthly_parameters(parameters,_yearsForMonthly,366)

            #generating label for months
            monthlabel = []

            month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            for y in _yearsForMonthly:
                for m in month:
                    monthlabel.append(m + str(y))
            result['MonthlyLabel'] = monthlabel
            print("Successfully calculated monthly parameters")
            #print(result['MonthlyQualityParameters'] )

        #print result
        #print("calling insert validated data into db")
        # get data from the processing collection to insert into validated data set
        processObj = DataProcess()

        data = processObj.getDataFromProcess()
        # insert the result into validated dataset
        dbObj = ValidatedData()

        dbObj.insertResult(result, data)

        results.append(result)

        #print({'ModelBasedSubType': 'StationBased', 'Result': results})
        return {'ModelBasedSubType': 'StationBased', 'Result': results}


    def processRegionBAsed(self, region, start_date, end_date,
                                isCleaningRequired, parameters, monthly,monthStartDate,monthEndDate, yearly, startYear, endYear):
        results =[]
        print("This is regionbased qp calculation for web service  data")
        obj = RegionData()
        # print obj.getAllRegionInfo()
        data = obj.getSingleRegionInfo(region)
        stationsInfo = data['data']['Stations']
        stations = []
        for stationdata in stationsInfo:
            station = stationdata['StationName']
            print("/n calculating parameters for station",station)
            result = self.processStationBased(region, station, start_date, end_date,
                            isCleaningRequired, parameters, monthly, monthStartDate, monthEndDate, yearly, startYear, endYear)
            print result["Result"][0]
            results.append(result["Result"][0])

        print("/n result for all stations in the given region is: ",{'ModelBasedSubType': 'RegionBased', 'Result': results})

        return {'ModelBasedSubType': 'RegionBased', 'Result': results}

