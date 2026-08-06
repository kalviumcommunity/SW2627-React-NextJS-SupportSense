from typing import Any, Dict, List
import pandas as pd
from duplicate_detection.utils.logger import setup_logger
from duplicate_detection.utils.exceptions import EmptyDatasetError, MissingColumnError

logger = setup_logger(__name__)

class NearDuplicateDetector:
    """
    Detects near-duplicates in a Pandas DataFrame based on configured key columns.
    Groups duplicate records and generates metadata report containing key-value pairs of duplicate groups.
    """

    def __init__(self, key_columns: List[str]):
        """
        Initializes the detector with a list of duplicate key columns.
        """
        if not key_columns:
            raise ValueError("key_columns list cannot be empty.")
        self.key_columns = key_columns

    def detect(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Groups DataFrame by duplicate keys and identifies duplicates (groups with size > 1).
        Returns a dictionary containing:
          - duplicate_groups: details of duplicate groups with keys and indices
          - total_near_duplicates: count of redundant rows that could be removed
          - duplicate_percentage: percentage of redundant rows
          - duplicate_indices: list of all indices belonging to duplicate groups (excluding the first one in each group)
        """
        logger.info(f"Starting near duplicate detection on keys: {self.key_columns}")
        
        if df.empty:
            logger.warning("Empty DataFrame passed to NearDuplicateDetector.")
            raise EmptyDatasetError("Cannot detect duplicates in an empty dataset.")

        # Check that all configured key columns exist in the DataFrame
        missing_cols = [col for col in self.key_columns if col not in df.columns]
        if missing_cols:
            error_msg = f"Key columns missing from dataset: {missing_cols}"
            logger.error(error_msg)
            raise MissingColumnError(error_msg)

        # Find duplicate rows on key columns
        # To group duplicates, we find all rows that have duplicate keys
        duplicate_mask = df.duplicated(subset=self.key_columns, keep=False)
        df_duplicates = df[duplicate_mask]
        
        duplicate_groups_report = []
        redundant_indices = []
        total_near_duplicates = 0
        
        if not df_duplicates.empty:
            # Group by key columns
            grouped = df_duplicates.groupby(self.key_columns, dropna=False)
            
            for keys, group in grouped:
                indices = group.index.tolist()
                count = len(indices)
                
                # Format key representation for report
                key_dict = {}
                if len(self.key_columns) == 1:
                    key_dict[self.key_columns[0]] = keys
                else:
                    for col, val in zip(self.key_columns, keys):
                        # Convert float/numpy values to standard Python types for JSON compatibility
                        if pd.isna(val):
                            key_dict[col] = None
                        elif hasattr(val, "item"):
                            key_dict[col] = val.item()
                        else:
                            key_dict[col] = val
                            
                duplicate_groups_report.append({
                    "keys": key_dict,
                    "indices": indices,
                    "count": count
                })
                
                # The first item in the group index is kept, the rest are redundant
                redundant_indices.extend(indices[1:])
                total_near_duplicates += (count - 1)

        total_rows = len(df)
        duplicate_percentage = round((total_near_duplicates / total_rows) * 100, 2)
        
        logger.info(
            f"Near duplicate detection completed. Found {len(duplicate_groups_report)} duplicate groups "
            f"representing {total_near_duplicates} redundant rows ({duplicate_percentage}% of total {total_rows} rows)."
        )
        
        return {
            "duplicate_groups": duplicate_groups_report,
            "total_near_duplicates": total_near_duplicates,
            "duplicate_percentage": duplicate_percentage,
            "duplicate_indices": redundant_indices
        }
