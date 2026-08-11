import pandas as pd
import numpy as np
import time
import os

# Generate sample data
np.random.seed(42)
num_rows = 1000000  # 1 million rows to show massive performance difference
df = pd.DataFrame({
    'customer_id': range(1, num_rows + 1),
    'revenue': np.random.uniform(10, 1000, size=num_rows)
})

print(f"Generated dataset with {num_rows:,} rows.")

# --- Task 1: Replace Loop with NumPy Vectorization (Min-Max) ---
print("\n--- Task 1: Min-Max Normalization ---")
# SLOW: Loop
start = time.time()
normalized_loop = []
rev_min = df['revenue'].min()
rev_max = df['revenue'].max()
rev_range = rev_max - rev_min
for val in df['revenue']:
    normalized_loop.append((val - rev_min) / rev_range)
loop_time_minmax = time.time() - start

# FAST: NumPy
start = time.time()
revenue_array = df['revenue'].values
normalized_np = (revenue_array - revenue_array.min()) / (revenue_array.max() - revenue_array.min())
np_time_minmax = time.time() - start

print(f"Loop Time: {loop_time_minmax:.4f}s")
print(f"NumPy Time: {np_time_minmax:.4f}s")
if np_time_minmax > 0:
    print(f"Speedup: {loop_time_minmax/np_time_minmax:.0f}x")

# --- Task 2: Z-Score Normalization ---
print("\n--- Task 2: Z-Score Normalization ---")
revenue_array = df['revenue'].values
z_scores = (revenue_array - revenue_array.mean()) / revenue_array.std()
print("Computed Z-Scores using NumPy.")

# --- Task 3: Bulk Ranking/Scoring ---
print("\n--- Task 3: Bulk Ranking ---")
# Rank all customers by revenue
revenue_array = df['revenue'].values
rankings = np.argsort(-revenue_array)  # Negative for descending
ranks = np.empty_like(rankings)
ranks[rankings] = np.arange(1, len(rankings) + 1)
print("Computed rankings using NumPy.")

# --- Task 4: Time Performance Comparison (Multiplication) ---
print("\n--- Task 4: Time Performance Comparison ---")
# Time loop version
start = time.time()
result_loop = []
for val in df['revenue']:
    result_loop.append(val * 1.1)
loop_time_mult = time.time() - start

# Time NumPy version
start = time.time()
result_np = df['revenue'].values * 1.1
np_time_mult = time.time() - start

print(f"Loop: {loop_time_mult:.4f}s")
print(f"NumPy: {np_time_mult:.4f}s")
if np_time_mult > 0:
    print(f"Speedup: {loop_time_mult/np_time_mult:.0f}x")

# --- Task 5: Integrate Back to DataFrame ---
print("\n--- Task 5: Integrate Back to DataFrame ---")
# All NumPy results go back to DataFrame as new columns
df['revenue_normalized'] = normalized_np
df['revenue_zscore'] = z_scores
df['revenue_rank'] = ranks

# Verify types and shapes
print(f"Shape: {df.shape}")
print(f"Dtypes:\n{df.dtypes}")

# Save sample output
os.makedirs('data/processed', exist_ok=True)
df.head(100).to_csv('data/processed/vectorized_revenue_sample.csv', index=False)
print("\nSaved first 100 rows to data/processed/vectorized_revenue_sample.csv")
