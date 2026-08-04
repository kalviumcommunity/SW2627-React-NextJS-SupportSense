"""
Numerical Profiler
Calculates statistical metrics for numeric columns in a dataset.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np
from dataset_profiling.utils.logger import get_logger
from dataset_profiling.utils.helpers import safe_convert_to_native
from dataset_profiling.config.settings import SETTINGS

logger = get_logger(__name__)

class NumericalProfiler:
    """Class to profile numerical columns in a dataset."""

    @staticmethod
    def profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Profiles numerical columns for statistical metrics.
        
        Args:
            df (pd.DataFrame): The dataset to profile.
            
        Returns:
            Dict[str, Any]: A dictionary containing numerical analysis results.
        """
        logger.info("Starting Numerical Profiling...")
        
        results: Dict[str, Any] = {}
        
        if len(df) == 0:
            logger.warning("Empty dataframe provided to NumericalProfiler.")
            return results
            
        # Select numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        for col in numeric_df.columns:
            col_data = numeric_df[col].dropna()
            
            if col_data.empty:
                continue
                
            q1 = col_data.quantile(0.25)
            q3 = col_data.quantile(0.75)
            iqr = q3 - q1
            
            # Using safe_convert_to_native to ensure JSON serialization
            metrics = {
                "minimum": safe_convert_to_native(col_data.min()),
                "maximum": safe_convert_to_native(col_data.max()),
                "mean": safe_convert_to_native(col_data.mean()),
                "median": safe_convert_to_native(col_data.median()),
                "mode": safe_convert_to_native(col_data.mode().iloc[0]) if not col_data.mode().empty else None,
                "std_dev": safe_convert_to_native(col_data.std()),
                "variance": safe_convert_to_native(col_data.var()),
                "q1": safe_convert_to_native(q1),
                "q3": safe_convert_to_native(q3),
                "iqr": safe_convert_to_native(iqr),
                "skewness": safe_convert_to_native(col_data.skew()),
                "kurtosis": safe_convert_to_native(col_data.kurtosis()),
                "unique_values": safe_convert_to_native(col_data.nunique())
            }
            
            # Round float values for cleaner output
            for k, v in metrics.items():
                if isinstance(v, float) and pd.notna(v):
                    metrics[k] = round(v, 4)
                    
            results[col] = metrics
            
        logger.info(f"Numerical Profiling completed. Profiled {len(results)} numerical columns.")
        return results
