''' Python frontend for Catalogue API's '''

import requests
import json
import types
import multiprocessing

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def getData(c):
    ''' HTTP get on latest resource data '''
    return {"id":c["id"], "data":requests.get(c["latestResourceData"], verify=False).json()}

def getHistoric(c, startTime, endTime):
    ''' HTTP get on latest resource data '''
    NAME  = c["NAME"]
    return {"id":c["id"], "data":requests.get(c["latestResourceData"], verify=False).json()}

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
        print(url)
        return requests.get(url,verify=False).json()


    def getLatestDataFromItems(self, items) :
        ''' Get latest data for all items that are part of an array '''
        pool = multiprocessing.Pool(processes=3)
        pool_outputs = pool.map(getData, items)
        pool.close()
        pool.join()
        return pool_outputs

    def getHistoricDataFromItems(self, items, startTime, endTime):
        ''' Get historic data for the items between the timestamps '''
        pool = multiprocessing.Pool(processes=3)
        pool_outputs = pool.map(getHistoric, items, startTime, endTime)
        pool.close()
        pool.join()
        return pool_outputs

