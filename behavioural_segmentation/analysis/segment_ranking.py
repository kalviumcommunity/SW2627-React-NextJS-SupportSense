import logging
import pandas as pd

logger = logging.getLogger("behavioural_segmentation.analysis.segment_ranking")

def rank_segments(segment_metrics: pd.DataFrame) -> pd.DataFrame:
    """
    Ranks the calculated segments based on numeric metrics.
    Lower numerical rank is better (1 is best).
    """
    logger.info("Ranking segments across LTV, Churn, and Retention metrics.")
    
    df_ranked = segment_metrics.copy()
    
    # Higher LTV is better
    df_ranked["ltv_rank"] = df_ranked["avg_ltv"].rank(ascending=False, method="min").astype(int)
    
    # Lower churn is better
    df_ranked["churn_rank"] = df_ranked["churn_rate"].rank(ascending=True, method="min").astype(int)
    
    # Higher retention is better
    df_ranked["retention_rank"] = df_ranked["avg_retention"].rank(ascending=False, method="min").astype(int)
    
    logger.info("Successfully ranked segments.")
    return df_ranked
