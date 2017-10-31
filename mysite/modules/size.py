
__author__ = 'ciacicode'

#script to pupulate Bottom database
from db_models import Bottom
from db_models import db
import csv
import json
import os
import pdb


def generate_data(input_file):
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
                jeans = dict()
                jeans['waist'] = json.dumps({'cm':float(row['w']), 'in': cm_to_in(float(row['w']))})
                jeans['hip'] = json.dumps({'cm':float(row['h']), 'in': cm_to_in(float(row['h']))})
                jeans['category'] = row['cat']
                jeans['product_type'] = row['type']
                jeans['gender'] = row['gender']
                manufacturer_sizes = get_sizes(row)
                jeans['sizes'] = json.dumps(manufacturer_sizes)
                #create a Bottom object as a row in the Bottom database
                b = Bottom(jeans)
                db.session.add(b)
                db.session.commit()

    except IOError as io:
        print io

def get_sizes(jeans):
    """
    accepts dict of sizes from csv and returns structured dict as
    "Brand:\{'std':,'numeric':, 'us:','uk':, 'it'}"
    """
    brands = ['Gap', 'Levis', 'Zara', 'Diesel', 'Belstaff', 'G-STAR', 'Asos', 'AE', 'Forever 21', 'Pepe Jeans', 'Topshop', 'Lee', 'True Religion', 'Wrangler', 'CK']
    manufacturer_sizes = dict()
    for brand in brands:
        #create key in the dict
        manufacturer_sizes[brand] = dict()
        for k in jeans.keys():
            #found the exact brand
            if brand == k:
                continue
            elif brand in k:
                #found a manufacturer size, I substitute it
                if 'us' in k:
                    #this is a us sizes
                    manufacturer_sizes[brand]['us'] = jeans[k]
                elif 'uk' in k:
                    #this is a uk size
                    manufacturer_sizes[brand]['uk'] = jeans[k]
                elif 'std' in k:
                    #this is a std size
                    manufacturer_sizes[brand]['std'] = jeans[k]
                elif 'it' in k:
                    #this is an italian size
                    manufacturer_sizes[brand]['it'] = jeans[k]
                elif 'Numeric' in k:
                    #manufacturer size
                    manufacturer_sizes[brand]['numeric'] = jeans[k]
                    #create output dict
    return manufacturer_sizes




def cm_to_in(cm):
    """
    cm: int
    Converts centimeter units into inches
    Returns a rounded number
    """
    return int(round(int(cm)*2.54))

generate_data('db.csv')
