import logging
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger("behavioural_segmentation.visualization.heatmap")

def generate_comparison_heatmap(df_metrics: pd.DataFrame, output_path: Path) -> None:
    """
    Generates and saves a normalized heatmap comparing key segment metrics.
    Normalization (Min-Max scaling) is applied so metrics of different scales 
    (like LTV in $100k vs Churn in 0.05) can be visually compared using color intensity.
    """
    logger.info(f"Generating normalized segment comparison heatmap at {output_path}")
    
    # Columns to include in the heatmap
    metric_cols = ["avg_ltv", "churn_rate", "avg_tickets", "avg_retention"]
    
    # Extract data
    heatmap_data = df_metrics.set_index("segment")[metric_cols].copy()
    
    # Min-Max Normalization per column
    # Normalization formula: (x - min) / (max - min)
    normalized_data = heatmap_data.copy()
    for col in metric_cols:
        min_val = heatmap_data[col].min()
        max_val = heatmap_data[col].max()
        if max_val > min_val:
            normalized_data[col] = (heatmap_data[col] - min_val) / (max_val - min_val)
        else:
            # If all values are identical, set to 0.5 for neutral color
            normalized_data[col] = 0.5
            
    # Set up matplotlib figure
    plt.figure(figsize=(10, 6))
    
    # Generate heatmap
    ax = sns.heatmap(
        normalized_data, 
        annot=heatmap_data, # Annotate with actual raw values, not normalized values
        fmt=".2f",
        cmap="YlGnBu", 
        linewidths=.5,
        cbar_kws={'label': 'Normalized Intensity (Min-Max Scaling)'}
    )
    
    plt.title("Segment Behavioral Comparison Heatmap", pad=20, fontsize=14)
    plt.xlabel("Metrics", labelpad=10)
    plt.ylabel("Segments", labelpad=10)
    
    # Improve tick labels
    ax.set_xticklabels(["Avg LTV", "Churn Rate", "Avg Tickets", "Avg Retention"], rotation=0)
    plt.tight_layout()
    
    # Save visualization
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    logger.info("Heatmap successfully saved.")
