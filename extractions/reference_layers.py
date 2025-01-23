reference_layers = [
    {
        "name": "aquifer_name",
        "url": "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Aquifers_Feature_Layer_view/FeatureServer/0",
        "extraction_method": "spatial_join_majority",
        "field": "AQ_NAME",
        "query": '1=1'
    },
    {
        "name": "ej_com",
        "url": "https://2nformspatial.com/server/rest/services/ESG_Publishing/FeatureServer/0",
        "extraction_method": "spatial_join_majority",
        "field": "cc",
        "query": '1=1'
    },
    {
        "name": "flood",
        "url": "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Flood_Hazard_Reduced_Set_gdb/FeatureServer/0",
        "extraction_method": "spatial_join_majority",
        "field": "esri_symbology",
        "query": '1=1'
    },
    # {
    #     "name": "svi",
    #     "url": "https://services3.arcgis.com/ZvidGQkLaDJxRSJ2/ArcGIS/rest/services/CDC_Social_Vulnerability_Index_2018/FeatureServer/2",
    #     "extraction_method": "spatial_join_majority",
    #     "field": "RPL_THEMES",
    #     "query": '1=1'
    # },
    {
        "name": "huc8_name",
        "url": "https://hydrowfs.nationalmap.gov/arcgis/rest/services/wbd/MapServer/4",
        "extraction_method": "spatial_join_majority",
        "field": "name"
    },
    {
        "name": "huc6_name",
        "url": "https://hydrowfs.nationalmap.gov/arcgis/rest/services/wbd/MapServer/3",
        "extraction_method": "spatial_join_majority",
        "field": "name"
    },
    {
        "name": "county",
        "url": "https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_Census_Counties/FeatureServer/0",
        "extraction_method": "attribute_join",
        "field": "NAME"
    },
    # @TODO: Add landuse layer back once we have a dissolved version
    # {
    #     "name": "landuse",
    #     "url": "https://2nformspatial.com/server/rest/services/telr_landuse/MapServer/0",
    #     "extraction_method": "spatial_join_majority",
    #     "field": "lu"
    # },
    # {
    #     "name": "imp_mean",
    #     "type": "image_server",
    #     "url": "https://landscape10.arcgis.com/arcgis/rest/services/USA_NLCD_Impervious_Surface_TimeSeries/ImageServer",
    #     "extraction_method": "zonal_stats",
    #     "fallback_method": "extract_center_point",
    #     "stat": "mean",
    #     "query": "Name = 'USA_NLCD_Impervious_2021'",
    #     "processing_template": None
    # },
    # {
    #     "name": "slope",
    #     "type": "image_server",
    #     "url": "https://elevation.arcgis.com/arcgis/rest/services/NED30m/ImageServer",
    #     "extraction_method": "zonal_stats",
    #     "fallback_method": "extract_center_point",
    #     "stat": "mean",
    #     "query": '1=1',
    #     "processing_template": "Slope_Percent"
    # },
    # {
    #     "name": "aspect",
    #     "url": "https://elevation.arcgis.com/arcgis/rest/services/NED30m/ImageServer",
    #     "extraction_method": "zonal_stats",
    #     "fallback_method": "extract_center_point",
    #     "stat": "mean",
    #     "query": '1=1',
    #     "processing_template": "Aspect"
    # },
    # {
    #     "name": "lithology",
    #     "url": "https://landscape6.arcgis.com/arcgis/rest/services/World_Lithology/ImageServer",
    #     "extraction_method": "zonal_stats",
    #     "fallback_method": "extract_center_point",
    #     "stat": "majority",
    #     "query": "Name = 'lithology'",
    #     "processing_template": None
    # },
    # {
    #     "name": "soil",
    #     "url": "https://2nformspatial.com/server/rest/services/telr_matrix_soils/ImageServer",
    #     "extraction_method": "zonal_stats",
    #     "fallback_method": "extract_center_point",
    #     "stat": "majority",
    #     "query": None,
    #     "processing_template": None
    # },
    # {
    #     "name": "avg_ppt",
    #     "url": "https://2nformspatial.com/server/rest/services/telrmatrix_ppt_meanannual_inches/ImageServer",
    #     "extraction_method": "extract_center_point",
    #     "field": "RASTERVALU",
    #     "query": "1=1",
    #     "processing_template": None
    # },
    # {
    #     "name": "p85_gcm_hist",
    #     "url": "https://2nformspatial.com/server/rest/services/p85_gcm_hist/ImageServer",
    #     "extraction_method": "extract_center_point",
    #     "field": "RASTERVALU",
    #     "query": None,
    #     "processing_template": None
    # },
    # {
    #     "name": "p85_gcm_2050",
    #     "url": "https://2nformspatial.com/server/rest/services/p85_gcm_2050/ImageServer",
    #     "extraction_method": "extract_center_point",
    #     "field": "RASTERVALU",
    #     "query": None,
    #     "processing_template": None
    # },
    # {
    #     "name": "design_storm_hist",
    #     "url": "https://2nformspatial.com/server/rest/services/p85_prism/ImageServer",
    #     "extraction_method": "extract_center_point",
    #     "field": "RASTERVALU",
    #     "query": None,
    #     "processing_template": None
    # },
    # {
    #     "name": "sea_rise_10ft",
    #     "url": "https://www.coast.noaa.gov/arcgis/rest/services/dc_slr/conf_10ft/MapServer/0",
    #     "extraction_method": "extract_center_point",
    #     "field": "RASTERVALU",
    #     "query": None,
    #     "processing_template": None
    # },
]
