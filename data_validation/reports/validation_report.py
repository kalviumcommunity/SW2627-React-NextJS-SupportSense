import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd

logger = logging.getLogger("data_validation.reports.validation_report")

class ValidationReport:
    @staticmethod
    def generate_json_report(
        status: str,
        dataset_name: str,
        total_records: int,
        passed_records: int,
        failed_records: int,
        rule_stats: Dict[str, Dict[str, int]],
        output_json_path: Path,
        error_message: str = None
    ) -> None:
        """
        Generates a summary JSON validation report.
        """
        logger.info(f"Generating summary JSON report at {output_json_path}")
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        if status == "ERROR":
            report = {
                "status": "ERROR",
                "timestamp": timestamp,
                "dataset_name": dataset_name,
                "error_message": error_message
            }
        else:
            pass_percentage = round((passed_records / total_records) * 100.0, 2) if total_records > 0 else 0.0
            fail_percentage = round((failed_records / total_records) * 100.0, 2) if total_records > 0 else 0.0
            
            report = {
                "status": "COMPLETED",
                "timestamp": timestamp,
                "dataset_name": dataset_name,
                "total_records": total_records,
                "passed_records": passed_records,
                "failed_records": failed_records,
                "pass_percentage": pass_percentage,
                "failure_percentage": fail_percentage,
                "rules": rule_stats
            }
            
        try:
            output_json_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4)
            logger.info("Summary JSON report generated successfully.")
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {str(e)}")

    @staticmethod
    def append_to_audit_log(
        dataset_name: str,
        rule_stats: Dict[str, Dict[str, int]],
        audit_log_path: Path,
        status: str = "SUCCESS"
    ) -> None:
        """
        Appends validation rule stats to the audit log CSV.
        Record columns: timestamp, dataset, rule, records_checked, records_failed, action, status
        """
        logger.info(f"Appending validation records to audit trail log at {audit_log_path}")
        
        timestamp = datetime.now(timezone.utc).isoformat()
        audit_records = []
        
        for rule, stats in rule_stats.items():
            checked = stats["passed"] + stats["failed"]
            failed = stats["failed"]
            action = f"Validated rule '{rule}'. Isolated {failed} failures."
            
            record = {
                "timestamp": timestamp,
                "dataset": dataset_name,
                "rule": rule,
                "records_checked": checked,
                "records_failed": failed,
                "action": action,
                "status": status
            }
            audit_records.append(record)
            
        if not audit_records:
            # If no rules ran (e.g. error occurred), write a single error record
            audit_records.append({
                "timestamp": timestamp,
                "dataset": dataset_name,
                "rule": "N/A",
                "records_checked": 0,
                "records_failed": 0,
                "action": "Pipeline failed or aborted before rule execution.",
                "status": "ERROR"
            })
            
        audit_df = pd.DataFrame(audit_records)
        
        try:
            audit_log_path.parent.mkdir(parents=True, exist_ok=True)
            if audit_log_path.exists():
                audit_df.to_csv(audit_log_path, mode="a", header=False, index=False)
            else:
                audit_df.to_csv(audit_log_path, index=False)
            logger.info("Audit log appended successfully.")
        except Exception as e:
            logger.error(f"Failed to append to audit log: {str(e)}")
