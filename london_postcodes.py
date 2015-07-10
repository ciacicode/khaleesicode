'''
This modules exposes geometry data for London Postcodes. It exposes a dictionary 'data' which is
indexed by the two-tuple containing (parent_area_id, area_id) and has the following dictionary as the
associated value:
    data[(1,1)]['name']
    data[(1,1)]['lats']
    data[(1,1)]['lons']

Data is powered by MapIt
'''
from __future__ import absolute_import
import csv
import pdb


data = {}

with open('static/london_postcodes.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        parent_id = row['parent_id']
        area_id = row['area_id']
        lats = row['lats'].split(',')
        lons = row['lons'].split(',')
        name = row['name']

        # manipulate list to have floats instead of integers
        new_lats = []
        new_lons = []
        for la in range(0, len(lats)):
            lat_coord = float(lats[la])
            new_lats.append(lat_coord)
        for lo in range(0, len(lons)):
            lon_coord = float(lons[lo])
            new_lons.append(lon_coord)

        lats = new_lats
        lons = new_lons

        data[str(name)] = {'lats': lats, 'lons': lons, }