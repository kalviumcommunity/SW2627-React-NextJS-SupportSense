import pandas as pd
from typing import List, Tuple, Dict, Any

def validate_schema(df: pd.DataFrame, expected_columns: List[str]) -> Tuple[bool, Dict[str, Any]]:
    """
    Validates that the dataframe matches the expected schema.
    Detects missing and extra columns.
    
    Args:
        df (pd.DataFrame): The loaded dataset.
        expected_columns (List[str]): List of expected column names.
        
    Returns:
        Tuple[bool, Dict[str, Any]]: A boolean indicating if validation passed, 
        and a report dictionary containing missing and extra columns.
    """
    actual_columns = set(df.columns)
    expected_set = set(expected_columns)
    
    missing_columns = list(expected_set - actual_columns)
    extra_columns = list(actual_columns - expected_set)
    
    is_valid = len(missing_columns) == 0
    
    report = {
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "is_valid": is_valid
    }
    
    return is_valid, report
