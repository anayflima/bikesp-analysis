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

HeatMap(bus_coordinates, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        # gradient = gradient
        ).add_to(folium.FeatureGroup(name='Bus lines').add_to(fmap))

HeatMap(train_coordinates, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        # gradient = gradient
        ).add_to(folium.FeatureGroup(name='Train lines').add_to(fmap))

HeatMap(subway_coordinates, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        # gradient = gradient
        ).add_to(folium.FeatureGroup(name='Subway lines').add_to(fmap))

HeatMap(public_transportation, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        # gradient = gradient
        ).add_to(folium.FeatureGroup(name='Public Transportation').add_to(fmap))

HeatMap(cycle_paths_coordinates, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        # gradient = gradient
        ).add_to(folium.FeatureGroup(name='Cycle Paths').add_to(fmap))

HeatMap(all_modes, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        # gradient = gradient
        ).add_to(folium.FeatureGroup(name='All (public transportation + cycle paths)').add_to(fmap))

HeatMap(train_and_subway, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        # gradient = gradient
        ).add_to(folium.FeatureGroup(name='Train + subway').add_to(fmap))

HeatMap(train_subway_cycle_paths, 
        radius=12, 
        blur=10, 
        min_opacity=.2, 
        # gradient = gradient
        ).add_to(folium.FeatureGroup(name='Train + subway + cycle paths)').add_to(fmap))

folium.LayerControl().add_to(fmap)

from branca.element import Figure
fig = Figure(width=800, height=1100)
fig.add_child(fmap)


fmap.save(destination_folder_path + "mobility_infrastructure" + '.html')