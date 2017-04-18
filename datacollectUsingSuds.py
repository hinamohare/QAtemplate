"""from zeep import Client
server = SOAPpy.SOAPProxy("http://cdmo.baruch.sc.edu/webservices2/requests.cfc?wsdl")

        #stationcode="pdbjewq"
        responsedata =  server.exportAllParamsDateRangeXMLNew(stationcode, start_date, end_date,'*')
       # print responsedata
        pythonObject = SOAPpy.Types.simplify(responsedata)
        #jsonObject = json.dumps(pythonObject)
        #assert type(jsonObject) == str
        dataArray =  pythonObject["returnData"]["data"] # returns {  [{...},{....},.....]}

client = Client("http://cdmo.baruch.sc.edu/webservices2/requests.cfc?wsdl")
result = client.service.exportAllParamsDateRangeXMLNew('pdbjewq', '2014-12-30', '2014-12-31','*')
print(result)

import osa
cl = osa.Client("http://cdmo.baruch.sc.edu/webservices2/requests.cfc?wsdl")
result =  cl.service.exportAllParamsDateRangeXMLNew('pdbjewq', '2014-12-30', '2014-12-31','*')
print(result)

from zeep import Client

client = Client('http://www.webservicex.net/ConvertSpeed.asmx?WSDL')
result = client.service.ConvertSpeed(
    100, 'kilometersPerhour', 'milesPerhour')

print(result)



from suds.client import Client

soapClient = Client("http://cdmo.baruch.sc.edu/webservices2/requests.cfc?wsdl", timeout=90, retxml=True)

#Get the station codes SOAP request example.
#station_codes = soapClient.service.exportStationCodesXML()

#print station_codes

#Get all parameters from the station NIWOLMET for the date range of 2014-12-30 to 2014-12-31
params = soapClient.service.exportAllParamsDateRangeXML('niwolmet', '2014-12-30', '2014-12-31', '*')
print (params)

from suds.client import Client
client = Client('http://localhost:8181/soap/helloservice?wsdl', username='bob', password='catbob')
result = client.service.sayHello('bob')
"""
"""from zeep import Client

client = Client("http://cdmo.baruch.sc.edu/webservices2/requests.cfc?wsdl")
result = client.service.exportAllParamsDateRangeXMLNew('niwolmet', '2014-12-30', '2014-12-31','*')

print(result)
"""