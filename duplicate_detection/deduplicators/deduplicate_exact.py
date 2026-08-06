from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple
import pandas as pd
from duplicate_detection.utils.logger import setup_logger
from duplicate_detection.utils.exceptions import InvalidStrategyError, EmptyDatasetError
from duplicate_detection.config.settings import VALID_STRATEGIES

logger = setup_logger(__name__)

class ExactDeduplicator:
    """
    Deduplicates a Pandas DataFrame by removing completely identical rows.
    Supports strategies: keep_first, keep_last, keep_most_complete.
    Records an audit log of all removed records.
    """

    def __init__(self, strategy: str = "keep_first"):
        """
        Initializes the deduplicator with a selection strategy.
        """
        if strategy not in VALID_STRATEGIES:
            error_msg = f"Invalid strategy '{strategy}'. Allowed: {VALID_STRATEGIES}"
            logger.error(error_msg)
            raise InvalidStrategyError(error_msg)
        self.strategy = strategy

    def deduplicate(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict[str, Any]]]:
        """
        Removes exact duplicates from a DataFrame.
        Returns:
          - A new cleaned DataFrame (copy of the original).
          - A list of audit trail dictionaries for removed records.
        """
        logger.info(f"Executing exact deduplication using strategy: {self.strategy}")
        
        if df.empty:
            logger.warning("Empty DataFrame passed to ExactDeduplicator.")
            raise EmptyDatasetError("Cannot deduplicate an empty dataset.")

        df_cleaned = df.copy()
        audit_trail: List[Dict[str, Any]] = []

        # Find rows that have duplicate copies
        duplicate_mask = df_cleaned.duplicated(keep=False)
        df_duplicates = df_cleaned[duplicate_mask]

        if df_duplicates.empty:
            logger.info("No exact duplicates found. Nothing to deduplicate.")
            return df_cleaned, audit_trail

        # Group by all columns to find exact duplicate clusters
        # dropna=False is important to make sure rows with nulls are grouped together
        grouped = df_duplicates.groupby(list(df_duplicates.columns), dropna=False)
        
        removed_indices = []
        timestamp = datetime.now(timezone.utc).isoformat() + "Z"

        for _, group in grouped:
            indices = group.index.tolist()
            if len(indices) <= 1:
                continue

            # For exact duplicates, all columns are identical, so their completeness is the same.
            # Thus, "keep_most_complete" resolves to keeping the first occurrence.
            if self.strategy in ("keep_first", "keep_most_complete"):
                kept_idx = indices[0]
                dropped_indices = indices[1:]
            elif self.strategy == "keep_last":
                kept_idx = indices[-1]
                dropped_indices = indices[:-1]
            else:
                raise InvalidStrategyError(f"Unsupported strategy '{self.strategy}' in execution.")

            removed_indices.extend(dropped_indices)

            for idx in dropped_indices:
                audit_trail.append({
                    "Original Row Index": idx,
                    "Duplicate Type": "Exact",
                    "Reason Removed": f"Exact duplicate of row kept at index {kept_idx}.",
                    "Strategy Used": self.strategy,
                    "Timestamp": timestamp
                })

        # Remove the records from the copied DataFrame
        df_cleaned = df_cleaned.drop(index=removed_indices)
        logger.info(f"Exact deduplication finished. Removed {len(removed_indices)} rows.")
        
        return df_cleaned, audit_trail
