
import pandas as pd
import geopandas as gpd
import json
from bokeh.io import curdoc, show
from bokeh.plotting import figure
from bokeh.models import Title, GeoJSONDataSource, LogColorMapper, LinearColorMapper, ColorBar, Slider, HoverTool
from bokeh.palettes import brewer
from bokeh.layouts import widgetbox, column, row
from bokeh.models.widgets import Button, TextInput
import os
import pickle
import Stream


fileDir = os.path.dirname(os.path.abspath(__file__)) + "/shape_files/"
lod_changed = True

shape_file = fileDir + 'ne_110m_admin_0_countries.shp'
shape_file_states = fileDir + "us_states.shp"
datafile = 'obese.csv'


gdf_country = gpd.read_file(
    shape_file)[['ISO_A2', 'ADMIN', 'TYPE', 'geometry']]

gdf_state = gpd.read_file(shape_file_states)[
    ['postal', 'name', 'type', 'geometry']]


gdf_country.columns = ['name', 'full_name', 'type', 'geometry']
gdf_state.columns = ['name', 'full_name', 'type', 'geometry']

gdf_country = gdf_country.drop(gdf_country.index[159])

dataframesList = [gdf_state, gdf_country]

rdf = gpd.GeoDataFrame(pd.concat(dataframesList, ignore_index=True))
rdf['count'] = 0
rdf['flash'] = 0
rdf.loc[rdf['name'] == 'DC', 'type'] = 'State'

rdf.loc[rdf['type'] != 'State', 'name'] += '_c'


country_rdf = rdf[rdf['type'] != 'State']
state_rdf = rdf[rdf['type'] == 'State']

country_data = json.dumps(json.loads(country_rdf.to_json()))
state_data = json.dumps(json.loads(state_rdf.to_json()))


geosource = GeoJSONDataSource(geojson=country_data)


# palette = brewer['YlGnBu'][8]

# palette = palette[::-1]


palette = ['#293238', '#245472', '#3684b1', '#4e9bc9',
           '#78b3d6', '#aacfe6', '#d7e8f2', '#ffffff']
color_mapper = LinearColorMapper(
    palette=palette, low=0, high=8)


palette_flash = ['#254a60', '#ffffff']
color_mapper_flash = LinearColorMapper(
    palette=palette_flash, low=0, high=1)

tick_labels = {'0': '0', '1': '1', '2': '2', '3': '3',
               '4': '4', '5': '5', '6': '6', '7': '7', '8': '>8'}

color_bar = ColorBar(background_fill_color="#222222", color_mapper=color_mapper, label_standoff=5, width=600, height=20,
                     border_line_color=None, location='center', orientation='horizontal', major_label_overrides=tick_labels, major_label_text_color="white")


p = figure(tooltips=None,
           width=1500, height=720, tools="pan,wheel_zoom", active_scroll="wheel_zoom", title_location="above")

p.grid.visible = False
p.toolbar.logo = None
p.xaxis.visible = False
p.yaxis.visible = False
p.toolbar_location = None
p.background_fill_color = "#2a2a2a"


cr = p.patches('xs', 'ys', source=geosource,
               line_color={'field': 'flash', 'transform': color_mapper_flash}, line_width=0.9, hover_fill_color={'field': 'count', 'transform': color_mapper}, hover_line_color="white", fill_color={'field': 'count', 'transform': color_mapper})


p.add_tools(HoverTool(tooltips=[
    ("Name", "@full_name"), ("Num. of Tweets", "@count")], renderers=[cr]))
p.hover.point_policy = "follow_mouse"
p.add_layout(color_bar, 'below')


def update_lod(attr, new, old):

    global lod_changed
    # global gdf_world

    if new and old:
        if abs(p.x_range.start - p.x_range.end) < 120 and lod_changed:

            print("detail")

            color_mapper = LinearColorMapper(
                palette=palette, low=0, high=8)

            tick_labels = {'0': '0', '1': '1', '2': '2', '3': '3',
                           '4': '4', '5': '5', '6': '6', '7': '7', '8': '>8'}

            color_bar.color_mapper = color_mapper
            color_bar.major_label_overrides = tick_labels

            # state_rdf = rdf[rdf['type'] == 'State']
            rdf_us = rdf.drop(rdf.index[55])

            state_data = json.dumps(json.loads(rdf_us.to_json()))
            geosource.geojson = state_data
            lod_changed = False

        elif abs(p.x_range.start - p.x_range.end) > 130 and not lod_changed:
            print("all")

            color_mapper = LinearColorMapper(
                palette=palette, low=0, high=8)

            tick_labels = {'0': '0', '1': '1', '2': '2', '3': '3',
                           '4': '4', '5': '5', '6': '6', '7': '7', '8': '>8'}
            color_bar.color_mapper = color_mapper
            color_bar.major_label_overrides = tick_labels

            country_rdf = rdf[rdf['type'] != 'State']

            country_data = json.dumps(json.loads(country_rdf.to_json()))

            geosource.geojson = country_data
            lod_changed = True


straming = False


def start_button_click():

    # print("start")
    curdoc().add_periodic_callback(update_counts, 1000)
    Stream.start_streaming(text_input.value)
    global straming
    straming = True

    rdf['count'] = 0
    if lod_changed:

        country_rdf = rdf[rdf['type'] != 'State']

        country_data = json.dumps(json.loads(country_rdf.to_json()))

        geosource.geojson = country_data
    else:
        rdf_us = rdf.drop(rdf.index[55])

        state_data = json.dumps(json.loads(rdf_us.to_json()))
        geosource.geojson = state_data


def stop_button_click():

    print("stop")
    Stream.twitterStream.disconnect()
    global straming
    straming = False
    rdf['flash'] = 0


# def update_count():
    # start_button_click


p.x_range.on_change('end', update_lod)
start_button = Button(label="Start", button_type="primary", width=100)
start_button.on_click(start_button_click)
stop_button = Button(label="Stop", button_type="danger", width=100)
stop_button.on_click(stop_button_click)
text_input = TextInput(value="default", width=600)
layout = column(row(text_input, start_button, stop_button), p)


def update_counts():

    if straming:

        new_dict = Stream.get_counts()
        for index, place in enumerate(new_dict):
            if rdf.iloc[index]['count'] != new_dict[place]:
                rdf.loc[rdf['name'] == place, 'count'] = new_dict[place]
                rdf.loc[rdf['name'] == place, 'flash'] = 1

        if lod_changed:

            country_rdf = rdf[rdf['type'] != 'State']

            country_data = json.dumps(json.loads(country_rdf.to_json()))

            geosource.geojson = country_data

        else:
            rdf_us = rdf.drop(rdf.index[55])

            state_data = json.dumps(json.loads(rdf_us.to_json()))
            geosource.geojson = state_data


def flash():
    rdf['flash'] = 0


curdoc().add_periodic_callback(flash, 200)
curdoc().add_root(layout)

show(p)
