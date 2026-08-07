import logging
import pandas as pd
from outlier_detection.detectors.base_detector import BaseDetector, OutlierResult
from outlier_detection.utils.exceptions import InvalidThresholdError

logger = logging.getLogger("outlier_detection.detectors.zscore_detector")

class ZScoreDetector(BaseDetector):
    def __init__(self, threshold: float = 3.0):
        if threshold <= 0:
            raise InvalidThresholdError(f"Z-score threshold must be greater than zero. Received: {threshold}")
        self.threshold = threshold

    def detect(self, df: pd.DataFrame, column: str) -> OutlierResult:
        """
        Detects outliers using Z-score method: abs(z_score) > threshold.
        """
        series = df[column]
        
        # Calculate statistics
        mean = series.mean()
        std = series.std(ddof=1)  # Sample standard deviation

        logger.info(f"Running Z-Score outlier detection on column '{column}' with threshold {self.threshold}")
        
        if pd.isna(std) or std == 0:
            logger.warning(
                f"Column '{column}' has zero or NaN standard deviation (no variance). "
                "Outlier detection skipped for this column."
            )
            # Set bounds to mean
            lower_bound = mean
            upper_bound = mean
            outlier_mask = pd.Series(False, index=df.index)
        else:
            lower_bound = mean - self.threshold * std
            upper_bound = mean + self.threshold * std
            
            # Calculate Z-scores (handle NaNs gracefully by treating them as False in mask)
            z_scores = (series - mean) / std
            outlier_mask = z_scores.abs() > self.threshold
            # Ensure NaN values are not flagged as outliers
            outlier_mask = outlier_mask.fillna(False)

        outlier_count = int(outlier_mask.sum())
        total_count = len(series)
        outlier_percentage = float(outlier_count / total_count) if total_count > 0 else 0.0

        logger.info(
            f"Z-Score detection completed for '{column}': Found {outlier_count} outliers "
            f"({outlier_percentage * 100:.2f}%) with bounds [{lower_bound:.4f}, {upper_bound:.4f}]"
        )

        return OutlierResult(
            column=column,
            outlier_mask=outlier_mask,
            outlier_count=outlier_count,
            outlier_percentage=outlier_percentage,
            lower_bound=float(lower_bound),
            upper_bound=float(upper_bound),
            method="zscore",
            threshold=self.threshold
        )
