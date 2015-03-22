import MySQLdb
import dbconfig

# loop through the xml files in the database and update the postcode database
# parse the file with the etree library

# connect to database
db = MySQLdb.connect(host=dbconfig.host,user=dbconfig.user, passwd= dbconfig.password, db = dbconfig.database);
# creating cursor object
cur = db.cursor()
cur.execute('TRUNCATE TABLE fci_data.postcodes')
    
# execute insert query
cur.execute('SELECT URL FROM fci_data.sources')

for url in cur.fetchall():
    # pass the url to an xmlparser function
    print url

    
# commit query and close
    
db.commit()
db.close()