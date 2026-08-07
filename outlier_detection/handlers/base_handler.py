from abc import ABC, abstractmethod
import pandas as pd
from outlier_detection.detectors.base_detector import OutlierResult

class BaseHandler(ABC):
    """
    Abstract interface for outlier handling strategies.
    All handlers must implement the handle method, returning a new copy of the DataFrame.
    """
    @abstractmethod
    def handle(self, df: pd.DataFrame, result: OutlierResult) -> pd.DataFrame:
        """
        Applies a specific outlier handling strategy (e.g. cap, remove, flag).
        Returns a copy of the DataFrame with the strategy applied.
        """
        pass
