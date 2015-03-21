import MySQLdb
import jsonparser
import dbconfig

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
    db = MySQLdb.connect(host=dbconfig.host,user=dbconfig.user, passwd= dbconfig.password, db = dbconfig.database);
    # creating cursor object
    cur = db.cursor()
    
    # execute insert query
    cur.execute('INSERT INTO sources (ID,Area,LastModified,URL) VALUES (%s,%s,%s,%s)',(dbID,tempArea,lastModified,url))
    
    # commit query and close
    
    db.commit()
    db.close()
    
    