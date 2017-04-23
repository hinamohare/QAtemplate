from pymongo import MongoClient


class QPCalculation:
    def __init__(self):
        self.client = MongoClient()
        # Select appropriate database
        self.db = self.client.SFB
        # Select appropriate collection
        self.coll = self.db.FMWQ_e
        # Select the first document
        self.doc = self.coll.find_one()
        # Find the total number of documents
        self.total_docs = self.coll.find().count()
        # Iterate over keys pulled from first document
        self.count = 0
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
            validity = (self.total_fields - invalid) * 100.0 / self.total_fields
            return validity

    def get_timeliness(self):
        timeliness = 95.0
        return timeliness

    def get_correctness(self):
        correctness = 80.0
        return correctness

    def get_usability(self):
        usability = self.parameters["Completeness"] * (self.parameters["Correctness"] / 100.0) * (
        self.parameters["Timeliness"] / 100.0)
        return usability

    def calculate_parameters(self):
        completeness = self.get_completeness()
        self.parameters["Completeness"] = completeness

        uniqueness = self.get_uniqueness()
        self.parameters["Uniqueness"] = uniqueness

        validity = self.get_validity()
        self.parameters["Validity"] = validity

        timeliness = self.get_timeliness()
        self.parameters["Timeliness"] = timeliness

        correctness = self.get_correctness()
        self.parameters["Correctness"] = correctness

        usability = self.get_usability()
        self.parameters["Usability"] = usability

        print self.parameters


params = QPCalculation()
params.calculate_parameters()

