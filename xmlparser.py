import xml.etree.ElementTree as ET
from urllib import urlopen
from xml.etree.ElementTree import parse
import jsonparser

# json data
json = 'http://data.gov.uk/api/2/rest/package/uk-food-hygiene-rating-data'
allAreasData = jsonparser.fciResources(json)

# parse the file with the etree library
u = urlopen('http://data.gov.uk/data/resource_cache/1e/1e5a0ed1-9c70-4f0d-88ea-c563880dfd44/FHRS519en-GB.xml')
tree = ET.parse(u)
root = tree.getroot()
collection = root.find('EstablishmentCollection')

zipInput = raw_input('What is your zip code? ')
# need to ensure the zipInput is correctly formatted

def zipToArea(zip):
    "takes a zip code, cleans it and returns the area code"
    zip = zip.upper()
    zip = zip.replace(" ","");
    inputLength = len(zip)
    zoneInput = zip[:inputLength-3]
    return zoneInput

zoneInput = zipToArea(zipInput)

increment = 0
count = 0.00

for detail in collection.findall('EstablishmentDetail'):
    postCode = detail.findtext('PostCode')
    if postCode is not None:
        zoneXML = zipToArea(postCode)
        if zoneInput == zoneXML:
            rating = detail.find('RatingValue').text
            if rating != 'Exempt' and rating != 'AwaitingInspection':
                rating = float(rating)
                increment = increment + rating
                count += 1.00
                # print postCode, rating

if count > 0:
    FCI = increment / count
    print ('FCI Index is '), FCI
    print ('There are '), count, (' restaurants in the area.')
else:
    print ('There are no restaurants in your area.')
            

