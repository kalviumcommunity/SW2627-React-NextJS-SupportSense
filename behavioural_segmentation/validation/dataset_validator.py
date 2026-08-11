import logging
from typing import List
import pandas as pd

class MissingColumnError(Exception):
    """Raised when a required column is missing from the dataset."""
    pass

def validate_dataset(df: pd.DataFrame, segment_column: str, required_columns: List[str], logger: logging.Logger) -> None:
    """
    Validates that the dataset contains all required columns and the specified segmentation column.
    Raises MissingColumnError if validation fails.
    """
    logger.info(f"Validating dataset structure. Segment column: '{segment_column}'. Required core columns: {required_columns}")

    # Check segment column
    if segment_column not in df.columns:
        err_msg = f"Segmentation column '{segment_column}' is missing from the dataset."
        logger.error(err_msg)
        raise MissingColumnError(err_msg)

    # Check required core columns
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        err_msg = f"Required column(s) missing from dataset: {', '.join(missing)}"
        logger.error(err_msg)
        raise MissingColumnError(err_msg)
    
    logger.info("Dataset validation passed successfully.")
