from shapely.geometry import LineString
from shapely.geometry import MultiLineString
import sys
sys.path.insert(1, './data_analysis/spatial/modules/')
sys.path.insert(1, './spatial/modules/')
sys.path.insert(1, './modules/')
from BikeScience import BikeScience
import folium

class SpatialAnalysis:
    def __init__(self, geo_df, zone_origin_column, zone_destination_column, destination_folder_path):
        self.geo_df = geo_df
        self.zone_origin_column = zone_origin_column
        self.zone_destination_column = zone_destination_column
        self.destination_folder_path = destination_folder_path
    def extract_coords(self,row):
        if isinstance(row, LineString):
            return [(y, x) for x, y in list(row.coords)]
        if isinstance(row, MultiLineString):
            return [(y, x) for line in row.geoms for x, y in line.coords]
        return None
    
    def count_number_of_trips_in_each_zone(self, trips_df, expansion_factor = False):
        '''
            expansion faltor - False or a string containing the expansion factor
        '''
        if expansion_factor:
            number_trips = [trips_df[(trips_df[self.zone_origin_column] == zone_number) |
                                     ((trips_df[self.zone_destination_column] == zone_number))][expansion_factor].sum() for zone_number in self.geo_df['NumeroZona']]
        else:
            number_trips = [len(trips_df[(trips_df[self.zone_origin_column] == zone_number) |
                                         ((trips_df[self.zone_destination_column] == zone_number))]) for zone_number in self.geo_df['NumeroZona']]
        return number_trips

    def plot_map_for_each_social_class(self, df, social_class_column, classes_index_map, title, expansion_factor = False):
        bs = BikeScience()
        # for each social class, calculate the number of bike trips and save the fmap
        for key in classes_index_map.keys():
            column_name_class = 'number_' + title + '_trips_class_' + classes_index_map[key]
            df_class = df[df[social_class_column] == key]
            number_df_class = self.count_number_of_trips_in_each_zone(df_class, expansion_factor = expansion_factor)
            self.geo_df[column_name_class] = number_df_class

            fmap_class = bs.map_around_sp(the_grid = '', plot_grid=False, zoom = 11, north_offset=.12, east_offset=.4)

            bs.plot_zones(fmap_class, self.geo_df,column_name_class , 'Blues')

            fmap_class.save(self.destination_folder_path + column_name_class + '.html')


    def plot_map_for_each_social_class_single_map(self, df, social_class_column, classes_index_map, title, expansion_factor = False):
        bs = BikeScience()

        fmap = bs.map_around_sp(the_grid = '', plot_grid=False, zoom = 11, north_offset=.12, east_offset=.4)
        style_zones = lambda x: {'color': 'black', 'weight': 1, 'opacity': 0.3, 'fillOpacity': 0.1}

        folium.GeoJson(self.geo_df,
                style_function = style_zones,
                name='Zones', control=False).add_to(fmap)
        
        # for each social class, calculate the number of bike trips and add to the fmap
        for key in classes_index_map.keys():
            column_name_class = 'number_' + title + '_trips_class_' + classes_index_map[key]
            df_class = df[df[social_class_column] == key]
            number_df_class = self.count_number_of_trips_in_each_zone(df_class, expansion_factor = expansion_factor)
            self.geo_df[column_name_class] = number_df_class

            color =  'Blues'
            folium.Choropleth(
                geo_data=self.geo_df,
                data=self.geo_df,
                columns=['NumeroZona', column_name_class],
                key_on="feature.properties.NumeroZona",
                fill_color = color,
                fill_opacity = 1,
                line_opacity = 1,
                Highlight= True,
                line_color = "black",
                show=True,
                overlay=True,
                control=True,
                nan_fill_color = "Black",
                name='Social Class ' + classes_index_map[key],
                legend_name='Social Class ' + classes_index_map[key],
                zoom_control = False
            ).add_to(folium.FeatureGroup(name='Social Class ' + classes_index_map[key])).add_to(fmap)

        fmap.add_child(folium.LayerControl())


        fmap.save(self.destination_folder_path + 'number_' + title + '_trips_all_classes'+ '.html')

    
