#FCI

This is a python project to create an application that calculates a London area's Fried Chicken Index (FCI).
The FCI is calculated based on instances of fried chicken shops and their hygiene rating in the area.

## Requirements
python 2.7
flask
MySQL

## Databases
* fci_data.sources
* fci_data.postcodes
* fci_data.ordered_postcodes

## List of custom libraries
* fci Utils.py

## List of files
fci.py
Main application for flask frontend.

orderedPostcodes.py
Script to sort postcodes in alphabetical order for better faster search.

updatePostcodes.py
Script to update postcodes

updateSources.py
Script to download all necessary URLs containing xml files with hygiene rating information

xmlparser.py
Legacy main app, will be phased out to handle FCI calculation to then serve it to the front-end




