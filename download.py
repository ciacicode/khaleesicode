import urllib

# download and save data in a file
url = "http://data.gov.uk/data/resource_cache/be/be400256-25b3-4228-a556-3ffa557b4c18/FHRS524en-GB.xml"
urllib.urlretrieve (url,"/home/martin/fci/data.xml")