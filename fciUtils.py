'''
    fciUtils is a set of common functions used in the realm of the project
    
    by ciacicode & Grutin
'''

import xml.etree.ElementTree as ET
from urllib import urlopen
from xml.etree.ElementTree import parse
import json
import re

def zipToArea(zip):
    '''takes a zip code, cleans it and returns the area code'''
    zip = zip.upper()
    zip = zip.replace(" ","")
    inputLength = len(zip)
    if inputLength >= 3:
        zoneInput = zip[:inputLength-3]
    else:
        zoneInput = zip
    return zoneInput

def postToArea(postcode):
    '''takes a postcode, returns area code'''
    postcode = postcode.upper()
    splice = re.split(',| ',postcode)
    return splice[0]
      

def postcodesDict (url, areaName):
    ''' takes url of xml and area name
        output dict as {'area':{'unique postcodes'}}
    '''
    # parse the file with the etree library
    readURL = urlopen(url)
    tree = ET.parse(readURL)
    root = tree.getroot()
    collection = root.find('EstablishmentCollection')
    outputDict = {}  
    nestList = []
    # iterate through the collection and append area postcode to a list
    for detail in collection.findall('EstablishmentDetail'):
        postCode = detail.findtext('PostCode')
        if postCode is not None:
            zonePostcode = postToArea(postCode)
            #add postcodes to nested list
            nestList.append(zonePostcode)     
        
    #normalise list
    nestList = set(nestList)
    nestList = list(nestList)
    outputDict[areaName] = nestList
    return outputDict

def resourcesDict(url):
    '''
        input url of json formatted data
        output dict
        { 'area': {'last_modified', 'url'}}
    '''
    readData = urlopen(url)
    jsonSimple = json.load(readData)
    jsonEncoded = json.dumps(jsonSimple)
    jsonDecoded = json.loads(jsonEncoded)
    resourcesDict={}
    for key in jsonDecoded.keys():
        if key == 'resources':
            #dive into the resources
            resourcesList = jsonDecoded['resources']
                
    for entry in resourcesList:
        nestDict = {}
        nestDict['last_modified'] = entry['last_modified']
        nestDict['url'] = entry['url']
        resourcesDict[entry['description']] = nestDict
    return resourcesDict
    
    
    
    

    
    
    


        
        
            
    
