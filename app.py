import os
from bson.json_util import dumps
import datetime
import uuid

from flask import jsonify, request, session, json, redirect, flash
from flask import Flask, render_template, app
from pymongo import MongoClient

from model import RegionData, ValidatedData
from process import FileInputProcess, WebAPIInputProcess
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

UPLOAD_FOLDER = './data/csv'
ALLOWED_EXTENSIONS = set(['csv', 'xls','txt'])

app = Flask(__name__)  # define app using Flask
app.secret_key = '445424ad-df86-4c03-91ce-cc4b0d5dc9d3'  # Secret key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def gethome():
    return render_template('index.html')


@app.route('/index')
def getindex():
    return render_template('index.html')


# api to return all the regions and station information
@app.route('/getallregioninfo', methods=['GET'])
def getRegionInformation():
    obj = RegionData()
    data = obj.getAllRegionInfo()
    # return data
    return jsonify({"regions":json.loads(dumps(data))})


# api to search the station record in the validated dataset
@app.route('/search', methods=['GET'])
def searchData():
    """
    searches the record for the station into database
    :return: if data is found into the database
                return { found: "yes", data: { record}}
            else
                return { found: "no", data: {}}
    """

    # extract the parameters from the request body
    # input_json = request.get_json(force=True)
    region =  request.args.get('Region')
   # region = request.json["Region"]  # region name
    station = request.args.get("Station")  # station name
    #if len(station) is 0:
     #   station = None
    start_date = request.args.get("FromDate")  # start_date name
    if len(start_date) is 0:
        start_date = None
    end_date = request.args.get("ToDate")  # end_date name
    if len(end_date) is 0:
        end_date = None

    # query the database
    obj = ValidatedData()
    if (region != None and station != None and start_date != None and end_date != None):
        records = obj.searchValidatedDataForStation(region, station, start_date, end_date)
    elif (region != None and station != None):
        records = obj.searchAllValidatedDataForStation(region, station)
    elif (region != None):
        records = obj.searchAllValidatedDataForRegion(region)

    if (records is not None):
        return jsonify(data={'found': 'yes', 'records': json.loads( dumps(records))})
    else:
        return jsonify(data={'found': "no"})


"""
#api to collect user input file
@app.route('/getUserFile', methods=['POST'])
def getUserDataFile():
    input_json = request.get_json(force=True)

    region = request.json["region"]  # region name
    print "region: " + region

    station = request.json["station"]  # station name
    print "station: " + station

    start_date = request.json["from"]  # start_date name
    print "from: " + start_date

    end_date = request.json["to"]  # end_date name
    print "to: " + end_date
    #code for uploading file


#api to collect user input filters to collect data from webservice
@app.route('/getDataFromWebService', methods=['POST'])
def getDataFromAPI():
    input_json = request.get_json(force=True)

    region = request.json["region"]  # region name
    print "region: " + region

    station = request.json["station"]  # station name
    print "station: " + station

    start_date = request.json["from"]  # start_date name
    print "from: " + start_date

    end_date = request.json["to"]  # end_date name
    print "to: " + end_date
    #code for downloading data

"""


