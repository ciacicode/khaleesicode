__author__ = 'ciacicode'


from modules.db_models import *
from modules.fci import postcodes_return, post_to_area, fci_object_return, find_max
from flask import request
from flask import jsonify
from mysite import app


@app.route('/api')
def api_root():
    resp = jsonify({
        "description": "This is the home of khaleesicode apis",
        "apis":
                {
                    "api": "Fried Chicken Index",
                    "description": "Returns FCI for a given postcode",
                    "endpoint": "/api/fci",
                }

    })
    return resp


@app.route('/api/fci')
def api_fci():
    """
    :return: in case of no parameters given it returns the entire mapping of the api endpoints. if a postcode is provided in the form of a gest parameter, it will return the value of the resource
    """
    all_postcodes = postcodes_return()
    all_postcodes = all_postcodes['postcodes']
    if 'postcode' in request.args:
        # check also if the postcode is among the ones we have data for
        p = post_to_area(request.args['postcode'])
        if p in all_postcodes:
            resp = fci_object_return(request.args['postcode'])
            resp = jsonify(resp)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    else:
        resp = jsonify(
            {
    "url": "https://www.khaleesicode.com/api/fci",
    "description": "Returns FCI value for a given postcode as GET parameter khaleesicode.com/api/fci?postcode=<postcode>",
    "resources": {
        "postcodes": {
            "url": "https://www.khaleesicode.com/api/fci/postcodes",
            "description":"Returns list of postcodes comprised in the FCI"
        },
        "maximum": {
            "url": "https://www.khaleesicode.com/api/fci/maximum",
            "description": "Returns the postcode associated with the maximum value of FCI as of latest available information",
        },
    },
})
        resp.status_code = 200
        return resp


@app.route('/api/fci/postcodes')
def api_postcodes():
    """

    :return: all the postcodes where there is a Fried Chicken Index value
    """
    fci_api_postcodes = postcodes_return()
    resp = jsonify(fci_api_postcodes)
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/api/fci/maximum')
def api_maximum():
    """

    :return: the maximum value of fci in the database
    """
    resp = find_max()
    resp = jsonify(resp)
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(debug=True)