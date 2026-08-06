import json
from pathlib import Path
from typing import Any, Dict
import pandas as pd
from duplicate_detection.utils.logger import setup_logger
from duplicate_detection.utils.exceptions import EmptyDatasetError, DeduplicationError

logger = setup_logger(__name__)

def load_data(filepath: Path) -> pd.DataFrame:
    """
    Loads dataset from CSV, Excel, or JSON based on file extension.
    Verifies that the dataset is not empty.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset file not found: {filepath}")
        
    logger.info(f"Loading dataset from {filepath}...")
    try:
        suffix = filepath.suffix.lower()
        if suffix == '.csv':
            df = pd.read_csv(filepath)
        elif suffix in ['.xls', '.xlsx']:
            df = pd.read_excel(filepath)
        elif suffix == '.json':
            df = pd.read_json(filepath)
        else:
            raise DeduplicationError(f"Unsupported file format: {suffix}")
    except Exception as e:
        logger.error(f"Failed to read file {filepath}: {str(e)}")
        raise DeduplicationError(f"Failed to read file {filepath}: {str(e)}") from e

    if df.empty:
        raise EmptyDatasetError(f"The loaded dataset from {filepath} is empty (0 rows).")
        
    return df


def save_json(data: Dict[str, Any], filepath: Path) -> None:
    """
    Saves a dictionary to a JSON file.
    """
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Successfully saved JSON report to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save JSON report to {filepath}: {str(e)}")
        raise DeduplicationError(f"Failed to save JSON report: {str(e)}") from e


def save_csv(df: pd.DataFrame, filepath: Path) -> None:
    """
    Saves a pandas DataFrame to a CSV file.
    """
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath, index=False)
        logger.info(f"Successfully saved CSV dataset to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save CSV to {filepath}: {str(e)}")
        raise DeduplicationError(f"Failed to save CSV dataset: {str(e)}") from e
