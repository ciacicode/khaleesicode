import MySQLdb
import dbconfig
import fciUtils
import pdb

db = MySQLdb.connect(host=dbconfig.host,user=dbconfig.user, passwd= dbconfig.password, db = dbconfig.database);
cur = db.cursor()
cur.execute('TRUNCATE TABLE fci_data.ordered_postcodes')


cur.execute('SELECT Postcode, Area FROM fci_data.postcodes ORDER BY Postcode')

for Postcode, Area in cur.fetchall():
    cur.execute('INSERT INTO ordered_postcodes (Postcode,Area) VALUES (%s,%s)',(Postcode,Area))
    db.commit()

db.close()
    
