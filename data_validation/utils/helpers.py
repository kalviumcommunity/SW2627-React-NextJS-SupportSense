from pathlib import Path
import pandas as pd
from data_validation.utils.exceptions import DatasetLoadError, EmptyDatasetError

def load_dataset(file_path: Path) -> pd.DataFrame:
    """
    Loads a dataset from the specified file path (supports CSV and Excel).
    Raises DatasetLoadError or EmptyDatasetError on failures.
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

def save_dataset(df: pd.DataFrame, file_path: Path) -> None:
    """
    Saves the dataset to the specified file path (supports CSV and Excel).
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.suffix.lower() == ".csv":
            df.to_csv(file_path, index=False)
        elif file_path.suffix.lower() in [".xlsx", ".xls"]:
            df.to_excel(file_path, index=False)
        else:
            raise DatasetLoadError(f"Unsupported save format: {file_path.suffix}. Only CSV and Excel are supported.")
    except Exception as e:
        raise DatasetLoadError(f"Failed to save dataset to {file_path}: {str(e)}")
