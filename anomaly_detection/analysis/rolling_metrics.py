import logging
import pandas as pd
from typing import Tuple

logger = logging.getLogger("anomaly_detection.analysis.rolling_metrics")

def calculate_rolling_metrics(df: pd.DataFrame, metric_col: str, window: int = 7) -> pd.DataFrame:
    """
    Calculates 7-day rolling mean and standard deviation for a given metric.
    Avoids incorrectly labeling the initial incomplete rolling periods.
    """
    logger.info(f"Calculating {window}-day rolling statistics for '{metric_col}'.")
    
    df_metrics = df.copy()
    
    # Calculate rolling statistics
    df_metrics["rolling_mean"] = df_metrics[metric_col].rolling(window=window, min_periods=window).mean()
    df_metrics["rolling_std"] = df_metrics[metric_col].rolling(window=window, min_periods=window).std()
    
    # Calculate expected bounds
    df_metrics["expected_lower_bound"] = df_metrics["rolling_mean"] - (2 * df_metrics["rolling_std"])
    df_metrics["expected_upper_bound"] = df_metrics["rolling_mean"] + (2 * df_metrics["rolling_std"])
    
    return df_metrics

def apply_lookback_window(df: pd.DataFrame, lookback_days: int) -> pd.DataFrame:
    """
    Filters the dataset to the most recent X days for primary anomaly analysis.
    """
    if len(df) <= lookback_days:
        logger.info(f"Dataset length ({len(df)}) is less than or equal to lookback period ({lookback_days}). Using all available data.")
        return df.copy()
        
    logger.info(f"Applying lookback window of the most recent {lookback_days} days.")
    # Since it's sorted chronologically, tail gives the most recent records
    return df.tail(lookback_days).copy().reset_index(drop=True)
