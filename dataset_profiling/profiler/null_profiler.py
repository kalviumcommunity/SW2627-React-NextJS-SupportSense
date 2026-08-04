"""
Null Profiler
Analyzes missing values per column, calculates percentages, and ranks them.
"""

from typing import Dict, Any, List
import pandas as pd
from dataset_profiling.config.settings import SETTINGS
from dataset_profiling.utils.logger import get_logger
from dataset_profiling.utils.helpers import safe_convert_to_native

logger = get_logger(__name__)

class NullProfiler:
    """Class to profile null/missing values in a dataset."""

    @staticmethod
    def profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Profiles the dataset for missing values.
        
        Args:
            df (pd.DataFrame): The dataset to profile.
            
        Returns:
            Dict[str, Any]: A dictionary containing null analysis results.
        """
        logger.info("Starting Null Profiling...")
        
        total_rows = len(df)
        null_counts = df.isnull().sum()
        
        results: Dict[str, Any] = {
            "columns_with_nulls": {},
            "total_null_cells": 0,
            "columns_exceeding_threshold": []
        }
        
        if total_rows == 0:
            logger.warning("Empty dataframe provided to NullProfiler.")
            return results
            
        for col, count in null_counts.items():
            count = safe_convert_to_native(count)
            if count > 0:
                percentage = (count / total_rows) * 100
                
                results["columns_with_nulls"][col] = {
                    "total_nulls": count,
                    "null_percentage": round(percentage, 2)
                }
                
                results["total_null_cells"] += count
                
                if percentage > SETTINGS.NULL_THRESHOLD:
                    results["columns_exceeding_threshold"].append(col)
                    
        # Sort columns by missing values (descending)
        results["columns_with_nulls"] = dict(
            sorted(
                results["columns_with_nulls"].items(),
                key=lambda item: item[1]["total_nulls"],
                reverse=True
            )
        )
        
        logger.info(f"Null Profiling completed. Found {len(results['columns_with_nulls'])} columns with missing values.")
        return results
