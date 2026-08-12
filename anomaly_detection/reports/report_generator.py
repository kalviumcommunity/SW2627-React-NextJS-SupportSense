import logging
import json
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger("anomaly_detection.reports.report_generator")

def generate_reports(
    alerts: List[Dict[str, Any]], 
    lookback_days: int, 
    total_observations: int,
    metrics_monitored: List[str],
    output_dir: Path
) -> None:
    """
    Generates the audit log (CSV), JSON report, and prints a business-friendly terminal summary.
    """
    logger.info("Generating anomaly detection reports.")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Calculate summary metrics
    total_anomalies = len(alerts)
    anomaly_rate = (total_anomalies / total_observations * 100) if total_observations > 0 else 0
    
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    threshold_count = 0
    zscore_count = 0
    
    for alert in alerts:
        sev = alert.get("severity")
        if sev in severity_counts:
            severity_counts[sev] += 1
            
        method = alert.get("detection_method", "")
        if method.startswith("THRESHOLD"):
            threshold_count += 1
        elif method.startswith("STATISTICAL_ZSCORE"):
            zscore_count += 1
            
    # 1. Generate JSON Report
    report = {
        "analysis_status": "SUCCESS",
        "analysis_timestamp": pd.Timestamp.utcnow().isoformat(),
        "lookback_days": lookback_days,
        "metrics_monitored": metrics_monitored,
        "total_observations": total_observations,
        "total_anomalies": total_anomalies,
        "anomaly_rate": round(anomaly_rate, 2),
        "severity_counts": severity_counts,
        "threshold_alert_count": threshold_count,
        "zscore_alert_count": zscore_count,
        "anomalies": alerts,
        "warnings": []
    }
    
    json_path = output_dir / "anomaly_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
        
    logger.info(f"JSON report saved to {json_path}")
    
    # 2. Generate Audit Log (CSV)
    csv_path = output_dir / "anomalies_log.csv"
    if alerts:
        df_alerts = pd.DataFrame(alerts)
        df_alerts.to_csv(csv_path, index=False)
    else:
        # Create empty CSV with proper headers
        pd.DataFrame(columns=[
            "timestamp", "anomaly_date", "metric", "value", "mean", 
            "standard_deviation", "expected_range", "z_score", 
            "severity", "detection_method", "status"
        ]).to_csv(csv_path, index=False)
        
    logger.info(f"Anomaly audit log saved to {csv_path}")
    
    # 3. Print Terminal Summary
    print("\n" + "=" * 40)
    print("ANOMALY DETECTION REPORT")
    print("=" * 40)
    print(f"\nLookback period: {lookback_days} days")
    print(f"Metric: {', '.join(metrics_monitored)}")
    print(f"Observations: {total_observations}")
    print(f"Anomalies: {total_anomalies}")
    print(f"Anomaly rate: {anomaly_rate:.1f}%")
    
    print("\n" + "-" * 40)
    print("SEVERITY")
    print("-" * 40)
    print(f"\nCRITICAL: {severity_counts['CRITICAL']}")
    print(f"HIGH: {severity_counts['HIGH']}")
    print(f"MEDIUM: {severity_counts['MEDIUM']}")
    print(f"LOW: {severity_counts['LOW']}")
    
    print("\n" + "-" * 40)
    print("ANOMALIES")
    print("-" * 40)
    
    if total_anomalies == 0:
        print("\nNo anomalies detected.")
    else:
        # Print top 5 or all if few
        for i, alert in enumerate(alerts):
            print(f"\n{alert['anomaly_date']}")
            if alert['metric'] == 'daily_revenue':
                print(f"Revenue: ${alert['value']:,.2f}")
            else:
                print(f"Value: {alert['value']}")
                
            if alert['z_score'] is not None:
                print(f"Z-score: {alert['z_score']:.2f}")
                
            print(f"Severity: {alert['severity']}")
            print(f"Status: {alert['status']}")
            
            # Print cautious interpretation
            if alert['z_score'] is not None:
                z_abs = abs(alert['z_score'])
                direction_word = "below" if alert['z_score'] < 0 else "above"
                print(f"\n[INTERPRETATION]: {alert['metric']} on {alert['anomaly_date']} was significantly {direction_word} the historical mean and exceeded the anomaly boundary. This should be investigated for possible data pipeline failure, system outage, holiday effects, or genuine business shifts. (OBSERVATION -> INVESTIGATION NEEDED)")
            else:
                print(f"\n[INTERPRETATION]: {alert['metric']} on {alert['anomaly_date']} breached static business thresholds. This requires investigation to understand the deviation from expected operational boundaries. (OBSERVATION -> INVESTIGATION NEEDED)")
                
    print("\n" + "=" * 40 + "\n")
