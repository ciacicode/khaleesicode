__author__ = 'ciacicode'

from bokeh.charts import Bar, output_file, show, save

import fciUtils



def fcichart(data):

    # output to static HTML file
    output_file("templates/bar.html")

    # create a new line chat with a title and axis labels
    p = Bar(data[0], cat=data[1], title="FCI",
        xlabel='postcodes', ylabel='FCI', yscale='linear',width=800, height=600)

    # show the results
    show(p)



def findproperties(object):
    for property, value in vars(object).iteritems():
        print property, ": ", value

def example_chart(data):
    # output to static HTML file
    output_file("templates/example.html")

    # create a new line chat with a title and axis labels
    p = Bar(data, cat=['C1', 'C2', 'C3', 'D1', 'D2'], title="Bar example",
        xlabel='categories', ylabel='values', width=400, height=400)

    # show the results
    show(p)