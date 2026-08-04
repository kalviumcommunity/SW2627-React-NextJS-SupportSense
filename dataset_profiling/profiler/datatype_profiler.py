"""
Data Type Profiler
Analyzes column types, flags suspicious types, and checks expected vs. detected types.
"""

from typing import Dict, Any
import pandas as pd
from dataset_profiling.utils.logger import get_logger

logger = get_logger(__name__)

class DataTypeProfiler:
    """Class to profile data types of dataset columns."""

    @staticmethod
    def profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Profiles column data types and flags potential issues.
        
        Args:
            df (pd.DataFrame): The dataset to profile.
            
        Returns:
            Dict[str, Any]: A dictionary containing data type analysis results.
        """
        logger.info("Starting Data Type Profiling...")
        
        results: Dict[str, Any] = {
            "column_types": {},
            "suspicious_columns": []
        }
        
        if len(df) == 0:
            logger.warning("Empty dataframe provided to DataTypeProfiler.")
            return results
            
        for col in df.columns:
            detected_type = str(df[col].dtype)
            results["column_types"][col] = detected_type
            
            # Simple heuristic for suspicious columns
            suspicious = False
            reason = ""
            
            if detected_type == 'object':
                # Check if it could be numeric
                col_data = df[col].dropna()
                if not col_data.empty:
                    # Attempt to convert to numeric to see if it's stored as text
                    # We just take a small sample to speed it up
                    sample = col_data.head(100)
                    try:
                        pd.to_numeric(sample)
                        # If successful without error and not just empty
                        if not sample.empty:
                            suspicious = True
                            reason = "Numeric stored as object/string"
                    except ValueError:
                        pass
                        
                    # Check if it could be datetime
                    if not suspicious:
                        try:
                            # Try parsing with a strict format or standard format
                            pd.to_datetime(sample, format='mixed')
                            suspicious = True
                            reason = "Date stored as object/string"
                        except (ValueError, TypeError, Exception):
                            pass
                            
                    # Check if it could be boolean
                    if not suspicious:
                        unique_vals = set(sample.str.lower().unique() if sample.dtype == 'object' else sample.unique())
                        if unique_vals.issubset({"true", "false", "t", "f", "1", "0", "yes", "no", "y", "n"}):
                            suspicious = True
                            reason = "Boolean stored as text"

            if suspicious:
                results["suspicious_columns"].append({
                    "column": col,
                    "detected_type": detected_type,
                    "reason": reason
                })
                
        logger.info(f"Data Type Profiling completed. Found {len(results['suspicious_columns'])} suspicious columns.")
        return results
