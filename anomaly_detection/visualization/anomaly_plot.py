import logging
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

logger = logging.getLogger("anomaly_detection.visualization.anomaly_plot")

def plot_anomalies(df: pd.DataFrame, metric_col: str, anomaly_mask: pd.Series, output_path: Path) -> None:
    """
    Creates a professional time-series visualization showing raw data,
    rolling averages, expected standard deviation boundaries, and highlighting anomalies.
    """
    logger.info(f"Generating anomaly visualization plot for '{metric_col}'.")
    
    plt.figure(figsize=(12, 6))
    
    # Ensure dates are datetime for plotting
    dates = pd.to_datetime(df["date"])
    
    # 1. Plot raw time series
    plt.plot(dates, df[metric_col], label="Raw Data", color="steelblue", marker="o", markersize=4, linestyle="-", linewidth=1.5)
    
    # 2. Plot expected range boundaries (mean +/- 2 std) as shaded area
    plt.fill_between(
        dates, 
        df["expected_lower_bound"], 
        df["expected_upper_bound"], 
        color="lightgray", 
        alpha=0.4, 
        label="Expected Range (±2 Std Dev)"
    )
    
    # 3. Plot 7-day rolling average
    plt.plot(dates, df["rolling_mean"], label="7-Day Rolling Avg", color="darkorange", linestyle="--", linewidth=2)
    
    # 4. Highlight anomalies
    anomalies_df = df[anomaly_mask]
    if not anomalies_df.empty:
        anomaly_dates = pd.to_datetime(anomalies_df["date"])
        plt.scatter(
            anomaly_dates, 
            anomalies_df[metric_col], 
            color="red", 
            s=100, 
            zorder=5, 
            label="Statistical Anomaly (|Z| > 2)",
            edgecolors="black"
        )
        
        # Annotate top 5 extreme anomalies to avoid clutter
        anomalies_df = anomalies_df.copy()
        # Sort by absolute Z-score (approximated by distance from mean if z-score not precalculated here, but we can compute it on the fly)
        anomalies_df["abs_z"] = abs((anomalies_df[metric_col] - anomalies_df["rolling_mean"]) / anomalies_df["rolling_std"])
        top_anomalies = anomalies_df.sort_values(by="abs_z", ascending=False).head(5)
        
        for _, row in top_anomalies.iterrows():
            plt.annotate(
                f"{row[metric_col]:,.0f}", 
                (pd.to_datetime(row["date"]), row[metric_col]),
                textcoords="offset points", 
                xytext=(0, 10), 
                ha='center',
                fontsize=9,
                color="darkred",
                fontweight="bold"
            )
            
    # Styling
    plt.title(f"Anomaly Detection: {metric_col.replace('_', ' ').title()}", fontsize=16, pad=20)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.legend(loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.6)
    
    # Rotate dates
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    logger.info(f"Anomaly plot saved successfully to {output_path}")
