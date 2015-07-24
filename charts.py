__author__ = 'ciacicode'

from collections import OrderedDict
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool
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
postcode_name = []
postcode_fci = []

for name in london_p:
    try:
        parent = name[0]
        fci_value = float(fci_data[parent])
        idx = int(fci_value/20)
        postcode_colours.append(colors[idx])
        postcode_name.append(name[1])
        postcode_fci.append(fci_value)
    except KeyError:
        postcode_colours.append("black")

source = ColumnDataSource( data = dict(x=postcode_xs, y=postcode_ys, color=postcode_colours, name=postcode_name, rate=postcode_fci,))

output_file("static/london_fci.html", title="mapexample")

TOOLS = "pan, wheel_zoom, box_zoom, reset, hover, save"

p = figure(title="fci 2015", toolbar_location="left", plot_width=1100, plot_height=700, tools = TOOLS)

p.patches('x', 'y', fill_color='color', fill_alpha=0.7, line_color="#884444", line_width=0.5, source=source)

hover = p.select(dict(type=HoverTool))
hover.point_policy = "follow_mouse"
hover.tooltips = OrderedDict([("Name","@name"),("FCI","@rate"),("Long, Lat","$x, $y"),])

show(p)