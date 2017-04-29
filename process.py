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
        results =[]

        # result = {'Region':region,'Station':station, 'FromDate':start_date, 'EndDate': end_date,
        #           'IsCleaned':isCleaningRequired,'DefaultQualityParameters': '', 'YearlyQualityParameters':'',
        #           'MonthlyQualityParameters':''}
        result = {'Region': region, 'Station': station, 'FromDate': start_date, 'EndDate': end_date, 'IsCleaned':isCleaningRequired}

        if isCleaningRequired:
            # perform clenaing
            dataCleaner = DataCleaning()
            dataCleaner.cleanCSVData(filename)

        else :
            #read file and insert data into processing collection
            self.import_content(filename)

        #now data is in processing collection (cleaned or uncleaned) db = qaplatformdb and collection = wqprocess contains the cleaned data
        #defaultQAParameters = {}
        qpDefaultObj = QPCalculation()
        result['DefaultQualityParameters'] = qpDefaultObj.calculate_parameters(parameters)
        #{'Overall Data Quality': '91.22', 'Completeness': '98.05', 'Timeliness': '95.00',
        #'Correctness': '80.00', 'Validity': '100.00', 'Uniqueness': '99.73', 'Usability': '74.52'}
        if yearly :
            _years =[]
            for year in range(int(startYear), int(endYear)+1):
                _years.append(year)
            qpYearlyObj = YearlyQPCalculation()
            result['YearlyQualityParameters'] = qpYearlyObj.calculate_yearly_parameters(_years, parameters)

        if monthly :
            _yearsForMonthly = []
            for year in range(int(monthStartDate), int(monthEndDate)+1):
                _years.append(year)
            qpMonthlyObj = MonthlyQPCalculation()
            result['MonthlyQualityParameters'] = qpMonthlyObj.calculate_monthly_parameters(_yearsForMonthly, parameters)

        #get data from the processing collection to insert into validated data set
        processObj = DataProcess()
        data = processObj.getDataFromProcess()
        #insert the result into validated dataset
        dbObj = ValidatedData()
        dbObj.insertResult(result, data)

        results.append(result)
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

        result['DefaultQualityParameters'] = qpDefaultObj.calculate_parameters(parameters)
        # {'Overall Data Quality': '91.22', 'Completeness': '98.05', 'Timeliness': '95.00',
        # 'Correctness': '80.00', 'Validity': '100.00', 'Uniqueness': '99.73', 'Usability': '74.52'}
        if yearly:
            _years = []
            for year in range(int(startYear), int(endYear) + 1):
                _years.append(year)
            qpYearlyObj = YearlyQPCalculation()
            result['YearlyQualityParameters'] = qpYearlyObj.calculate_yearly_parameters(_years, parameters)

        if monthly:
            _yearsForMonthly = []
            for year in range(int(monthStartDate), int(monthEndDate) + 1):
                _years.append(year)
            qpMonthlyObj = MonthlyQPCalculation()
            result['MonthlyQualityParameters'] = qpMonthlyObj.calculate_monthly_parameters(_yearsForMonthly, parameters)

        # get data from the processing collection to insert into validated data set
        processObj = DataProcess()
        data = processObj.getDataFromProcess()
        # insert the result into validated dataset
        dbObj = ValidatedData()
        dbObj.insertResult(result, data)
        results.append(result)
        return {'ModelBasedSubType': 'StationBased', 'Result': results}


    def processRegionBAsed(self, region, start_date, end_date,
                                isCleaningRequired, parameters, monthly,monthStartDate,monthEndDate, yearly, startYear, endYear):
        results =[]

        obj = RegionData()
        # print obj.getAllRegionInfo()
        data = obj.getSingleRegionInfo(region)
        stationsInfo = data['data']['Stations']
        stations = []
        for stationdata in stationsInfo:
            station = stationdata['StationName']
            result = self.processStationBased(region, station, start_date, end_date,
                            isCleaningRequired, parameters, monthly, monthStartDate, monthEndDate, yearly, startYear, endYear)
            results.append(result[0])

        return {'ModelBasedSubType': 'RegionBased', 'Result': results}

