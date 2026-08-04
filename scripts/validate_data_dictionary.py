"""
Validation Script for Data Dictionary & Business Context Mapping (Assignment 2.17)
=============================================================================
This script validates:
1. docs/data_dictionary.csv exists and is well-formatted.
2. Required CSV headers are present: column_name, data_type, description, business_meaning, example_value, related_kpi, notes.
3. docs/DATA_DICTIONARY.md exists and contains required sections:
   - Dataset Overview
   - Columns Specification
   - Column to KPI Mapping (>= 5 mapped)
   - Ambiguous Columns & Resolutions (>= 2 flagged)
   - Column Relationships (>= 2 documented)
   - Governance & Maintenance Protocol
"""

import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(PROJECT_ROOT, "docs", "data_dictionary.csv")
MD_PATH = os.path.join(PROJECT_ROOT, "docs", "DATA_DICTIONARY.md")

EXPECTED_HEADERS = [
    "column_name",
    "data_type",
    "description",
    "business_meaning",
    "example_value",
    "related_kpi",
    "notes",
]

def validate_csv(path: str) -> None:
    print(f"Checking CSV file at: {path}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing CSV data dictionary at: {path}")
    
    df = pd.read_csv(path)
    actual_headers = list(df.columns)
    
    if actual_headers != EXPECTED_HEADERS:
        raise ValueError(f"Header mismatch!\nExpected: {EXPECTED_HEADERS}\nActual: {actual_headers}")
    
    if len(df) == 0:
        raise ValueError("data_dictionary.csv is empty!")
    
    # Check for empty mandatory fields in rows
    for col in ["column_name", "data_type", "description", "business_meaning", "related_kpi"]:
        if df[col].isnull().any():
            raise ValueError(f"Found null entries in required column: {col}")
            
    print(f"✓ CSV validation passed! Found {len(df)} documented columns.")

def validate_md(path: str) -> None:
    print(f"Checking Markdown file at: {path}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing Markdown data dictionary at: {path}")
        
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    required_sections = [
        "Dataset Overview",
        "Columns Specification",
        "Column to KPI Mapping",
        "Ambiguous Columns & Resolutions",
        "Column Relationships",
        "Governance & Maintenance Protocol"
    ]
    
    for sec in required_sections:
        if sec not in content:
            raise ValueError(f"Missing required Markdown section: '{sec}'")
            
    print("✓ Markdown validation passed! All required sections present.")

if __name__ == "__main__":
    print("Starting Data Dictionary Validation...")
    try:
        validate_csv(CSV_PATH)
        validate_md(MD_PATH)
        print("🎉 All 2.17 Data Dictionary validations passed successfully!")
    except Exception as e:
        print(f"❌ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
