'''
This modules exposes geometry data for London Postcodes. It exposes a dictionary 'data' which is
indexed by the two-tuple containing (parent postcode, specific postcode) and has the following dictionary as the
associated value:


Data is powered by http://www.opendoorlogistics.com/data/
'''
from __future__ import absolute_import
import csv
from mysite.configs.khal_config import Config


data = {}

with open(Config.LONDONCSVPATH) as f:
    reader = csv.DictReader(f)
    for row in reader:
        parent = row['parent']
        postcode = row['name']
        lons = row['lons']
        float_lons = map(float, lons.split(','))
        lats = row['lats']
        float_lats = map(float, lats.split(','))
        data[parent, postcode] = {'lons': float_lons, 'lats': float_lats, }