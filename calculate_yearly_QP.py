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
        for key in self.doc:
            # print key
            self.count += 1  # Keep track of total number of keys/columns
        #print self.count
        self.monthly_parameters = {"Completeness": {}, "Uniqueness": {}, "Validity": {}, "Timeliness": {}, "Correctness": {}, "Usability": {}}

    def get_completeness(self, temp_total_fields):
        total_null = 0
        # Iterate over keys pulled from first document to find all null values
        for key in self.doc:
            total_null = total_null + self.coll.count({key: ""})
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
            if key == "Temp":
                invalid = invalid + self.coll.find({key: {'$ne': "", '$lt': -5, '$gt': 50}}).count()
            if key == "SpCond":
                invalid = invalid + self.coll.find({key: {'$ne': "", '$lt': 0, '$gt': 200}}).count()
            if key == "Sal":
                invalid = invalid + self.coll.find({key: {'$ne': "", '$lt': 0, '$gt': 70}}).count()
            if key == "DO_pct":
                invalid = invalid + self.coll.find({key: {'$ne': "", '$lt': 0, '$gt': 500}}).count()
            if key == "DO_mgl":
                invalid = invalid + self.coll.find({key: {'$ne': "", '$lt': 0, '$gt': 50}}).count()
            if key == "Depth":
                invalid = invalid + self.coll.find({key: {'$ne': "", '$lt': 0, '$gt': 33}}).count()
            if key == "pH":
                invalid = invalid + self.coll.find({key: {'$ne': "", '$lt': 0, '$gt': 14}}).count()
            if key == "Turb":
                invalid = invalid + self.coll.find({key: {'$ne': "", '$lt': 0, '$gt': 4000}}).count()

            if temp_total_fields:
                validity = (temp_total_fields - invalid) * 100.0 / temp_total_fields
            else:
                validity = 0.0
            return validity

    def get_timeliness(self):
        timeliness = 95.0
        return timeliness

    def get_correctness(self):
        correctness = 80.0
        return correctness

    def calculate_yearly_parameters(self, _years, params):
        """
        Call this function to get quality parameters on a yearly basis
        :param _years: List of years for which data quality parameters are to be calculated.
        for e.g. years = [2016, 2017]
        :return: Dictionary of dictionaries
        for e.g. {'Completeness': {2016: '98.05', 2017: '0.00'}, 'Timeliness': {2016: '95.00', 2017: '95.00'}, 
        'Correctness': {2016: '80.00', 2017: '80.00'}, 'Validity': {2016: '100.00', 2017: '0.00'}, 
        'Uniqueness': {2016: '99.73', 2017: '0.00'}, 'Usability': {2016: '74.52', 2017: '0.00'}}
        """
        if params['Usability'] == "true":
            params['Completeness'] = 'true'
            params['Correctness'] = 'true'
            params['Timeliness'] = 'true'
        years = _years
        for year in years:
            pattern = "/" + str(year) + " "
            #print pattern
            self.coll.aggregate([{"$match": {"DateTimeStamp": {"$regex": pattern}}}, {"$out": "temp_coll"}])

            self.coll = self.db.temp_coll
            # print temp_total_docs
            temp_total_docs = self.coll.find().count()
            # print temp_total_fields
            temp_total_fields = temp_total_docs * self.count

            if params['Completeness'] == 'true':
                completeness = self.get_completeness(temp_total_fields)
                self.monthly_parameters["Completeness"][year] = "{0:.2f}".format(completeness)
            else :
                self.monthly_parameters["Completeness"] = {}

            if params['Uniqueness'] == 'true':
                uniqueness = self.get_uniqueness(temp_total_docs)
                self.monthly_parameters["Uniqueness"][year] = "{0:.2f}".format(uniqueness)
            else:
                self.monthly_parameters["Uniqueness"] = {}

            if params['Validity'] == 'true':
                validity = self.get_validity(temp_total_fields)
                self.monthly_parameters["Validity"][year] = "{0:.2f}".format(validity)
            else:
                self.monthly_parameters["Validity"] = {}

            if params['Timeliness'] == 'true':
                timeliness = self.get_timeliness()
                self.monthly_parameters["Timeliness"][year] = "{0:.2f}".format(timeliness)
            else:
                self.monthly_parameters["Timeliness"] = {}

            if params['Correctness'] == 'true':
                correctness = self.get_correctness()
                self.monthly_parameters["Correctness"][year] = "{0:.2f}".format(correctness)
            else:
                self.monthly_parameters["Correctness"] = {}

            if params['Correctness'] == 'true':
                usability = completeness * timeliness * correctness/10000.0
                self.monthly_parameters["Usability"][year] = "{0:.2f}".format(usability)
            else:
                self.monthly_parameters["Usability"] = {}

            self.coll = self.db.wqprocess
        return self.monthly_parameters

# Instantiating the class for testing purpose
params = YearlyQPCalculation()
years = [2016, 2017]
p= params.calculate_yearly_parameters(years)
print p
