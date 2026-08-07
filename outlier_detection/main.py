import argparse
import sys
import time
from pathlib import Path
from typing import List

# Add parent directory to path so absolute imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from outlier_detection.config import settings
from outlier_detection.detectors.zscore_detector import ZScoreDetector
from outlier_detection.detectors.iqr_detector import IQRDetector
from outlier_detection.handlers.cap_handler import CapHandler
from outlier_detection.handlers.remove_handler import RemoveHandler
from outlier_detection.handlers.flag_handler import FlagHandler
from outlier_detection.reports.report_generator import ReportGenerator
from outlier_detection.utils.logger import setup_logger
from outlier_detection.utils.exceptions import (
    OutlierError,
    DatasetLoadError,
    EmptyDatasetError,
    MissingColumnError,
    InvalidMethodError,
    InvalidStrategyError,
    InvalidThresholdError
)
from outlier_detection.utils.helpers import (
    load_dataset,
    save_dataset,
    detect_numerical_columns
)

def parse_args():
    parser = argparse.ArgumentParser(description="Enterprise Outlier Detection & Handling Pipeline")
    parser.add_argument("input_file", type=str, help="Path to input CSV or Excel dataset")
    parser.add_argument(
        "--method",
        type=str,
        choices=["zscore", "iqr"],
        default=settings.DEFAULT_DETECTION_METHOD,
        help="Outlier detection method (default: %(default)s)"
    )
    parser.add_argument(
        "--strategy",
        type=str,
        choices=["cap", "remove", "flag"],
        default=settings.DEFAULT_HANDLING_STRATEGY,
        help="Outlier handling strategy (default: %(default)s)"
    )
    parser.add_argument(
        "--keys",
        type=str,
        nargs="+",
        default=None,
        help="Columns to process. If empty, all numerical columns are processed."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Statistical threshold (Z-score limit or IQR multiplier)"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=None,
        help="Path to save processed dataset"
    )
    return parser.parse_args()

