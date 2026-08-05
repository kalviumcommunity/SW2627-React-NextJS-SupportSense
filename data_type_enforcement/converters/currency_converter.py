import pandas as pd
import re
from data_type_enforcement.config.settings import CURRENCY_SYMBOLS
from data_type_enforcement.utils.logger import setup_logger

logger = setup_logger(__name__)

def convert_to_currency(series: pd.Series) -> pd.Series:
    """
    Strips currency symbols, whitespace, and commas, then converts to float.
    Uses pd.to_numeric with errors='coerce' so invalid values become NaN.
    """
    logger.info(f"Starting currency conversion for column: '{series.name}'")
    
    if pd.api.types.is_numeric_dtype(series):
        logger.info(f"Column '{series.name}' is already numeric. Converting to float.")
        return series.astype(float)

    try:
        # Create a regex pattern to match any of the symbols, commas, or whitespace
        escaped_symbols = [re.escape(sym) for sym in CURRENCY_SYMBOLS]
        # Includes space, comma, and the specific symbols
        pattern = '|'.join(escaped_symbols + [r'\s+', ','])
        
        # Clean the string representations
        cleaned_series = series.astype(str).str.replace(pattern, '', regex=True)
        
        # Replace string representations of missing values like 'nan', 'None' back to actual NA before parsing
        cleaned_series = cleaned_series.replace(['nan', 'None', '<NA>'], pd.NA)
        
        # Convert to float
        converted = pd.to_numeric(cleaned_series, errors='coerce')
        logger.info(f"Successfully converted column '{series.name}' to currency (float).")
        return converted
    except Exception as e:
        logger.error(f"Failed to convert column '{series.name}' to currency: {str(e)}")
        return series
