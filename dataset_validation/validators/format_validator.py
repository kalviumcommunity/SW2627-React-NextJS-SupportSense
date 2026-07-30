from pathlib import Path
from typing import Tuple
from dataset_validation.config.settings import Settings

def validate_format(file_path: Path) -> Tuple[bool, str]:
    """
    Validates that the file has a supported extension.
    
    Args:
        file_path (Path): Path to the dataset file.
        
    Returns:
        Tuple[bool, str]: A boolean indicating success, and an error message if any.
    """
    ext = file_path.suffix.lower()
    if ext not in Settings.SUPPORTED_FORMATS:
        return False, f"Unsupported format '{ext}'. Supported formats: {Settings.SUPPORTED_FORMATS}"
        
    return True, ""
