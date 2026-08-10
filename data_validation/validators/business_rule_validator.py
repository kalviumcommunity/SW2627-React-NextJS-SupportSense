import logging
from typing import List, Tuple, Callable, Dict
import pandas as pd
from data_validation.validators.base_validator import BaseValidator

logger = logging.getLogger("data_validation.validators.business_rule_validator")

class BusinessRuleValidator(BaseValidator):
    def __init__(self, business_rules: List[Tuple[str, Callable[[pd.DataFrame], pd.Series], str]]):
        self.business_rules = business_rules

    def validate(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Executes custom business rules.
        Each rule callable receives the full DataFrame and returns a boolean Series.
        """
        logger.info(f"Running Business Rules Validation for registered rules.")
        results = {}
        
        for rule_name, rule_fn, failure_reason in self.business_rules:
            validation_col_name = f"valid_business_{rule_name}"
            
            try:
                # Call validation function
                pass_mask = rule_fn(df)
                
                # Make sure it returns a boolean Series
                if not isinstance(pass_mask, pd.Series):
                    logger.error(f"Business rule '{rule_name}' did not return a pandas Series.")
                    pass_mask = pd.Series(False, index=df.index)
                else:
                    # Cast to bool and fillna(False) to ensure no NaN leaks
                    pass_mask = pass_mask.astype(bool).fillna(False)
                    
            except Exception as e:
                logger.error(f"Error executing business rule '{rule_name}': {str(e)}")
                # Mark all as False on error
                pass_mask = pd.Series(False, index=df.index)
                
            results[validation_col_name] = pass_mask
            
            failed_count = int((~pass_mask).sum())
            logger.info(f"Business rule '{rule_name}': {len(df) - failed_count} passed, {failed_count} failed.")
            
        return results
