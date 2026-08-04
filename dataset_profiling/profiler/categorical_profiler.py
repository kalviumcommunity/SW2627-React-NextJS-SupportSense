"""
Categorical Profiler
Calculates metrics like cardinality, frequencies, and top categories for categorical columns.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np
from dataset_profiling.utils.logger import get_logger
from dataset_profiling.utils.helpers import safe_convert_to_native
from dataset_profiling.config.settings import SETTINGS

logger = get_logger(__name__)

class CategoricalProfiler:
    """Class to profile categorical columns in a dataset."""

    @staticmethod
    def profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Profiles categorical columns for cardinality and frequencies.
        
        Args:
            df (pd.DataFrame): The dataset to profile.
            
        Returns:
            Dict[str, Any]: A dictionary containing categorical analysis results.
        """
        logger.info("Starting Categorical Profiling...")
        
        results: Dict[str, Any] = {}
        
        if len(df) == 0:
            logger.warning("Empty dataframe provided to CategoricalProfiler.")
            return results
            
        # Select non-numeric columns (object, category, bool)
        cat_df = df.select_dtypes(exclude=[np.number])
        
        for col in cat_df.columns:
            col_data = cat_df[col].dropna()
            
            if col_data.empty:
                continue
                
            unique_count = col_data.nunique()
            value_counts = col_data.value_counts()
            
            # Get top categories (up to 5)
            top_categories = {
                str(k): safe_convert_to_native(v) 
                for k, v in value_counts.head(5).items()
            }
            
            most_frequent = None
            least_frequent = None
            if not value_counts.empty:
                most_frequent = str(value_counts.index[0])
                least_frequent = str(value_counts.index[-1])
                
            is_high_cardinality = unique_count > SETTINGS.HIGH_CARDINALITY_THRESHOLD
            
            metrics = {
                "unique_values": safe_convert_to_native(unique_count),
                "cardinality": "High" if is_high_cardinality else "Low/Medium",
                "top_categories": top_categories,
                "most_frequent_value": most_frequent,
                "least_frequent_value": least_frequent,
                "is_constant": unique_count == 1
            }
            
            results[col] = metrics
            
        logger.info(f"Categorical Profiling completed. Profiled {len(results)} categorical columns.")
        return results
