class ValidationError(Exception):
    """Base exception class for Data Validation framework."""
    pass

class EmptyDatasetError(ValidationError):
    """Raised when the dataset being validated is empty."""
    pass

class MissingColumnError(ValidationError):
    """Raised when a required column or configured validation column is missing from the dataset."""
    pass

class InvalidConfigurationError(ValidationError):
    """Raised when the validation configuration (regex, ranges, rules) is invalid or malformed."""
    pass

class MissingReferenceDatasetError(ValidationError):
    """Raised when referential integrity dataset lookup file cannot be loaded or found."""
    pass

class MissingReferenceKeyError(ValidationError):
    """Raised when referential integrity dataset lookup key is missing in either dataset."""
    pass

class DatasetLoadError(ValidationError):
    """Raised when loading the primary dataset fails."""
    pass
