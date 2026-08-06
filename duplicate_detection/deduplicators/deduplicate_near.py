from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple
import pandas as pd
from duplicate_detection.utils.logger import setup_logger
from duplicate_detection.utils.exceptions import InvalidStrategyError, MissingColumnError, EmptyDatasetError
from duplicate_detection.config.settings import VALID_STRATEGIES

logger = setup_logger(__name__)

class NearDeduplicator:
    """
    Deduplicates a Pandas DataFrame by removing rows with duplicate keys.
    Supports strategies: keep_first, keep_last, keep_most_complete.
    Records an audit log of all removed records.
    """

    def __init__(self, key_columns: List[str], strategy: str = "keep_first"):
        """
        Initializes the deduplicator with a selection strategy and key columns.
        """
        if not key_columns:
            raise ValueError("key_columns list cannot be empty.")
        if strategy not in VALID_STRATEGIES:
            error_msg = f"Invalid strategy '{strategy}'. Allowed: {VALID_STRATEGIES}"
            logger.error(error_msg)
            raise InvalidStrategyError(error_msg)
            
        self.key_columns = key_columns
        self.strategy = strategy

    def _get_completeness_score(self, row: pd.Series) -> int:
        """
        Computes completeness score for a row.
        Score is the number of columns that are non-null and not empty/whitespace strings.
        """
        score = 0
        for val in row:
            if pd.notna(val) and val is not None:
                if isinstance(val, str):
                    if val.strip() != "":
                        score += 1
                else:
                    score += 1
        return score

    def deduplicate(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict[str, Any]]]:
        """
        Removes near duplicates from a DataFrame.
        Returns:
          - A new cleaned DataFrame (copy of the original).
          - A list of audit trail dictionaries for removed records.
        """
        logger.info(f"Executing near deduplication on keys: {self.key_columns} using strategy: {self.strategy}")
        
        if df.empty:
            logger.warning("Empty DataFrame passed to NearDeduplicator.")
            raise EmptyDatasetError("Cannot deduplicate an empty dataset.")

        # Validate that key columns exist
        missing_cols = [col for col in self.key_columns if col not in df.columns]
        if missing_cols:
            error_msg = f"Key columns missing from dataset: {missing_cols}"
            logger.error(error_msg)
            raise MissingColumnError(error_msg)

        df_cleaned = df.copy()
        audit_trail: List[Dict[str, Any]] = []

        # Find rows that have duplicate keys
        duplicate_mask = df_cleaned.duplicated(subset=self.key_columns, keep=False)
        df_duplicates = df_cleaned[duplicate_mask]

        if df_duplicates.empty:
            logger.info("No near duplicates found. Nothing to deduplicate.")
            return df_cleaned, audit_trail

        # Group by the key columns
        grouped = df_duplicates.groupby(self.key_columns, dropna=False)
        
        removed_indices = []
        timestamp = datetime.now(timezone.utc).isoformat() + "Z"

        for _, group in grouped:
            indices = group.index.tolist()
            if len(indices) <= 1:
                continue

            if self.strategy == "keep_first":
                kept_idx = indices[0]
                dropped_indices = indices[1:]
            elif self.strategy == "keep_last":
                kept_idx = indices[-1]
                dropped_indices = indices[:-1]
            elif self.strategy == "keep_most_complete":
                # Calculate scores for all indices
                scores = [self._get_completeness_score(group.loc[idx]) for idx in indices]
                max_score = max(scores)
                # Filter indices with the maximum score
                tied_indices = [idx for idx, score in zip(indices, scores) if score == max_score]
                # Tie-breaking: keep the first occurrence among the tied records
                kept_idx = tied_indices[0]
                
                dropped_indices = [idx for idx in indices if idx != kept_idx]
            else:
                raise InvalidStrategyError(f"Unsupported strategy '{self.strategy}' in execution.")

            removed_indices.extend(dropped_indices)

            for idx in dropped_indices:
                audit_trail.append({
                    "Original Row Index": idx,
                    "Duplicate Type": "Near",
                    "Reason Removed": (
                        f"Near duplicate on keys: {self.key_columns}. "
                        f"Kept row at index {kept_idx}."
                    ),
                    "Strategy Used": self.strategy,
                    "Timestamp": timestamp
                })

        # Remove the records from the copied DataFrame
        df_cleaned = df_cleaned.drop(index=removed_indices)
        logger.info(f"Near deduplication finished. Removed {len(removed_indices)} rows.")
        
        return df_cleaned, audit_trail
