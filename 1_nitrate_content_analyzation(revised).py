from bokeh.plotting import figure, ColumnDataSource, gmap
from bokeh.io import show, output_notebook
import pandas as pd
import numpy as np
from bokeh.models.widgets import Panel, Tabs, DataTable, DateFormatter, TableColumn
from bokeh.models import HoverTool, LabelSet, Label, GMapOptions
from bokeh.layouts import column, widgetbox, row, gridplot

def datetime(x):
    return np.array(x, dtype='datetime64[D]')

data1 = pd.read_csv('C:/Users/Always9/Desktop/Soil Samples/Data/Together.csv')
data1['Date'] = datetime(data1['Date'])

Apple = ['Top Right', 'Top Left', 'Bottom Right', 'Bottom Left']
Perl = ['Perl North', 'Perl South']
Hofer = ['Hofer West', 'Hofer Middle', 'Hofer East']

def get_data(location):
    return data1[(data1.Region == location)]

def get_source(data):
    name = data1[(data1.Area == data)]['Region'].iloc[0]
    new_data = get_data(name)
    condition = new_data[(new_data.Area == data)]
    x = condition['Date']
    y = condition['micro']
    z = condition['mg']
    horiba = condition['horiba']
    merck = condition['merck']
    color = condition['color']
    return {'x': x, 'y': y, 'z': z, 'horiba': horiba, 'merck': merck, 'color': color}

def make_plot(area):
    title_name = data1[(data1.Area == area[0])].Region.iloc[0]
    plot = figure(title='2018 ' + str(title_name) + ' Fields Nitrate Content',
                  x_axis_type="datetime", x_axis_label='Date', y_axis_label='Nitrate Content(μmol)',
                  plot_width=420, plot_height=400, y_range=(0, 2000), toolbar_location=None)
    for x in area:
        line_color = data1[(data1.Area == x)]['color'].iloc[0]
        source = ColumnDataSource(data=get_source(x))
        plot.line('x', 'y', color=line_color, legend=x, source=source)
        plot.circle('x', 'y', color='color', fill_color="white", source=source)
        labels = LabelSet(x="x", y="y", text="y", x_offset=5, y_offset=5, text_font_size="7pt",
                          text_color="#555555", source=source, text_align='center')
        plot.add_layout(labels)

    hover = HoverTool(tooltips=[('Date', '@x{%F}'), ("μmol", "@y{0,0.00}"),
                                ("mg/L", "@z"), ("Horiba", "@horiba"), ("Merck", "@merck")],
                      formatters={'x': 'datetime'})
    plot.add_tools(hover)
    plot.legend.location = 'top_right'
    return plot

def make_map(area, lat, lng, size):
    map_options = GMapOptions(lat=lat, lng=lng, map_type="satellite", zoom=size)
    data2 = data1[(data1.Region == area) & (data1.Date == data1[(data1.Region == area)].Date.unique()[0])]
    source = ColumnDataSource(data2)
    p_map = gmap("AIzaSyDzhOqlGE7EN2Vy9gy5JRbupJlCrcR09iU", map_options,
                 title=area + " Map" + ' (' + str(lat) + ', ' + str(lng) + ')', plot_width=300,
                 plot_height=400, toolbar_location=None)
    p_map.axis.visible = False
    color = data2.color[::-1]
    data3 = {'Apple': [[[15.711965, 15.713562, 15.713219, 15.712334, 15.712369, 15.711703],
                        [15.713568, 15.713822, 15.713044, 15.712171],
                        [15.713609, 15.714764, 15.714596, 15.713955, 15.713237],
                        [15.713650, 15.713846, 15.715750, 15.715557]],

                       [[47.223237, 47.223645, 47.225226, 47.224970, 47.224338, 47.223936],
                        [47.223570, 47.222634, 47.222503, 47.223248],
                        [47.223685, 47.223952, 47.224847, 47.225322, 47.225234],
                        [47.223588, 47.222628, 47.222990, 47.223961]]],

             'Hofer': [[[15.641922, 15.641447, 15.643072, 15.644024, 15.645142, 15.645208],
                        [15.645323, 15.646113, 15.649310, 15.647611, 15.647018],
                        [15.650919, 15.647627, 15.647918, 15.650740, 15.651293, 15.652723]],

                       [[47.158920, 47.158138, 47.157579, 47.157747, 47.157568, 47.157859],
                        [47.157523, 47.159077, 47.156907, 47.156023, 47.157243],
                        [47.158064, 47.155710, 47.154601, 47.156329, 47.155954, 47.156926]]],
             'Perl': [[[15.679830, 15.677504, 15.678461, 15.680532],
                       [15.680532, 15.681283, 15.684410, 15.683781]],

                      [[47.131326, 47.129918, 47.129489, 47.130734],
                       [47.131063, 47.130454, 47.132222, 47.132854]]]}

    for x, y, z in zip(data3[area][0], data3[area][1], color):
        p_map.patch(x, y, fill_color=z, fill_alpha=0.1, line_color=z)
        labels = LabelSet(x="lon", y="lat", text="Area", x_offset=3, y_offset=5, text_font_size="9pt",
                          text_color="white", source=source, text_align='center')
        p_map.add_layout(labels)
    return p_map

