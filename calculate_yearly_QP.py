from pymongo import MongoClient


class YearlyQPCalculation:

    def __init__(self):
        self.client = MongoClient()
        # Select appropriate database
        self.db = self.client.qaplatformdb
        # Select appropriate collection
        self.coll = self.db.wqprocess
        # Select the first document
        self.doc = self.coll.find_one()

        # Iterate over keys pulled from first document
        self.count = 0
        self.incomplete = 0
        self.invalid = 0
        for key in self.doc:
            # print key
            self.count += 1  # Keep track of total number of keys/columns
        #print self.count
        self.yearly_parameters = {"Completeness": [], "Uniqueness": [], "Validity": [], "Timeliness": [], "Correctness": [], "Usability": []}

    def get_completeness(self, temp_total_fields):
        total_null = 0
        # Iterate over keys pulled from first document to find all null values
        for key in self.doc:
            total_null = total_null + self.coll.find({'$or': [{key: {'$type': 10}}, {key: ""}]}).count()
            self.incomplete = total_null
        if temp_total_fields:
            completeness = ((temp_total_fields - total_null) * 100.0) / temp_total_fields
        else:
            completeness = 0.0
        return completeness

    def get_uniqueness(self, temp_total_docs):
        cursor = self.coll.aggregate([{"$group": {"_id": "$DateTimeStamp", "count": {"$sum": 1}}}])
        u_count = 0
        u_rows = 0
        for _ in cursor:
            if _[u'count'] > 1:
                # print _
                u_count += _[u'count']
                u_rows += 1

        # print u_count
        # print u_rows
        # print self.total_docs

        unique_rows = temp_total_docs - u_count + u_rows

        # print "Unique rows based on",u_key,"are",unique_rows

        if temp_total_docs:
            uniqueness = unique_rows * 100.0 / temp_total_docs
        else:
            uniqueness = 0.0
        return uniqueness

    def get_validity(self, temp_total_fields):
        invalid = 0
        for key in self.doc:
            if key == 'Temp':
                invalid = invalid + self.coll.find({'$or': [{key: {'$lt': -5}}, {key: {'$gt': 50}}]}).count()
            if key == "SpCond":
                invalid = invalid + self.coll.find({'$or': [{key: {'$lt': 0}}, {key: {'$gt': 40}}]}).count()
            if key == "Sal":
                invalid = invalid + self.coll.find({'$or': [{key: {'$lt': 0}}, {key: {'$gt': 25}}]}).count()
            if key == "DO_pct":
                invalid = invalid + self.coll.find({'$or': [{key: {'$lt': 0}}, {key: {'$gt': 500}}]}).count()
            if key == "DO_mgl":
                invalid = invalid + self.coll.find({'$or': [{key: {'$lt': 0}}, {key: {'$gt': 50}}]}).count()
            if key == "Depth":
                invalid = invalid + self.coll.find({'$or': [{key: {'$lt': 0}}, {key: {'$gt': 33}}]}).count()
            if key == "pH":
                invalid = invalid + self.coll.find({'$or': [{key: {'$lt': 0}}, {key: {'$gt': 10}}]}).count()
            if key == "Turb":
                invalid = invalid + self.coll.find({'$or': [{key: {'$lt': 0}}, {key: {'$gt': 4000}}]}).count()
            if key == "Level":
                invalid = invalid + self.coll.find({'$or': [{key: {'$lt': 0}}, {key: {'$gt': 1}}]}).count()
            if key == "ChlFluor":
                invalid = invalid + self.coll.find({'$or': [{key: {'$lt': 0}}, {key: {'$gt': 11}}]}).count()
        self.invalid = invalid
        if temp_total_fields:
            validity = (temp_total_fields - invalid) * 100.0 / temp_total_fields
        else:
            validity = 0.0
        return validity

    def get_timeliness(self, days):
        print days * 96
        distinct = self.coll.distinct("DateTimeStamp", {"DateTimeStamp": {"$ne": ""}})
        timely = len(distinct)
        print timely
        timeliness = timely * 100.0 / (96.0 * days)
        return timeliness

    def get_correctness(self, temp_total_fields):
        incorrect = self.incomplete + self.invalid
        if temp_total_fields:
            correctness = (temp_total_fields - incorrect) * 100.0 / temp_total_fields
        else:
            correctness = 0.0
        return correctness

    def calculate_yearly_parameters(self, params, years):
        """
        Call this function to get quality parameters on a yearly basis
        :param days: Duration of the data set in days
        :param params: dictionary indicating which quality parameters are to be calculated
        :param years: List of years for which data quality parameters are to be calculated.
        for e.g. years = [2016, 2017]
        :return: Dictionary of dictionaries
        for e.g. {'Completeness': {2016: '98.05', 2017: '0.00'}, 'Timeliness': {2016: '95.00', 2017: '95.00'}, 
        'Correctness': {2016: '80.00', 2017: '80.00'}, 'Validity': {2016: '100.00', 2017: '0.00'}, 
        'Uniqueness': {2016: '99.73', 2017: '0.00'}, 'Usability': {2016: '74.52', 2017: '0.00'}}
        """
        try:
            print("yearly qp calculate function called")
            if params['Usability'] == "true" or params['Usability'] == True:
                params['Completeness'] = 'true'
                params['Correctness'] = 'true'
                params['Timeliness'] = 'true'

            if params['Correctness'] == "true" or params['Correctness'] == True:
                params['Completeness'] = 'true'
                params['Validity'] = 'true'

            #years = _years
            for year in years:
                pattern = "[-/]" + str(year) + " "
                #print pattern
                self.coll.aggregate([{"$match": {"DateTimeStamp": {"$regex": pattern}}}, {"$out": "temp_coll"}])

                self.coll = self.db.temp_coll

                temp_total_docs = self.coll.find().count()
                # print temp_total_fields
                temp_total_fields = temp_total_docs * self.count

                if params['Completeness'] == 'true' or params['Completeness'] == True:
                    completeness = self.get_completeness(temp_total_fields)
                    #self.monthly_parameters["Completeness"][year] = "{0:.2f}".format(completeness)
                    self.yearly_parameters["Completeness"].append(float("{0:.2f}".format(completeness)))
                else:
                    completeness = 0
                    self.yearly_parameters["Completeness"] = []

                if params['Uniqueness'] == 'true' or params['Uniqueness'] == True:
                    uniqueness = self.get_uniqueness(temp_total_docs)
                    #self.monthly_parameters["Uniqueness"][year] = "{0:.2f}".format(uniqueness)
                    self.yearly_parameters["Uniqueness"].append(float("{0:.2f}".format(uniqueness)))
                else:
                    uniqueness = 0
                    self.yearly_parameters["Uniqueness"] = []

                if params['Validity'] == 'true' or params['Validity'] == True:
                    validity = self.get_validity(temp_total_fields)
                    # self.monthly_parameters["Validity"][year] = "{0:.2f}".format(validity)
                    self.yearly_parameters["Validity"].append(float("{0:.2f}".format(validity)))
                else:
                    validity = 0
                    self.yearly_parameters["Validity"] = []

                if params['Timeliness'] == 'true' or params['Timeliness'] == True:
                    if year % 4 == 0:
                        days = 366
                    else:
                        days = 365
                    timeliness = self.get_timeliness(days)
                    # self.monthly_parameters["Timeliness"][year] = "{0:.2f}".format(timeliness)
                    self.yearly_parameters["Timeliness"].append(float("{0:.2f}".format(timeliness)))
                else:
                    timeliness = 0
                    self.yearly_parameters["Timeliness"] = []

                if params['Correctness'] == 'true' or params['Correctness'] == True:
                    correctness = self.get_correctness(temp_total_fields)
                    # self.monthly_parameters["Correctness"][year] = "{0:.2f}".format(correctness)
                    self.yearly_parameters["Correctness"].append(float("{0:.2f}".format(correctness)))
                else:
                    correctness = 0
                    self.yearly_parameters["Correctness"] = []

                if params['Usability'] == 'true' or params['Usability'] == True:
                    usability = completeness * timeliness * correctness/10000.0
                    # self.monthly_parameters["Usability"][year] = "{0:.2f}".format(usability)
                    self.yearly_parameters["Usability"].append(float("{0:.2f}".format(usability)))
                else:
                    usability = 0
                    self.yearly_parameters["Usability"] = []

                self.coll = self.db.wqprocess
            return self.yearly_parameters
        except Exception:
            print("exception in yearly qp")
            return 0

# Instantiating the YearlyQPCalculation class for testing purpose
# param = YearlyQPCalculation()
# _years = [2012, 2013, 2014, 2015, 2016]
# _params = {'Completeness': 'true', 'Correctness': 'true', 'Timeliness': 'true', 'Validity': 'true',
#            'Uniqueness': 'true', 'Usability': 'true'}
#
# p = param.calculate_yearly_parameters(_params, _years)
# print p
