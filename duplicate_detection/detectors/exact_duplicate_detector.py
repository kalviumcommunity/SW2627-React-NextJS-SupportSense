from typing import Any, Dict
import pandas as pd
from duplicate_detection.utils.logger import setup_logger
from duplicate_detection.utils.exceptions import EmptyDatasetError

logger = setup_logger(__name__)

class ExactDuplicateDetector:
    """
    Detects completely identical rows within a Pandas DataFrame.
    Provides metadata about duplicate counts, percentages, and sample records.
    """

    def detect(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyzes the DataFrame for exact duplicates.
        Returns a summary report dictionary containing:
          - duplicate_count: number of redundant rows
          - duplicate_percentage: percentage of redundant rows in the dataset
          - duplicate_samples: sample duplicate rows (first 10 records that have duplicates)
          - duplicate_indices: list of original indices that are redundant duplicates
        """
        logger.info("Starting exact duplicate detection process.")
        
        if df.empty:
            logger.warning("Empty DataFrame passed to ExactDuplicateDetector.")
            raise EmptyDatasetError("Cannot detect duplicates in an empty dataset.")

        # Find which indices are redundant (i.e. we keep first, and these are the duplicates to be dropped)
        redundant_mask = df.duplicated(keep="first")
        duplicate_indices = df.index[redundant_mask].tolist()
        duplicate_count = len(duplicate_indices)
        
        total_rows = len(df)
        duplicate_percentage = round((duplicate_count / total_rows) * 100, 2)
        
        # Find all occurrences of duplicates (including the first one) to show as samples
        all_duplicates_mask = df.duplicated(keep=False)
        duplicate_samples = df[all_duplicates_mask].head(10).to_dict(orient="records")
        
        logger.info(
            f"Exact duplicate detection completed. Found {duplicate_count} "
            f"redundant rows ({duplicate_percentage}% of total {total_rows} rows)."
        )
        
        return {
            "duplicate_count": duplicate_count,
            "duplicate_percentage": duplicate_percentage,
            "duplicate_samples": duplicate_samples,
            "duplicate_indices": duplicate_indices
        }