def make_hist(area, device, color, second_color):
    a = get_data(area)
    h = np.array(a[device], dtype=float)[~np.isnan(np.array(a[device]))]
    hist, edges = np.histogram(h, bins=9)
    p_hist = figure(title='The number of ' + device, x_axis_label=device,
                    y_axis_label='Count of ' + device, x_range=(-1, 11), plot_width=190,
                    plot_height=400)
    p_hist.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=color, line_color=color)
    average_h = float('{:01.2f}'.format(np.mean(h)))
    p_hist.line([average_h, average_h], [0, max(hist)],
                legend='Average = ' + str(average_h), color=second_color)
    p_hist = gridplot(p_hist, ncols=2, toolbar_location=None)
    return p_hist

def make_box(area):
    a = get_data(area)
    h = np.array(a['F(Horiba)'], dtype=float)[~np.isnan(np.array(a['F(Horiba)']))]
    m = np.array(a['F(Merck)'])[~np.isnan(np.array(a['F(Merck)']))]
    raw_data = {'device': ['Horiba', 'Merck'],
                'high': [max(h), max(m)],
                'low': [min(h), min(m)],
                'average': [float(x) for x in ['{:01.2f}'.format(y) for y in [np.mean(h), np.mean(m)]]],
                'color': ["#0d3362", "#c64737"],
                'text': ['Average of F(Horiba)', 'Average of F(Merck)'],
                'size': [np.mean(h) * 10, np.mean(m) * 10]}
    df = pd.DataFrame(raw_data, columns=['device', 'high', 'low', 'average', 'color', 'text', 'size'])
    source = ColumnDataSource(data=df)
    box = figure(title='Result differences based on Mobilab',
                 y_axis_label="Diference degree = F(x)",
                 x_axis_label='Devices', x_range=np.array(df.device), y_range=(-1, 20),
                 plot_width=340, plot_height=350, toolbar_location=None)
    box.grid.grid_line_alpha = 1
    box.segment('device', 'high', 'device', 'low', color='color', source=source)
    box.rect('device', 'low', 0.2, 0.01, line_color='color', source=source)
    box.rect('device', 'high', 0.2, 0.01, line_color='color', source=source)
    box.circle('device', 'average', size='size', color='color', source=source, legend='text')
    labels = LabelSet(x="device", y="average", text="average",
                      x_offset=0, y_offset=-4, text_font_size="7pt",
                      text_color="white", source=source, text_align='center')
    box.add_layout(labels)
    citation = Label(x=10, y=-60, x_units='screen', y_units='screen',
                     text="F(x)=|result from Mobilab-result from 'x'| Conclusion: Horiba is more similar than Merck",
                     render_mode='css',
                     border_line_color='white', border_line_alpha=1.0,
                     background_fill_color='white', background_fill_alpha=1.0)
    box.add_layout(citation)
    return box

def make_columns(name):
    new_data = get_data(name)
    source = ColumnDataSource(data=new_data)
    columns = [
        TableColumn(field="Area", title="Area"),
        TableColumn(field="Date", title="Date", formatter=DateFormatter()),
        TableColumn(field="micro", title="μmol"),
        TableColumn(field="mg", title="mg/L"),
        TableColumn(field="horiba", title="Horiba"),
        TableColumn(field="merck", title="Merck"),
        TableColumn(field="F(Horiba)", title="F(Horiba)"),
        TableColumn(field="F(Merck)", title="F(Merck)")]
    return DataTable(source=source, columns=columns, width=720, height=500)

A_hist = (row(make_hist('Apple', 'F(Horiba)', "#0d3362", '#A6CEE3'),
              make_hist('Apple', 'F(Merck)', "#c64737", '#FB9A99')))
H_hist = (row(make_hist('Hofer', 'F(Horiba)', "#0d3362", '#A6CEE3'),
              make_hist('Hofer', 'F(Merck)', "#c64737", '#FB9A99')))
P_hist = (row(make_hist('Perl', 'F(Horiba)', "#0d3362", '#A6CEE3'),
              make_hist('Perl', 'F(Merck)', "#c64737", '#FB9A99')))

p1 = column(row(make_plot(Apple), make_map('Apple', 47.223724, 15.713170, 16)),
            column(row(A_hist, make_box('Apple')), widgetbox(make_columns('Apple'))))
p2 = column(row(make_plot(Hofer), make_map('Hofer', 47.157594, 15.647279, 15)),
            column(row(H_hist, make_box('Hofer')), widgetbox(make_columns('Hofer'))))
p3 = column(row(make_plot(Perl), make_map('Perl', 47.130798, 15.680602, 15)),
            column(row(P_hist, make_box('Perl')), widgetbox(make_columns('Perl'))))

tab1 = Panel(child=p1, title='Apple Orchard')
tab2 = Panel(child=p2, title='Hofer')
tab2 = Panel(child=p2, title='Hofer')
tab2 = Panel(child=p2, title='Hofer')
tab3 = Panel(child=p3, title='Perl')

layout = Tabs(tabs=[tab1, tab2, tab3])
show(layout)