# api to calculate the quality parameters
@app.route('/getWaterQuality', methods=['POST'])
def getWaterQuality():
    """
    this api collects the user input and then process the data to calculate the quality paramaters
    :return: result = {"region": regionname , "station": stationname,
         "from": startdate, "to": enddate, "TotalWaterQuality": totalquality,
        "qualityParameters": {"completeness": cp, "accuracy": a, "timeliness": t, "uniqueness": un, "validity" : v, "consistency": c,
         reliability: r, "usability"": us} }
    """
    # return "data received"
    try:

        input_json = request.get_json(force=True)
        print(input_json)
        region = input_json['Region']  # region name

        station = input_json['Station']  # station name

        start_date = input_json['FromDate']  # start_date format  mm/dd/yy

        end_date = input_json['ToDate']  # end_date name

        clean = input_json["IsRequiredClean"]  # true or false
        if clean == "true":
            isCleaningRequired = True
        else :
            isCleaningRequired = False

        #validationType = input_json['ValidationType'] #modelbased or toolbased
        #parameters = input_json['Parameters']
        #parameters {  'Completeness': 'true', 'Timeliness': 'true', 'Correctness': 'true','Validity': 'true',
         #                       'Uniqueness': 'true','Usability': 'true'}

        monthlyValidation = input_json['MonthlyValidation'] #true/false
        if monthlyValidation == "true":
            monthly = True
            monthStartDate = input_json['MonthStartDate'] #yyyy
            monthEndDate = input_json['MonthEndDate'] #yyyy
        else :
            monthly = False
            monthStartDate=''
            monthEndDate =''

        yearlyValidation = input_json['YearlyValidation'] #true/false
        if yearlyValidation == "true":
            yearly = True
            startYear = input_json['StartYear'] #yyyy
            endYear = input_json['EndYear'] #yyyy
        else :
            yearly = False
            startYear=''
            endYear = ''

        parameters = {'Completeness': input_json["Parameters"]["Completeness"],
                      'Timeliness': input_json["Parameters"]["Timeliness"],
                      'Correctness': input_json["Parameters"]["Correctness"],
                      'Validity': input_json["Parameters"]["Validity"],
                      'Uniqueness': input_json["Parameters"]["Uniqueness"],
                      'Usability': input_json["Parameters"]["Usability"],
                      }

        source = input_json["Source"]  # WebService or CSV

        # if source is user uploaded csv file
        if source == 'CSV':
            filename = input_json['CsvFileName'] #read filename
            fileProcessObj = FileInputProcess();
            result = fileProcessObj.process(region, station, start_date, end_date, filename,
                            isCleaningRequired, parameters, monthly,monthStartDate,monthEndDate, yearly, startYear, endYear);
            return jsonify(data=result)

        #source is WebService
        else :
            modelBasedSubType = input_json['ModelBasedSubType']  # Stationbased or regionbased; only considered for source = WebService
            apiDataProcessObj = WebAPIInputProcess()
            if modelBasedSubType == "StationBased":
                result = apiDataProcessObj.processStationBased(region, station, start_date, end_date,
                            isCleaningRequired, parameters, monthly,monthStartDate,monthEndDate, yearly, startYear, endYear)
            else:
                result = apiDataProcessObj.processRegionBAsed(region, start_date, end_date,
                            isCleaningRequired, parameters, monthly,monthStartDate,monthEndDate, yearly, startYear, endYear)

            return jsonify(data=result)

    except Exception:
        return "Can't calculate quality parameters for this dataset"



    """
    request body for webservice =>
    {'Source': 'WebService', 'CsvFileName': '98723420348.csv', 'Region': 'San Francisco Bay, CA',
     'Station': 'China Camp', 'FromDate': '2/1/2017', 'ToDate': '2/2/2017', 'IsRequiredClean': 'false',
     'Parameters': {'Completeness': 'true', 'Accuracy': 'true', 'Timeliness': 'true', 'Uniqueness': 'true',
                    'Validity': 'true', 'Consistency': 'true', 'Reliability': 'true', 'Usability': 'true',
                    'Availability': True}, 'Model': 'Model1', 'ValidationType': 'ModelBased',
     'ModelBasedSubType': 'StationBased'}
     
     
     request body for file input =>
    {'Source': 'CSV', 'CsvFileName': '98723420348.csv', 'Region': 'San Francisco Bay, CA', 'Station': 'China Camp',
     'FromDate': '2/1/2017', 'ToDate': '2/2/2017', 'IsRequiredClean': 'false',
     'Parameters': {'Completeness': 'true', 'Accuracy': 'true', 'Timeliness': 'true', 'Uniqueness': 'true',
                    'Validity': 'true', 'Consistency': 'true', 'Reliability': 'true', 'Usability': 'true',
                    'Availability': True}, 'Model': 'Model1', 'ValidationType': 'ModelBased',
     'ModelBasedSubType': 'StationBased'}
     """






def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        print("upload called")
        if 'csvfile' not in request.files:
            flash('No file part')
            return jsonify( {"result": {"status": "failed - No File Part"}})
            #  return redirect(request.url)
        file = request.files['csvfile']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return jsonify({"result": 'no file selected'})
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) +"_" + secure_filename(file.filename)
            #  saveatlocation = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            saveatlocation = app.config['UPLOAD_FOLDER']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print (filename)
            return jsonify(result ={"filename": filename})

@app.route('/report/<id>', methods=['GET'])
def getReportFor():

    client = MongoClient()  # setting connection with the mongoclient
    db = client.qaplatformdb  # getting database
    collection = db.validateddata  # getting validateddata collections
    #collection = db.stationdata
    result = collection.find({"_id": ObjectId(id)})
    return jsonify(report=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # run app in debug mode
