import pandas as pd
import logging
import argparse
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def ingest(file_path):
    """Stage 1: Load raw data."""
    logger.info("Ingesting data from: " + file_path)
    df = pd.read_csv(file_path)
    logger.info("Ingested " + str(len(df)) + " rows")
    return df

def clean(df):
    """Stage 2: Clean and validate."""
    logger.info("Cleaning data...")
    initial = len(df)
    
    # Drop rows missing crucial fields
    df = df.dropna(subset=["customer_id", "amount"])
    
    # Enforce types and positive values
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df[df["amount"] > 0]
    
    # Safely handle missing expected columns for aggregation downstream
    if "segment" not in df.columns:
        df["segment"] = "Unknown"
    if "order_id" not in df.columns:
        df["order_id"] = range(1, len(df) + 1)
        
    logger.info("Cleaned: " + str(initial) + " -> " + str(len(df)) + " rows")
    return df

def aggregate(df):
    """Stage 3: Compute aggregations."""
    logger.info("Aggregating...")
    agg = df.groupby("segment").agg(
        total_revenue=("amount", "sum"),
        order_count=("order_id", "count"),
        avg_order=("amount", "mean")
    ).reset_index()
    logger.info("Aggregated " + str(len(agg)) + " segments")
    return agg

def output(df, agg, output_dir):
    """Stage 4: Write output files."""
    os.makedirs(output_dir, exist_ok=True)
    logger.info("Writing output to: " + output_dir)
    df.to_csv(os.path.join(output_dir, "cleaned_data.csv"), index=False)
    agg.to_csv(os.path.join(output_dir, "aggregated_metrics.csv"), index=False)
    logger.info("Pipeline complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to raw data CSV")
    parser.add_argument("--output", default="output", help="Directory for processed output files")
    args = parser.parse_args()
    
    try:
        raw = ingest(args.input)
        cleaned = clean(raw)
        agg = aggregate(cleaned)
        output(cleaned, agg, args.output)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
