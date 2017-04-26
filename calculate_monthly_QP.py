from pymongo import MongoClient


class MonthlyQPCalculation:

    def __init__(self):
        self.client = MongoClient()
        # Select appropriate database
        self.db = self.client.SFB
        # Select appropriate collection
        self.coll = self.db.FMWQ_e
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

    def get_validity(self,temp_total_fields):
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

    def calculate_monthly_parameters(self):
        """
        Call this function to get quality parameters on a monthly basis
        :return: dictionary of dictionaries self.monthly_parameters
        for e.g. {'Completeness': {'Mar': '99.95', 'Feb': '99.95', 'Aug': '99.97', 'Sep': '99.92', 'Apr': '99.99', 
        'Jun': '99.95', 'Jul': '100.00', 'Jan': '77.97', 'May': '99.86', 'Nov': '100.00', 'Dec': '99.97', 'Oct': '100.00'}, 
        'Timeliness': {'Mar': '95.00', 'Feb': '95.00', 'Aug': '95.00', 'Sep': '95.00', 'Apr': '95.00', 'Jun': '95.00', 
        'Jul': '95.00', 'Jan': '95.00', 'May': '95.00', 'Nov': '95.00', 'Dec': '95.00', 'Oct': '95.00'}, 
        'Correctness': {'Mar': '80.00', 'Feb': '80.00', 'Aug': '80.00', 'Sep': '80.00', 'Apr': '80.00', 'Jun': '80.00',
         'Jul': '80.00', 'Jan': '80.00', 'May': '80.00', 'Nov': '80.00', 'Dec': '80.00', 'Oct': '80.00'}, 
         'Validity': {'Mar': '100.00', 'Feb': '100.00', 'Aug': '100.00', 'Sep': '100.00', 'Apr': '100.00', 'Jun': '100.00', 
         'Jul': '100.00', 'Jan': '100.00', 'May': '100.00', 'Nov': '100.00', 'Dec': '100.00', 'Oct': '100.00'}, 
         'Uniqueness': {'Mar': '100.00', 'Feb': '100.00', 'Aug': '100.00', 'Sep': '100.00', 'Apr': '100.00', 'Jun': '100.00', 
         'Jul': '100.00', 'Jan': '97.51', 'May': '100.00', 'Nov': '100.00', 'Dec': '99.40', 'Oct': '100.00'}, '
         Usability': {'Mar': '75.96', 'Feb': '75.96', 'Aug': '75.98', 'Sep': '75.94', 'Apr': '75.99', 'Jun': '75.96', 
         'Jul': '76.00', 'Jan': '59.25', 'May': '75.89', 'Nov': '76.00', 'Dec': '75.98', 'Oct': '76.00'}}
        """
        month = 0
        month_mapping ={1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11:"Nov", 12: "Dec"}
        months = ["^01/", "^02/", "^03/", "^04/", "^05/", "^06/", "^07/", "^08/", "^09/", "^10/", "^11/", "^12/"]
        for _ in months:
            month += 1
            month_key = month_mapping[month]
            #print _
            self.coll.aggregate([{"$match": {"DateTimeStamp": {"$regex": _}}}, {"$out": "temp_coll"}])

            self.coll = self.db.temp_coll

            temp_total_docs = self.coll.find().count()
            #print temp_total_docs
            temp_total_fields = temp_total_docs * self.count
            #print temp_total_fields
            completeness = self.get_completeness(temp_total_fields)
            self.monthly_parameters["Completeness"][month_key] = "{0:.2f}".format(completeness)

            uniqueness = self.get_uniqueness(temp_total_docs)
            self.monthly_parameters["Uniqueness"][month_key] = "{0:.2f}".format(uniqueness)

            validity = self.get_validity(temp_total_fields)
            self.monthly_parameters["Validity"][month_key] = "{0:.2f}".format(validity)

            timeliness = self.get_timeliness()
            self.monthly_parameters["Timeliness"][month_key] = "{0:.2f}".format(timeliness)

            correctness = self.get_correctness()
            self.monthly_parameters["Correctness"][month_key] = "{0:.2f}".format(correctness)

            usability = completeness * correctness * timeliness/10000.0
            self.monthly_parameters["Usability"][month_key] = "{0:.2f}".format(usability)

            self.coll = self.db.FMWQ_e
        return self.monthly_parameters

# Instantiating the class for testing purpose
params = MonthlyQPCalculation()
p = params.calculate_monthly_parameters()
print p
