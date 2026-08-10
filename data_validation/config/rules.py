import re
import pandas as pd
from typing import List, Dict, Any, Tuple, Callable

# Required columns (Null validation)
REQUIRED_COLUMNS: List[str] = [
    "customer_id",
    "email"
]

# Range validation boundaries (Min, Max or Min-only, Max-only)
RANGE_RULES: Dict[str, Dict[str, float]] = {
    "age": {"min": 0, "max": 120},
    "price": {"min": 0.0},
    "quantity": {"min": 1.0},
    "discount": {"min": 0.0}
}

# Format validation regex patterns
FORMAT_PATTERNS: Dict[str, str] = {
    "email": r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    "phone": r"^\d{10}$",
    "customer_id": r"^CUST-\d{3}$",
    "order_id": r"^ORD-\d{4}$"
}

# Referential integrity rules
REFERENTIAL_RULES: List[Dict[str, str]] = [
    {
        "child_foreign_key": "customer_id",
        "parent_dataset": "sample_data/customers.csv",
        "parent_key": "customer_id"
    }
]

# Reusable business rule functions returning a boolean mask (True = Pass, False = Fail)
def validate_date_order(df: pd.DataFrame) -> pd.Series:
    """
    Validates end_date >= start_date.
    If either start_date or end_date is missing or invalid, we treat it as passing
    since the null validator handles missingness, and invalid datetime values parse to NaT.
    """
    if "start_date" not in df.columns or "end_date" not in df.columns:
        return pd.Series(True, index=df.index)
        
    start = pd.to_datetime(df["start_date"], errors="coerce")
    end = pd.to_datetime(df["end_date"], errors="coerce")
    
    # Pass if end is after/equal to start, or if either is NaT (null)
    return (end >= start) | (start.isna() | end.isna())

def validate_discount_vs_price(df: pd.DataFrame) -> pd.Series:
    """
    Validates discount <= price.
    """
    if "discount" not in df.columns or "price" not in df.columns:
        return pd.Series(True, index=df.index)
        
    discount = df["discount"].fillna(0.0)
    price = df["price"].fillna(0.0)
    
    return discount <= price

# Registered business rules: (rule_name, function, failure_reason)
BUSINESS_RULES: List[Tuple[str, Callable[[pd.DataFrame], pd.Series], str]] = [
    ("date_order", validate_date_order, "end_date_before_start_date"),
    ("discount_limit", validate_discount_vs_price, "discount_exceeds_price")
]
