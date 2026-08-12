import sys
import argparse
from pathlib import Path

# Fix relative imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from anomaly_detection.utils.logger import setup_logger
from anomaly_detection.utils.helpers import load_and_validate_dataset, DataValidationError, DatasetLoadError
from anomaly_detection.analysis.aggregation import aggregate_daily_metrics
from anomaly_detection.analysis.rolling_metrics import calculate_rolling_metrics, apply_lookback_window
from anomaly_detection.detection.threshold_detector import check_thresholds
from anomaly_detection.detection.zscore_detector import detect_anomalies_zscore
from anomaly_detection.reports.report_generator import generate_reports
from anomaly_detection.visualization.anomaly_plot import plot_anomalies
from anomaly_detection.config.alert_rules import ALERT_RULES, LOOKBACK_DAYS, ZSCORE_ANOMALY_THRESHOLD

def parse_args():
    parser = argparse.ArgumentParser(description="Anomaly Detection & Risk Identification Pipeline")
    parser.add_argument("input_file", type=str, help="Path to the input transaction dataset (CSV)")
    return parser.parse_args()

def run_pipeline(args) -> int:
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info("Anomaly Detection Analysis Started")
    logger.info("=" * 60)
    
    input_path = Path(args.input_file)
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 1. Load & Validate Data
        logger.info(f"Loading dataset from: {input_path}")
        df = load_and_validate_dataset(input_path)
        logger.info(f"Loaded {len(df)} transaction rows. Date range: {df['date'].min().date()} to {df['date'].max().date()}")
        
        # 2. Aggregate Daily Metrics
        daily_metrics = aggregate_daily_metrics(df)
        
        # 3. Threshold Detection (Pre-Lookback window to evaluate all if needed, but we apply to lookback)
        # 4. Rolling Statistics
        df_stats = calculate_rolling_metrics(daily_metrics, metric_col="daily_revenue", window=7)
        
        # 5. Lookback Window (Apply to last X days)
        df_lookback = apply_lookback_window(df_stats, lookback_days=LOOKBACK_DAYS)
        
        if df_lookback.empty:
            logger.error("Lookback dataset is empty. Cannot perform analysis.")
            return 1
            
        # 6. Detection Logic
        logger.info("Loaded threshold rules.")
        threshold_alerts = check_thresholds(df_lookback, metric_col="daily_revenue", rules=ALERT_RULES)
        
        logger.info("Starting Z-score analysis.")
        zscore_alerts, anomaly_mask = detect_anomalies_zscore(df_lookback, metric_col="daily_revenue", z_threshold=ZSCORE_ANOMALY_THRESHOLD)
        
        logger.info("Severity classification completed during detection phase.")
        
        # Combine alerts
        all_alerts = threshold_alerts + zscore_alerts
        # Sort alerts chronologically
        all_alerts.sort(key=lambda x: x["anomaly_date"])
        
        # 7. Visualization
        plot_path = output_dir / "anomaly_detection.png"
        logger.info("Generating visualization.")
        plot_anomalies(df_lookback, metric_col="daily_revenue", anomaly_mask=anomaly_mask, output_path=plot_path)
        
        # 8. Reports & Audit Log
        logger.info("Generating Audit log and Reports.")
        generate_reports(
            alerts=all_alerts,
            lookback_days=min(LOOKBACK_DAYS, len(df_lookback)),
            total_observations=len(df_lookback),
            metrics_monitored=["daily_revenue"],
            output_dir=output_dir
        )
        
        logger.info("=" * 60)
        logger.info("Analysis completed successfully.")
        logger.info("=" * 60)
        
        return 0

    except (DataValidationError, DatasetLoadError) as e:
        logger.error(f"Validation failed: {str(e)}")
        return 1
    except Exception as e:
        logger.exception("Pipeline execution failed with an unexpected error:")
        return 1

if __name__ == "__main__":
    args = parse_args()
    sys.exit(run_pipeline(args))
