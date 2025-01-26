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
            self.ej_community_conversion(self.dirty_data)
            clean_df = self.dirty_data
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
    
    def map_name_to_full_name(self, df: pd.DataFrame) -> pd.DataFrame:
        name_mappings = extraction_constants.name_to_full_name
        df['name'] = df['name'].map(name_mappings)
        return df

    def format_df_to_dict(self, df: pd.DataFrame) -> dict:
        logging.info(df.to_dict(orient='records'))
        payload = df.to_dict(orient='records')

        if payload:
            payload[0] = {str(k): v for k, v in payload[0].items()}
        
        return payload[0]

