"""
Helper functions for the Dataset Profiling Framework.
Includes common utilities for data manipulation, formatting, and file I/O.
"""

from typing import Union
import pandas as pd
import numpy as pd_np
import numpy as np

def format_memory_size(size_in_bytes: int) -> str:
    """
    Converts bytes into a human-readable string (KB, MB, GB, etc.).
    
    Args:
        size_in_bytes (int): Size in bytes.
        
    Returns:
        str: Human-readable memory size.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"

def safe_convert_to_native(value: any) -> any:
    """
    Safely converts numpy/pandas types to native Python types for JSON serialization.
    
    Args:
        value: Any value (could be np.int64, np.float64, pd.NA, etc.).
        
    Returns:
        Native Python type (int, float, str, None).
    """
    if pd.isna(value) or value is None:
        return None
    if isinstance(value, bool) or isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, int) or isinstance(value, (np.integer, np.int64, np.int32)):
        return int(value)
    if isinstance(value, float) or isinstance(value, (np.floating, np.float64, np.float32)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return str(value)
