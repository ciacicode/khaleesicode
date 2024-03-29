__author__ = 'ciacicode'

from collections import OrderedDict
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.embed import components
import csv
import london_postcodes as lp
from mysite.configs.khal_config import Config
from bs4 import BeautifulSoup

def create_chart_data():
    fci_data = {}

    with open(Config.FCICSVPATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ps = row['postcode']
            fci = row['fci']
            fci_data[str(ps)] = fci

    london_p = lp.data.copy()
    postcode_xs = [london_p[name]["lons"] for name in london_p]
    postcode_ys = [london_p[name]["lats"] for name in london_p]

    colors = ["#eaf9fd", "#c1edfa", "#99e1f7", "#70d5f4", "#47c9f1", "#33c3f0", "#2dafd8", "#2388a8", "#196178", "#0f3a48",
              "#0a2730"]

    postcode_name = []
    postcode_colours = []
    postcode_fci = []

    for name in london_p:
        parent = name[0]
        try:
            fci_value = float(fci_data[parent])
            idx = int(fci_value/10)
            postcode_colours.append(colors[idx])
            postcode_name.append(parent)
            postcode_fci.append(fci_value)
        except KeyError:
            idx = int(fci_value/10)
            postcode_colours.append(colors[idx])
            postcode_name.append(parent)
            postcode_fci.append(fci_value)


    source = ColumnDataSource(data=dict(x=postcode_xs, y=postcode_ys, color=postcode_colours, name=postcode_name,
                                        rate=postcode_fci,))

    TOOLS = "pan, wheel_zoom, box_zoom, reset, hover, save"

    p = figure(title="", toolbar_location="left", plot_width=800, plot_height=450, tools=TOOLS)

    p.patches('x', 'y', fill_color='color', fill_alpha=0.7, line_color="#884444", line_width=0.5, source=source)

    hover = p.select(dict(type=HoverTool))
    hover.point_policy = "follow_mouse"
    hover.tooltips = OrderedDict([("Name", "@name"), ("FCI", "@rate"), ("Long, Lat", "$x, $y"), ])
    script, div = components(p)
    return script, div

def save_chart(components):
#save div and script to files...
    with open(Config.FCICHART, 'w+') as c:
        c.write(components[0])
        c.write(components[1])

#open chart info and return script and div
def open_chart():
    """

    :return: script and div strings as tuple
    """
    with open(Config.FCICHART, 'r') as html:
        soup = BeautifulSoup(html, "lxml")
        script = soup.script
        div = soup.div
        return script, div