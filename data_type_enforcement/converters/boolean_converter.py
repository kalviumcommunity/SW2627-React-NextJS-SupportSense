import pandas as pd
from data_type_enforcement.config.settings import BOOLEAN_MAPPING
from data_type_enforcement.utils.logger import setup_logger

logger = setup_logger(__name__)

def convert_to_boolean(series: pd.Series) -> pd.Series:
    """
    Converts a pandas Series to boolean dtype based on predefined mappings.
    Handles various truthy/falsy representations.
    Unmapped values will become NaN/pd.NA if they can't be coerced.
    """
    logger.info(f"Starting boolean conversion for column: '{series.name}'")
    
    # Fast path: already boolean
    if pd.api.types.is_bool_dtype(series):
        logger.info(f"Column '{series.name}' is already boolean.")
        return series

    try:
        # Convert to lowercase string for uniform mapping
        # Only stringify non-nulls for mapping
        mapped_series = series.map(
            lambda x: BOOLEAN_MAPPING.get(str(x).strip().lower(), pd.NA) if pd.notna(x) else pd.NA
        )
        
        # Cast to pandas boolean type (which supports pd.NA for missing values)
        converted = mapped_series.astype('boolean')
        logger.info(f"Successfully converted column '{series.name}' to boolean.")
        return converted
    except Exception as e:
        logger.error(f"Failed to convert column '{series.name}' to boolean: {str(e)}")
        # In case of catastrophic failure, return original (or let it fail)
        return series
