import xml.etree.ElementTree as ET
from urllib import urlopen
from xml.etree.ElementTree import parse

# parse the file with the etree library
u = urlopen('http://data.gov.uk/data/resource_cache/be/be400256-25b3-4228-a556-3ffa557b4c18/FHRS524en-GB.xml')
tree = ET.parse(u)
root = tree.getroot()
collection = root.find('EstablishmentCollection')

for detail in collection.findall('EstablishmentDetail'):
    bizName = detail.find('BusinessName').text
    postCode = detail.findtext('PostCode')
    rating = detail.find('RatingValue').text
    print bizName, postCode, rating