import streamlit as st
import sys
from pathlib import Path
from src.data_loader import get_raw_orders, get_raw_customers

# Ensure sql_joins_analysis is in path for any potential utilities
project_root = Path(__file__).resolve().parent.parent
sql_dir = project_root / 'sql_joins_analysis'
if str(sql_dir) not in sys.path:
    sys.path.insert(0, str(sql_dir))

st.set_page_config(page_title="Data Explorer", page_icon="🔎", layout="wide")

st.title("🔎 Data Explorer")
st.markdown(
    "Interactively filter and inspect the underlying raw tables. "
    "Use the controls in the sidebar to narrow down the view."
)

# Sidebar filters
st.sidebar.header("Filters")

# Load raw data (cached)
orders_df = get_raw_orders()
customers_df = get_raw_customers()

# Date filter for orders if 'order_date' column exists
if "order_date" in orders_df.columns:
    min_date = orders_df["order_date"].min().date()
    max_date = orders_df["order_date"].max().date()
    date_range = st.sidebar.date_input(
        "Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if len(date_range) == 2:
        start, end = date_range
        orders_df = orders_df[(orders_df["order_date"] >= pd.Timestamp(start)) & (orders_df["order_date"] <= pd.Timestamp(end))]

# Segment filter for customers if column exists
if "customer_type" in customers_df.columns:
    segment_options = customers_df["customer_type"].unique().tolist()
    selected_segments = st.sidebar.multiselect("Customer Segments", options=segment_options, default=segment_options)
    customers_df = customers_df[customers_df["customer_type"].isin(selected_segments)]

# Revenue slider for orders if column exists
if "order_amount" in orders_df.columns:
    min_rev = int(orders_df["order_amount"].min())
    max_rev = int(orders_df["order_amount"].max())
    rev_range = st.sidebar.slider("Order Amount Range", min_rev, max_rev, (min_rev, max_rev))
    orders_df = orders_df[(orders_df["order_amount"] >= rev_range[0]) & (orders_df["order_amount"] <= rev_range[1])]

st.divider()

# Show preview of orders
st.subheader("Orders Table")
with st.expander("View Orders Data"):
    st.dataframe(orders_df.head(100), use_container_width=True)
    st.caption(f"Showing {len(orders_df)} of {len(get_raw_orders())} total order records after filters.")

# Show preview of customers
st.subheader("Customers Table")
with st.expander("View Customers Data"):
    st.dataframe(customers_df.head(100), use_container_width=True)
    st.caption(f"Showing {len(customers_df)} of {len(get_raw_customers())} total customer records after filters.")
