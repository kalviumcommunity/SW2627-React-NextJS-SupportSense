from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd

class BaseValidator(ABC):
    """
    Abstract Base Class for all validators in the framework.
    """
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Executes validation on the given DataFrame.
        Returns a dictionary mapping validation column names to boolean pandas Series
        where True represents passing and False represents failing the validation check.
        """
        pass
