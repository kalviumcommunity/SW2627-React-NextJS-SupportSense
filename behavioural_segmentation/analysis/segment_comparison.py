import logging
import pandas as pd
from typing import Dict, Any

logger = logging.getLogger("behavioural_segmentation.analysis.segment_comparison")

def identify_top_performers(df_ranked: pd.DataFrame) -> Dict[str, str]:
    """
    Identifies highest and lowest performing segments for each key metric.
    """
    if df_ranked.empty:
        return {}

    # Highest and lowest LTV
    highest_ltv_seg = df_ranked.loc[df_ranked["avg_ltv"].idxmax(), "segment"]
    lowest_ltv_seg = df_ranked.loc[df_ranked["avg_ltv"].idxmin(), "segment"]

    # Highest and lowest Churn
    highest_churn_seg = df_ranked.loc[df_ranked["churn_rate"].idxmax(), "segment"]
    lowest_churn_seg = df_ranked.loc[df_ranked["churn_rate"].idxmin(), "segment"]

    # Highest and lowest Retention
    best_retention_seg = df_ranked.loc[df_ranked["avg_retention"].idxmax(), "segment"]
    lowest_retention_seg = df_ranked.loc[df_ranked["avg_retention"].idxmin(), "segment"]

    return {
        "highest_ltv": highest_ltv_seg,
        "lowest_ltv": lowest_ltv_seg,
        "highest_churn": highest_churn_seg,
        "lowest_churn": lowest_churn_seg,
        "best_retention": best_retention_seg,
        "lowest_retention": lowest_retention_seg
    }

def print_comparison_table(df_ranked: pd.DataFrame) -> None:
    """
    Prints a formatted, readable ASCII comparison table to the console.
    """
    # Create a copy for string formatting to prevent altering internal numeric representations
    format_df = df_ranked.copy()
    
    # Format rules
    format_df["customer_count"] = format_df["customer_count"].apply(lambda x: f"{int(x):,}")
    format_df["avg_ltv"] = format_df["avg_ltv"].apply(lambda x: f"${x:,.2f}")
    format_df["churn_rate"] = format_df["churn_rate"].apply(lambda x: f"{x * 100:.2f}%")
    format_df["avg_retention"] = format_df["avg_retention"].apply(lambda x: f"{x:,.0f} days")
    format_df["avg_tickets"] = format_df["avg_tickets"].apply(lambda x: f"{x:,.1f}")

    print("\n" + "=" * 80)
    print("SEGMENT COMPARISON SUMMARY")
    print("=" * 80)
    
    # Define columns to print
    cols_to_print = ["segment", "customer_count", "avg_ltv", "churn_rate", "avg_tickets", "avg_retention"]
    
    # Print headers manually aligned or using Pandas built-in to_string for alignment
    print(format_df[cols_to_print].to_string(index=False))
    
    print("=" * 80 + "\n")
