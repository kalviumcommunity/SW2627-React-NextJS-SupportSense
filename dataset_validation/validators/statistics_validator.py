import os
import pandas as pd
from pathlib import Path
from typing import Dict, Any

def calculate_statistics(file_path: Path, df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates basic statistics for a dataset.
    
    Args:
        file_path (Path): Path to the dataset file (to get size).
        df (pd.DataFrame): The loaded dataset.
        
    Returns:
        Dict[str, Any]: Dictionary containing dataset statistics.
    """
    try:
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = round(file_size_bytes / (1024 * 1024), 4)
        
        # Convert pandas dtypes to string representations
        dtypes_dict = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "file_size_mb": file_size_mb,
            "column_names": list(df.columns),
            "data_types": dtypes_dict
        }
    except Exception as e:
        return {
            "error": f"Failed to calculate statistics: {str(e)}"
        }
