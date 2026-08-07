import logging
import pandas as pd
from outlier_detection.handlers.base_handler import BaseHandler
from outlier_detection.detectors.base_detector import OutlierResult

logger = logging.getLogger("outlier_detection.handlers.remove_handler")

class RemoveHandler(BaseHandler):
    def handle(self, df: pd.DataFrame, result: OutlierResult) -> pd.DataFrame:
        """
        Removes rows where the specified column contains an outlier.
        Uses dataframe index alignment to safely drop rows.
        """
        logger.info(f"Applying REMOVE strategy to column '{result.column}'")
        
        # Identify index labels of outliers that currently exist in df
        outlier_indices = result.outlier_mask[result.outlier_mask].index
        existing_outlier_indices = outlier_indices.intersection(df.index)
        
        rows_before = len(df)
        df_copy = df.drop(index=existing_outlier_indices)
        rows_after = len(df_copy)
        rows_removed = rows_before - rows_after

        logger.info(
            f"Successfully removed {rows_removed} rows containing outliers in "
            f"column '{result.column}'. Rows before: {rows_before}, after: {rows_after}"
        )
        return df_copy
