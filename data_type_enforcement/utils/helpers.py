import json
import numpy as np

class NpEncoder(json.JSONEncoder):
    """
    Custom JSON Encoder for NumPy datatypes to ensure compatibility
    when writing reports to JSON.
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super(NpEncoder, self).default(obj)

def save_json(data: dict, filepath: str) -> None:
    """Safely writes dictionary data to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, cls=NpEncoder, indent=4)
