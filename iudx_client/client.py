''' Python frontend for Catalogue API's '''

import requests
import json
import types
import multiprocessing

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


baseURL = "https://pune.iudx.org.in/api/1.0.0/resource"

headers = {"apikey":"vasanth@rbccps", "id":"vasanth"}

def getData(i):
    ''' HTTP get on latest resource data '''
    return {"id":i["id"], "data":requests.get(i["latestResourceData"], verify=False).json()}


#def getHistoric(i):
#    ''' HTTP get on latest resource data '''
#    startTime = i["startTime"].replace(" ", "%20")
#    endTime = i["endTime"].replace(" ", "%20")
#    c = i["item"]
#    NAME  = c["NAME"].replace(" ", "%20")
#    iD = c["id"]
#    openAPIObj = requests.get(c["accessInformation"][0]["accessSchema"], verify=False).json()
#    apis = openAPIObj["paths"].keys()
#    queryTemplate = ""
#    for api in apis:
#        if "query" in api:
#            queryTemplate = api
#    if queryTemplate is not "":
#        queryURL = baseURL + queryTemplate.replace("{NAME}", NAME).replace("{startTime}", startTime).replace("{endTime}",endTime)
#    data = []
#    try:
#        print(queryURL)
#        d = {"id":iD, "data":requests.get(queryURL, headers=headers,verify=False).json()}
#        print(d)
#    except Exception as e:
#        print(e)
#    return data
    


class Cat:
    '''
        Cat Class to perform various operations
    '''
    def __init__(self, catURL, clientCertificate=None):
        if catURL[-1] != "/":
            catURL += "/"
        self.catURL = catURL
        #self.cat = requests.get(catURL,verify=False).json()

    def getTags(self):
        ''' Get all catalogue tags '''
        cat = requests.get(self.catURL,verify=False).json()
        tags = set() 
        for c in cat:
            for t in c["tags"]:
                tags.add(t)
        return list(tags)

    def generateLink(self, attributes=None, filters=None, location=None):
        ''' Generate a http link based on provided parameters'''
        attrStr = "attribute?"
        filterStr = "attributeFilter=("
        locationStr = "location={"
        if attributes is not None:
            for attr in attributes:
                if type(attributes[attr]) is list:
                    attrStr +=  attr+"=("+"".join(att+"," for att in attributes[attr])[:-1] + ")"
                else:
                    attrStr +=  attr+"="+attributes[attr]
        if filters is not None:
            filterStr +=  "".join(fltr + "," for fltr in filters)[:-1] + ")"
        if location is not None:
            locationStr +=  "\"lat\":"+ str(location["lat"]) + ",\"long\":"+ str(location["long"]) + ",\"radius\":" + str(location["radius"]) + "}"

        lnk = self.catURL + (attrStr +"&" if attributes is not None else "") + (filterStr + "&" if filters is not None else "") + (locationStr + "&" if location is not None else "")
        return lnk


    def getItems(self, attributes=None, filters=None, location=None):
        ''' Get all items based on povided parameters '''
        items = []
        url = self.generateLink(attributes=attributes, filters=filters, location=location) 
        return requests.get(url,verify=False).json()


    def getLatestDataFromItems(self, items) :
        ''' Get latest data for all items that are part of an array '''
        pool_outputs = []
        try:
            pool = multiprocessing.Pool(processes=3)
            pool_outputs = pool.map(getData, items)
            pool.close()
            pool.join()
        except Exception as e:
            print(e)

        return pool_outputs

#    def getHistoricDataFromItems(self, items, startTime, endTime):
#        ''' Get historic data for the items between the timestamps '''
#        pool_outputs = []
#        try:
#            pool = multiprocessing.Pool(processes=3)
#            pool_outputs = pool.map(getHistoric, [ {"item": i, "startTime":startTime, "endTime":endTime} for i in items])
#            pool.close()
#            pool.join()
#        except Exception as e:
#            print(e)
#        return pool_outputs



