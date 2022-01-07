import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import Select
from bokeh.layouts import column, row
from bokeh.models.widgets import Div
from bokeh.io import curdoc


# Import data
data = pd.read_csv('Semua/ANTM.csv', parse_dates=['date'])
# print(data.info())

# # Set axes
# x = data['date']
# y = data['close_price']

# Set output 
# output_file('index.html')

# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'x'             : data['date'],
    'y'             : data['close'],
    'open'          : data['open_price'],
    'first_trade'   : data['first_trade'],
    'high'          : data['high'],
    'low'           : data['low'],
    'close'         : data['close'],
    'volume'        : data['volume'],
    'frequency'     : data['frequency']
})

class Close_price : pass
close_price = Close_price()
close_price.highest_op = data['close'].max(),
close_price.lowest_op = data['close'].min()

# Create plot
# p = figure(
#     title='Stock Price',
#     plot_width = 800,
#     plot_height = 600,
#     x_axis_label='Date',
#     x_axis_type='datetime',
#     y_axis_label='Price'
# )
p = figure(
    title='Stock Price', 
    x_axis_label='Date',
    x_axis_type='datetime',
    y_axis_label='Price',
    plot_height=600, 
    plot_width=1200, 
    tools=[HoverTool(
        tooltips=[
            ("Datetime", "@x{%d-%m-%Y}"),
            ("Open", '@open'),
            ("High", "@high"),
            ("Low", "@low"),
            ("Close", "@close"),
            ("Volume", "@volume"),
            ("Frequency", "@frequency")
        ],
        formatters={
            "@x": 'datetime'
        }
    )])

# Add line glyph
p.line(
    x='x', 
    y='y', 
    source=source, 
    color='gray',
    line_width=2)

# Add a circle glyph to the figure p
p.circle(
    x='x', 
    y='y', 
    source=source, 
    fill_alpha=0.8,
    color='slateblue',
    # color=dict(field='region', transform=color_mapper), 
    legend='Close Price')

# Set the legend and axis attributes
p.legend.location = 'bottom_left'


# Define the callback function: update_plot
def update_plot(attr, old, new):
    # set the `yr` name to `slider.value` and `source.data = new_data`
    x = x_select.value
    y = y_select.value

    # Label axes of plot
    p.xaxis.axis_label = x
    p.yaxis.axis_label = y

    # new source
    new_source = pd.read_csv('Semua/'+y+'.csv', parse_dates=['date'])

    if (x == 'Latest week'):
        new_source = new_source.iloc[:7]
    elif (x == "Latest month"):
        new_source = new_source.iloc[:30]
    elif (x == "Latest 3 months"):
        new_source = new_source.iloc[:90]
    elif (x == "Latest 6 months"):
        new_source = new_source.iloc[:180]

    # print(new_source)

    # new data
    new_data = {
        'x'             : new_source['date'],
        'y'             : new_source['close'],
        'open'          : new_source['open_price'],
        'first_trade'   : new_source['first_trade'],
        'high'          : new_source['high'],
        'low'           : new_source['low'],
        'close'         : new_source['close'],
        'volume'         : new_source['volume'],
        'frequency'     : new_source['frequency']
    }
    source.data = new_data
    
    close_price.highest_op = new_source['close'].max()
    close_price.lowest_op = new_source['close'].min()

    # Add title to figure: plot.title.text
    p.title.text = y

    curdoc().add_next_tick_callback(refresh_div)


# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['All time', 'Latest week', 'Latest month', 'Latest 3 months', 'Latest 6 months'],
    value='All time',
    title='Time'
)
# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options = ['ANTM', 'BBNI', 'BBCA', 'BBRI', 'TLKM', 'UNVR', 'BMRI'],
    value = 'ANTM',
    title = 'Choose issuer'
)

# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)
    
div_title_highest = Div(text="""
    <p style="font-size:15px">Highest close price.</p>
    """, width=200, height=10)

div_highest = Div(text="""
    <b><p style="font-size:30px">Rp"""+str(close_price.highest_op)+"""</p><b>"""
    , width=200, height=10)

div_br = Div(text="""<br><br>""")

div_title_lowest = Div(text="""
    <p style="font-size:15px">Lowest close price.</p>
    """, width=200, height=10)

div_lowest = Div(text="""
    <b><p style="font-size:30px">Rp"""+str(close_price.lowest_op)+"""</p><b>"""
    , width=200, height=10)


def refresh_div():
    div_highest.text="""<b><p style="font-size:30px">Rp"""+str(close_price.highest_op)+"""</p><b>"""
    div_lowest.text="""<b><p style="font-size:30px">Rp"""+str(close_price.lowest_op)+"""</p><b>"""


# Create layout and add to current document
layout = row(
    column(
        x_select, 
        y_select, 
        div_title_highest,
        div_highest,
        div_br,
        div_title_lowest,
        div_lowest), 
p)
curdoc().add_root(layout)



# Show output
show(p)
# show(row(column(y_select, width=100), p))

# bokeh serve --show app.py
