import argparse
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

# Add the parent directory of duplicate_detection to sys.path so absolute imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from duplicate_detection.config.settings import (
    DEFAULT_DUPLICATE_KEYS,
    DEFAULT_STRATEGY,
    AUDIT_FILE_PATH,
    REPORT_FILE_PATH,
    CLEANED_DATA_PATH
)
from duplicate_detection.utils.logger import setup_logger
from duplicate_detection.utils.helpers import load_data, save_csv
from duplicate_detection.utils.exceptions import DeduplicationError
from duplicate_detection.detectors.exact_duplicate_detector import ExactDuplicateDetector
from duplicate_detection.detectors.near_duplicate_detector import NearDuplicateDetector
from duplicate_detection.deduplicators.deduplicate_exact import ExactDeduplicator
from duplicate_detection.deduplicators.deduplicate_near import NearDeduplicator
from duplicate_detection.reports.report_generator import ReportGenerator

logger = setup_logger("main")

def main():
    parser = argparse.ArgumentParser(description="Duplicate Detection & Record Deduplication Framework")
    parser.add_argument("input_file", help="Path to the input dataset (CSV, JSON, Excel)")
    parser.add_argument(
        "--strategy",
        default=DEFAULT_STRATEGY,
        choices=["keep_first", "keep_last", "keep_most_complete"],
        help=f"Deduplication strategy to use (default: {DEFAULT_STRATEGY})"
    )
    parser.add_argument(
        "--keys",
        nargs="+",
        default=DEFAULT_DUPLICATE_KEYS,
        help=f"Key columns for near duplicate detection (default: {DEFAULT_DUPLICATE_KEYS})"
    )
    args = parser.parse_args()

    start_time = time.time()
    logger.info("=" * 60)
    logger.info(f"Duplicate Detection & Deduplication Framework Started")
    logger.info(f"Input file: {args.input_file}")
    logger.info(f"Strategy: {args.strategy}")
    logger.info(f"Key columns: {args.keys}")
    logger.info("=" * 60)

    report_gen = ReportGenerator()
    rows_before = 0

    try:
        input_path = Path(args.input_file)
        
        # 1. Load Dataset
        df_raw = load_data(input_path)
        rows_before = len(df_raw)
        logger.info(f"Successfully loaded dataset with {rows_before} rows and {len(df_raw.columns)} columns.")

        # 2. Detect Duplicates (On Original Raw Data)
        exact_detector = ExactDuplicateDetector()
        near_detector = NearDuplicateDetector(key_columns=args.keys)

        logger.info("Running exact duplicate detection on raw dataset...")
        exact_detect_results = exact_detector.detect(df_raw)
        
        logger.info("Running near duplicate detection on raw dataset...")
        near_detect_results = near_detector.detect(df_raw)

        # 3. Deduplicate Dataset (Non-destructive, creates a cleaned copy)
        # Phase 3a: Exact Deduplication
        exact_deduplicator = ExactDeduplicator(strategy=args.strategy)
        df_exact_cleaned, exact_audit = exact_deduplicator.deduplicate(df_raw)

        # Phase 3b: Near Deduplication (on the result of exact deduplication)
        near_deduplicator = NearDeduplicator(key_columns=args.keys, strategy=args.strategy)
        df_final_cleaned, near_audit = near_deduplicator.deduplicate(df_exact_cleaned)

        # 4. Generate Audit Trail
        combined_audit = exact_audit + near_audit
        report_gen.generate_audit_csv(combined_audit, AUDIT_FILE_PATH)
        logger.info(f"Audit report generated at {AUDIT_FILE_PATH}")

        # 5. Save Cleaned Dataset
        save_csv(df_final_cleaned, CLEANED_DATA_PATH)
        logger.info(f"Saved cleaned dataset to {CLEANED_DATA_PATH}")

        # 6. Post-Validation & Verification
        logger.info("Performing post-deduplication validation...")
        rows_after = len(df_final_cleaned)
        
        # Validate exact duplicates in cleaned data
        post_exact = exact_detector.detect(df_final_cleaned)
        if post_exact["duplicate_count"] > 0:
            logger.warning(
                f"VALIDATION WARNING: Cleaned dataset still contains {post_exact['duplicate_count']} exact duplicates!"
            )
            
        # Validate near duplicates in cleaned data
        post_near = near_detector.detect(df_final_cleaned)
        if post_near["total_near_duplicates"] > 0:
            logger.warning(
                f"VALIDATION WARNING: Cleaned dataset still contains {post_near['total_near_duplicates']} near duplicates on keys {args.keys}!"
            )

        if post_exact["duplicate_count"] == 0 and post_near["total_near_duplicates"] == 0:
            logger.info("VALIDATION SUCCESS: Cleaned dataset has zero duplicate keys or identical rows remaining.")

        # 7. Generate Comparison Report
        json_report = report_gen.generate_json_report(
            status="SUCCESS",
            rows_before=rows_before,
            rows_after=rows_after,
            strategy=args.strategy,
            duplicate_columns=args.keys,
            filepath=REPORT_FILE_PATH
        )

        execution_time = time.time() - start_time
        logger.info(f"Framework execution completed in {execution_time:.3f} seconds.")
        logger.info("=" * 60)

        # Print user summary report to console
        print("\n" + "=" * 50)
        print("DEDUPLICATION RUN SUMMARY")
        print("=" * 50)
        print(f"Status:               {json_report['status']}")
        print(f"Strategy Used:        {json_report['strategy']}")
        print(f"Key Columns:          {', '.join(json_report['duplicate_columns'])}")
        print(f"Rows Before:          {json_report['rows_before']}")
        print(f"Rows After:           {json_report['rows_after']}")
        print(f"Duplicates Removed:   {json_report['duplicates_removed']}")
        print(f"Duplicate Percentage: {json_report['duplicate_percentage']}%")
        print(f"Cleaned Dataset:      {CLEANED_DATA_PATH.resolve()}")
        print(f"Audit Trail:          {AUDIT_FILE_PATH.resolve()}")
        print(f"Execution Time:       {execution_time:.3f} seconds")
        print("=" * 50 + "\n")

    except Exception as e:
        logger.error(f"Execution Error occurred: {str(e)}", exc_info=True)
        # Attempt to write error JSON report
        try:
            report_gen.generate_json_report(
                status="ERROR",
                rows_before=rows_before,
                rows_after=0,
                strategy=args.strategy,
                duplicate_columns=args.keys,
                filepath=REPORT_FILE_PATH,
                error_message=str(e)
            )
        except Exception as inner_err:
            logger.critical(f"Failed to save error JSON report: {str(inner_err)}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
