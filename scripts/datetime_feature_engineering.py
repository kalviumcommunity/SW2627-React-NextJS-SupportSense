import pandas as pd
import numpy as np
import os

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def parse_timestamps(df):
    """Task 1: Parse Timestamp Strings with Explicit Format."""
    print("\n--- Task 1: Parse Timestamp Strings ---")
    print(f"Original dtype: {df['transaction_date'].dtype}")
    
    # Parse with explicit format
    df['transaction_date'] = pd.to_datetime(
        df['transaction_date'],
        format='%Y-%m-%d %H:%M:%S'
    )
    
    print(f"Parsed dtype: {df['transaction_date'].dtype}")
    return df

def extract_time_features(df):
    """Task 2: Extract Day-of-Week and Hour-of-Day."""
    print("\n--- Task 2: Extract Time Features ---")
    df['day_of_week'] = df['transaction_date'].dt.day_name()
    df['hour'] = df['transaction_date'].dt.hour
    
    hourly_volume = df.groupby('hour').size()
    print("Hourly Volume Distribution:")
    print(hourly_volume)
    
    if MATPLOTLIB_AVAILABLE:
        plt.figure(figsize=(10, 6))
        hourly_volume.plot(kind='bar', color='skyblue')
        plt.title('Transaction Volume by Hour')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Transactions')
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        os.makedirs('output', exist_ok=True)
        plt.savefig('output/hourly_distribution.png')
        plt.close()
        print("Saved hourly distribution plot to output/hourly_distribution.png")
    else:
        print("Matplotlib not installed. Skipping plot generation.")
        
    return df

def compute_weekly_metrics(df):
    """Task 3: Compute Week Number and Resample Data."""
    print("\n--- Task 3: Weekly Resampling ---")
    df['week_num'] = df['transaction_date'].dt.isocalendar().week
    
    # Resample for weekly metrics
    df_ts = df.set_index('transaction_date')
    weekly_revenue = df_ts['amount'].resample('W').sum()
    print("Weekly Revenue Trend:")
    print(weekly_revenue)
    
    return df

def compute_recency(df):
    """Task 4: Compute Days-Since-Event Metric."""
    print("\n--- Task 4: Recency Metrics ---")
    # For reproducible results, assume today is slightly after the last record
    # Or just use Timestamp.now()
    today = pd.Timestamp.now()
    
    # By customer
    customer_last_purchase = df.groupby('customer_id')['transaction_date'].max()
    
    recency_df = pd.DataFrame({
        'last_purchase_date': customer_last_purchase
    })
    recency_df['days_since_last_purchase'] = (today - recency_df['last_purchase_date']).dt.days
    
    print("Recency Distribution (days since last purchase):")
    print(recency_df['days_since_last_purchase'].describe())
    
    return df, recency_df

def time_indexed_aggregation(df):
    """Task 5: Build Time-Indexed Aggregation."""
    print("\n--- Task 5: Time-Indexed Aggregation ---")
    
    # Multi-level groupby
    hourly_daily = df.groupby(['day_of_week', 'hour']).agg({
        'amount': ['sum', 'count', 'mean']
    })
    
    print("Hourly/Daily Aggregations (first 5 rows):")
    print(hourly_daily.head())
    
    # Pivot for visualization
    pivot_table = pd.pivot_table(
        df,
        values='amount',
        index='hour',
        columns='day_of_week',
        aggfunc='sum',
        fill_value=0
    )
    
    print("\nPivot Table (Hour x Day of Week - Sum of Amount):")
    print(pivot_table)
    
    return pivot_table

def run_tests(df, recency_df):
    print("\n--- Testing Instructions ---")
    print(f"Min date: {df['transaction_date'].min()}")
    print(f"Max date: {df['transaction_date'].max()}")
    print(f"Days in dataset: {(df['transaction_date'].max() - df['transaction_date'].min()).days}")
    print(f"Hours with data: {sorted(df['hour'].unique())}")
    print(f"Weeks in dataset: {df['week_num'].nunique()}")
    print(f"Min days since purchase: {recency_df['days_since_last_purchase'].min()}")
    print(f"Max days since purchase: {recency_df['days_since_last_purchase'].max()}")
    
    print("\n--- Edge Cases ---")
    test_dates = [
        '2025-01-15 14:30:45',        # Standard
        '2025-1-15 14:30:45',         # Single-digit month
        '15/01/2025 14:30:45',        # European format
        '2025-01-15T14:30:45Z',       # ISO format with Z
    ]
    for date_str in test_dates:
        try:
            parsed = pd.to_datetime(date_str, format='%Y-%m-%d %H:%M:%S')
            print(f"✓ {date_str} parsed as {parsed}")
        except Exception as e:
            print(f"✗ {date_str} - format mismatch ({type(e).__name__})")

if __name__ == "__main__":
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    data_file = 'data/raw/transactions_dates.csv'
    
    # Generate data if not exists
    if not os.path.exists(data_file):
        data = {
            'transaction_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'customer_id': [101, 102, 101, 103, 102, 104, 101, 103, 105, 105],
            'transaction_date': [
                '2025-01-15 14:30:45', '2025-01-15 16:45:00', '2025-01-20 09:15:20', 
                '2025-01-22 18:30:00', '2025-02-05 11:00:00', '2025-02-10 14:30:00', 
                '2025-02-15 10:15:30', '2025-03-01 19:45:10', '2025-03-10 08:30:00', 
                '2025-03-12 15:20:00'
            ],
            'amount': [150.50, 200.00, 50.25, 300.00, 120.75, 45.00, 80.00, 210.50, 95.00, 110.00]
        }
        df_raw = pd.DataFrame(data)
        df_raw.to_csv(data_file, index=False)
        print("Created sample data at", data_file)
    
    # Load raw data
    df = pd.read_csv(data_file)
    print("Initial Data:")
    print(df.head())
    
    # Pipeline
    df = parse_timestamps(df)
    df = extract_time_features(df)
    df = compute_weekly_metrics(df)
    df, recency_df = compute_recency(df)
    pivot = time_indexed_aggregation(df)
    
    # Save processed data
    df.to_csv('data/processed/transactions_dates_processed.csv', index=False)
    print("\n✓ Processed data saved to data/processed/transactions_dates_processed.csv")
    
    # Tests
    run_tests(df, recency_df)
