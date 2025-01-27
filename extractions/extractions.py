import logging
import os
import time
from arcgis.gis import GIS
from arcgis.raster import ImageryLayer
from arcgis.features import FeatureLayer
from arcgis.geometry.filters import intersects
import rasterio
import pandas as pd
import geopandas as gpd
import json
from rasterstats import zonal_stats
import tempfile
import common
from extractions import reference_layers


class Extractions:
    def __init__(self, gdf: gpd.GeoDataFrame):
        gdf.set_crs(epsg=4326, inplace=True)
        gdf["geometry"] = gdf["geometry"].buffer(
            0)  # Fix self-intersecting polygons
        self.gdf = gdf[~gdf["geometry"].is_empty & gdf["geometry"].notnull()]
        self.job_id = "001"  # make uuids
        self.logger = logging.getLogger(__name__)
        self.reference_layers = reference_layers.reference_layers
        self.geom_type = self.gdf.geom_type
        self.buffer = 0.01
        self.bulk = False
        self.config = common.get_config_parser()
        self.gis = common.connect_to_gis(
            self.config["agol"]["url"],
            self.config["agol"]["username"],
            self.config["agol"]["password"],
        )

    def extract_reference_layers(self):
        for layer in self.reference_layers:
            try:
                self.logger.info(
                    "Extracting reference layer: {}".format(layer["name"]))
                self.extract_reference_layer(layer)
            except Exception as e:
                self.logger.error(
                    "Error extracting reference layer: {} {}".format(layer["name"], e))
                if not self.bulk:
                    raise ValueError(e)
                else:
                    self.logger.error(e)
                    continue
        dirty_df = pd.DataFrame(self.gdf.drop(columns='geometry'))
        return dirty_df

    def extract_reference_layer(self, layer: dict):
        if layer["extraction_method"] == "zonal_stats":
            if self.geom_type.isin(['Polygon', 'MultiPolygon']).all():
                zonal_stats = getattr(self, layer["extraction_method"])
                return zonal_stats(layer)
            else:
                self.logger.info(
                    "Geometry type is not Polygon or MultiPolygon, using fallback method")
                extract_center_point = getattr(self, layer["fallback_method"])
                return extract_center_point(layer)
        elif layer["extraction_method"] == "extract_center_point":
            extract_center_point = getattr(self, layer["extraction_method"])
            return extract_center_point(layer)
        elif layer["extraction_method"] == "spatial_join_majority":
            spatial_join_majority = getattr(self, layer["extraction_method"])
            return spatial_join_majority(layer)
        elif layer["extraction_method"] == "attribute_join":
            attribute_join = getattr(self, layer["extraction_method"])
            return attribute_join(layer)
        else:
            self.logger.error("Extraction method not found: {}".format(
                layer["extraction_method"]))

    def attribute_join(self, layer):
        feature_layer = self.get_feature_layer_from_server(layer)
        if feature_layer is None:
            self.gdf[layer['name']] = None
            return self.gdf
        feature_df = feature_layer.df.drop(columns=['SHAPE'])

        if len(feature_df) > 1:
            self.logger.info(
                "More than one feature found in layer, selecting first feature")
            feature_df = feature_df.iloc[[0]]
        elif len(feature_df) == 0:
            self.gdf[layer['name']] = None
            return self.gdf

        feature_df.rename(
            columns={layer['field']: layer['name']}, inplace=True)
        attribute = feature_df[layer['name']].iloc[0]
        self.gdf[layer['name']] = attribute
        return self.gdf

    def spatial_join_majority(self, layer):
        feature_layer = self.get_feature_layer_from_server(layer)
        if feature_layer is None:
            self.gdf[layer['name']] = None
            return self.gdf
        feature_gdf = self.gdf_from_feature_layer(feature_layer, 4326)
        project_gdf = self.gdf.to_crs(epsg=4326)

        if len(feature_gdf) > 1:
            self.logger.info(
                "More than one feature found in layer, selecting majority intersection")
            feature_gdf = self.select_majority_intersection(
                feature_gdf, project_gdf)
        elif len(feature_gdf) == 0:
            self.gdf[layer['name']] = None
            return self.gdf

        joined_gdf = gpd.sjoin(project_gdf, feature_gdf,
                               how='left', predicate='intersects')
        joined_gdf.rename(
            columns={layer['field']: layer['name']}, inplace=True)
        self.gdf[layer['name']] = joined_gdf[layer['name']]
        return self.gdf

    def select_majority_intersection(self, feature_gdf, project_gdf):
        try:
            index_field = self._get_index_field(feature_gdf)
            intersection = gpd.overlay(
                project_gdf.to_crs(epsg=5070), feature_gdf.to_crs(epsg=5070), how='intersection')
            intersection['area'] = intersection.area
            intersection.set_index(index_field, inplace=True)
            majority_id = intersection.groupby(intersection.index)[
                'area'].sum().idxmax()
            feature_gdf = feature_gdf.set_index(index_field)
            return feature_gdf[feature_gdf.index == majority_id]
        except Exception as e:
            return feature_gdf

    def gdf_from_feature_layer(self, feature_layer, wkid):
        if feature_layer.features:
            geojson = feature_layer.to_geojson
            gdf = gpd.read_file(geojson)
            if gdf.geometry is None or gdf.geometry.is_empty.all():
                fixed_geojson = self._correct_multipolygon_nesting_as_string(
                    geojson)
                gdf = gpd.read_file(fixed_geojson)
            gdf = gdf.to_crs(epsg=wkid)
            return gdf
        else:
            return gpd.GeoDataFrame()

    def get_feature_layer_from_server(self, layer):
        feature_layer = FeatureLayer(layer['url'], self.gis)
        wkid = 4326
        try:
            project_gdf = self.gdf.to_crs(epsg=wkid)
            bounding_box = project_gdf.total_bounds
            bounding_box_dict = {
                "xmin": bounding_box[0], "ymin": bounding_box[1], "xmax": bounding_box[2], "ymax": bounding_box[3],
                "spatialReference": {"wkid": wkid}
            }
            query_filter = intersects(bounding_box_dict, sr=wkid)
            feature_layer = feature_layer.query(
                geometry_filter=query_filter, out_sr=wkid, out_fields=f"{layer['field']}")
            return feature_layer
        except Exception as e:
            self.logger.error(
                "Error processing layer {}: {}".format(layer['name'], str(e)))
            return None

    def zonal_stats(self, layer):
        image_info = self.get_image_from_server(layer)
        if image_info is None:
            self.gdf[layer['name']] = None
            return self.gdf
        image = image_info[0]
        project_gdf = image_info[1]
        stat = layer['stat']

        with rasterio.open(image) as src:
            affine_transform = src.transform
            stats = zonal_stats(project_gdf, src.read(
                1), affine=affine_transform, stats=stat)

        value = stats[0][stat]
        self.gdf[layer['name']] = value
        return value

    def extract_center_point(self, layer):
        image_info = self.get_image_from_server(layer)
        if image_info is None:
            self.gdf[layer['name']] = None
            return self.gdf
        image = image_info[0]
        project_gdf = image_info[1]
        project_gdf['centroid'] = project_gdf['geometry'].centroid
        point_coords = project_gdf['centroid'].iloc[0].coords[0]

        with rasterio.open(image) as src:
            affine_transform = src.transform
            row, col = src.index(point_coords[0], point_coords[1])
            value = src.read(1)[row, col]

        self.gdf[layer['name']] = value
        return value

    def get_image_from_server(self, layer):
        image_layer = ImageryLayer(layer['url'], self.gis)
        rendering_rule = {"rasterFunction": layer['processing_template']}
        try:
            metadata = image_layer.properties
            spatial_reference = metadata['spatialReference']
            lookup_wkid = self.wkid_lookup(spatial_reference)
            project_gdf = self.gdf.to_crs(epsg=lookup_wkid)
            self.logger.info(project_gdf.head())
            project_gdf['centroid'] = project_gdf['geometry'].centroid
            bounding_box = ','.join(map(str, project_gdf.total_bounds)) if project_gdf.geom_type.isin(['Polygon', 'MultiPolygon']).all(
            ) else self.get_bounding_box_from_lat_lon(project_gdf['centroid'].iloc[0].y, project_gdf['centroid'].iloc[0].x)
            self.logger.info(f"bounding box is: {bounding_box}")
            exported_image = image_layer.export_image(bbox=bounding_box,
                                                      bbox_sr=lookup_wkid,
                                                      image_sr=lookup_wkid,
                                                      rendering_rule=rendering_rule,
                                                      f='image',
                                                      save_folder=os.getcwd(),  # tempfile.gettempdir(),
                                                      save_file='temp_raster.tif',
                                                      export_format='tiff')
            return [exported_image, project_gdf]
        except Exception as e:
            self.logger.error(
                "Error processing layer {}: {}".format(layer['name'], str(e)))
            return None

    def wkid_lookup(self, spatial_reference):
        wkid = spatial_reference['wkid'] if 'wkid' in spatial_reference else spatial_reference['wkt']
        if wkid == 102008:
            return 5070
        elif 'NAD_1983_Albers' in str(wkid):
            return 5070
        else:
            return wkid

    def _correct_multipolygon_nesting_as_string(self, geojson_data):
        geojson_data = json.loads(geojson_data)
        for feature in geojson_data['features']:
            if feature['geometry']['type'] == 'MultiPolygon':
                corrected_coordinates = [feature['geometry']['coordinates']]
                feature['geometry']['coordinates'] = corrected_coordinates

        return json.dumps(geojson_data, indent=4)

    def _get_index_field(self, gdf):
        if 'objectid' in gdf.columns:
            return 'objectid'
        elif 'OBJECTID' in gdf.columns:
            return 'OBJECTID'
        else:
            gdf['objectid'] = gdf.index
            return 'objectid'

    def get_bounding_box_from_lat_lon(self, lat, lon):
        return f'{lon - self.buffer},{lat - self.buffer},{lon + self.buffer},{lat + self.buffer}'
