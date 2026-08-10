import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

# Add the parent directory of data_validation to sys.path so absolute imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from data_validation.config import rules
from data_validation.validators.null_validator import NullValidator
from data_validation.validators.range_validator import RangeValidator
from data_validation.validators.format_validator import FormatValidator
from data_validation.validators.reference_validator import ReferenceValidator
from data_validation.validators.business_rule_validator import BusinessRuleValidator
from data_validation.reports.validation_report import ValidationReport
from data_validation.utils.logger import setup_logger
from data_validation.utils.helpers import load_dataset, save_dataset
from data_validation.utils.exceptions import (
    ValidationError,
    EmptyDatasetError,
    MissingColumnError,
    DatasetLoadError
)

def parse_args():
    parser = argparse.ArgumentParser(description="Enterprise Data Consistency & Validation Rules Framework")
    parser.add_argument("input_file", type=str, help="Path to the input dataset to validate (CSV or Excel)")
    return parser.parse_args()

def run_validation(args) -> int:
    logger = setup_logger()
    start_time = time.time()
    
    input_path = Path(args.input_file)
    dataset_name = input_path.name
    
    logger.info("=" * 60)
    logger.info("Data Consistency & Validation Rules Pipeline Started")
    logger.info(f"Input Dataset: {input_path.resolve()}")
    logger.info("=" * 60)
    
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_json_path = output_dir / "validation_report.json"
    audit_log_path = output_dir / "validation_audit.log"
    validated_csv_path = output_dir / "validated_data.csv"
    failures_csv_path = output_dir / "validation_failures.csv"

    # Pre-populate empty variables for error reporting
    total_records = 0
    passed_records = 0
    failed_records = 0
    rule_stats: Dict[str, Dict[str, int]] = {}

    try:
        # 1. Load Primary Dataset
        df = load_dataset(input_path)
        total_records = len(df)
        logger.info(f"Successfully loaded dataset with {total_records} records.")

        # 2. Check for required columns existence before validating
        # This raises a MissingColumnError immediately for missing required headers
        missing_reqs = [c for c in rules.REQUIRED_COLUMNS if c not in df.columns]
        if missing_reqs:
            raise MissingColumnError(f"Required column(s) missing from input dataset: {missing_reqs}")

        # 3. Instantiate and run validators
        validators = [
            NullValidator(rules.REQUIRED_COLUMNS),
            RangeValidator(rules.RANGE_RULES),
            FormatValidator(rules.FORMAT_PATTERNS),
            ReferenceValidator(rules.REFERENTIAL_RULES, base_dir=input_path.parent),
            BusinessRuleValidator(rules.BUSINESS_RULES)
        ]
        
        # Dictionary to store all validator boolean Series
        validation_results: Dict[str, pd.Series] = {}
        
        # Keep track of custom descriptive reasons for failures
        # Map: validator column name -> (friendly_name, rule_failure_reason)
        reason_map: Dict[str, Tuple[str, str]] = {}
        
        # Populate friendly name & reason mappings for standard rules
        for col in rules.REQUIRED_COLUMNS:
            reason_map[f"valid_null_{col}"] = (f"{col}_required", f"{col} cannot be null")
            
        for col in rules.RANGE_RULES.keys():
            reason_map[f"valid_range_{col}"] = (f"{col}_range", f"{col} outside allowed range")
            
        for col in rules.FORMAT_PATTERNS.keys():
            reason_map[f"valid_format_{col}"] = (f"{col}_format", f"invalid {col} format")
            
        for rule in rules.REFERENTIAL_RULES:
            ckey = rule["child_foreign_key"]
            pref = rule["parent_dataset"]
            reason_map[f"valid_ref_{ckey}"] = (f"{ckey}_reference", f"{ckey} reference not found in {Path(pref).name}")
            
        for rule_name, _, reason in rules.BUSINESS_RULES:
            reason_map[f"valid_business_{rule_name}"] = (rule_name, reason)

        # Run each validator
        for validator in validators:
            res = validator.validate(df)
            validation_results.update(res)

        # 4. Compile Validation Results
        val_df = pd.DataFrame(validation_results)
        
        # Calculate rules statistics
        for val_col in val_df.columns:
            friendly_name, _ = reason_map.get(val_col, (val_col, "failed validation"))
            passed_count = int(val_df[val_col].sum())
            failed_count = total_records - passed_count
            rule_stats[friendly_name] = {
                "passed": passed_count,
                "failed": failed_count
            }

        # passes_all_checks: Row passes only if every check column is True
        df["passes_all_checks"] = val_df.all(axis=1)
        passed_records = int(df["passes_all_checks"].sum())
        failed_records = total_records - passed_records

        # 5. Extract failed rule names and error descriptions
        failed_rules_list = []
        failure_reasons_list = []
        
        for idx, row in val_df.iterrows():
            failed_cols = val_df.columns[~row]
            
            rule_names = []
            reasons = []
            for col in failed_cols:
                friendly_name, reason = reason_map.get(col, (col, "invalid value"))
                rule_names.append(friendly_name)
                reasons.append(reason)
                
            failed_rules_list.append("; ".join(rule_names) if rule_names else "")
            failure_reasons_list.append("; ".join(reasons) if reasons else "")

        df["failed_rule_names"] = failed_rules_list
        df["validation_errors"] = failure_reasons_list

        # 6. Isolate and Save Clean Dataset
        clean_df = df[df["passes_all_checks"]].copy()
        # Drop framework validation helper columns from clean output dataset
        clean_output_df = clean_df.drop(
            columns=["passes_all_checks", "failed_rule_names", "validation_errors"]
        )
        save_dataset(clean_output_df, validated_csv_path)
        logger.info(f"Clean records isolated ({passed_records} rows). Saved to {validated_csv_path}")

        # 7. Isolate and Save Failed Dataset
        failed_df = df[~df["passes_all_checks"]].copy()
        
        # Format validation_failures file columns
        # Include original record + validation status + failed rules + reasons + timestamp
        failed_output_df = failed_df.copy()
        failed_output_df["validation_status"] = "FAILED"
        failed_output_df["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        # Drop temporary boolean checks from failures CSV to keep it clean
        failed_output_df = failed_output_df.drop(columns=["passes_all_checks"])
        
        save_dataset(failed_output_df, failures_csv_path)
        logger.info(f"Failed records isolated ({failed_records} rows). Saved to {failures_csv_path}")

        # 8. Reports & Audits
        ValidationReport.generate_json_report(
            status="COMPLETED",
            dataset_name=dataset_name,
            total_records=total_records,
            passed_records=passed_records,
            failed_records=failed_records,
            rule_stats=rule_stats,
            output_json_path=report_json_path
        )
        
        ValidationReport.append_to_audit_log(
            dataset_name=dataset_name,
            rule_stats=rule_stats,
            audit_log_path=audit_log_path,
            status="SUCCESS"
        )

        duration = time.time() - start_time
        pass_rate = (passed_records / total_records * 100.0) if total_records > 0 else 0.0
        fail_rate = (failed_records / total_records * 100.0) if total_records > 0 else 0.0

        # 9. Print Concise Summary
        print("\n" + "=" * 40)
        print("DATA VALIDATION REPORT")
        print("=" * 40)
        print(f"Records checked: {total_records:,}")
        print(f"Passed:          {passed_records:,}")
        print(f"Failed:          {failed_records:,}")
        print(f"Pass rate:       {pass_rate:.2f}%")
        print(f"Failure rate:    {fail_rate:.2f}%")
        print("-" * 40)
        print("RULE RESULTS")
        print("-" * 40)
        for rule, stats in rule_stats.items():
            print(f"{rule}")
            print(f"Passed: {stats['passed']:,}")
            print(f"Failed: {stats['failed']:,}")
            print()
        print("=" * 40 + "\n")
        
        logger.info("Pipeline completed successfully.")
        return 0

    except ValidationError as e:
        logger.error(f"Pipeline execution aborted: {str(e)}")
        ValidationReport.generate_json_report(
            status="ERROR",
            dataset_name=dataset_name,
            total_records=0,
            passed_records=0,
            failed_records=0,
            rule_stats={},
            output_json_path=report_json_path,
            error_message=str(e)
        )
        # Append error status to audit log
        ValidationReport.append_to_audit_log(
            dataset_name=dataset_name,
            rule_stats={},
            audit_log_path=audit_log_path,
            status="ERROR"
        )
        return 1
    except Exception as e:
        logger.exception("An unexpected critical error occurred:")
        ValidationReport.generate_json_report(
            status="ERROR",
            dataset_name=dataset_name,
            total_records=0,
            passed_records=0,
            failed_records=0,
            rule_stats={},
            output_json_path=report_json_path,
            error_message=f"Critical error: {str(e)}"
        )
        ValidationReport.append_to_audit_log(
            dataset_name=dataset_name,
            rule_stats={},
            audit_log_path=audit_log_path,
            status="ERROR"
        )
        return 1

if __name__ == "__main__":
    args = parse_args()
    sys.exit(run_validation(args))
