import pandas as pd
from data_type_enforcement.utils.logger import setup_logger

logger = setup_logger(__name__)

def convert_to_datetime(series: pd.Series, format: str) -> pd.Series:
    """
    Converts string dates to datetime using an explicit format.
    Values that fail to parse will become NaT (Not a Time).
    """
    logger.info(f"Starting datetime conversion for column: '{series.name}' with format '{format}'")
    
    if pd.api.types.is_datetime64_any_dtype(series):
        logger.info(f"Column '{series.name}' is already datetime.")
        return series

    if not format:
        logger.warning(f"No explicit format provided for column '{series.name}'. Conversion might be ambiguous or fail.")
    
    try:
        # errors='coerce' turns unparseable values into NaT
        converted = pd.to_datetime(series, format=format, errors='coerce')
        
        # Check how many failed
        failed_count = converted.isna().sum() - series.isna().sum()
        if failed_count > 0:
            logger.warning(f"{failed_count} values in column '{series.name}' failed to parse as datetime with format '{format}'.")
            
        logger.info(f"Successfully converted column '{series.name}' to datetime.")
        return converted
    except Exception as e:
        logger.error(f"Failed to convert column '{series.name}' to datetime: {str(e)}")
        return series
