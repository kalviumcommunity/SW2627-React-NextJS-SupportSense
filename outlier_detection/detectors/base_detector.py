from abc import ABC, abstractmethod
from dataclasses import dataclass
import pandas as pd

@dataclass
class OutlierResult:
    column: str
    outlier_mask: pd.Series  # Boolean Series indicating outliers
    outlier_count: int
    outlier_percentage: float
    lower_bound: float
    upper_bound: float
    method: str
    threshold: float

class BaseDetector(ABC):
    """
    Abstract interface for all outlier detection methods.
    """
    @abstractmethod
    def detect(self, df: pd.DataFrame, column: str) -> OutlierResult:
        """
        Runs outlier detection on a single column of the DataFrame.
        Returns an OutlierResult instance.
        """
        pass
