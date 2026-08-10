import logging
from datetime import datetime
from typing import Dict, Any
import pandas as pd
from data_validation.validators.base_validator import BaseValidator

logger = logging.getLogger("data_validation.validators.range_validator")

class RangeValidator(BaseValidator):
    def __init__(self, range_rules: Dict[str, Dict[str, Any]]):
        self.range_rules = range_rules

    def validate(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Validates values fall within min and max boundaries.
        Supports both numeric and datetime ranges (including dynamic constraints like 'now' or 'today').
        """
        logger.info(f"Running Range Validation for rules: {self.range_rules}")
        results = {}
        
        for col, rules in self.range_rules.items():
            validation_col_name = f"valid_range_{col}"
            
            if col not in df.columns:
                logger.warning(f"Configured range validation column '{col}' is missing from input dataset.")
                results[validation_col_name] = pd.Series(True, index=df.index)
                continue
                
            series = df[col]
            
            # Determine if this column is date-like
            is_date = False
            if pd.api.types.is_datetime64_any_dtype(series) or "date" in col.lower():
                is_date = True
                
            if is_date:
                series_to_check = pd.to_datetime(series, errors="coerce")
            else:
                series_to_check = pd.to_numeric(series, errors="coerce")
                
            # If value is null, range validator defaults to True (NullValidator is responsible for empty checks)
            pass_mask = pd.Series(True, index=df.index)
            non_null_mask = series_to_check.notna()
            
            # 1. Minimum Limit validation
            if "min" in rules:
                min_val = rules["min"]
                if is_date:
                    min_limit = pd.to_datetime(datetime.now() if min_val in ["now", "today"] else min_val)
                else:
                    min_limit = float(min_val)
                
                # Check condition where element is not null
                pass_mask = pass_mask & (~non_null_mask | (series_to_check >= min_limit))
                
            # 2. Maximum Limit validation
            if "max" in rules:
                max_val = rules["max"]
                if is_date:
                    max_limit = pd.to_datetime(datetime.now() if max_val in ["now", "today"] else max_val)
                else:
                    max_limit = float(max_val)
                
                # Check condition where element is not null
                pass_mask = pass_mask & (~non_null_mask | (series_to_check <= max_limit))
                
            results[validation_col_name] = pass_mask
            
            failed_count = int((~pass_mask).sum())
            logger.info(f"Column '{col}' range validation: {len(df) - failed_count} passed, {failed_count} failed.")
            
        return results
