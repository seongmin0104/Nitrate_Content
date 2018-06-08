from bokeh.plotting import figure, ColumnDataSource
from bokeh.io import show, output_file, curdoc
import pandas as pd
import numpy as np
from bokeh.models.widgets import Select, DataTable, DateFormatter, TableColumn, Panel, Tabs, CheckboxGroup
from bokeh.models import HoverTool, LabelSet
from bokeh.layouts import column, widgetbox
from bokeh.palettes import Spectral4
import webapp2
def datetime(x):
    return np.array(x, dtype='datetime64[D]')

df = pd.read_csv('C:/Users/Always9/Desktop/Soil Samples/Data/Together.csv')
df['Date'] = datetime(df['Date'])

def get_data(go):
    tf = df[df.Region == go]
    xs = list(tf[(tf.Area == r)]['Date'] for r in
              tf['Area'].unique().tolist())
    ys = list(tf[(tf.Area == r)]['Nitrate'] for r in
              tf['Area'].unique().tolist())
    color = Spectral4
    region = tf['Area'].unique().tolist()
    return {'xs': xs, 'ys': ys, 'color': color, 'region': region}

def new_data(gogo):
    tf = df[df.Region == gogo]
    x = tf['Date']
    y = tf['Nitrate']
    area = tf['Area']
    return {'x': x, 'y': y,'area':area}

source = ColumnDataSource(data=get_data('Apple'))
source1 = ColumnDataSource(data=new_data('Apple'))
p = figure(x_axis_type="datetime", x_axis_label='Date', y_axis_label='Nitrate Content(micromol)', plot_width=400,
              plot_height=400)
p.multi_line(xs="xs", ys="ys", line_width=1,line_color='color', legend = 'region', source= source)
p.circle(x = 'x', y = 'y', fill_color = 'white', line_color = 'black', line_alpha = 0.5 ,source= source1)
p.legend.location = 'top_right'

labels = LabelSet(x="x", y="y", text="y", x_offset=5, y_offset=5, text_font_size="7pt", text_color="#555555", source=source1, text_align='center')
p.add_layout(labels)


def callback(attr, old, new):
    source.data = get_data(select.value)
    source1.data = new_data(select.value)

select = Select(
    options=['Apple', 'Perl', 'Hofer'],
    value='Apple',
    title='Area')

select.on_change('value', callback)

columns = [
        TableColumn(field="area", title="Area"),
        TableColumn(field="x", title="Date", formatter=DateFormatter()),
        TableColumn(field="y", title="Nitrate"),
    ]
data_table = DataTable(source=source1, columns=columns, width=400, height=400)

layout1 = column(widgetbox(select), p)
layout2 = column(layout1,widgetbox(data_table))

curdoc().add_root(layout2)

app = webapp2.WSGIApplication([
    ('/', layout2),
], debug=True)








