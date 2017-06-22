from pymongo import MongoClient


class MonthlyQPCalculation:
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
        # print self.count
        self.monthly_parameters = {"Completeness": [], "Uniqueness": [], "Validity": [], "Timeliness": [],
                                   "Correctness": [], "Usability": []}

    def get_completeness(self, temp_total_fields):
        total_null = 0
        # Iterate over keys pulled from first document to find all null values
        for key in self.doc:
            total_null = total_null + self.coll.find({'$or': [{key: {'$type': 10}}, {key:""}]}).count()
            print total_null
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
        distinct = self.coll.distinct("DateTimeStamp", {"DateTimeStamp": {"$ne": ""}})
        timely = len(distinct)
        timeliness = timely * 100.0 / (96.0 * days)
        return timeliness

    def get_correctness(self, temp_total_fields):
        incorrect = self.incomplete + self.invalid
        if temp_total_fields:
            correctness = (temp_total_fields - incorrect) * 100.0 / temp_total_fields
        else:
            correctness = 0.0
        return correctness

    def calculate_monthly_parameters(self, params, years):
        """
        Call this function to get quality parameters on a monthly basis
        :param years: List of years for which data quality parameters are to be calculated.
        for e.g. years = [2016, 2017]
        :type params: dictionary indicating which quality parameters are to be calculated

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
        try:

            print("calculate monthly qp called")
            #print ("parameters: ", params)

            if params['Usability'] == "true" or params['Usability'] == True:
                params['Completeness'] = 'true'
                params['Correctness'] = 'true'
                params['Timeliness'] = 'true'

            if params['Correctness'] == "true" or params['Correctness'] == True:
                params['Completeness'] = 'true'
                params['Validity'] = 'true'

            month_mapping = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep",
                             10: "Oct", 11: "Nov", 12: "Dec"}
            months = ["^0?1[/-]", "^0?2[/-]", "^0?3[/-]", "^0?4[/-]", "^0?5[/-]", "^0?6[/-]", "^0?7[/-]", "^0?8[/-]", "^0?9[/-]", "^10[/-]", "^11[/-]", "^12[/-]"]
            # print params
            for year in years:
                month = 0
                pattern = "[/-]" + str(year) + " "
                # print pattern
                self.coll.aggregate([{"$match": {"DateTimeStamp": {"$regex": pattern}}}, {"$out": "temp_year_coll"}])
                self.coll = self.db.temp_year_coll
                for _ in months:
                    month += 1
                    key = month_mapping[month] + " " + str(year)
                    # print key
                    self.coll.aggregate([{"$match": {"DateTimeStamp": {"$regex": _}}}, {"$out": "temp_month_coll"}])

                    self.coll = self.db.temp_month_coll

                    temp_total_docs = self.coll.find().count()
                    # print temp_total_docs
                    temp_total_fields = temp_total_docs * self.count
                    # print temp_total_fields
                    if params['Completeness'] == 'true' :
                        #print ("calculating Completeness")
                        completeness = self.get_completeness(temp_total_fields)
                        #self.monthly_parameters["Completeness"][key] = "{0:.2f}".format(completeness)
                        self.monthly_parameters["Completeness"].append(float("{0:.2f}".format(completeness)))
                    else:
                        completeness = 0
                        self.monthly_parameters["Completeness"] = []

                    if params['Uniqueness'] == 'true' :
                        #print ("calculating uniqueness")
                        uniqueness = self.get_uniqueness(temp_total_docs)
                        #self.monthly_parameters["Uniqueness"][key] = "{0:.2f}".format(uniqueness)
                        self.monthly_parameters["Uniqueness"].append(float("{0:.2f}".format(uniqueness)))
                    else:
                        uniqueness = 0
                        self.monthly_parameters["Uniqueness"] = []

                    if params['Validity'] == 'true' :
                        #print ("calculating validity")
                        validity = self.get_validity(temp_total_fields)
                        #self.monthly_parameters["Validity"][key] = "{0:.2f}".format(validity)
                        self.monthly_parameters["Validity"].append(float("{0:.2f}".format(validity)))
                    else:
                        validity = 0
                        self.monthly_parameters["Validity"] = []

                    if params['Timeliness'] == 'true':
                        #print ("calculating timeliness")
                        if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
                            days = 31
                        elif month == 2 or 4 or 6 or 9 or 11:
                            days = 30
                        elif month == 2 and (year % 4) == 0:
                            days = 29
                        else:
                            days = 28
                        timeliness = self.get_timeliness(days)
                        #self.monthly_parameters["Timeliness"][key] = "{0:.2f}".format(timeliness)
                        self.monthly_parameters["Timeliness"].append(float("{0:.2f}".format(timeliness)))
                    else:
                        timeliness = 0
                        self.monthly_parameters["Timeliness"] = []

                    if params['Correctness'] == 'true' :
                        #print ("calculating correctness")
                        correctness = self.get_correctness(temp_total_fields)
                        #self.monthly_parameters["Correctness"][key] = "{0:.2f}".format(correctness)
                        self.monthly_parameters["Correctness"].append(float("{0:.2f}".format(correctness)))
                    else:
                        correctness = 0
                        self.monthly_parameters["Correctness"] = []

                    if params['Usability'] == 'true':
                        #print ("calculating usability")
                        usability = completeness * correctness * timeliness / 10000.0
                        #self.monthly_parameters["Usability"][key] = "{0:.2f}".format(usability)
                        self.monthly_parameters["Usability"].append(float("{0:.2f}".format(usability)))
                    else:
                        self.monthly_parameters["Usability"] = []

                    self.coll = self.db.temp_year_coll
                self.coll = self.db.wqprocess
            return self.monthly_parameters
        except Exception:
            print("Exception in monthly qp calculation")
            return 0


# Instantiating the MonthlyQPCalculation() class for testing purpose
# param = MonthlyQPCalculation()
# _years = [2012]
# _params = {'Completeness': 'true', 'Correctness': 'true', 'Timeliness': 'true', 'Validity': 'true',
#             'Uniqueness': 'true', 'Usability': 'true'}
# p = param.calculate_monthly_parameters(_params, _years)
# print p
