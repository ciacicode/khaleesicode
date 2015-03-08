import json
import urllib2

def fciResources(data):
    '''
        input url of json formatted data
        output dict
        { '<area>': {'last_modified', 'url':}}
    '''
    jsonSimple = json.load(data)
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
    
    
    
    
