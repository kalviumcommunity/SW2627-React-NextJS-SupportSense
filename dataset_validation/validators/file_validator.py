import os
from pathlib import Path
from typing import Tuple

def validate_file_exists(file_path: Path) -> Tuple[bool, str]:
    """
    Validates that the file exists and is not empty.
    
    Args:
        file_path (Path): Path to the file.
        
    Returns:
        Tuple[bool, str]: A boolean indicating success, and an error message if any.
    """
    if not file_path.exists():
        return False, f"File not found: {file_path}"
        
    if not file_path.is_file():
        return False, f"Path is not a file: {file_path}"
        
    if os.path.getsize(file_path) == 0:
        return False, f"File is empty: {file_path}"
        
    return True, ""
