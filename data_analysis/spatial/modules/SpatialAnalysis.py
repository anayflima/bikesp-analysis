from shapely.geometry import LineString
from shapely.geometry import MultiLineString
import sys
sys.path.insert(1, './data_analysis/spatial/modules/')
sys.path.insert(1, './spatial/modules/')
sys.path.insert(1, './modules/')

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