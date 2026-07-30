import chardet
from pathlib import Path
from typing import Tuple, Dict, Any, Optional

def detect_encoding(file_path: Path) -> Tuple[Optional[str], float, Optional[str]]:
    """
    Detects the encoding of a text file using chardet.
    
    Args:
        file_path (Path): Path to the dataset file.
        
    Returns:
        Tuple[Optional[str], float, Optional[str]]: 
            - Detected encoding (str)
            - Confidence level (float)
            - Error message (str) if an issue occurs.
    """
    # Encoding detection only applies to text-based files like CSV and JSON
    if file_path.suffix.lower() not in [".csv", ".json"]:
        return None, 0.0, None
        
    try:
        with open(file_path, 'rb') as f:
            # Read first 100KB for faster detection
            raw_data = f.read(100000)
            
        result = chardet.detect(raw_data)
        encoding = result.get('encoding')
        confidence = result.get('confidence', 0.0)
        
        if not encoding:
            return None, 0.0, "Could not detect encoding"
            
        return encoding, confidence, None
        
    except Exception as e:
        return None, 0.0, f"Exception during encoding detection: {str(e)}"
