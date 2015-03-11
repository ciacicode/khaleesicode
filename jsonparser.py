import json
from urllib2 import urlopen

def fciResources(data):
    '''
        input url of json formatted data
        output dict
        { '<area>': {'last_modified', 'url':}}
    '''
    readData = urlopen(data)
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
    
    
    
    
