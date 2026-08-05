import pandas as pd
from typing import Dict, Any

from data_type_enforcement.converters.boolean_converter import convert_to_boolean
from data_type_enforcement.converters.currency_converter import convert_to_currency
from data_type_enforcement.converters.date_converter import convert_to_datetime
from data_type_enforcement.utils.logger import setup_logger

logger = setup_logger(__name__)

class DataTypeConverter:
    """
    Facade class that orchestrates the conversion of all columns in a DataFrame
    based on a provided Type Mapping Dictionary.
    """
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        
    def convert(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Safely converts every column in the dataframe according to the schema.
        Returns a new DataFrame with enforced types.
        """
        logger.info("Starting DataFrame type conversion process.")
        df_converted = df.copy()
        
        for column, config in self.schema.items():
            if column not in df_converted.columns:
                logger.warning(f"Column '{column}' is defined in schema but missing from DataFrame.")
                continue
                
            target_type = config.get("type", "string").lower()
            
            try:
                if target_type == "boolean":
                    df_converted[column] = convert_to_boolean(df_converted[column])
                elif target_type == "currency":
                    df_converted[column] = convert_to_currency(df_converted[column])
                elif target_type == "date":
                    date_format = config.get("format", None)
                    df_converted[column] = convert_to_datetime(df_converted[column], date_format)
                elif target_type == "int":
                    # Int64 supports nullable integers in pandas
                    df_converted[column] = pd.to_numeric(df_converted[column], errors='coerce').astype('Int64')
                    logger.info(f"Successfully converted column '{column}' to Int64.")
                elif target_type == "float":
                    df_converted[column] = pd.to_numeric(df_converted[column], errors='coerce').astype(float)
                    logger.info(f"Successfully converted column '{column}' to float.")
                elif target_type == "string":
                    df_converted[column] = df_converted[column].astype("string")
                    logger.info(f"Successfully converted column '{column}' to string.")
                else:
                    logger.warning(f"Unsupported target type '{target_type}' for column '{column}'. Skipping.")
            except Exception as e:
                logger.error(f"Unexpected error converting column '{column}' to '{target_type}': {str(e)}")

        logger.info("DataFrame type conversion process complete.")
        return df_converted
