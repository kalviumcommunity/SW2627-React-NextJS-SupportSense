class OutlierError(Exception):
    """Base exception class for Outlier Detection framework."""
    pass

class EmptyDatasetError(OutlierError):
    """Raised when the loaded dataset contains no rows or is empty."""
    pass

class MissingColumnError(OutlierError):
    """Raised when a requested key column is missing from the dataset."""
    pass

class InvalidStrategyError(OutlierError):
    """Raised when an unsupported outlier handling strategy is specified."""
    pass

class InvalidMethodError(OutlierError):
    """Raised when an unsupported outlier detection method is specified."""
    pass

class InvalidThresholdError(OutlierError):
    """Raised when statistical thresholds (Z-score threshold or IQR multiplier) are invalid (e.g. negative)."""
    pass

class ZeroVarianceError(OutlierError):
    """Raised when standard deviation or IQR is zero, making calculations invalid."""
    pass

class DatasetLoadError(OutlierError):
    """Raised when loading the dataset from the filesystem fails."""
    pass
