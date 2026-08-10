import logging
from typing import List, Dict
import pandas as pd
from data_validation.validators.base_validator import BaseValidator

logger = logging.getLogger("data_validation.validators.null_validator")

class NullValidator(BaseValidator):
    def __init__(self, required_columns: List[str]):
        self.required_columns = required_columns

    def validate(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Validates that required columns contain non-null, non-blank, non-sentinel values.
        """
        logger.info(f"Running Null Validation for required columns: {self.required_columns}")
        results = {}
        
        for col in self.required_columns:
            validation_col_name = f"valid_null_{col}"
            
            if col not in df.columns:
                logger.error(f"Required column '{col}' is missing from input dataset.")
                # Mark all as False (failed) since the column is missing
                results[validation_col_name] = pd.Series(False, index=df.index)
                continue
                
            series = df[col]
            # 1. Standard pandas NaN/None check
            null_mask = series.isna()
            
            # 2. String-level null checks (blank, "NULL", "None", etc.)
            # Convert dtype safely to check for string objects
            if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
                str_series = series.astype(str).str.strip().str.lower()
                sentinel_mask = str_series.isin(["", "nan", "null", "none", "na", "<null>", "undefined"])
                null_mask = null_mask | sentinel_mask
                
            # If it passes, it is NOT null (negate the null mask)
            results[validation_col_name] = ~null_mask
            
            failed_count = int(null_mask.sum())
            logger.info(f"Column '{col}' validation: {len(df) - failed_count} passed, {failed_count} failed.")
            
        return results
