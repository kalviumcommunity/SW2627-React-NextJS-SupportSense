import logging
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger("behavioural_segmentation.visualization.comparison_charts")

def generate_comparison_charts(df_metrics: pd.DataFrame, output_dir: Path) -> None:
    """
    Generates individual comparative bar charts for each major segment metric.
    """
    logger.info(f"Generating individual metric bar charts at {output_dir}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set global plotting style
    sns.set_theme(style="whitegrid")
    
    metrics = [
        {"col": "avg_ltv", "title": "Average Lifetime Value (LTV) by Segment", "ylabel": "LTV ($)", "filename": "ltv_by_segment.png", "color": "skyblue"},
        {"col": "churn_rate", "title": "Churn Rate by Segment", "ylabel": "Churn Rate (Ratio)", "filename": "churn_by_segment.png", "color": "salmon"},
        {"col": "avg_tickets", "title": "Average Support Tickets by Segment", "ylabel": "Average Tickets", "filename": "tickets_by_segment.png", "color": "lightgreen"},
        {"col": "avg_retention", "title": "Average Retention Days by Segment", "ylabel": "Retention (Days)", "filename": "retention_by_segment.png", "color": "orange"}
    ]
    
    for metric in metrics:
        plt.figure(figsize=(8, 5))
        
        # Sort values for better visual comparison (highest to lowest)
        plot_data = df_metrics.sort_values(by=metric["col"], ascending=False)
        
        ax = sns.barplot(
            x="segment", 
            y=metric["col"], 
            data=plot_data, 
            color=metric["color"]
        )
        
        plt.title(metric["title"], pad=15, fontsize=14)
        plt.xlabel("Segment", labelpad=10)
        plt.ylabel(metric["ylabel"], labelpad=10)
        
        # Add value annotations on top of bars
        for p in ax.patches:
            val = p.get_height()
            if metric["col"] == "avg_ltv":
                label = f"${val:,.0f}"
            elif metric["col"] == "churn_rate":
                label = f"{val*100:.1f}%"
            else:
                label = f"{val:,.1f}"
                
            ax.annotate(
                label, 
                (p.get_x() + p.get_width() / 2., val), 
                ha='center', va='bottom', 
                xytext=(0, 5), 
                textcoords='offset points',
                fontsize=10
            )
            
        plt.tight_layout()
        out_file = output_dir / metric["filename"]
        plt.savefig(out_file, dpi=300, bbox_inches="tight")
        plt.close()
        
    logger.info("Individual metric comparison charts saved successfully.")
