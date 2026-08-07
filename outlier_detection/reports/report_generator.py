from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from outlier_detection.detectors.base_detector import OutlierResult

logger = logging.getLogger("outlier_detection.reports.report_generator")

class ReportGenerator:
    @staticmethod
    def generate_audit_log(
        results: List[OutlierResult],
        handling_strategy: str,
        rows_removed_dict: Dict[str, int],
        output_csv_path: Path
    ) -> None:
        """
        Generates or appends to a CSV log auditing every outlier detection and handling step.
        """
        logger.info(f"Generating outlier cleaning log CSV at {output_csv_path}")
        
        audit_records = []
        timestamp = datetime.now(timezone.utc).isoformat()
        
        for res in results:
            rows_removed = rows_removed_dict.get(res.column, 0)
            
            # Action description
            if handling_strategy == "flag":
                action = f"Created binary indicator column 'is_{res.column}_outlier'."
            elif handling_strategy == "cap":
                action = f"Capped {res.outlier_count} values outside boundaries."
            elif handling_strategy == "remove":
                action = f"Removed {rows_removed} rows containing outliers."
            else:
                action = f"Applied strategy: {handling_strategy}"
                
            record = {
                "timestamp": timestamp,
                "column": res.column,
                "detection_method": res.method,
                "handling_strategy": handling_strategy,
                "threshold": res.threshold,
                "lower_bound": res.lower_bound,
                "upper_bound": res.upper_bound,
                "outlier_count": res.outlier_count,
                "outlier_percentage": res.outlier_percentage,
                "rows_removed": rows_removed,
                "reason/action": action
            }
            audit_records.append(record)
            
        audit_df = pd.DataFrame(audit_records)
        
        # Write/append handling
        try:
            output_csv_path.parent.mkdir(parents=True, exist_ok=True)
            if output_csv_path.exists():
                # Append to existing
                audit_df.to_csv(output_csv_path, mode="a", header=False, index=False)
            else:
                # Create new
                audit_df.to_csv(output_csv_path, index=False)
            logger.info("Outlier cleaning CSV log saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save CSV audit log: {str(e)}")

    @staticmethod
    def generate_summary_report(
        status: str,
        detection_method: str,
        handling_strategy: str,
        rows_before: int,
        rows_after: int,
        results: List[OutlierResult],
        output_json_path: Path,
        error_message: str = None
    ) -> None:
        """
        Generates the standard summary JSON report.
        """
        logger.info(f"Generating summary JSON report at {output_json_path}")
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        if status == "ERROR":
            report = {
                "status": "ERROR",
                "error_message": error_message,
                "timestamp": timestamp
            }
        else:
            columns_data = {}
            for res in results:
                columns_data[res.column] = {
                    "lower_bound": res.lower_bound,
                    "upper_bound": res.upper_bound,
                    "outlier_count": res.outlier_count,
                    "outlier_percentage": res.outlier_percentage
                }
                
            report = {
                "status": "SUCCESS",
                "detection_method": detection_method,
                "handling_strategy": handling_strategy,
                "rows_before": rows_before,
                "rows_after": rows_after,
                "timestamp": timestamp,
                "columns": columns_data
            }
            
        try:
            output_json_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4)
            logger.info("Summary JSON report generated successfully.")
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {str(e)}")
