import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from src.data_loader import get_raw_orders, get_raw_customers

st.set_page_config(
    page_title="Reactive Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚡ Real-Time Reactive KPI Dashboard")
st.markdown("Instantly interact with data. Upload a new dataset or use filters to watch KPIs and charts react in real-time.")

st.divider()

# --- 1. DATA UPLOAD & CACHING ---
st.sidebar.header("1. Upload New Data")
st.sidebar.info("Upload a new `orders.csv` to instantly replace the underlying dataset and recalculate all metrics.")
uploaded_file = st.sidebar.file_uploader("Upload orders.csv", type=["csv"])

if uploaded_file is not None:
    # Save the uploaded file to overwrite the raw orders dataset
    project_root = Path(__file__).resolve().parent
    data_path = project_root / 'sql_joins_analysis' / 'data' / 'orders.csv'
    
    with open(data_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # Crucial: Clear cache so data_loader re-fetches the new DB
    st.cache_data.clear()
    st.cache_resource.clear()
    
    st.sidebar.success("✅ Dataset uploaded and cache cleared!")
    
if st.sidebar.button("Force Cache Reset"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.sidebar.success("Cache cleared!")

# --- 2. LOAD DATA ---
# We use raw data because we need granular filtering (e.g. by order amount and date)
df_orders = get_raw_orders()
df_customers = get_raw_customers()

# Merge into a single raw dataframe for cross-filtering
# Using a left join from orders to keep all orders even if orphaned, testing our SQL join logic
raw_df = pd.merge(df_orders, df_customers, on='customer_id', how='left')

# Ensure date is datetime format
raw_df['order_date'] = pd.to_datetime(raw_df['order_date'])

# Fill missing segment for orphaned orders
raw_df['customer_type'] = raw_df['customer_type'].fillna('Unknown')

# --- 3. REACTIVE FILTERING ---
st.sidebar.header("2. Dashboard Filters")

# Date Range Filter
min_date = raw_df['order_date'].min().date()
max_date = raw_df['order_date'].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Segment Filter
all_segments = raw_df['customer_type'].unique().tolist()
selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    options=all_segments,
    default=all_segments
)

# Order Amount Range Filter
min_amount = float(raw_df['order_amount'].min())
max_amount = float(raw_df['order_amount'].max())

# Avoid slider error if min == max
if min_amount == max_amount:
    amount_range = (min_amount, max_amount)
    st.sidebar.text(f"Order Amount: ${min_amount:,.2f}")
else:
    amount_range = st.sidebar.slider(
        "Order Amount Range",
        min_value=min_amount,
        max_value=max_amount,
        value=(min_amount, max_amount)
    )

# --- 4. APPLY FILTERS ---
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = date_range[0], date_range[0]

filtered_df = raw_df[
    (raw_df['order_date'] >= pd.Timestamp(start_date)) &
    (raw_df['order_date'] <= pd.Timestamp(end_date)) &
    (raw_df['customer_type'].isin(selected_segments)) &
    (raw_df['order_amount'] >= amount_range[0]) &
    (raw_df['order_amount'] <= amount_range[1])
]

# --- 5. EMPTY STATE HANDLING ---
if filtered_df.empty:
    st.warning("⚠️ No data matches the current filters. Try broadening your selection.")
    st.stop()

# --- 6. REACTIVE KPI CARDS (5 metrics) ---
st.header("Key Performance Indicators")

total_revenue = filtered_df['order_amount'].sum()
total_orders = len(filtered_df)
unique_customers = filtered_df['customer_id'].nunique()
avg_order_value = filtered_df['order_amount'].mean()
avg_customer_value = total_revenue / unique_customers if unique_customers > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Active Customers", f"{unique_customers:,}")
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")
col5.metric("Avg Customer Value", f"${avg_customer_value:,.2f}")

st.divider()

# --- 7. REACTIVE CHARTS (3 types) ---
st.header("Interactive Analytics")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # 1. Line Chart: Revenue over time
    daily_rev = filtered_df.groupby('order_date', as_index=False)['order_amount'].sum()
    fig_line = px.line(
        daily_rev, x='order_date', y='order_amount', 
        title="Revenue Trend Over Time",
        labels={'order_date': 'Date', 'order_amount': 'Revenue ($)'},
        markers=True
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
with chart_col2:
    # 2. Bar Chart: Revenue by Segment
    segment_rev = filtered_df.groupby('customer_type', as_index=False)['order_amount'].sum()
    fig_bar = px.bar(
        segment_rev, x='customer_type', y='order_amount',
        title="Revenue by Customer Segment",
        labels={'customer_type': 'Segment', 'order_amount': 'Revenue ($)'},
        color='customer_type'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# 3. Histogram: Distribution of Order Amounts
fig_hist = px.histogram(
    filtered_df, x='order_amount', nbins=20,
    title="Distribution of Order Amounts",
    labels={'order_amount': 'Order Amount ($)'},
    marginal="box", # Adds a box plot above the histogram
    opacity=0.7
)
st.plotly_chart(fig_hist, use_container_width=True)
