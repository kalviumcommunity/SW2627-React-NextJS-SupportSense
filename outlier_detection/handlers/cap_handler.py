import logging
import pandas as pd
from outlier_detection.handlers.base_handler import BaseHandler
from outlier_detection.detectors.base_detector import OutlierResult

logger = logging.getLogger("outlier_detection.handlers.cap_handler")

class CapHandler(BaseHandler):
    def handle(self, df: pd.DataFrame, result: OutlierResult) -> pd.DataFrame:
        """
        Caps values outside boundaries [lower_bound, upper_bound] to the boundaries.
        Returns a modified copy of the DataFrame.
        """
        logger.info(f"Applying CAP strategy to column '{result.column}'")
        df_copy = df.copy()
        
        # Original values
        original_series = df_copy[result.column]
        
        # Apply clipping to boundary values
        df_copy[result.column] = original_series.clip(
            lower=result.lower_bound, 
            upper=result.upper_bound
        )

        logger.info(
            f"Successfully capped {result.outlier_count} values in column '{result.column}' "
            f"to boundaries [{result.lower_bound:.4f}, {result.upper_bound:.4f}]"
        )
        return df_copy
