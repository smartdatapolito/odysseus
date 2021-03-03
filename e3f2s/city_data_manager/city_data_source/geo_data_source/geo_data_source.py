import os

import geopandas as gpd

from e3f2s.city_data_manager.config.config import data_paths_dict
from e3f2s.utils.path_utils import check_create_path


class GeoDataSource:

	def __init__(self, city_id, data_source_id):

		self.city_id = city_id
		self.data_source_id = data_source_id
		self.data_type_id = "geo"

		self.raw_data_path = os.path.join(
			data_paths_dict[self.city_id]["raw"][self.data_type_id],
			self.data_source_id,
		)

		self.norm_data_path = os.path.join(
			data_paths_dict[self.city_id]["norm"][self.data_type_id],
			self.data_source_id
		)
		check_create_path(self.norm_data_path)

		self.gdf = gpd.GeoDataFrame()
		self.gdf_norm = gpd.GeoDataFrame()

	def load_raw(self):
		return

	def load_norm(self):
		return
