# import geopandas as gpd
# import pandas as pd
# import json
# from bokeh.io import output_notebook, show, output_file, curdoc

# from bokeh.plotting import figure
# from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, Slider, HoverTool, WheelZoomTool
# from bokeh.palettes import brewer
# from bokeh.layouts import widgetbox, row, column
# shapefile = 'DEU_adm/DEU_adm1.shp'
# # Read shapefile using Geopandas
# gdf = gpd.read_file(shapefile)  # [['ADMIN', 'ADM0_A3', 'geometry']]
# # Rename columns.
# #gdf.columns = ['country', 'country_code', 'geometry']
# #gdf = gdf.drop(gdf.index[159])
# # print(gdf.columns)
# # print(gdf['geometry'])
# datafile = 'DEU_adm/DEU_adm1.csv'
# df = pd.read_csv(datafile, skiprows=1, names=['1','2','3','4','5','6','7','8','9','10'])
# print(df.head())
# # datafile = 'obese.csv'
# # # Read csv file using pandas
# # df = pd.read_csv(datafile, names=[
# #                  'entity', 'code', 'year', 'per_cent_obesity'], skiprows=1)
# # df_2016 = df[df['year'] == 2016]

# # merged = gdf.merge(df_2016, left_on='country_code',
# #                    right_on='code', how='left')
# # merged.fillna('No data', inplace=True)

# # merged_json = json.loads(merged.to_json())
# # json_data = json.dumps(merged_json)


# # # Input GeoJSON source that contains features for plotting.
# # geosource = GeoJSONDataSource(geojson=json_data)
# # # Define a sequential multi-hue color palette.
# # palette = brewer['YlGnBu'][8]
# # # Reverse color order so that dark blue is highest obesity.
# # palette = palette[::-1]
# # # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
# # color_mapper = LinearColorMapper(
# #     palette=palette, low=0, high=40, nan_color='#d9d9d9')
# # # Define custom tick labels for color bar.
# # tick_labels = {'0': '0%', '5': '5%', '10': '10%', '15': '15%',
# #                '20': '20%', '25': '25%', '30': '30%', '35': '35%', '40': '>40%'}
# # # Create color bar.
# # color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20,
# #                      border_line_color=None, location=(0, 0), orientation='horizontal', major_label_overrides=tick_labels)
# # # Create figure object.


# # p = figure(title='Share of adults who are obese, 2016', tooltips=None,
# #            width=1400, height=720, tools="pan,wheel_zoom", active_scroll="wheel_zoom")
# # p.grid.grid_line_color = None
# # p.background_fill_color = "#222222"
# # p.xgrid.grid_line_color = None
# # p.ygrid.grid_line_color = None
# # # Add patch renderer to figure.
# # p.toolbar.logo = None
# # p.toolbar_location = None
# # cr = p.patches('xs', 'ys', source=geosource, fill_color={'field': 'per_cent_obesity', 'transform': color_mapper},
# #                line_color='white', line_width=0.1, fill_alpha=1, hover_alpha=0.5, hover_fill_color="pink")
# # # Specify figure layout.
# # p.add_tools(HoverTool(tooltips=[
# #     ("Country", "@country"), ("per_cent_obesity", "@per_cent_obesity")], renderers=[cr]))


# # p.add_layout(color_bar, 'below')
# # # Display figure inline in Jupyter Notebook.

# # # Display figure.


# # x_start = 0
# # x_end = 0
# # y_start = 0
# # y_end = 0


# # # def get_x_range(attr, old, new):

# # #     x_end = new
# # #     update_pplot()


# # # def get_y_range(attr, old, new):

# # #     y_end = new
# # #     update_pplot()


# # # def update_pplot():
# # #     # if x_end < -40 and y_end < 80:
# # #     print(x_end, y_end)


# # # #p.x_range.on_change('start', get_x_range)
# # # p.x_range.on_change('end', get_x_range)
# # # # p.y_range.on_change('start', get_y_range)
# # # p.y_range.on_change('end', get_y_range)

# # # print(p.range)


# # def update_plot(attr, old, new):
# #     yr = slider.value
# #     df_2016 = df[df['year'] == int(yr)]

# #     merged = gdf.merge(df_2016, left_on='country_code',
# #                        right_on='code', how='left')
# #     merged.fillna('No data', inplace=True)

# #     merged_json = json.loads(merged.to_json())
# #     json_data = json.dumps(merged_json)

# #     new_data = json_data
# #     geosource.geojson = new_data
# #     p.title.text = str(p.x_range)


# # # Make a slider object: slider
# # slider = Slider(title='Year', start=1975, end=2016, step=1, value=2016)
# # slider.on_change('value', update_plot)
# # # Make a column layout of widgetbox(slider) and plot, and add it to the current document
# # layout = column(p, widgetbox(slider))
# # curdoc().add_root(layout)
# # show(p)

# # # from random import random

# # # from bokeh.layouts import column
# # # from bokeh.models import Button
# # # from bokeh.palettes import RdYlBu3
# # # from bokeh.plotting import figure, curdoc

# # # # create a plot and style its properties
# # # p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
# # # p.border_fill_color = 'black'
# # # p.background_fill_color = 'black'
# # # p.outline_line_color = None
# # # p.grid.grid_line_color = None

# # # # add a text renderer to our plot (no data yet)
# # # r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
# # #            text_baseline="middle", text_align="center")

