import geopandas as gpd
import os

if 'spatial' in os.getcwd():
    data_folder = '../../data/'
elif 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'infrastructure/'
destination_folder_path = data_folder + 'infrastructure/maps/'

zone_shp = gpd.read_file(source_folder_path + 'shapes/Zonas_2017_region.shp')
zone_shp.crs = {'init': 'epsg:31983'}  
zone_shp.to_crs(epsg='4326', inplace=True)

zone_shp_sp = zone_shp[zone_shp['NumeroMuni'] == 36]

cycle_paths = gpd.read_file(source_folder_path + 'shapes/CET/bikelanes.shp')

bus_lines = gpd.read_file(source_folder_path + 'LB15_MSP_CEM_V3/LB15_LI_MSP_CEM_V3.shp')

train_lines = gpd.read_file(source_folder_path + 'shapes/SIRGAS_SHP_linhatrem.shp')
train_lines.crs = {'init': 'epsg:31983'}  
train_lines.to_crs(epsg='4326', inplace=True)

subway_lines = gpd.read_file(source_folder_path + 'shapes/SIRGAS_SHP_linhametro_line.shp')
subway_lines.crs = {'init': 'epsg:31983'}
subway_lines.to_crs(epsg='4326', inplace=True)

from modules.SpatialAnalysis import SpatialAnalysis

sa = SpatialAnalysis(zone_shp_sp, 'zone_origin_column', 'zone_destination_column', destination_folder_path)

cycle_paths['coordinates'] = cycle_paths['geometry'].apply(sa.extract_coords)
bus_lines['coordinates'] = bus_lines['geometry'].apply(sa.extract_coords)
train_lines['coordinates'] = train_lines['geometry'].apply(sa.extract_coords)
subway_lines['coordinates'] = subway_lines['geometry'].apply(sa.extract_coords)

cycle_paths_coordinates = cycle_paths['coordinates'].explode().tolist()
train_coordinates = train_lines['coordinates'].explode().tolist()
subway_coordinates = subway_lines['coordinates'].explode().tolist()
bus_coordinates = bus_lines['coordinates'].explode().tolist()

train_and_subway = train_coordinates + subway_coordinates
public_transportation = train_coordinates + subway_coordinates + bus_coordinates
all_modes = public_transportation + cycle_paths_coordinates
train_subway_cycle_paths = train_and_subway + cycle_paths_coordinates


import folium

from modules.BikeScience import BikeScience

bs = BikeScience()

fmap = bs.map_around_sp(the_grid = '', plot_grid=False, zoom = 11, north_offset=.12, east_offset=.4)
style_zones = lambda x: {'color': 'black', 'weight': 1, 'opacity': 0.3, 'fillOpacity': 0.1}

folium.GeoJson(zone_shp_sp,
        style_function = style_zones,
        name='Zonas', control=False).add_to(fmap)

from folium.plugins import HeatMap

# gradient1 = {0.4: 'red', 0.65: 'purple', 1: 'blue'}
# gradient2 = {0.4: 'green', 0.65: 'orange', 1: 'yellow'}
# gradient3 = {0.4: 'pink', 0.65: 'brown', 1: 'grey'}

# gradient_1 = {0.0: 'blue', 0.2: 'cyan', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}
# gradient_2 = {0.0: 'purple', 0.2: 'indigo', 0.4: 'blue', 0.6: 'green', 0.8: 'yellow', 1: 'orange'}
# gradient_3 = {0.0: 'black', 0.2: 'brown', 0.4: 'red', 0.6: 'orange', 0.8: 'pink', 1: 'white'}
# gradient_4 = {0.0: 'black', 0.2: 'brown', 0.4: 'red', 0.6: 'orange', 0.8: 'yellow', 1: 'white'}

# gradient_1 = {0.0: 'blue', 0.1: 'cyan', 0.2: 'lime', 0.3: 'green', 0.4: 'yellow', 0.5: 'orange', 0.6: 'red', 0.7: 'brown', 0.8: 'purple', 0.9: 'pink', 1: 'white'}
# gradient_2 = {0.0: 'navy', 0.1: 'blue', 0.2: 'aqua', 0.3: 'teal', 0.4: 'olive', 0.5: 'green', 0.6: 'lime', 0.7: 'yellow', 0.8: 'orange', 0.9: 'red', 1: 'maroon'}
# gradient_3 = {0.0: 'black', 0.1: 'gray', 0.2: 'brown', 0.3: 'red', 0.4: 'orange', 0.5: 'yellow', 0.6: 'lime', 0.7: 'green', 0.8: 'aqua', 0.9: 'blue', 1: 'purple'}
# gradient_4 = {0.0: 'purple', 0.1: 'indigo', 0.2: 'blue', 0.3: 'aqua', 0.4: 'cyan', 0.5: 'green', 0.6: 'lime', 0.7: 'yellow', 0.8: 'orange', 0.9: 'red', 1: 'brown'}

