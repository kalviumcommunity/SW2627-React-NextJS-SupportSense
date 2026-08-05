import argparse
import sys
import pandas as pd
import time
from pathlib import Path

# Add the parent directory of data_type_enforcement to sys.path so absolute imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_type_enforcement.config.settings import DEFAULT_SCHEMA, OUTPUT_DIR
from data_type_enforcement.converters.datatype_converter import DataTypeConverter
from data_type_enforcement.validators.dtype_validator import DTypeValidator
from data_type_enforcement.utils.logger import setup_logger
from data_type_enforcement.utils.helpers import save_json

logger = setup_logger("main")

def load_data(filepath: str) -> pd.DataFrame:
    path = Path(filepath)
    if not path.exists():
        logger.error(f"File not found: {filepath}")
        sys.exit(1)
        
    try:
        if path.suffix.lower() == '.csv':
            return pd.read_csv(filepath)
        elif path.suffix.lower() in ['.xls', '.xlsx']:
            return pd.read_excel(filepath)
        elif path.suffix.lower() == '.json':
            return pd.read_json(filepath)
        else:
            logger.error(f"Unsupported file format: {path.suffix}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading data from {filepath}: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Data Type Enforcement & Standardization Framework")
    parser.add_argument("input_file", help="Path to the untyped dataset (CSV, JSON, Excel)")
    args = parser.parse_args()
    
    start_time = time.time()
    logger.info(f"--- Conversion Started for {args.input_file} ---")
    
    # 1. Load Data
    logger.info("Loading dataset...")
    df_raw = load_data(args.input_file)
    logger.info(f"Loaded dataset with {len(df_raw)} rows and {len(df_raw.columns)} columns.")
    
    # 2. Convert Data Types
    converter = DataTypeConverter(schema=DEFAULT_SCHEMA)
    df_converted = converter.convert(df_raw)
    
    # 3. Validation & Reporting
    validator = DTypeValidator(schema=DEFAULT_SCHEMA)
    report_data = validator.validate_and_report(df_raw, df_converted)
    
    # 4. Save Reports
    report_df = pd.DataFrame(report_data)
    
    csv_report_path = OUTPUT_DIR / "dtype_conversion_report.csv"
    json_report_path = OUTPUT_DIR / "dtype_conversion_report.json"
    
    report_df.to_csv(csv_report_path, index=False)
    logger.info(f"Saved CSV report to {csv_report_path}")
    
    save_json(report_data, json_report_path)
    logger.info(f"Saved JSON report to {json_report_path}")
    
    # 5. Save Standardized Dataset
    output_data_path = OUTPUT_DIR / f"standardized_{Path(args.input_file).name}"
    if output_data_path.suffix.lower() == '.csv':
        df_converted.to_csv(output_data_path, index=False)
    elif output_data_path.suffix.lower() == '.json':
        df_converted.to_json(output_data_path, orient='records', date_format='iso')
    else:
        # Default fallback if original was excel but we want standard csv
        output_data_path = output_data_path.with_suffix('.csv')
        df_converted.to_csv(output_data_path, index=False)
        
    logger.info(f"Saved standardized dataset to {output_data_path}")
    
    # Execution Summary
    execution_time = time.time() - start_time
    logger.info(f"--- Conversion Completed in {execution_time:.2f} seconds ---")
    
    # Print summary to console for immediate feedback
    print("\n" + "="*50)
    print("CONVERSION SUMMARY")
    print("="*50)
    print(report_df[['Column Name', 'Status', 'Error Message']].to_string(index=False))
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
