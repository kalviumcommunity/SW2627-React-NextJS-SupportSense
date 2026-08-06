import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timezone
import pandas as pd
from duplicate_detection.utils.logger import setup_logger
from duplicate_detection.utils.helpers import save_json

logger = setup_logger(__name__)

class ReportGenerator:
    """
    Generates JSON comparison reports and CSV audit trail reports.
    """

    def generate_audit_csv(self, audit_records: List[Dict[str, Any]], filepath: Path) -> None:
        """
        Saves the list of audit records to a CSV file.
        If no rows were removed, creates an empty DataFrame with the expected columns.
        """
        logger.info(f"Generating audit trail report at {filepath}...")
        columns = ["Original Row Index", "Duplicate Type", "Reason Removed", "Strategy Used", "Timestamp"]
        
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            if not audit_records:
                df_audit = pd.DataFrame(columns=columns)
            else:
                df_audit = pd.DataFrame(audit_records)
                # Ensure the columns match the exact case and spelling
                df_audit = df_audit[columns]
                
            df_audit.to_csv(filepath, index=False)
            logger.info(f"Audit report generated successfully with {len(df_audit)} entries.")
        except Exception as e:
            logger.error(f"Failed to generate audit CSV report: {str(e)}")
            raise

    def generate_json_report(
        self,
        status: str,
        rows_before: int,
        rows_after: int,
        strategy: str,
        duplicate_columns: List[str],
        filepath: Path,
        error_message: str = None
    ) -> Dict[str, Any]:
        """
        Constructs and saves the JSON summary report.
        Returns the report dictionary.
        """
        logger.info(f"Generating deduplication summary JSON report at {filepath}...")
        
        if status == "SUCCESS":
            removed = rows_before - rows_after
            percentage = round((removed / rows_before) * 100, 2) if rows_before > 0 else 0.0
            
            report = {
                "status": "SUCCESS",
                "rows_before": rows_before,
                "rows_after": rows_after,
                "duplicates_removed": removed,
                "duplicate_percentage": percentage,
                "strategy": strategy,
                "duplicate_columns": duplicate_columns
            }
        else:
            report = {
                "status": "ERROR",
                "error_message": error_message or "An unknown error occurred.",
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
            }

        try:
            save_json(report, filepath)
            logger.info("JSON report generated successfully.")
            return report
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {str(e)}")
            raise
