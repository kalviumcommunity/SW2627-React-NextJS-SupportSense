import logging
import re
from typing import Dict
import pandas as pd
from data_validation.validators.base_validator import BaseValidator

logger = logging.getLogger("data_validation.validators.format_validator")

class FormatValidator(BaseValidator):
    def __init__(self, format_patterns: Dict[str, str]):
        self.format_patterns = format_patterns

    def validate(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Validates column values match configured regular expressions.
        Null values are ignored (assumed True) to decouple null checks.
        """
        logger.info(f"Running Format Validation for patterns: {self.format_patterns}")
        results = {}
        
        for col, pattern in self.format_patterns.items():
            validation_col_name = f"valid_format_{col}"
            
            if col not in df.columns:
                logger.warning(f"Configured format validation column '{col}' is missing from input dataset.")
                results[validation_col_name] = pd.Series(True, index=df.index)
                continue
                
            series = df[col]
            non_null_mask = series.notna()
            
            # String representation nulls check (e.g. empty or sentinel)
            # If the value is a string-based null, we also consider it null (meaning format check passes, null check handles it)
            if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
                cleaned_str = series.astype(str).str.strip().str.lower()
                is_string_null = cleaned_str.isin(["", "nan", "null", "none", "na", "<null>", "undefined"])
                non_null_mask = non_null_mask & ~is_string_null
            
            # Apply regex check (using standard re compile or pandas str.match)
            # Match checks from the start of the string (anchor matches)
            # Force string conversion of values to check regex
            match_mask = series.astype(str).str.match(pattern, na=False)
            
            # Record passes range: it is either null, OR it successfully matches the regex pattern
            pass_mask = ~non_null_mask | match_mask
            results[validation_col_name] = pass_mask
            
            failed_count = int((~pass_mask).sum())
            logger.info(f"Column '{col}' format validation: {len(df) - failed_count} passed, {failed_count} failed.")
            
        return results
