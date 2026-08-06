class DeduplicationError(Exception):
    """Base exception for all errors within the Deduplication Framework."""
    pass


class EmptyDatasetError(DeduplicationError):
    """Raised when the input dataset has no rows."""
    pass


class MissingColumnError(DeduplicationError):
    """Raised when one or more required columns are missing from the dataset."""
    pass


class InvalidStrategyError(DeduplicationError):
    """Raised when an invalid deduplication strategy is selected or configured."""
    pass
