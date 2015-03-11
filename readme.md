FCI

This is a python project to create an application that calculates a London area's Fried Chicken Index (FCI).
The FCI is calculated based on instances of fried chicken shops and their hygiene rating in the area.

List of modules
* jsonparser.py
* xmlparser.py

jsonparse.py

This module includes a function called fciResources that takes the Food Hygiene Rating API's json response and creates a python dictionary containing the URLs of all xml resources available per London area.

xmlparser.py

This is the core of the application for the moment but it is likely to be separated from the rest to make the application more sustainable. Xml parser parses a specific area's xml data with hygiene rating information and then calculates a weighted average of the area's hygiene ratings of restaurants.