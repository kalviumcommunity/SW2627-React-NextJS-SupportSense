from pathlib import Path
import pandas as pd
import json
from typing import Dict, Any

class DatasetLoadError(Exception):
    """Raised when the dataset fails to load."""
    pass

class EmptyDatasetError(Exception):
    """Raised when the loaded dataset is empty."""
    pass

def load_dataset(file_path: Path) -> pd.DataFrame:
    """
    Loads a dataset from the specified file path (supports CSV and Excel).
    Raises EmptyDatasetError or DatasetLoadError on failures.
    """
    if not file_path.exists():
        raise DatasetLoadError(f"Dataset file not found: {file_path}")
    
    try:
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            raise DatasetLoadError(f"Unsupported file format: {file_path.suffix}. Only CSV and Excel are supported.")
    except Exception as e:
        raise DatasetLoadError(f"Failed to read dataset at {file_path}: {str(e)}")

    if df.empty:
        raise EmptyDatasetError(f"Loaded dataset at {file_path} is empty.")

    return df

def save_json(data: Dict[str, Any], file_path: Path) -> None:
    """
    Saves dictionary data to a JSON file safely.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
