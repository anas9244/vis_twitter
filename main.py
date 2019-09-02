
import pandas as pd
import geopandas as gpd
import json
from bokeh.io import curdoc, show
from bokeh.plotting import figure
from bokeh.models import Title, GeoJSONDataSource, LogColorMapper, LinearColorMapper, ColorBar, Slider, HoverTool
from bokeh.palettes import brewer
from bokeh.layouts import widgetbox, column
import os

fileDir = os.path.dirname(os.path.abspath(__file__)) + "/shape_files/"
lod_changed = True

shape_file = fileDir + 'ne_110m_admin_0_countries.shp'
shape_file_ger = fileDir + "us_states.shp"
datafile = 'obese.csv'


gdf_world = gpd.read_file(shape_file)[['ISO_A2', 'ADMIN', 'TYPE', 'geometry']]

gdf_ger = gpd.read_file(shape_file_ger)[['postal', 'name', 'type', 'geometry']]


gdf_world.columns = ['name', 'full_name', 'type', 'geometry']

gdf_ger.columns = ['name', 'full_name', 'type', 'geometry']

gdf_world = gdf_world.drop(gdf_world.index[159])

dataframesList = [gdf_ger, gdf_world]

rdf = gpd.GeoDataFrame(pd.concat(dataframesList, ignore_index=True))
rdf['count'] = 0
rdf.loc[rdf['name'] == 'DC', 'type'] = 'State'


country_rdf = rdf[rdf['type'] != 'State']
state_rdf = rdf[rdf['type'] == 'State']


country_json = json.loads(country_rdf.to_json())
country_data = json.dumps(country_json)

state_json = json.loads(state_rdf.to_json())
state_data = json.dumps(state_json)


geosource = GeoJSONDataSource(geojson=country_data)


palette = brewer['YlGnBu'][8]

palette = palette[::-1]

color_mapper = LinearColorMapper(
    palette=palette, low=0, high=1000)

tick_labels = {'0': '0', '125': '125', '250': '250', '375': '375',
               '500': '500', '625': '625', '750': '750', '875': '875', '1000': '>1000'}

color_bar = ColorBar(background_fill_color="#222222", color_mapper=color_mapper, label_standoff=8, width=600, height=20,
                     border_line_color=None, location='center', orientation='horizontal', major_label_overrides=tick_labels, major_label_text_color="white")


p = figure(title="Share of adults who are obese, 2016", tooltips=None,
           width=1400, height=720, tools="pan,wheel_zoom", active_scroll="wheel_zoom", title_location="above",)
p.title.align = "center"
p.grid.visible = False
p.toolbar.logo = None
p.toolbar_location = None
p.background_fill_color = "#2a2a2a"


cr = p.patches('xs', 'ys', source=geosource,
               line_color='#dedede', line_width=0.5, hover_fill_color="pink", hover_line_color="pink", fill_color={'field': 'count', 'transform': color_mapper})

p.add_tools(HoverTool(tooltips=[
    ("Name", "@full_name"), ("Num. of Tweets", "@count")], renderers=[cr]))
p.add_layout(color_bar, 'below')


# p.lod_factor = 10000


def update_lod(attr, new, old):

    global lod_changed
    #global gdf_world

    if new and old:
        if abs(p.x_range.start - p.x_range.end) < 140 and lod_changed:

            print("detail")

            geosource.geojson = state_data
            lod_changed = False

        elif abs(p.x_range.start - p.x_range.end) > 140 and not lod_changed:
            print("all")

            geosource.geojson = country_data
            lod_changed = True


p.x_range.on_change('end', update_lod)
layout = column(p)


curdoc().add_root(layout)

show(p)
