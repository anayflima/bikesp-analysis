import geopandas as gpd
import os

if 'spatial' in os.getcwd():
    data_folder = '../../data/'
elif 'data_analysis' in os.getcwd():
    data_folder = '../data/'
else:
    data_folder = './data/'

source_folder_path = data_folder + 'infrastructure/'
destination_folder_path = data_folder + 'infrastructure/maps/social_class/'

zone_shp = gpd.read_file(source_folder_path + 'shapes/Zonas_2017_region.shp')
zone_shp.crs = {'init': 'epsg:31983'}  
zone_shp.to_crs(epsg='4326', inplace=True)

zone_shp_sp = zone_shp[zone_shp['NumeroMuni'] == 36]

import pandas as pd
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  # default='warn'
source_folder_path_od = data_folder + 'OD/OD_2017/'
filename = 'OD_2017_v1.csv'

trips = pd.read_csv(source_folder_path_od + filename, encoding = "ISO-8859-1", sep = ',')

expansion_factor_trip = 'FE_VIA'
expansion_factor_person = 'FE_PESS'
origin_column = 'MUNI_O'
destination_column = 'MUNI_D'
residence_column = 'MUNI_DOM'
city_code = 36
trips_sp = trips[(trips[origin_column] == city_code) & ((trips[destination_column] == city_code))]

zone_origin_column = 'ZONA_O'
zone_destination_column = 'ZONA_D'

trips_sp[zone_origin_column] = trips_sp[zone_origin_column].astype(int)
trips_sp[zone_destination_column] = trips_sp[zone_destination_column].astype(int)

mode_column = 'TIPVG'
bike_filter = 4
bike_trips = trips_sp[trips_sp[mode_column] == 4]


social_class_column = 'CRITERIOBR'
classes_index_map = {1: 'A', 2:'B1', 3:'B2', 4: 'C1', 5:'C2', 6:'D-E'}

from modules.BikeScience import BikeScience
from modules.SpatialAnalysis import SpatialAnalysis

bs = BikeScience()
sa = SpatialAnalysis(zone_shp_sp, zone_origin_column, zone_destination_column, destination_folder_path)


# To plot each social class trips on a different map (generate an HTML for each class)
sa.plot_map_for_each_social_class(bike_trips, social_class_column, classes_index_map, title = 'bike', expansion_factor = expansion_factor_trip)
sa.plot_map_for_each_social_class(bike_trips, social_class_column, classes_index_map, title = 'bike_without_expansion_factor', expansion_factor = False)
sa.plot_map_for_each_social_class(trips_sp, social_class_column, classes_index_map, title = 'all', expansion_factor = expansion_factor_trip)


# To generate a single HTML file with all social classes trips as feature groups
sa.plot_map_for_each_social_class_single_map(bike_trips, social_class_column, classes_index_map, title = 'bike', expansion_factor = expansion_factor_trip)
sa.plot_map_for_each_social_class_single_map(bike_trips, social_class_column, classes_index_map, title = 'bike_without_expansion_factor', expansion_factor = False)
sa.plot_map_for_each_social_class_single_map(trips_sp, social_class_column, classes_index_map, title = 'all', expansion_factor = expansion_factor_trip)




