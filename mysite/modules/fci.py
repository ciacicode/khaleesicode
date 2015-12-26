from __future__ import division, absolute_import
__author__ = 'ciacicode'
from mysite.modules.db_models import *
import string
import re
from urllib import urlopen
import json
import xml.etree.ElementTree as ET
import datetime


def post_to_area(postcode):
    """takes a postcode, returns area code"""
    # normalise user input
    postcode = postcode.upper()
    postcode = re.sub('[\W_]', '', postcode)
    # remove last three chars for the house
    if len(postcode) >= 5:
        postcode = postcode[:-3]
        return postcode
    else:
        return postcode


def postcodes_dict(url, area_name):
    """ takes url of xml and area name
        output dict as {'area':{'unique postcodes'}}
    """
    # parse the file with the etree library
    read_url = urlopen(url)
    tree = ET.parse(read_url)
    root = tree.getroot()
    collection = root.find('EstablishmentCollection')
    output_dict = {}
    nest_list = []
    # iterate through the collection and append area postcode to a list
    for detail in collection.findall('EstablishmentDetail'):
        post_code = detail.findtext('PostCode')
        if post_code is not None:
            zone_postcode = post_to_area(post_code)
            # add postcodes to nested list
            nest_list.append(zone_postcode)

    # normalise list
    nest_list = set(nest_list)
    nest_list = list(nest_list)
    output_dict[area_name] = nest_list
    return output_dict


def fci_calculate(postcode):
    """
        requires postcode
        returns fciindex
        and updates database
    """
    # create fci counter
    fci_count = 0
    restaurant_count = 0
    zone_input = post_to_area(postcode)
    keys = ("CHICKEN", "CHICK", "FRIED")
    no_keys = "NANDO"
    url_list = find_xml(zone_input)
    # unpack URLs from xml_dict
    for item in url_list:

        u = urlopen(item)
        tree = ET.parse(u)
        root = tree.getroot()
        collection = root.find('EstablishmentCollection')
        for detail in collection.findall('EstablishmentDetail'):
            xml_postcode = detail.findtext('PostCode')
            if xml_postcode is not None:
                zone_xml = post_to_area(xml_postcode)
                if zone_input == zone_xml:
                    restaurant_count += 1
                    business_name = detail.find('BusinessName').text
                    upper_business_name = business_name.upper()
                    if upper_business_name == '':
                        break
                    elif no_keys in upper_business_name:
                        break
                    else:
                        for key in keys:
                            if key in upper_business_name:

                                fci_count += 1
                                break
    if restaurant_count == 0:
        return fci_count
    else:
        result = fci_count/restaurant_count
        return result


def resources_list(url):
    """
        input url of json formatted data
        output list
        crete a list of FciSources database objects
    """
    read_data = urlopen(url)
    json_simple = json.load(read_data)
    json_encoded = json.dumps(json_simple)
    json_decoded = json.loads(json_encoded)
    res_list = list()
    final_list = list()
    for key in json_decoded.keys():
        if key == 'resources':
            # dive into the resources
            res_list = json_decoded['resources']
    for entry in res_list:
        last_modified = entry['last_modified']
        # Remove the bloody T from the date
        last_modified = string.split(last_modified, 'T')
        day = last_modified[0]
        hours = last_modified[1]
        dt_last_modified = day + " " + hours
        dt_last_modified = datetime.strptime(dt_last_modified, "%Y-%m-%d %H:%M:%S.%f")
        url = entry['url']
        area = entry['description']
        source = db.FciSources(area, url, dt_last_modified)
        final_list.append(source)
    return final_list


def generate_fci_chart_data():
    """
    Generate a csv holding all fci data
    """
    # db = connect_fci_db()
    #cur.execute("SELECT * FROM fciIndex ORDER BY FCI")
    #db.commit()
    #data = cur.fetchall()
    #db.close()
    #with open('static/fci.csv', 'w') as f:
    #    fieldnames = ['postcode', 'fci']
    #   writer = csv.DictWriter(f, fieldnames=fieldnames)
    #    writer.writeheader()
    #    for postcode, fci in data:
    #        writer.writerow({'postcode': str(postcode), 'fci': float(fci)})

# Functions to update or search databases


def update_sources():
    """
        performs database update of the FciSources table
    """
    # json data
    start_url = 'http://data.gov.uk/api/2/rest/package/uk-food-hygiene-rating-data'
    all_areas_data = resources_list(start_url)
    # drop fcisources table

    for s in all_areas_data:
        db.session.add(s)
    db.session.commit()


def update_locations():
    """
    performs database update of the Locations Table
    """
    # execute select query

    results = db.session.query(FciSources.area, FciSources.url)
    results = results.all()

    for area, url in results:
        # pass the url to an xmlparser function
        temp_dict = postcodes_dict(url, area)
        value_list = temp_dict.values()
        iterable = value_list[0]
        # parse the dict and write into database
        for value in iterable:
            if value == "":
                break
            else:
                # create instance of location
                location = Locations(area, value)
                # execute insert query
                db.session.add(location)
                # commit query
    db.session.commit()


def update_fci():
    """
        updates the fciindex table
    """
    results = db.session.query(db.Locations.postcode)
    results = results.all()
    postcodes = sorted(set(results))
    maximum = 0.0
    fci_dict = dict()
    for p in postcodes:
        p = str(p[0])
        fci = fci_calculate(p)
        fci_dict[p] = fci
        if fci > maximum:
            maximum = fci

    # time to write in the table
    for key, value in fci_dict.iteritems():
        fci = (value/maximum)*100
        record = FciIndex(key, fci)
        db.session.add(record)
    db.session.commit()


def find_xml(postcode):
    """
       input a postcode returns dict of
       xml URL of area(s)
    """
    p_postcode = post_to_area(postcode)
    location = Locations.query.filter_by(postcode=p_postcode).all()
    xml_list = list()
    for item in location:
        source = FciSources.query.filter_by(area=item.area).first()
        xml_list.append(source.url)
    return xml_list


def fci_return(postcode):
    """
        receives postcode
        returns formatted fci
    """
    # normalise input
    postcode = post_to_area(postcode)
    fci = FciIndex.query.filter_by(postcode=postcode).first()
    if fci.fci is None:
        return 'There is no FCI for this area'
    else:
        return "{0:.2f}".format(fci.fci)


def fci_object_return(postcode):
    """

    :param postcode:
    :return: the entire fci object
    """
    fci_object = dict()
    postcode = post_to_area(postcode)
    query_object = FciIndex.query.filter_by(postcode=postcode).first()
    fci_object['postcode'] = query_object.postcode
    fci_object['fci'] = query_object.fci
    fci_date = query_object.date
    fci_object['last_updated'] = fci_date.strftime("%Y-%m-%d")
    return fci_object


def postcodes_return():
    """
    :return: all postcodes for which we have an fci value
    """
    postcodes = db.session.query(FciIndex.postcode)
    all_postcodes = postcodes.all()
    postcode_list = list()
    for postcode in all_postcodes:
        postcode_list.append(postcode[0])
    j_object = dict()
    j_object["postcodes"] = postcode_list
    return j_object


def find_max():
    """
    :return: the fci object that is found to be the highest
    """
    query_object = FciIndex.query.filter_by(fci=100).first()
    max_postcode = query_object.postcode
    maximum_fci = fci_object_return(max_postcode)
    return maximum_fci


