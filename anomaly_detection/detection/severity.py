def classify_severity(z_score: float) -> str:
    """
    Assigns severity based on the absolute Z-score of a statistical anomaly.
    | Absolute Z-score | Severity |
    |------------------|----------|
    | <= 1.5           | LOW      |
    | > 1.5 and <= 2   | MEDIUM   |
    | > 2 and <= 3     | HIGH     |
    | > 3              | CRITICAL |
    
    Note: Standard detection processes generally only trigger on |Z| > 2.
    """
    abs_z = abs(z_score)
    
    if abs_z <= 1.5:
        return "LOW"
    elif abs_z <= 2.0:
        return "MEDIUM"
    elif abs_z <= 3.0:
        return "HIGH"
    else:
        return "CRITICAL"
