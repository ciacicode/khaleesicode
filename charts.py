__author__ = 'ciacicode'

from collections import OrderedDict
from bokeh.plotting import figure, show, output_file
import pdb
from bokeh.models import HoverTool
import london_postcodes as lp
import fciUtils


london_p = lp.data.copy()
fci = fciUtils.data


postcode_xs = [london_p[name]["lons"] for name in london_p]
postcode_ys = [london_p[name]["lats"] for name in london_p]

colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

postcode_colours = []

for name in london_p:
    try:
        fci_value = float(fci[name])
        idx = int(fci_value/20)
        postcode_colours.append(colors[idx])
    except KeyError:
        postcode_colours.append("black")


output_file("static/london_fci.html", title="mapexample")

p = figure(title="fci 2015", toolbar_location="left", plot_width=1100, plot_height=700)

p.patches(postcode_xs, postcode_ys, fill_color=postcode_colours, fill_alpha=0.7, line_color="#884444", line_width=2)

show(p)