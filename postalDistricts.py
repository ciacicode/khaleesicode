import MySQLdb
import jsonparser

# json data
json = 'http://data.gov.uk/api/2/rest/package/uk-food-hygiene-rating-data'
allAreasData = jsonparser.fciResources(json)


# loop through the dictionary and store the data in the database

dbID = 0
for key , value in allAreasData.items():
    # store the key
    tempArea = key
    # store the content of the value
    tempValue = value
    # access the tempValue dictionary to store variables
    lastModified = tempValue['last_modified']
    url = tempValue['url']
    dbID = dbID + 1
    # write in the database all this stuff

    # connect to database
    db = MySQLdb.connect(host='localhost',user='fci_admin', passwd='FCIChimichanga6*', db = 'fci_data');
    
    # creating cursor object
    cur = db.cursor()
    
    # execute insert query
    cur.execute('INSERT INTO sources (ID,Area,LastModified,URL) VALUES (%s,%s,%s,%s)',(dbID,tempArea,lastModified,url))
    
    # commit query and close
    
    db.commit()
    db.close()
    
    
areasDict = {
'Barking and Dagenham':['IG11','RM5','RM8','RM9', 'RM10','RM6','RM7'],
'Barnet':['EN4','EN5','NW7','NW4','NW11','NW12','NW2','NW9','HA8','N11','N2'],
'Bexley':['DA5','DA6','DA7'],
'Brent':[],
'Bromley' :['BR1','BR2'],
'Camden':[],
'Croydon':[],
'Ealing':[],
'Enfield':['EN1','EN2','EN3'],
'Greenwich':[],
'Hackney':[],
'Hammersmith and Fulham':[],
'Haringey':[],
'Harrow':[],
'Hillingdon':[],
'Havering':[],
'Hounslow':[],
'Islington':[],
'Kensington and Chelsea':[],
'Kingston-Upon-Thhames':[],
'Lambeth':[],
'Lewisham':[],
'London (City of)':[],
'Merton':[],
'Redbridge':[],
'Richmond-Upon-Thames':[],
'Southwark':[],
'Sutton':[],
'Tower Hamlets':[],
'Waltham Forest':[],
'Wandsworth':[],
'Westminster':[]
    }
