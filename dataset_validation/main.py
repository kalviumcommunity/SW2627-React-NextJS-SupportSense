import argparse
import sys
import json
import datetime
from pathlib import Path
import pandas as pd

from dataset_validation.config.settings import Settings
from dataset_validation.utils.logger import setup_logger
from dataset_validation.validators.file_validator import validate_file_exists
from dataset_validation.validators.format_validator import validate_format
from dataset_validation.validators.encoding_validator import detect_encoding
from dataset_validation.validators.schema_validator import validate_schema
from dataset_validation.validators.statistics_validator import calculate_statistics

logger = setup_logger(__name__)

def load_dataset(file_path: Path) -> pd.DataFrame:
    """Loads a dataset into a pandas DataFrame based on file extension."""
    ext = file_path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext == ".json":
        return pd.read_json(file_path)
    elif ext == ".xlsx":
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported extension for loading: {ext}")

def main():
    parser = argparse.ArgumentParser(description="Dataset Intake & Source Validation")
    parser.add_argument("file_path", type=str, help="Path to the dataset file to validate")
    args = parser.parse_args()
    
    file_path = Path(args.file_path).resolve()
    
    logger.info(f"Validation Started for file: {file_path}")
    
    # Initialize report structure
    report = {
        "status": "PENDING",
        "timestamp": datetime.datetime.now().isoformat(),
        "file": file_path.name,
        "checks": {},
        "statistics": {},
        "warnings": [],
        "errors": []
    }
    
    validation_passed = True
    
    try:
        # 1. File Exists
        logger.info("Running File Exists validation...")
        exists, exists_err = validate_file_exists(file_path)
        report["checks"]["file_exists"] = exists
        if not exists:
            report["errors"].append(exists_err)
            validation_passed = False
            logger.error(f"File validation failed: {exists_err}")
            # Cannot proceed without a file
            generate_report(report, validation_passed)
            sys.exit(1)
            
        # 2. Format
        logger.info("Running Format validation...")
        valid_format, format_err = validate_format(file_path)
        report["checks"]["format"] = valid_format
        if not valid_format:
            report["errors"].append(format_err)
            validation_passed = False
            logger.error(f"Format validation failed: {format_err}")
            # Cannot load unsupported format
            generate_report(report, validation_passed)
            sys.exit(1)
            
        # 3. Encoding Detection (Text files only)
        logger.info("Running Encoding detection...")
        encoding, confidence, enc_err = detect_encoding(file_path)
        if enc_err:
            report["warnings"].append(enc_err)
            logger.warning(f"Encoding detection issue: {enc_err}")
        else:
            if encoding:
                report["checks"]["encoding"] = f"{encoding} (confidence: {confidence:.2f})"
                logger.info(f"Detected encoding: {encoding} with confidence {confidence:.2f}")
            else:
                report["checks"]["encoding"] = "N/A"
        
        # Load dataset for schema and stats validations
        logger.info("Loading dataset for deep validation...")
        df = load_dataset(file_path)
        
        # 4. Schema Validation
        logger.info("Running Schema validation...")
        schema_valid, schema_report = validate_schema(df, Settings.DEFAULT_EXPECTED_SCHEMA)
        report["checks"]["schema"] = schema_valid
        
        if not schema_valid:
            validation_passed = False
            msg = f"Schema mismatch. Missing: {schema_report['missing_columns']}, Extra: {schema_report['extra_columns']}"
            report["errors"].append(msg)
            logger.error(msg)
            
        # 5. Statistics Validation
        logger.info("Capturing Dataset Statistics...")
        stats = calculate_statistics(file_path, df)
        if "error" in stats:
            report["warnings"].append(stats["error"])
            logger.warning(f"Statistics capture issue: {stats['error']}")
        else:
            report["statistics"] = stats
            
    except Exception as e:
        validation_passed = False
        error_msg = f"Unexpected error during validation: {str(e)}"
        report["errors"].append(error_msg)
        logger.exception(error_msg)
        
    # Finalize and exit
    generate_report(report, validation_passed)
    
    if validation_passed:
        logger.info("Validation Passed")
        print("\nValidation Summary: PASSED")
        sys.exit(0)
    else:
        logger.info("Validation Failed")
        print("\nValidation Summary: FAILED")
        for err in report["errors"]:
            print(f"- {err}")
        sys.exit(1)

def generate_report(report: dict, validation_passed: bool):
    """Saves the validation report to disk."""
    report["status"] = "PASSED" if validation_passed else "FAILED"
    
    Settings.ensure_directories()
    
    report_file = Settings.REPORTS_DIR / "validation_report.json"
    
    try:
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=4)
        logger.info(f"Validation report generated: {report_file}")
    except Exception as e:
        logger.error(f"Failed to write validation report: {str(e)}")

if __name__ == "__main__":
    main()
