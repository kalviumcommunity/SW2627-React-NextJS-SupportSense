# SQL Joins & Multi-Table Analysis (Task 2.40)

An end-to-end Python-based analytical project demonstrating how SQL JOINs operate under the hood, how one-to-many relationships cause row multiplication, and how to detect unmatched (orphaned) records.

## 1. Project Objective
To provide a beginner-friendly, mathematically validated demonstration of SQL Joins. It answers common questions like "Why did my row count increase?" and "How do I find records that don't match?".

## 2. Dataset & Relationships
The `data/` directory contains 4 deliberately designed tables:
- `customers.csv`: Contains customers, including one (Eve) with **no orders**.
- `orders.csv`: Contains orders, including multiple orders for Alice (1-to-many), and one **orphaned order** (no matching customer).
- `products.csv`: Product catalog.
- `order_items.csv`: Line items linking orders to products.

**Relationships**:
- `customers` (1) → (Many) `orders`
- `orders` (1) → (Many) `order_items`
- `products` (1) → (Many) `order_items`

## 3. JOIN Concepts & Row Multiplication
Why do JOIN row counts increase?
When joining `customers` to `orders`, if one customer (e.g., Alice) has 2 orders, the database duplicates Alice's customer information to attach it to both orders. 
- **1-to-1**: Row count stays the same.
- **1-to-Many**: Row count expands to match the "Many" side.
- **Many-to-Many**: Row count expands exponentially (Cartesian product behavior if not filtered properly).

## 4. How Duplicate Financial Totals Occur
If you aggregate (SUM) the `order_amount` *after* joining to `order_items`, an order with 3 items will have its `order_amount` duplicated 3 times. Summing this joined table will inflate the financial totals. Always aggregate before joining, or calculate line-item totals strictly from the lowest grain.

## 5. Tasks Implemented
- **Task 1 (`sql/task1_left_join.sql`)**: Uses `LEFT JOIN` + `GROUP BY` to safely count distinct orders and sum totals per customer, preserving customers with 0 orders.
- **Task 2 (`sql/task2_unmatched_keys.sql`)**: Uses `LEFT JOIN ... IS NULL` to detect missing relationships (Customers without orders, Orphaned orders).
- **Task 3 (`sql/task3_join_comparison.sql`)**: Demonstrates INNER, LEFT, and FULL OUTER (using UNION ALL to ensure broad database compatibility).
- **Task 4 (`sql/task4_multi_table_join.sql`)**: Chains 4 tables together and calculates strict line totals without double counting.

## 6. Interactive Visualization Layer (Dashboard)
The project now includes a production-grade visualization layer built with **Plotly** and **Streamlit**. It strictly consumes the output of the pre-aggregated SQL data layer, avoiding complex business logic duplication in the frontend.

**Features Implemented:**
- **Metric Selection**: Switch between Revenue, Orders, and Avg Order Value instantly using Plotly `updatemenus`.
- **Date Zooming**: Plotly range sliders and range selectors (1W, 1M, All) enable deep temporal exploration.
- **Custom Tooltips**: Formatted currencies and anomaly indicators using `hovertemplate`.
- **Anomaly Detection**: Dynamically highlights unusual metrics ($|Z| > 1.5$) directly on the chart.
- **Offline HTML Export**: A standalone interactive chart is generated automatically upon running the dashboard.

## 7. How to Run

Ensure you have Python 3 installed. Install the dependencies:
```bash
pip install -r requirements.txt
```

**Run the SQL Validation Pipeline:**
```bash
python main.py
python src/validate_layer.py
```

**Run the Interactive Dashboard:**
```bash
streamlit run dashboard/app.py
```
*(The interactive offline chart will be saved to `output/interactive_chart.html` automatically.)*

## 8. Expected Outputs & Validation
The pipeline executes all queries via an in-memory SQLite database powered by Pandas and SQLAlchemy.
- It will write `.csv` reports to the `output/` directory.
- It generates a `validation_report.json` mathematically asserting that the row counts and financial totals are exactly correct based on the raw inputs.
