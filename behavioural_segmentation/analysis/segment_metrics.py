import logging
import pandas as pd
import numpy as np
from typing import Tuple

logger = logging.getLogger("behavioural_segmentation.analysis.segment_metrics")

def calculate_segment_metrics(df: pd.DataFrame, segment_column: str) -> pd.DataFrame:
    """
    Groups the dataframe by the segment column and calculates key business metrics.
    Ensures safe casting of the churn column before calculating rates.
    """
    logger.info(f"Calculating segment metrics grouped by '{segment_column}'.")
    
    # Work on a copy to avoid modifying original dataframe
    working_df = df.copy()

    # Safely parse churn to numeric 1/0 for mean calculation
    if pd.api.types.is_object_dtype(working_df["churn"]) or pd.api.types.is_string_dtype(working_df["churn"]):
        str_churn = working_df["churn"].astype(str).str.strip().str.lower()
        # Map common string representations of True to 1, False to 0
        working_df["churn_numeric"] = str_churn.map({"true": 1, "yes": 1, "1": 1, "y": 1, "false": 0, "no": 0, "0": 0, "n": 0})
        # If mapping fails and yields NaN, fallback to numeric conversion
        if working_df["churn_numeric"].isna().any():
            working_df["churn_numeric"] = pd.to_numeric(working_df["churn"], errors="coerce").fillna(0)
    elif pd.api.types.is_bool_dtype(working_df["churn"]):
        working_df["churn_numeric"] = working_df["churn"].astype(int)
    else:
        # It is already numeric
        working_df["churn_numeric"] = pd.to_numeric(working_df["churn"], errors="coerce").fillna(0)

    # Ensure other columns are numeric
    for col in ["lifetime_value", "support_tickets", "retention_days"]:
        working_df[col] = pd.to_numeric(working_df[col], errors="coerce").fillna(0)
    
    # Calculate aggregate metrics
    agg_funcs = {
        "lifetime_value": "mean",
        "churn_numeric": "mean",
        "support_tickets": "mean",
        "retention_days": "mean",
        "customer_id": "count"
    }

    segment_metrics = working_df.groupby(segment_column).agg(agg_funcs).reset_index()

    # Rename columns to clearly match requirements
    segment_metrics.rename(columns={
        segment_column: "segment",
        "lifetime_value": "avg_ltv",
        "churn_numeric": "churn_rate",
        "support_tickets": "avg_tickets",
        "retention_days": "avg_retention",
        "customer_id": "customer_count"
    }, inplace=True)

    # Calculate customer percentage
    total_customers = segment_metrics["customer_count"].sum()
    segment_metrics["customer_percentage"] = (segment_metrics["customer_count"] / total_customers) * 100.0 if total_customers > 0 else 0.0

    # Reorder columns for logical presentation
    column_order = [
        "segment", "customer_count", "customer_percentage", 
        "avg_ltv", "churn_rate", "avg_tickets", "avg_retention"
    ]
    segment_metrics = segment_metrics[column_order]

    logger.info(f"Successfully calculated metrics for {len(segment_metrics)} segments.")
    return segment_metrics
