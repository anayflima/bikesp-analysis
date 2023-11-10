import folium

'''
    The functions of the class BikeScience are originally from the BikeScience repository:

    https://gitlab.com/interscity/bike-science/-/tree/cycling-potential/sao-paulo/saopaulo

    The project Bike SP is part of the BikeScience group and thus has permission to use this code.

'''

class BikeScience():

    def __init__(self):
        self.SP_LAT = -23.5789
        self.SP_LON = -46.6388

    def map_around_sp(self, the_grid,zoom=12, plot_grid=True, 
                    style=lambda x: {'color': 'black', 'weight': 0.5, 'opacity': 0.3, 'fillOpacity': 0.0}, 
                    west_offset=-.3, east_offset=.3, north_offset=.3, south_offset=-.3):
        """
        Creates and returns a Folium map displaying the grid area.
        Parameters:
        zoom - zoom level of the map
        plot_grid - determines whether the grid must be plotted on the map
        style - a Folium style function for the grid look (see Folium docs)
        *_offset - map limits 
        """
        west_limit=self.SP_LON + west_offset
        east_limit=self.SP_LON + east_offset
        north_limit=self.SP_LAT + north_offset
        south_limit=self.SP_LAT + south_offset
        
        folium_map = folium.Map([(north_limit + south_limit) / 2, 
                                (west_limit + east_limit) / 2], 
                                control_scale = True,
                                min_lon = west_limit,
                                max_lon = east_limit,
                                zoom_start=zoom, tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', 
                                attr='&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>')
            
        if plot_grid:
            folium.GeoJson(the_grid.geodataframe().to_json(), name='grid', style_function=style).add_to(folium_map)
        
        return folium_map
    

    def plot_zones(self, fmap, geodf_zones, value_column, color, plot_rmsp = False):
        style_zones = lambda x: {'color': 'black', 'weight': 1, 'opacity': 0.3, 'fillOpacity': 0.1}
        folium.GeoJson(geodf_zones,
                    style_function = style_zones,
                    name='Zonas', control=False).add_to(fmap)
        data = geodf_zones
        if not plot_rmsp:
            data = data.loc[data['NumeroMuni'] == 36]

        folium.Choropleth(
            geo_data=data,
            data=data,
            columns=['NumeroZona', value_column],
            key_on="feature.properties.NumeroZona",
            fill_color = color,
            fill_opacity = 1,
            line_opacity = 1,
            Highlight= True,
            line_color = "black",
            show=True,
            overlay=True,
            control=False,
            nan_fill_color = "Black",
            zoom_control = False
            ).add_to(fmap)
    
    def plot_zones_tooltip(self, fmap, geodf, fields, aliases):
        """
            Function to set the tooltip (text that appear when the cursor is over)
            Fields are the collumns of the geodf to be written
            Aliases and fields must be in the same order 
        """
        
        tooltip_zona=folium.features.GeoJsonTooltip(
                            fields, aliases)
        folium.GeoJson(geodf,
                    style_function = lambda x : {'opacity': 0, 'fillOpacity': 0},
                    name = 'Detalhes da zona', control = True,
                    tooltip = tooltip_zona).add_to(fmap)