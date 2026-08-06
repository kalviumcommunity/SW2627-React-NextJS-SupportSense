import pandas as pd
import numpy as np
import os

def strip_all_strings(df):
    """Strip whitespace from all string columns."""
    print("\n--- Task 1: Strip Whitespace ---")
    string_cols = df.select_dtypes(include=['object']).columns
    
    for col in string_cols:
        if df[col].dtype == 'object':
            # Count before
            before = df[col].nunique()
            
            # Apply strip
            df[col] = df[col].str.strip()
            
            # Count after
            after = df[col].nunique()
            
            print(f"{col}: {before} → {after} unique values")
    
    return df

def normalize_casing(df, columns_to_lower):
    """Normalize casing for specified columns."""
    print("\n--- Task 2: Normalize Casing ---")
    for col in columns_to_lower:
        print(f"Before normalization ({col}):")
        print(df[col].head().tolist())
        
        df[col] = df[col].str.lower()
        print(f"Normalized {col} to lowercase")
        
        print(f"After normalization ({col}):")
        print(df[col].head().tolist())
    
    return df

def remove_special_characters(df, columns):
    """Remove special characters from specified columns."""
    print("\n--- Task 3: Remove Special Characters ---")
    # Using regex [^a-zA-Z0-9 ] matches any character that is NOT a letter, number, or space
    for col in columns:
        print(f"Before removing special chars ({col}):")
        print(df[col].head().tolist())
        
        df[col] = df[col].str.replace('[^a-zA-Z0-9 ]', '', regex=True)
        print(f"Removed special characters from {col}")
        
        print(f"After removing special chars ({col}):")
        print(df[col].head().tolist())
    
    return df

def standardize_categories(df):
    """Standardize Categorical Labels Using Mapping Dictionary."""
    print("\n--- Task 4: Standardize Categories ---")
    segment_map = {
        'b2b': 'B2B',
        'b 2 b': 'B2B',
        'b2 b': 'B2B',
        'sme': 'SMB',
        'small medium enterprise': 'SMB',
        'enterprise': 'Enterprise'
    }

    print("Mapping Dictionary Used:")
    print(segment_map)
    print("\nJustification: Consolidating B2B variations to 'B2B', SME variants to 'SMB' (Small and Medium Business), and keeping 'Enterprise' capitalized. This aligns with CRM standard labels.")
    
    before_counts = df['segment'].value_counts().to_dict()
    print(f"\nValue counts before mapping:\n{before_counts}")

    df['segment'] = df['segment'].map(segment_map).fillna(df['segment'])
    
    after_counts = df['segment'].value_counts().to_dict()
    print(f"\nValue counts after mapping:\n{after_counts}")
    
    return df

def clean_text_column(series, lowercase=True, strip=True, remove_special=False, mapping=None):
    """Reusable text cleaning function for any string column."""
    result = series.copy()
    
    if result.isna().any():
        print(f"Warning: {result.isna().sum()} null values in column")
    
    if strip:
        result = result.str.strip()
    
    if lowercase:
        result = result.str.lower()
    
    if remove_special:
        result = result.str.replace('[^a-zA-Z0-9 ]', '', regex=True)
    
    if mapping:
        result = result.map(mapping).fillna(result)
    
    return result

if __name__ == "__main__":
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # Create sample messy data
    data = {
        'product_name': [' Electronics ', 'electronics', 'ELECTRONICS', '  Furniture', 'FURNITURE'],
        'segment': ['b2b', 'b 2 b', 'b2 b', 'sme', 'enterprise'],
        'city': ['São Paulo', 'Montréal', 'New York', 'München', 'Paris!']
    }
    df = pd.DataFrame(data)
    df.to_csv('data/raw/messy_text_data.csv', index=False)
    
    print("Initial Data:")
    print(df)
    
    # Task 1: Strip Whitespace
    df = strip_all_strings(df)
    
    # Task 2: Normalize Casing
    # We apply casing normalization to product_name and segment to prepare for mapping
    df = normalize_casing(df, ['product_name', 'segment'])
    
    # Task 3: Remove Special Characters
    # We clean city names of accents and punctuation
    df = remove_special_characters(df, ['city'])
    
    # Task 4: Standardize Categories
    df = standardize_categories(df)
    
    # Task 5: Testing reusable function
    print("\n--- Task 5: Reusable Function Test ---")
    test_cases = [
        '  Product A  ',      # Leading/trailing spaces
        'PRODUCT B',         # All caps
        'Product_C',         # Special char
        None,                # Null value
        ''                   # Empty string
    ]
    test_series = pd.Series(test_cases)
    print("Original Test Series:")
    print(test_series.tolist())
    
    result = clean_text_column(test_series, lowercase=True, strip=True, remove_special=True)
    print("\nCleaned Test Series:")
    print(result.tolist())
    
    # Save the processed data
    df.to_csv('data/processed/cleaned_text_data.csv', index=False)
    print("\n✓ Cleaned data saved to data/processed/cleaned_text_data.csv")
