import logging
import pandas as pd

logger = logging.getLogger("anomaly_detection.analysis.aggregation")

def aggregate_daily_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates transaction-level data to daily business metrics.
    Currently groups by date and sums the amount to create daily_revenue.
    """
    logger.info("Aggregating daily business metrics.")
    
    # Ensure date is just the day component if it includes time
    df["date"] = df["date"].dt.normalize()
    
    daily_metrics = df.groupby("date")["amount"].sum().reset_index()
    daily_metrics.rename(columns={"amount": "daily_revenue"}, inplace=True)
    
    # Sort chronologically to ensure time-series operations are valid
    daily_metrics = daily_metrics.sort_values(by="date").reset_index(drop=True)
    
    logger.info(f"Generated daily metrics for {len(daily_metrics)} days.")
    return daily_metrics
