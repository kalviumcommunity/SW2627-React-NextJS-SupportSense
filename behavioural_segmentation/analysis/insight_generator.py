import logging
import pandas as pd
from typing import List, Dict, Any

logger = logging.getLogger("behavioural_segmentation.analysis.insight_generator")

def generate_insights(df_ranked: pd.DataFrame, total_avg_ltv: float, total_avg_churn: float) -> List[Dict[str, str]]:
    """
    Generates rule-based business insights and identifies actionable items.
    """
    logger.info("Generating data-driven business insights per segment.")
    insights = []
    
    for _, row in df_ranked.iterrows():
        segment = row["segment"]
        ltv = row["avg_ltv"]
        churn = row["churn_rate"]
        tickets = row["avg_tickets"]
        retention = row["avg_retention"]
        
        # Analyze magnitude differences
        churn_diff_pct = (churn - total_avg_churn) * 100
        ltv_ratio = ltv / total_avg_ltv if total_avg_ltv > 0 else 1.0
        
        # Rule 1: High Value & Low Churn (e.g. Enterprise)
        if ltv_ratio > 1.2 and churn < total_avg_churn:
            what = f"The '{segment}' segment has an exceptionally high average LTV (${ltv:,.2f}) and below-average churn ({churn*100:.1f}%)."
            characteristic = "High-value, strong retention profile."
            why = "These customers generate disproportionate revenue and are loyal, making them the most profitable cohort."
            action = "Maintain premium support SLAs and implement proactive account management to defend this revenue."
            
        # Rule 2: High Churn & High Tickets (e.g. SMB struggling)
        elif churn > total_avg_churn and tickets > df_ranked["avg_tickets"].mean():
            what = f"The '{segment}' segment shows a high churn rate ({churn*100:.1f}%) combined with high average support tickets ({tickets:.1f})."
            characteristic = "High friction, elevated flight risk."
            why = "The correlation between high ticket volume and high churn suggests onboarding challenges or product friction driving customers away."
            action = "Investigate common support ticket themes for this segment and improve self-service onboarding flows."
            
        # Rule 3: Low LTV & Short Retention (e.g. Startup/Free)
        elif ltv_ratio < 0.8 and retention < df_ranked["avg_retention"].mean():
            what = f"The '{segment}' segment exhibits lower than average LTV (${ltv:,.2f}) and shorter retention ({retention:.0f} days)."
            characteristic = "Low barrier to entry, low commitment."
            why = "This cohort provides volume but lower unit economics, meaning high-touch support models may be unprofitable."
            action = "Transition to scalable, lower-cost self-service models and automated lifecycle email campaigns."
            
        # Default fallback
        else:
            what = f"The '{segment}' segment has an average LTV of ${ltv:,.2f} and a churn rate of {churn*100:.1f}%."
            characteristic = "Average behavioral profile."
            why = "This segment tracks closely to the baseline population averages."
            action = "Continue standard engagement strategies while monitoring for behavioral shifts."
            
        insight = {
            "segment": segment,
            "what_data_shows": what,
            "behavioural_characteristic": characteristic,
            "why_it_matters": why,
            "business_action": action,
            "magnitude_note": f"Churn difference from average: {churn_diff_pct:+.1f} percentage points."
        }
        insights.append(insight)

    return insights
