import pandas as pd
from typing import Dict, Any, List
from datetime import datetime

from data_type_enforcement.utils.logger import setup_logger

logger = setup_logger(__name__)

class DTypeValidator:
    """
    Validates conversion results, comparing before and after data types.
    Generates a detailed status report for each column.
    """
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        
    def validate_and_report(self, df_before: pd.DataFrame, df_after: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Compares dataframes and returns a list of dictionaries representing the report rows.
        """
        logger.info("Starting validation and reporting process.")
        report_data = []
        
        # Check for missing columns defined in schema
        for column in self.schema.keys():
            if column not in df_before.columns:
                logger.warning(f"Schema column '{column}' is entirely missing from the dataset.")
                report_data.append({
                    "Column Name": column,
                    "Original Type": "N/A",
                    "Converted Type": "N/A",
                    "Status": "Failed",
                    "Error Message": "Column missing from dataset",
                    "Timestamp": datetime.now().isoformat()
                })
        
        # Compare columns that exist in the original dataframe
        for column in df_before.columns:
            orig_dtype = str(df_before[column].dtype)
            
            if column not in self.schema:
                # Column not in schema, meaning it wasn't converted by us, but we can still report it
                report_data.append({
                    "Column Name": column,
                    "Original Type": orig_dtype,
                    "Converted Type": orig_dtype,
                    "Status": "Skipped",
                    "Error Message": "Not defined in schema",
                    "Timestamp": datetime.now().isoformat()
                })
                continue
                
            after_dtype = str(df_after[column].dtype)
            expected_type = self.schema[column].get("type", "unknown")
            
            status = "Success"
            error_msg = "None"
            
            # Basic heuristic validation based on target type
            if expected_type == "boolean" and after_dtype != "boolean":
                status = "Warning/Failed"
                error_msg = f"Expected boolean, got {after_dtype}"
            elif expected_type == "date" and "datetime" not in after_dtype:
                status = "Failed"
                error_msg = f"Expected datetime, got {after_dtype}"
            elif expected_type in ["currency", "float"] and "float" not in after_dtype:
                status = "Failed"
                error_msg = f"Expected float, got {after_dtype}"
            elif expected_type == "int" and "Int" not in after_dtype and "int" not in after_dtype:
                status = "Failed"
                error_msg = f"Expected int, got {after_dtype}"
                
            # Check for newly introduced NaNs/NaTs which indicates coercion failures
            before_nas = df_before[column].isna().sum()
            after_nas = df_after[column].isna().sum()
            if after_nas > before_nas:
                failed_count = after_nas - before_nas
                if status == "Success":
                    status = "Warning"
                error_msg = f"{failed_count} values could not be converted and were coerced to NA. " + (error_msg if error_msg != "None" else "")
                
            report_data.append({
                "Column Name": column,
                "Original Type": orig_dtype,
                "Converted Type": after_dtype,
                "Status": status,
                "Error Message": error_msg.strip(),
                "Timestamp": datetime.now().isoformat()
            })
            
        logger.info("Validation complete.")
        return report_data
