import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger("anomaly_detection.utils.helpers")

class DatasetLoadError(Exception):
    pass

class DataValidationError(Exception):
    pass

def load_and_validate_dataset(file_path: Path) -> pd.DataFrame:
    """
    Loads transaction data, validates structure, and ensures dates and amounts are correct.
    Excludes invalid rows and logs missing/corrupt values instead of silently failing or filling.
    """
    if not file_path.exists():
        raise DatasetLoadError(f"Dataset file not found: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise DatasetLoadError(f"Failed to read dataset: {str(e)}")

    if df.empty:
        raise DataValidationError("Dataset is empty.")

    if "date" not in df.columns:
        raise DataValidationError("Required column 'date' is missing.")
    if "amount" not in df.columns:
        raise DataValidationError("Required column 'amount' is missing.")

    initial_rows = len(df)
    
    # Safely parse date and amount, turning errors into NaNs
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Log exclusions
    missing_dates = df["date"].isna().sum()
    missing_amounts = df["amount"].isna().sum()
    
    if missing_dates > 0:
        logger.warning(f"Found {missing_dates} rows with missing or invalid dates. These will be excluded.")
    if missing_amounts > 0:
        logger.warning(f"Found {missing_amounts} rows with missing or non-numeric amounts. These will be excluded.")

    df_clean = df.dropna(subset=["date", "amount"]).copy()
    excluded = initial_rows - len(df_clean)
    
    if excluded > 0:
        logger.info(f"Excluded {excluded} rows due to missing/invalid values. {len(df_clean)} rows remaining.")

    if df_clean.empty:
        raise DataValidationError("Dataset is empty after removing invalid rows.")

    return df_clean
