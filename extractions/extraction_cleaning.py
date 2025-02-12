import pandas as pd
import numpy as np
import logging
from extractions import extraction_constants


class ExtractionCleaning:
    def __init__(self, df: pd.DataFrame):
        self.dirty_data = df
        self.logger = logging.getLogger(__name__)

    def clean_data(self, bulk=False) -> pd.DataFrame:
        self.bulk = bulk
        try:
            self.soil_type_conversion(self.dirty_data)
            self.lithology_type_conversion(self.dirty_data)
            self.landcover_value_to_class(self.dirty_data)
            self.ej_community_conversion(self.dirty_data)
            clean_df = self.clean_and_classify_data(self.dirty_data)
            clean_df = clean_df.replace({np.nan: None})
            clean_spatial_ref_dict = self.format_df_to_dict(clean_df)
            return clean_spatial_ref_dict
        except Exception as e:
            if not self.bulk:
                raise e
            else:
                self.logger.error(e)

    def soil_type_conversion(self, df: pd.DataFrame) -> pd.DataFrame:
        df['soil'] = df['soil'].astype(int)
        df['soil'] = df['soil'].map(extraction_constants.soils_reclass_name)
        return df

    def lithology_type_conversion(self, df: pd.DataFrame) -> pd.DataFrame:
        df['lithology'] = df['lithology'].astype(int)
        df['lithology'] = df['lithology'].map(
            extraction_constants.lithology_reclass_name)
        return df

    def ej_community_conversion(self, df: pd.DataFrame) -> pd.DataFrame:
        df["ej_com"] = np.where(df["ej_com"] > 0, "yes", "no")
        return df

    def landcover_value_to_class(self, df: pd.DataFrame) -> pd.DataFrame:
        df['landcover'] = df['landcover'].astype(int)
        df['landcover'] = df['landcover'].map(
            extraction_constants.nlcd_classes)
        return df

    def map_name_to_full_name(self, df: pd.DataFrame) -> pd.DataFrame:
        name_mappings = extraction_constants.name_to_full_name
        df = df.rename(columns=name_mappings)
        return df

    def clean_and_classify_data(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Cleaning and classifying")
        df = df.map(lambda x: round(x, 2) if isinstance(
            x, (int, float, np.integer, np.floating)) else x)

        if 'aspect' in df.columns:
            df['aspect'] = df['aspect'].apply(self._aspect_to_direction)
        self.logger.info(df.head())
        return df

    def _aspect_to_direction(self, aspect):
        if pd.isnull(aspect):
            return np.nan
        directions = ['North', 'Northeast', 'East', 'Southeast',
                      'South', 'Southwest', 'West', 'Northwest']
        idx = int(((aspect + 22.5) % 360) / 45)
        return f"{directions[idx]} facing"

    def format_df_to_dict(self, df: pd.DataFrame) -> dict:
        payload = df.to_dict(orient='records')
        if payload:
            payload[0] = {str(k): v for k, v in payload[0].items()}
        categorized_data = self.format_extracted_data(payload[0])
        logging.info(categorized_data)
        return categorized_data

    def format_extracted_data(self, extracted_data):
        structured_data = {
            "Flood Risk & Water Management": {
                "Flood Hazard": extracted_data.get("flood"),
                "Avg Precipitation (inches)": extracted_data.get("avg_ppt"),
                "Extreme Rainfall Events (Historic)": extracted_data.get("p85_gcm_hist"),
                "Extreme Rainfall Events (2050 Projection)": extracted_data.get("p85_gcm_2050"),
            },
            "Urban Heat & Impervious Cover": {
                "Impervious Surface (%)": extracted_data.get("imp_mean"),
                "Slope (%)": extracted_data.get("slope"),
                "Aspect (Sun Exposure)": extracted_data.get("aspect"),
            },
            "Social & Environmental Factors": {
                "Social Vulnerability Index": extracted_data.get("svi"),
                "Environmental Justice Community": extracted_data.get("ej_com"),
                "County": extracted_data.get("county"),
            },
            "Soil & Geology": {
                "Soil Type": extracted_data.get("soil"),
                "Lithology": extracted_data.get("lithology"),
            },
            "Hydrology & Watershed": {
                "HUC 8 Watershed": extracted_data.get("huc8_name"),
                "HUC 6 Watershed": extracted_data.get("huc6_name"),
                "Aquifer Name": extracted_data.get("aquifer_name"),
            }
        }
        return structured_data
