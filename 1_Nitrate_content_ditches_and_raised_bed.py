from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.plotting import figure, ColumnDataSource, gmap
from bokeh.io import show, output_notebook
import pandas as pd
import numpy as np
from bokeh.models.widgets import Panel, Tabs, DataTable, DateFormatter, TableColumn
from bokeh.models import HoverTool, LabelSet, Label, GMapOptions
from bokeh.layouts import column, widgetbox, row, gridplot
from bokeh.models import ColumnDataSource, Range1d, Plot, LinearAxis, Grid
from bokeh.models.glyphs import ImageURL


area = ['Hofer West', 'Hofer Middle', 'Hofer East']
years = ['Raised bed', 'Ditch']

data = {'area' : area,
        'Raised bed'   : [16, 11, 12],
        'Ditch'   : [19, 12, 18]
        }
source = ColumnDataSource(data=data)
p = figure(x_range=area, y_range=(0, 27), plot_height=300, plot_width=320, title="Comparison between Raised bed and Ditch",
           toolbar_location=None, tools="", y_axis_label='Nitrate Content(mg)')

p.vbar(x=dodge('area', -0.15, range=p.x_range), top='Raised bed', width=0.2, source=source,
       color="#e84d60", legend=value("Raised bed"))

p.vbar(x=dodge('area',  0.10,  range=p.x_range), top='Ditch', width=0.2, source=source,
       color="#718dbf", legend=value("Ditch"))

p.x_range.range_padding = 0.1
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

columns = [TableColumn(field="area", title="Area"),
           TableColumn(field="Raised bed", title="Raised bed(mg)"),
           TableColumn(field="Ditch", title="Ditch(mg)")]
data_table = DataTable(source=source, columns=columns, width=300, height=300)


url = "https://www.ces.ncsu.edu/wp-content/uploads/2013/07/DSC_0489.jpg"
source = ColumnDataSource(dict(
    url = [url]))

xdr = Range1d(start=0, end=300)
ydr = Range1d(start=0, end=300)
plot = Plot(
    title=None, x_range=xdr, y_range=ydr, plot_width=500, plot_height=420, toolbar_location=None)
image = ImageURL(url="url", w=300, h=300, anchor="bottom_left")
plot.add_glyph(source, image)

show(row(column(p, widgetbox(data_table)), plot))