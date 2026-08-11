import argparse
import sys
from pathlib import Path
import pandas as pd

# Fix relative imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from behavioural_segmentation.config.settings import REQUIRED_COLUMNS, DEFAULT_SEGMENT_COLUMN, SMALL_SAMPLE_THRESHOLD
from behavioural_segmentation.utils.logger import setup_logger
from behavioural_segmentation.utils.helpers import load_dataset, save_json
from behavioural_segmentation.validation.dataset_validator import validate_dataset, MissingColumnError
from behavioural_segmentation.analysis.segment_metrics import calculate_segment_metrics
from behavioural_segmentation.analysis.segment_ranking import rank_segments
from behavioural_segmentation.analysis.segment_comparison import identify_top_performers, print_comparison_table
from behavioural_segmentation.analysis.insight_generator import generate_insights
from behavioural_segmentation.visualization.heatmap import generate_comparison_heatmap
from behavioural_segmentation.visualization.comparison_charts import generate_comparison_charts

def parse_args():
    parser = argparse.ArgumentParser(description="Behavioural Analysis & User Segmentation Pipeline")
    parser.add_argument("input_file", type=str, help="Path to the input dataset (CSV/Excel)")
    parser.add_argument("--segment-by", type=str, default=DEFAULT_SEGMENT_COLUMN, 
                        help="Column to segment by (default: customer_type)")
    return parser.parse_args()

def run_pipeline(args) -> int:
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info("Behavioural Analysis & User Segmentation Started")
    logger.info("=" * 60)
    
    input_path = Path(args.input_file)
    segment_col = args.segment_by
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 1. Load Dataset
        logger.info(f"Loading dataset from: {input_path}")
        df = load_dataset(input_path)
        
        # 2. Validate Dataset
        validate_dataset(df, segment_col, REQUIRED_COLUMNS, logger)
        
        # 3 & 4. Calculate Segment Metrics
        metrics_df = calculate_segment_metrics(df, segment_col)
        
        # 5. Rank Segments
        ranked_df = rank_segments(metrics_df)
        
        # 6. Top/Bottom Performers & Visualization Prep
        top_performers = identify_top_performers(ranked_df)
        print_comparison_table(ranked_df)
        
        # Save Summary CSV
        summary_csv_path = output_dir / "segment_summary.csv"
        ranked_df.to_csv(summary_csv_path, index=False)
        logger.info(f"Saved segment summary to {summary_csv_path}")
        
        # 7. Visualizations
        heatmap_path = output_dir / "segment_comparison_heatmap.png"
        generate_comparison_heatmap(ranked_df, heatmap_path)
        generate_comparison_charts(ranked_df, output_dir)
        
        # 8. Sample Size Warnings & Insights
        warnings = []
        for _, row in ranked_df.iterrows():
            if row["customer_count"] < SMALL_SAMPLE_THRESHOLD:
                warnings.append(
                    f"Segment '{row['segment']}' has only {row['customer_count']:.0f} customers. "
                    "Segment-level conclusions should be treated cautiously."
                )
                logger.warning(warnings[-1])
        
        total_avg_ltv = df["lifetime_value"].mean()
        # Parse global churn dynamically like we did in metrics
        churn_series = df["churn"]
        if pd.api.types.is_object_dtype(churn_series) or pd.api.types.is_string_dtype(churn_series):
            churn_series = churn_series.astype(str).str.strip().str.lower().map({"true": 1, "yes": 1, "1": 1, "y": 1, "false": 0, "no": 0, "0": 0, "n": 0})
        total_avg_churn = churn_series.mean()
        
        insights = generate_insights(ranked_df, total_avg_ltv, total_avg_churn)
        
        # 9. Structured Reports
        insights_path = output_dir / "segment_insights.json"
        save_json(insights, insights_path)
        logger.info(f"Saved insights to {insights_path}")
        
        # Format segments payload for the JSON report
        segments_payload = {}
        for _, row in ranked_df.iterrows():
            segments_payload[row["segment"]] = {
                "customer_count": int(row["customer_count"]),
                "customer_percentage": round(row["customer_percentage"], 2),
                "avg_ltv": float(row["avg_ltv"]),
                "churn_rate": float(row["churn_rate"]),
                "avg_tickets": float(row["avg_tickets"]),
                "avg_retention": float(row["avg_retention"]),
                "ltv_rank": int(row["ltv_rank"]),
                "churn_rank": int(row["churn_rank"]),
                "retention_rank": int(row["retention_rank"])
            }
        
        analysis_report = {
            "analysis_status": "SUCCESS",
            "segment_column": segment_col,
            "segment_count": len(ranked_df),
            "total_customers": int(ranked_df["customer_count"].sum()),
            "segments": segments_payload,
            "top_performers": top_performers,
            "warnings": warnings,
            "insights": insights
        }
        
        report_path = output_dir / "analysis_report.json"
        save_json(analysis_report, report_path)
        logger.info(f"Saved complete analysis report to {report_path}")
        
        logger.info("=" * 60)
        logger.info("Behavioural Analysis Pipeline Completed Successfully")
        logger.info("=" * 60)
        
        return 0

    except Exception as e:
        logger.exception("Pipeline execution failed:")
        return 1

if __name__ == "__main__":
    args = parse_args()
    sys.exit(run_pipeline(args))
