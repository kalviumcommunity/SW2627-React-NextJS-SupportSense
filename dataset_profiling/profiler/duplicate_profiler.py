"""
Duplicate Profiler
Analyzes a dataset for exact duplicate rows.
"""

from typing import Dict, Any
import pandas as pd
from dataset_profiling.config.settings import SETTINGS
from dataset_profiling.utils.logger import get_logger

logger = get_logger(__name__)

class DuplicateProfiler:
    """Class to profile exact duplicate rows in a dataset."""

    @staticmethod
    def profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Profiles the dataset for exact duplicate rows.
        
        Args:
            df (pd.DataFrame): The dataset to profile.
            
        Returns:
            Dict[str, Any]: A dictionary containing duplicate analysis results.
        """
        logger.info("Starting Duplicate Profiling...")
        
        total_rows = len(df)
        results: Dict[str, Any] = {
            "exact_duplicate_rows": 0,
            "duplicate_percentage": 0.0,
            "duplicate_samples": [],
            "exceeds_threshold": False
        }
        
        if total_rows == 0:
            logger.warning("Empty dataframe provided to DuplicateProfiler.")
            return results
            
        duplicate_mask = df.duplicated(keep=False)
        duplicate_rows = df[duplicate_mask]
        
        # Calculate exact number of duplicate records (all occurrences of a duplicate)
        # Or, we can just calculate the number of duplicated rows (keeping the first)
        exact_duplicates = df.duplicated(keep='first').sum()
        
        if exact_duplicates > 0:
            percentage = (exact_duplicates / total_rows) * 100
            
            # Fetch a sample of duplicates. Group by all columns and take head
            sample_df = df[df.duplicated(keep='first')].head(SETTINGS.MAX_DUPLICATE_SAMPLES)
            # Replace NaNs with None for JSON serialization
            sample_df = sample_df.where(pd.notnull(sample_df), None)
            samples = sample_df.to_dict(orient="records")
            
            results["exact_duplicate_rows"] = int(exact_duplicates)
            results["duplicate_percentage"] = round(percentage, 2)
            results["duplicate_samples"] = samples
            
            if percentage > SETTINGS.DUPLICATE_THRESHOLD:
                results["exceeds_threshold"] = True
                
        logger.info(f"Duplicate Profiling completed. Found {results['exact_duplicate_rows']} duplicate rows.")
        return results
