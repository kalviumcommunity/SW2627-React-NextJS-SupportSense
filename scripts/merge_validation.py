import pandas as pd
import numpy as np
import json
import os

def create_sample_data():
    """Create sample datasets that simulate real-world join scenarios."""
    np.random.seed(42)
    # 1000 customers
    customers_df = pd.DataFrame({
        'customer_id': range(1, 1001),
        'name': [f"Customer_{i}" for i in range(1, 1001)],
        'segment': np.random.choice(['B2B', 'B2C', 'Enterprise'], 1000)
    })

    # Orders for most customers (1-800), leaving 200 customers with no orders
    order_customers = np.random.choice(range(1, 801), size=4900, replace=True).tolist()
    # Orders for non-existent customers (1001-1050), creating orphaned orders
    order_customers.extend(np.random.choice(range(1001, 1051), size=100, replace=True).tolist())

    orders_df = pd.DataFrame({
        'order_id': range(1, 5001),
        'customer_id': order_customers,
        'amount': np.random.uniform(10, 500, size=5000).round(2),
        'order_date': pd.date_range(start='2025-01-01', periods=5000, freq='h')
    })

    os.makedirs('data/raw', exist_ok=True)
    customers_df.to_csv('data/raw/customers_merge.csv', index=False)
    orders_df.to_csv('data/raw/orders_merge.csv', index=False)
    return customers_df, orders_df

if __name__ == "__main__":
    os.makedirs('output', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # Generate and load data
    df_customers, df_orders = create_sample_data()

    print("\n--- Task 1: Explicit Join with Row Count Validation ---")
    print(f"Left table (customers): {len(df_customers)}")
    print(f"Right table (orders): {len(df_orders)}")

    df_merged = pd.merge(df_customers, df_orders, on='customer_id', how='left')

    print(f"Merged result (left join): {len(df_merged)}")
    print(f"Change vs customers: {len(df_merged) - len(df_customers)}")
    
    print("\n--- Task 2: Detect Unmatched Keys ---")
    unmatched_customers = df_customers[~df_customers['customer_id'].isin(df_orders['customer_id'])]
    unmatched_orders = df_orders[~df_orders['customer_id'].isin(df_customers['customer_id'])]

    print(f"Customers without orders: {len(unmatched_customers)}")
    print(f"Orphaned orders: {len(unmatched_orders)}")

    unmatched_customers.to_csv('output/unmatched_customers.csv', index=False)
    unmatched_orders.to_csv('output/unmatched_orders.csv', index=False)
    print("Saved unmatched records to output/unmatched_customers.csv and output/unmatched_orders.csv")

    print("\n--- Task 3: Compare Join Types ---")
    inner = pd.merge(df_customers, df_orders, on='customer_id', how='inner')
    left = pd.merge(df_customers, df_orders, on='customer_id', how='left')
    right = pd.merge(df_customers, df_orders, on='customer_id', how='right')
    outer = pd.merge(df_customers, df_orders, on='customer_id', how='outer')

    print(f"Inner: {len(inner)}, Left: {len(left)}, Right: {len(right)}, Outer: {len(outer)}")

    print("\n--- Task 4: Validate No Unexpected Duplication ---")
    print("Merged columns:", df_merged.columns.tolist())
    key_counts = df_merged['customer_id'].value_counts()
    print(f"Max orders per customer: {key_counts.max()}")

    print("\n--- Task 5: Document Join Decision ---")
    join_report = {
        'join_type': 'left',
        'left_table': 'customers',
        'right_table': 'orders',
        'join_key': 'customer_id',
        'left_rows': len(df_customers),
        'right_rows': len(df_orders),
        'result_rows': len(df_merged),
        'unmatched_left': len(unmatched_customers),
        'unmatched_right': len(unmatched_orders),
        'reasoning': 'Left join preserves all customers; unmatched customers have no orders. Orphaned orders in the right table are excluded.'
    }

    print("\nJoin Report:")
    print(json.dumps(join_report, indent=2))
    
    with open('output/join_report.json', 'w') as f:
        json.dump(join_report, f, indent=2)
        
    # Save the merged dataset
    df_merged.to_csv('data/processed/merged_customer_orders.csv', index=False)
    print("\n✓ Processed data saved to data/processed/merged_customer_orders.csv")
