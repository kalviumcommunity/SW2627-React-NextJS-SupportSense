import logging
import pandas as pd
from outlier_detection.handlers.base_handler import BaseHandler
from outlier_detection.detectors.base_detector import OutlierResult

logger = logging.getLogger("outlier_detection.handlers.flag_handler")

class FlagHandler(BaseHandler):
    def handle(self, df: pd.DataFrame, result: OutlierResult) -> pd.DataFrame:
        """
        Flags outliers by creating a new binary column 'is_<column>_outlier'.
        Original values in the target column remain unmodified.
        """
        flag_col_name = f"is_{result.column}_outlier"
        logger.info(f"Applying FLAG strategy to column '{result.column}'. Creating column '{flag_col_name}'")
        
        df_copy = df.copy()
        
        # Initialize flags as 0, then map the boolean mask
        # We align by index to handle cases where rows might have been dropped previously
        df_copy[flag_col_name] = 0
        
        # Filter mask to match only indexes present in the current dataframe
        aligned_mask = result.outlier_mask.reindex(df_copy.index, fill_value=False)
        df_copy.loc[aligned_mask, flag_col_name] = 1

        logger.info(
            f"Successfully added flag column '{flag_col_name}'. "
            f"Flagged {int(aligned_mask.sum())} active rows as outliers."
        )
        return df_copy
