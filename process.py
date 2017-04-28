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

class FileInputProcess:
    def __init__(self):
        pass

    def import_content(self, filename):
        try :
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

        except IOError, e:
            print "Error: can\'t find file or read data"
        except Exception, e:
            print "Failed to import file into mongodb "+str(e)
        else:
            print "data inserted succesfully"

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
        result = {'qpDefault': '', 'qpYearly':'', 'qpMonthly':''}
        try:
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
            result['qpDefault'] = qpDefaultObj.calculate_parameters(parameters)
            #{'Overall Data Quality': '91.22', 'Completeness': '98.05', 'Timeliness': '95.00',
            #'Correctness': '80.00', 'Validity': '100.00', 'Uniqueness': '99.73', 'Usability': '74.52'}
            if yearly :
                _years =[]
                for year in range(int(startYear), int(endYear)+1):
                    _years.append(year)
                qpYearlyObj = YearlyQPCalculation()
                result['qpYearly'] = qpYearlyObj.calculate_yearly_parameters(_years, parameters)

            if monthly :
                _yearsForMonthly = []
                for year in range(int(monthStartDate), int(monthEndDate)+1):
                    _years.append(year)
                qpMonthlyObj = MonthlyQPCalculation()
                result['qpMonthly'] = qpMonthlyObj.calculate_monthly_parameters(_yearsForMonthly, parameters)

        except Exception, e:
            print "Failed to calculate quality "+str(e)

        finally:
            return result




class WebAPIInputProcess:
    def __init__(self):
        pass
