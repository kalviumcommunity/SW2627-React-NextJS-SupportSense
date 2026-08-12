import logging
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from anomaly_detection.detection.severity import classify_severity

logger = logging.getLogger("anomaly_detection.detection.zscore_detector")

def detect_anomalies_zscore(df: pd.DataFrame, metric_col: str, z_threshold: float = 2.0) -> Tuple[List[Dict[str, Any]], pd.Series]:
    """
    Identifies statistical anomalies using Z-scores based on rolling statistics.
    Returns the list of anomaly alert dictionaries and a boolean mask indicating anomalies.
    """
    logger.info(f"Running Z-score statistical anomaly detection for '{metric_col}'.")
    alerts = []
    
    # Initialize a mask of all False
    anomaly_mask = pd.Series(False, index=df.index)
    
    for idx, row in df.iterrows():
        val = row[metric_col]
        mean = row["rolling_mean"]
        std = row["rolling_std"]
        date_str = row["date"].strftime("%Y-%m-%d") if pd.notna(row["date"]) else "Unknown Date"
        
        # Skip detection if required stats are missing (e.g. beginning of rolling window)
        if pd.isna(val) or pd.isna(mean) or pd.isna(std):
            continue
            
        if std == 0:
            # Cannot calculate Z-score when variance is exactly zero
            # We log but do not crash.
            continue
            
        z_score = (val - mean) / std
        
        if abs(z_score) > z_threshold:
            anomaly_mask[idx] = True
            severity = classify_severity(z_score)
            
            alerts.append({
                "timestamp": pd.Timestamp.utcnow().isoformat(),
                "anomaly_date": date_str,
                "metric": metric_col,
                "value": val,
                "mean": mean,
                "standard_deviation": std,
                "expected_range": f"{row['expected_lower_bound']:.2f} to {row['expected_upper_bound']:.2f}",
                "z_score": z_score,
                "severity": severity,
                "detection_method": "STATISTICAL_ZSCORE",
                "status": "OPEN"
            })
            
    logger.info(f"Detected {len(alerts)} statistical anomalies for '{metric_col}'.")
    return alerts, anomaly_mask
