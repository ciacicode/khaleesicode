import json
import urllib2

# open the json file
url = urllib2.urlopen('http://data.gov.uk/api/2/rest/package/uk-food-hygiene-rating-data')


def decode (data):
    '''
        takes json data as argument and returns decoded
        json ad python dict
    '''
    jsonSimple = json.load(data)
    jsonEncoded = json.dumps(jsonSimple)
    jsonDecoded = json.loads(jsonEncoded)
    return jsonDecoded

inputJson = decode(url)

for key in inputJson.keys():
    if key == 'resources':
        # dive into the resources
        resourcesList = inputJson['resources']
        
    '''resourcestList is a list of dictionaries each containing information
    regarding the area that was inspected for hygiene, when it was updated
    and where the xml file is tored'''
    

    '''The next part of the code will iterate over the resources to store
    last_modified, description,url into a dict'''

resourcesDict={}


for entry in resourcesList:
    nestDict = {}
    nestDict['last_modified'] = entry['last_modified']
    nestDict['url'] = entry['url']
    resourcesDict[entry['description']] = nestDict
    
    
    
    
