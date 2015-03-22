import xml.etree.ElementTree as ET
from urllib import urlopen
from xml.etree.ElementTree import parse

def fciPostcodes (url, areaName):
    '''
        input:
            url of xml 
            name of area
        output dict as
        {'area':['unique postcodes']}
    '''
    
    def zipToArea(zip):
        '''takes a zip code, cleans it and returns the area code'''
        zip = zip.upper()
        zip = zip.replace(" ","");
        inputLength = len(zip)
        zoneInput = zip[:inputLength-3]
        return zoneInput  
        
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
            zonePostcode = zipToArea(postCode)
            #add postcodes to nested list
            nestList.append(zonePostcode)     
        
    #normalise list
    nestList = set(nestList)
    outputDict[areaName] = nestList
    return outputDict
    
    
    


        
        
            
    
