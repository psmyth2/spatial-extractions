reference_layers = [
    {
        "name": "aquifer_name",
        "full_name": "Aquifer name",
        "url": "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Aquifers_Feature_Layer_view/FeatureServer/0",
        "extraction_method": "spatial_join_majority",
        "field": "AQ_NAME",
        "query": '1=1'
    },
    {
        "name": "ej_com",
        "full_name": "Environmental justice community",
        "url": "https://2nformspatial.com/server/rest/services/ESG_Publishing/FeatureServer/0",
        "extraction_method": "spatial_join_majority",
        "field": "cc",
        "query": '1=1'
    },
    {
        "name": "flood",
        "full_name": "Flood hazard type",
        "url": "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Flood_Hazard_Reduced_Set_gdb/FeatureServer/0",
        "extraction_method": "spatial_join_majority",
        "field": "esri_symbology",
        "query": '1=1'
    },
    {
        "name": "svi",
        "full_name": "Social vulnerability index",
        "url": "https://services3.arcgis.com/ZvidGQkLaDJxRSJ2/ArcGIS/rest/services/CDC_Social_Vulnerability_Index_2018/FeatureServer/2",
        "extraction_method": "spatial_join_majority",
        "field": "RPL_THEMES",
        "query": '1=1'
    },
    {
        "name": "huc8_name",
        "full_name": "HUC 8 name",
        "url": "https://hydrowfs.nationalmap.gov/arcgis/rest/services/wbd/MapServer/4",
        "extraction_method": "spatial_join_majority",
        "field": "name"
    },
    {
        "name": "huc6_name",
        "full_name": "HUC 6 name",
        "url": "https://hydrowfs.nationalmap.gov/arcgis/rest/services/wbd/MapServer/3",
        "extraction_method": "spatial_join_majority",
        "field": "name"
    },
    {
        "name": "county",
        "full_name": "County",
        "url": "https://services.arcgis.com/P3ePLMYs2RVChkJx/ArcGIS/rest/services/USA_Census_Counties/FeatureServer/0",
        "extraction_method": "attribute_join",
        "field": "NAME"
    },
    # @TODO: Add landcover layer back once we have a dissolved version
    # {
    #     "name": "landuse",
    #     "url": "https://2nformspatial.com/server/rest/services/telr_landuse/MapServer/0",
    #     "extraction_method": "spatial_join_majority",
    #     "field": "lu"
    # },
    {
        "name": "imp_mean",
        "full_name": "Percent impervious",
        "type": "image_server",
        "url": "https://landscape10.arcgis.com/arcgis/rest/services/USA_NLCD_Impervious_Surface_TimeSeries/ImageServer",
        "extraction_method": "zonal_stats",
        "fallback_method": "extract_center_point",
        "stat": "mean",
        "query": "Name = 'USA_NLCD_Impervious_2021'",
        "processing_template": None
    },
    {
        "name": "slope",
        "full_name": "Slope",
        "type": "image_server",
        "url": "https://elevation.arcgis.com/arcgis/rest/services/NED30m/ImageServer",
        "extraction_method": "zonal_stats",
        "fallback_method": "extract_center_point",
        "stat": "mean",
        "query": '1=1',
        "processing_template": "Slope_Percent"
    },
    {
        "name": "aspect",
        "full_name": "Aspect",
        "url": "https://elevation.arcgis.com/arcgis/rest/services/NED30m/ImageServer",
        "extraction_method": "zonal_stats",
        "fallback_method": "extract_center_point",
        "stat": "mean",
        "query": '1=1',
        "processing_template": "Aspect"
    },
    {
        "name": "lithology",
        "full_name": "Lithology type",
        "url": "https://landscape6.arcgis.com/arcgis/rest/services/World_Lithology/ImageServer",
        "extraction_method": "zonal_stats",
        "fallback_method": "extract_center_point",
        "stat": "majority",
        "query": "Name = 'lithology'",
        "processing_template": None
    },
    {
        "name": "soil",
        "full_name": "Soil type",
        "url": "https://2nformspatial.com/server/rest/services/telr_matrix_soils/ImageServer",
        "extraction_method": "zonal_stats",
        "fallback_method": "extract_center_point",
        "stat": "majority",
        "query": None,
        "processing_template": None
    },
    {
        "name": "avg_ppt",
        "full_name": "Average precipitation",
        "url": "https://2nformspatial.com/server/rest/services/telrmatrix_ppt_meanannual_inches/ImageServer",
        "extraction_method": "extract_center_point",
        "field": "RASTERVALU",
        "query": "1=1",
        "processing_template": None
    },
    {
        "name": "p85_gcm_hist",
        "full_name": "Precipitation in 85th percentile storm event (historical)",
        "url": "https://2nformspatial.com/server/rest/services/p85_gcm_hist/ImageServer",
        "extraction_method": "extract_center_point",
        "field": "RASTERVALU",
        "query": None,
        "processing_template": None
    },
    {
        "name": "p85_gcm_2050",
        "full_name": "Precipitation in 85th percentile storm event (2050)",
        "url": "https://2nformspatial.com/server/rest/services/p85_gcm_2050/ImageServer",
        "extraction_method": "extract_center_point",
        "field": "RASTERVALU",
        "query": None,
        "processing_template": None
    },
    {
        "name": "design_storm_hist",
        "full_name": "Historical design storm precipitation event",
        "url": "https://2nformspatial.com/server/rest/services/p85_prism/ImageServer",
        "extraction_method": "extract_center_point",
        "field": "RASTERVALU",
        "query": None,
        "processing_template": None
    },
    {
        "name": "sea_rise_10ft",
        "full_name": "Projected sea level rise",
        "url": "https://www.coast.noaa.gov/arcgis/rest/services/dc_slr/conf_10ft/MapServer/0",
        "extraction_method": "extract_center_point",
        "field": "RASTERVALU",
        "query": None,
        "processing_template": None
    },
]
