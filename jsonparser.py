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

for item in inputJson:
    if item == 'resources':
        # dive into the resources
        resourcesList = inputJson['resources']
        


        
        