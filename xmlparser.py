import xml.etree.ElementTree as ET


# parse the file with the etree library
tree = ET.parse('/home/maria/Desktop/ciacicode/fci/data.xml')
root = tree.getroot()
collection = root.find('EstablishmentCollection')

for detail in collection.findall('EstablishmentDetail'):
    bizName = detail.find('BusinessName').text
    rating = detail.find('RatingValue').text
    print bizName, rating