def run_pipeline(args) -> int:
    logger = setup_logger()
    start_time = time.time()
    
    input_path = Path(args.input_file)
    logger.info("=" * 60)
    logger.info("Outlier Detection & Handling Pipeline Started")
    logger.info(f"Input File:        {input_path}")
    logger.info(f"Detection Method:  {args.method}")
    logger.info(f"Handling Strategy: {args.strategy}")
    logger.info(f"Requested Keys:    {args.keys}")
    logger.info("=" * 60)

    try:
        # 1. Load Dataset
        df_raw = load_dataset(input_path)
        rows_before = len(df_raw)
        logger.info(f"Dataset loaded. Initial shape: {df_raw.shape}")

        # 2. Columns identification
        if args.keys:
            # Check if all requested keys exist and are numerical
            missing_keys = [k for k in args.keys if k not in df_raw.columns]
            if missing_keys:
                raise MissingColumnError(f"Requested column(s) not in dataset: {missing_keys}")
            
            non_num_keys = [k for k in args.keys if not pd.api.types.is_numeric_dtype(df_raw[k])]
            if non_num_keys:
                raise MissingColumnError(f"Requested column(s) are not numerical: {non_num_keys}")
            
            target_cols = args.keys
        else:
            target_cols = detect_numerical_columns(df_raw)
            if not target_cols:
                raise OutlierError("No numerical columns detected in the dataset.")
            logger.info(f"Auto-detected numerical columns: {target_cols}")

        # 3. Resolve Threshold
        if args.threshold is not None:
            threshold = args.threshold
        else:
            threshold = (
                settings.DEFAULT_Z_SCORE_THRESHOLD 
                if args.method == "zscore" 
                else settings.DEFAULT_IQR_MULTIPLIER
            )
            
        # 4. Instantiate Detector
        if args.method == "zscore":
            detector = ZScoreDetector(threshold=threshold)
        elif args.method == "iqr":
            detector = IQRDetector(multiplier=threshold)
        else:
            raise InvalidMethodError(f"Unsupported outlier detection method: {args.method}")

        # 5. Instantiate Handler
        if args.strategy == "cap":
            handler = CapHandler()
        elif args.strategy == "remove":
            handler = RemoveHandler()
        elif args.strategy == "flag":
            handler = FlagHandler()
        else:
            raise InvalidStrategyError(f"Unsupported handling strategy: {args.strategy}")

        # 6. Run pipeline on target columns
        results: List[OutlierResult] = []
        df_processed = df_raw.copy()
        
        # Track rows removed per column
        rows_removed_dict = {}
        
        for col in target_cols:
            # Run detection (always on the original raw column values for consistency)
            res = detector.detect(df_raw, col)
            results.append(res)
            
            # Apply handling strategy
            rows_pre_handle = len(df_processed)
            df_processed = handler.handle(df_processed, res)
            rows_post_handle = len(df_processed)
            
            rows_removed_dict[col] = rows_pre_handle - rows_post_handle

        rows_after = len(df_processed)
        total_outliers = sum(r.outlier_count for r in results)

        # 7. Output files resolution
        if args.output_file:
            output_path = Path(args.output_file)
        else:
            output_path = settings.OUTPUT_DIR / f"cleaned_{input_path.stem}{input_path.suffix}"

        # 8. Save output dataset
        save_dataset(df_processed, output_path)
        logger.info(f"Saved processed dataset to {output_path}")

        # 9. Reports generation
        ReportGenerator.generate_audit_log(
            results=results,
            handling_strategy=args.strategy,
            rows_removed_dict=rows_removed_dict,
            output_csv_path=settings.AUDIT_LOG_FILE
        )
        
        ReportGenerator.generate_summary_report(
            status="SUCCESS",
            detection_method=args.method,
            handling_strategy=args.strategy,
            rows_before=rows_before,
            rows_after=rows_after,
            results=results,
            output_json_path=settings.REPORT_JSON_FILE
        )

        duration = time.time() - start_time
        
        # 10. Run CLI print summary
        print("\n" + "=" * 50)
        print("OUTLIER PIPELINE RUN SUMMARY")
        print("=" * 50)
        print(f"Status:               SUCCESS")
        print(f"Method:               {args.method} (threshold: {threshold})")
        print(f"Strategy:             {args.strategy}")
        print(f"Rows Before:          {rows_before}")
        print(f"Rows After:           {rows_after}")
        print(f"Rows Removed:         {rows_before - rows_after}")
        print(f"Outliers Detected:    {total_outliers}")
        print(f"Processed Columns:    {', '.join(target_cols)}")
        print(f"Processed Dataset:    {output_path.resolve()}")
        print(f"Audit Trail:          {settings.AUDIT_LOG_FILE.resolve()}")
        print(f"Report:               {settings.REPORT_JSON_FILE.resolve()}")
        print(f"Execution Time:       {duration:.3f} seconds")
        print("=" * 50 + "\n")
        
        logger.info("Pipeline completed successfully.")
        return 0

    except OutlierError as e:
        logger.error(f"Pipeline execution aborted: {str(e)}")
        ReportGenerator.generate_summary_report(
            status="ERROR",
            detection_method=args.method,
            handling_strategy=args.strategy,
            rows_before=0,
            rows_after=0,
            results=[],
            output_json_path=settings.REPORT_JSON_FILE,
            error_message=str(e)
        )
        return 1
    except Exception as e:
        logger.exception("An unexpected error occurred during execution:")
        ReportGenerator.generate_summary_report(
            status="ERROR",
            detection_method=args.method,
            handling_strategy=args.strategy,
            rows_before=0,
            rows_after=0,
            results=[],
            output_json_path=settings.REPORT_JSON_FILE,
            error_message=f"Unexpected error: {str(e)}"
        )
        return 1

if __name__ == "__main__":
    args = parse_args()
    sys.exit(run_pipeline(args))
