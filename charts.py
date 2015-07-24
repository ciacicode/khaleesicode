__author__ = 'ciacicode'

from collections import OrderedDict
from bokeh.plotting import figure, show, output_file
import pdb
import csv
import london_postcodes as lp


fci_data = {}

with open('static/fci.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ps = row['postcode']
        fci = row['fci']
        fci_data[str(ps)] = fci

london_p = lp.data.copy()
postcode_xs = [london_p[name]["lons"] for name in london_p]
postcode_ys = [london_p[name]["lats"] for name in london_p]

colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

postcode_colours = []

for name in london_p:
    try:
        parent = name[0]
        fci_value = float(fci_data[parent])
        idx = int(fci_value/20)
        postcode_colours.append(colors[idx])
    except KeyError:
        postcode_colours.append("black")


output_file("static/london_fci.html", title="mapexample")

p = figure(title="fci 2015", toolbar_location="left", plot_width=1100, plot_height=700)

p.patches(postcode_xs, postcode_ys, fill_color=postcode_colours, fill_alpha=0.7, line_color="#884444", line_width=0.5)

show(p)