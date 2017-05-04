from pymongo import MongoClient


class QPCalculation:
    def __init__(self):
        self.client = MongoClient()
        # Select appropriate database
        self.db = self.client.qaplatformdb
        # Select appropriate collection
        self.coll = self.db.wqprocess
        # Select the first document
        self.doc = self.coll.find_one()
        # Find the total number of documents
        self.total_docs = self.coll.find().count()
        # Iterate over keys pulled from first document
        self.count = 0
        self.invalid = 0
        self.incomplete = 0
        for key in self.doc:
            # print key
            self.count += 1  # Keep track of total number of keys/columns
        # Adds the value of completeness to parameters
        # print count
        # print total_null
        self.total_fields = self.total_docs * self.count
        self.parameters = {}
        self.yearly_parameters = {}

    def get_completeness(self):
        total_null = 0
        # Iterate over keys pulled from first document to find all null values
        for key in self.doc:
            total_null = total_null + self.coll.count({key: ""})
            self.incomplete = total_null
        completeness = ((self.total_fields - total_null) * 100.0) / self.total_fields
        return completeness

    def get_uniqueness(self):
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

        unique_rows = self.total_docs - u_count + u_rows

        # print "Unique rows based on",u_key,"are",unique_rows
        uniqueness = unique_rows * 100.0 / self.total_docs
        return uniqueness

    def get_validity(self):
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
            self.invalid = invalid
            validity = (self.total_fields - invalid) * 100.0 / self.total_fields
            return validity

    def get_timeliness(self,days):
        distinct = self.coll.distinct("DateTimeStamp", {"DateTimeStamp": {"$ne": ""}})
        timely = len(distinct)
        timeliness = timely * 100.0 / (96.0 * days)
        return timeliness

    def get_correctness(self):
        incorrect = self.incomplete + self.invalid
        correctness = (self.total_fields - incorrect) * 100.0 / self.total_fields
        return correctness

    def get_usability(self):
        usability = self.parameters["Completeness"] * (self.parameters["Correctness"] / 100.0) * (self.parameters["Timeliness"] / 100.0)
        return usability

    def calculate_parameters(self, params, days):
        """
        Call this function to get Quality Parameters of the entire data set.
        :return: dictionary self.parameters
        {'Overall Data Quality': '91.22', 'Completeness': '98.05', 'Timeliness': '95.00', 
        'Correctness': '80.00', 'Validity': '100.00', 'Uniqueness': '99.73', 'Usability': '74.52'}
        """
        if params['Usability'] == "true":
            params['Completeness'] = 'true'
            params['Correctness'] = 'true'
            params['Timeliness'] = 'true'

        if params['Correctness'] == "true":
            params['Completeness'] = 'true'
            params['Validity'] = 'true'

        if params['Completeness'] == 'true':
            completeness = self.get_completeness()
            self.parameters["Completeness"] = "{0:.2f}".format(completeness)
        else:
            self.parameters["Completeness"] = 0
            completeness = 0

        if params['Uniqueness'] == 'true':
            uniqueness = self.get_uniqueness()
            self.parameters["Uniqueness"] = "{0:.2f}".format(uniqueness)
        else:
            self.parameters["Uniqueness"] = 0
            uniqueness = 0

        if params['Validity'] == 'true':
            validity = self.get_validity()
            self.parameters["Validity"] = "{0:.2f}".format(validity)
        else:
            self.parameters["Validity"] = 0
            validity = 0

        if params['Timeliness'] == 'true':
            timeliness = self.get_timeliness(days)
            self.parameters["Timeliness"] = "{0:.2f}".format(timeliness)
        else:
            self.parameters["Timeliness"] = 0
            timeliness = 0

        if params['Correctness'] == 'true':
            correctness = self.get_correctness()
            self.parameters["Correctness"] = "{0:.2f}".format(correctness)
        else:
            self.parameters["Correctness"] = 0
            correctness = 0

        if params['Usability'] == 'true':
            usability = completeness*timeliness*correctness/10000.0
            self.parameters["Usability"] = "{0:.2f}".format(usability)
        else:
            self.parameters["Usability"] = 0
            usability = 0

        overall_data_quality = (completeness+uniqueness+validity+timeliness+correctness+usability)/6.0
        self.parameters["Overall Data Quality"] = "{0:.2f}".format(overall_data_quality)

        return self.parameters

# Instantiating the QPCalculation class for testing purpose
# param = QPCalculation()
# _params = {'Completeness': 'true', 'Correctness': 'true' , 'Timeliness': 'true', 'Validity': 'true',
#            'Uniqueness': 'true', 'Usability': 'true'}
# _days = 366
# p = param.calculate_parameters(_params, _days)
# print (p)
