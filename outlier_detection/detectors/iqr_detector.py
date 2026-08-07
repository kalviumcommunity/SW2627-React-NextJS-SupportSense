import logging
import pandas as pd
from outlier_detection.detectors.base_detector import BaseDetector, OutlierResult
from outlier_detection.utils.exceptions import InvalidThresholdError

logger = logging.getLogger("outlier_detection.detectors.iqr_detector")

class IQRDetector(BaseDetector):
    def __init__(self, multiplier: float = 1.5):
        if multiplier <= 0:
            raise InvalidThresholdError(f"IQR multiplier must be greater than zero. Received: {multiplier}")
        self.multiplier = multiplier

    def detect(self, df: pd.DataFrame, column: str) -> OutlierResult:
        """
        Detects outliers using the Interquartile Range (IQR) method.
        """
        series = df[column]

        # Calculate percentiles
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        logger.info(f"Running IQR outlier detection on column '{column}' with multiplier {self.multiplier}")

        if pd.isna(iqr) or iqr == 0:
            logger.warning(
                f"Column '{column}' has an IQR of 0. Outlier detection might flag non-extreme values. "
                "Proceeding with bounds set around the constant value."
            )
            # When IQR is 0, bounds collapse to the single percentile value.
            lower_bound = q1
            upper_bound = q3
            # If all values are identical, outlier mask is all False.
            # Otherwise, any value different from the constant could be an outlier.
            # To be safe, we only flag values outside [q1, q3]
            outlier_mask = (series < lower_bound) | (series > upper_bound)
        else:
            lower_bound = q1 - self.multiplier * iqr
            upper_bound = q3 + self.multiplier * iqr
            outlier_mask = (series < lower_bound) | (series > upper_bound)
        
        # Ensure NaNs are not flagged
        outlier_mask = outlier_mask.fillna(False)

        outlier_count = int(outlier_mask.sum())
        total_count = len(series)
        outlier_percentage = float(outlier_count / total_count) if total_count > 0 else 0.0

        logger.info(
            f"IQR detection completed for '{column}': Found {outlier_count} outliers "
            f"({outlier_percentage * 100:.2f}%) with bounds [{lower_bound:.4f}, {upper_bound:.4f}]"
        )

        return OutlierResult(
            column=column,
            outlier_mask=outlier_mask,
            outlier_count=outlier_count,
            outlier_percentage=outlier_percentage,
            lower_bound=float(lower_bound),
            upper_bound=float(upper_bound),
            method="iqr",
            threshold=self.multiplier
        )
