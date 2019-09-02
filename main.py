
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


gdf_world = gpd.read_file(shape_file)[['ADM0_A3', 'geometry']]
gdf_ger = gpd.read_file(shape_file_ger)[['name', 'geometry']]


gdf_world.columns = ['country_code', 'geometry']

gdf_ger.columns = ['country_code', 'geometry']

gdf_world = gdf_world.drop(gdf_world.index[159])


# df = pd.read_csv(datafile, names=[
#                  'entity', 'code', 'year', 'per_cent_obesity'], skiprows=1)


# #yr = selectedYear
# df_yr = df[df['year'] == 2016]
# merged = gdf_world.merge(gdf_ger, left_on='country_code',
#                          right_on='code', how='left')
# # merged.fillna('No data', inplace=True)
merged_json = json.loads(gdf_ger.to_json())
json_data = json.dumps(merged_json)


# def json_data(selectedYear):
#     yr = selectedYear
#     df_yr = df[df['year'] == yr]
#     merged = gdf.merge(df_yr, left_on='country_code',
#                        right_on='code', how='left')
#     # merged.fillna('No data', inplace=True)
#     merged_json = json.loads(merged.to_json())
#     json_data = json.dumps(merged_json)
#     return json_data


geosource = GeoJSONDataSource(geojson=json_data)


palette = brewer['YlGnBu'][8]

palette = palette[::-1]

color_mapper = LinearColorMapper(
    palette=palette, low=0, high=40)

tick_labels = {'0': '0%', '5': '5%', '10': '10%', '15': '15%',
               '20': '20%', '25': '25%', '30': '30%', '35': '35%', '40': '>40%'}

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
               line_color='#dedede', line_width=0.5, fill_alpha=1, hover_fill_color="pink", hover_line_color="pink")

# p.add_tools(HoverTool(tooltips=[
#     ("Country", "@country"), ("per_cent_obesity", "@per_cent_obesity")], renderers=[cr]))
p.add_layout(color_bar, 'below')


# p.lod_factor = 10000


def update_title(attr, new, old):

    global lod_changed
    global gdf_world

    if new and old:
        if abs(p.x_range.start - p.x_range.end) < 140 and lod_changed:

            print("detail")
            # gdf_world = gdf_world.drop(gdf_world.index[121])
            # gdf_world = gdf_world.drop(gdf_world.index[4])
            dataframesList = [gdf_ger, gdf_world]

            rdf = gpd.GeoDataFrame(
                pd.concat(dataframesList, ignore_index=True))
            merged_json = json.loads(rdf.to_json())
            json_data = json.dumps(merged_json)
            geosource.geojson = json_data

            lod_changed = False

        elif abs(p.x_range.start - p.x_range.end) > 140 and not lod_changed:
            print("all")
            merged_json = json.loads(gdf_world.to_json())
            json_data = json.dumps(merged_json)
            geosource.geojson = json_data
            lod_changed = True


#p.x_range.on_change('end', update_title)
layout = column(p)


curdoc().add_root(layout)

show(p)