# gradient_1 = {0.0: '#ffffe5', 0.1: '#f7fcb9', 0.2: '#d9f0a3', 0.3: '#addd8e', 0.4: '#78c679', 0.5: '#41ab5d', 0.6: '#238443', 0.7: '#006837', 0.8: '#004529', 0.9: '#2c7fb8', 1: '#253494'}
# gradient_2 = {0.0: '#f7f4f9', 0.1: '#e7e1ef', 0.2: '#d4b9da', 0.3: '#c994c7', 0.4: '#df65b0', 0.5: '#e7298a', 0.6: '#ce1256', 0.7: '#980043', 0.8: '#67001f', 0.9: '#4d004b', 1: '#3f007d'}
# gradient_3 = {0.0: '#f7fcf0', 0.1: '#e0f3db', 0.2: '#ccebc5', 0.3: '#a8ddb5', 0.4: '#7bccc4', 0.5: '#4eb3d3', 0.6: '#2b8cbe', 0.7: '#0868ac', 0.8: '#08589e', 0.9: '#084081', 1: '#08306b'}

gradient_1 = {0.0: '#ffffe5', 0.1: '#fff7bc', 0.2: '#fee391', 0.3: '#fec44f', 0.4: '#fe9929', 0.5: '#ec7014', 0.6: '#cc4c02', 0.7: '#993404', 0.8: '#662506', 0.9: '#3c1a02', 1: '#1a0d00'}
gradient_2 = {0.0: '#f7f4f9', 0.1: '#e7e1ef', 0.2: '#d4b9da', 0.3: '#c994c7', 0.4: '#df65b0', 0.5: '#e7298a', 0.6: '#ce1256', 0.7: '#980043', 0.8: '#67001f', 0.9: '#4d004b', 1: '#3f007d'}
gradient_3 = {0.0: '#f7fcf0', 0.1: '#e0f3db', 0.2: '#ccebc5', 0.3: '#a8ddb5', 0.4: '#7bccc4', 0.5: '#4eb3d3', 0.6: '#2b8cbe', 0.7: '#0868ac', 0.8: '#08589e', 0.9: '#084081', 1: '#08306b'}



HeatMap(bus_coordinates, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        gradient = gradient_1,
        ).add_to(folium.FeatureGroup(name='Bus lines').add_to(fmap))

HeatMap(train_coordinates, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        gradient = gradient_2,
        ).add_to(folium.FeatureGroup(name='Train lines').add_to(fmap))

HeatMap(subway_coordinates, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        gradient = gradient_3,
        ).add_to(folium.FeatureGroup(name='Subway lines').add_to(fmap))


# HeatMap(cycle_paths_coordinates, 
#         radius=12, 
#         blur=10, 
#         min_opacity=.2, 
#         # gradient = gradient
#         ).add_to(folium.FeatureGroup(name='Cycle Paths').add_to(fmap))

folium.LayerControl().add_to(fmap)

import branca.colormap as cm

colormap_1 = cm.StepColormap(colors=list(gradient_1.values()), index=list(gradient_1.keys()), vmin=0, vmax=1, caption='Gradient Bus lines')
colormap_2 = cm.StepColormap(colors=list(gradient_2.values()), index=list(gradient_2.keys()), vmin=0, vmax=1, caption='Gradient Train lines')
colormap_3 = cm.StepColormap(colors=list(gradient_3.values()), index=list(gradient_3.keys()), vmin=0, vmax=1, caption='Gradient Subway lines')
# colormap_4 = cm.StepColormap(colors=list(gradient_4.values()), index=list(gradient_4.keys()), vmin=0, vmax=1, caption='Gradient 4')

# Add the color maps to the map
fmap.add_child(colormap_1)
fmap.add_child(colormap_2)
fmap.add_child(colormap_3)
# fmap.add_child(colormap_4)

from branca.element import Figure
fig = Figure(width=800, height=1100)
fig.add_child(fmap)


fmap.save(destination_folder_path + "presentation/public_transportation_infrastructure_heatmap_scale_colors" + '.html')