# # # i = 0

# # # ds = r.data_source

# # # # create a callback that will add a number in a random location


# # # def callback():
# # #     global i

# # #     # BEST PRACTICE --- update .data in one step with a new dict
# # #     new_data = dict()
# # #     new_data['x'] = ds.data['x'] + [random() * 70 + 15]
# # #     new_data['y'] = ds.data['y'] + [random() * 70 + 15]
# # #     new_data['text_color'] = ds.data['text_color'] + [RdYlBu3[i % 3]]
# # #     new_data['text'] = ds.data['text'] + [str(i)]
# # #     ds.data = new_data

# # #     i = i + 1


# # # # add a button widget and configure with the call back
# # # button = Button(label="Press Me")
# # # button.on_click(callback)

# # # # put the button and plot in a layout and add to the document
# # # curdoc().add_root(column(button, p))


import numpy as np
np.random.seed(1)

from bokeh.layouts import row, column, gridplot
from bokeh.models import ColumnDataSource, Slider, Select
from bokeh.plotting import curdoc, figure
from bokeh.driving import count

MA12, MA26, EMA12, EMA26 = '12-tick Moving Avg', '26-tick Moving Avg', '12-tick EMA', '26-tick EMA'

source = ColumnDataSource(dict(
    time=[], average=[], low=[], high=[], open=[], close=[],
    ma=[], macd=[], macd9=[], macdh=[], color=[]
))

p = figure(plot_height=500, tools="xpan,xwheel_zoom,xbox_zoom,reset",
           x_axis_type=None, y_axis_location="right")
p.x_range.follow = "end"
p.x_range.follow_interval = 100
p.x_range.range_padding = 0

p.line(x='time', y='average', alpha=0.2,
       line_width=3, color='navy', source=source)
p.line(x='time', y='ma', alpha=0.8, line_width=2, color='orange', source=source)
p.segment(x0='time', y0='low', x1='time', y1='high',
          line_width=2, color='black', source=source)
p.segment(x0='time', y0='open', x1='time', y1='close',
          line_width=8, color='color', source=source)

p2 = figure(plot_height=250, x_range=p.x_range,
            tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="right")
p2.line(x='time', y='macd', color='red', source=source)
p2.line(x='time', y='macd9', color='blue', source=source)
p2.segment(x0='time', y0=0, x1='time', y1='macdh', line_width=6,
           color='black', alpha=0.5, source=source)

mean = Slider(title="mean", value=0, start=-0.01, end=0.01, step=0.001)
stddev = Slider(title="stddev", value=0.04, start=0.01, end=0.1, step=0.01)
mavg = Select(value=MA12, options=[MA12, MA26, EMA12, EMA26])


def _create_prices(t):
    last_average = 100 if t == 0 else source.data['average'][-1]
    returns = np.asarray(np.random.lognormal(mean.value, stddev.value, 1))
    average = last_average * np.cumprod(returns)
    high = average * np.exp(abs(np.random.gamma(1, 0.03, size=1)))
    low = average / np.exp(abs(np.random.gamma(1, 0.03, size=1)))
    delta = high - low
    open = low + delta * np.random.uniform(0.05, 0.95, size=1)
    close = low + delta * np.random.uniform(0.05, 0.95, size=1)
    return open[0], high[0], low[0], close[0], average[0]


def _moving_avg(prices, days=10):
    if len(prices) < days:
        return [100]
    return np.convolve(prices[-days:], np.ones(days, dtype=float), mode="valid") / days


def _ema(prices, days=10):
    if len(prices) < days or days < 2:
        return [prices[-1]]
    a = 2.0 / (days + 1)
    kernel = np.ones(days, dtype=float)
    kernel[1:] = 1 - a
    kernel = a * np.cumprod(kernel)
    # The 0.8647 normalizes out that we stop the EMA after a finite number of terms
    return np.convolve(prices[-days:], kernel, mode="valid") / (0.8647)


@count()
def update(t):
    open, high, low, close, average = _create_prices(t)
    color = "green" if open < close else "red"

    new_data = dict(
        time=[t],
        open=[open],
        high=[high],
        low=[low],
        close=[close],
        average=[average],
        color=[color],
    )

    close = source.data['close'] + [close]
    ma12 = _moving_avg(close[-12:], 12)[0]
    ma26 = _moving_avg(close[-26:], 26)[0]
    ema12 = _ema(close[-12:], 12)[0]
    ema26 = _ema(close[-26:], 26)[0]

    if mavg.value == MA12:
        new_data['ma'] = [ma12]
    elif mavg.value == MA26:
        new_data['ma'] = [ma26]
    elif mavg.value == EMA12:
        new_data['ma'] = [ema12]
    elif mavg.value == EMA26:
        new_data['ma'] = [ema26]

    macd = ema12 - ema26
    new_data['macd'] = [macd]

    macd_series = source.data['macd'] + [macd]
    macd9 = _ema(macd_series[-26:], 9)[0]
    new_data['macd9'] = [macd9]
    new_data['macdh'] = [macd - macd9]

    source.stream(new_data, 300)


curdoc().add_root(column(row(mean, stddev, mavg), gridplot(
    [[p], [p2]], toolbar_location="left", plot_width=1000)))
curdoc().add_periodic_callback(update, 50)
curdoc().title = "OHLC"
