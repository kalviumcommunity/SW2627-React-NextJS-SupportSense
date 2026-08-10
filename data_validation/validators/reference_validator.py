import logging
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from data_validation.validators.base_validator import BaseValidator
from data_validation.utils.helpers import load_dataset
from data_validation.utils.exceptions import (
    MissingReferenceDatasetError,
    MissingReferenceKeyError,
    MissingColumnError
)

logger = logging.getLogger("data_validation.validators.reference_validator")

class ReferenceValidator(BaseValidator):
    def __init__(self, referential_rules: List[Dict[str, str]], base_dir: Path = None):
        self.referential_rules = referential_rules
        self.base_dir = base_dir or Path.cwd()

    def validate(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Validates child foreign keys exist in parent primary key sets.
        Allows null foreign keys to pass (delegates null checks to NullValidator).
        """
        logger.info(f"Running Referential Integrity Validation for rules: {self.referential_rules}")
        results = {}
        
        for rule in self.referential_rules:
            child_key = rule["child_foreign_key"]
            parent_key = rule["parent_key"]
            parent_rel_path = rule["parent_dataset"]
            
            validation_col_name = f"valid_ref_{child_key}"
            
            # 1. Validate child foreign key exists in child dataset
            if child_key not in df.columns:
                logger.error(f"Child foreign key '{child_key}' is missing from input dataset.")
                results[validation_col_name] = pd.Series(True, index=df.index)
                continue
                
            # 2. Resolve and load parent dataset
            parent_path = Path(parent_rel_path)
            if not parent_path.exists() and not parent_path.is_absolute():
                parent_path = self.base_dir / parent_rel_path
                
            logger.info(f"Loading parent dataset from: {parent_path}")
            
            try:
                parent_df = load_dataset(parent_path)
            except Exception as e:
                logger.error(f"Failed to load parent dataset: {str(e)}")
                raise MissingReferenceDatasetError(
                    f"Referential lookup failed. Parent dataset file '{parent_rel_path}' could not be loaded."
                ) from e
                
            # 3. Validate parent primary key exists in parent dataset
            if parent_key not in parent_df.columns:
                logger.error(f"Parent key '{parent_key}' is missing from parent dataset '{parent_rel_path}'.")
                raise MissingReferenceKeyError(
                    f"Referential lookup failed. Parent key '{parent_key}' is missing in parent dataset."
                )
                
            child_series = df[child_key]
            
            # Get parent unique keys as strings for robust cross-type validation
            parent_keys = set(parent_df[parent_key].dropna().astype(str).str.strip())
            
            # Map child values: True if NaN/null, or if stripped string matches parent keys
            non_null_mask = child_series.notna()
            
            # Handle string null representation checking
            if pd.api.types.is_object_dtype(child_series) or pd.api.types.is_string_dtype(child_series):
                cleaned_str = child_series.astype(str).str.strip().str.lower()
                is_string_null = cleaned_str.isin(["", "nan", "null", "none", "na", "<null>", "undefined"])
                non_null_mask = non_null_mask & ~is_string_null
                
            child_keys_str = child_series.astype(str).str.strip()
            
            # Evaluate referential match
            ref_match_mask = child_keys_str.isin(parent_keys)
            pass_mask = ~non_null_mask | ref_match_mask
            
            results[validation_col_name] = pass_mask
            
            failed_count = int((~pass_mask).sum())
            logger.info(f"Referential integrity '{child_key} -> {parent_rel_path}:{parent_key}': {len(df) - failed_count} passed, {failed_count} failed.")
            
        return results
