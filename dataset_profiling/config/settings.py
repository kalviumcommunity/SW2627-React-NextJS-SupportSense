"""
Configuration settings for the Dataset Profiling Framework.
Contains default thresholds and global settings.
"""

from dataclasses import dataclass

@dataclass
class ProfilerSettings:
    """Settings and thresholds for the profiler."""
    # Threshold for flagging columns with high null percentages (0-100)
    NULL_THRESHOLD: float = 30.0
    
    # Threshold for flagging high duplicate row percentages (0-100)
    DUPLICATE_THRESHOLD: float = 5.0
    
    # Threshold for defining a column as high cardinality
    HIGH_CARDINALITY_THRESHOLD: int = 100
    
    # Threshold for skewness (absolute value) to flag as highly skewed
    SKEWNESS_THRESHOLD: float = 3.0
    
    # Threshold for kurtosis (absolute value) to flag as having heavy tails
    KURTOSIS_THRESHOLD: float = 10.0
    
    # Output directory for reports
    REPORTS_DIR: str = "reports"
    
    # Default report filename
    DEFAULT_REPORT_FILENAME: str = "profile_report.json"
    
    # Maximum number of duplicate samples to include in the report
    MAX_DUPLICATE_SAMPLES: int = 5

# Global instance of settings
SETTINGS = ProfilerSettings()
