
__author__ = 'ciacicode'

#script to pupulate first version of the size database
from db_models import Bottom
from db_models import db
import csv
import json
import os
import pdb


def generate_bottom_db_data(input_file):
    """
    file: string
    Accepts csv file name in /static folder
    File must contain headers matching table column names
    """
    wd = '/home/maria/Desktop/ciacicode/khaleesicode/mysite/'
    try:
        with open( wd  + 'static/' + input_file, 'r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                #modify slightly some parts of the DictReader
                enriched_row = row
                enriched_row['w'] = json.dumps({'cm':int(row['w']), 'in': cm_to_in(int(row['w']))})
                enriched_row['h'] = json.dumps({'cm':int(row['h']), 'in': cm_to_in(int(row['h']))})
                pdb.set_trace()
                #create a Bottom object as a row in the Bottom database
                print enriched_row
                b = Bottom(enriched_row)
                db.session.add(b)
                print b
                db.session.commit()
                print 'object committed'
    except IOError as io:
        print io


def cm_to_in(cm):
    """
    cm: int
    Converts centimeter units into inches
    Returns a rounded number
    """
    return int(round(int(cm)*2.54))
