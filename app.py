import streamlit as st
import pandas as pd
from src.data_loader import get_daily_revenue, get_customer_summary

st.set_page_config(
    page_title="SupportSense Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 SupportSense Business Overview")
st.markdown(
    "Welcome to the **SupportSense Analytics Platform**. "
    "Use the sidebar to navigate through detailed trends, customer segments, and raw data exploration."
)

st.divider()

# Load Cached Data
df_daily = get_daily_revenue()
df_customers = get_customer_summary()

# Calculate Top-Level KPIs
total_revenue = df_daily['total_revenue'].sum()
total_orders = df_daily['order_count'].sum()
unique_customers = len(df_customers)
aov = df_daily['avg_order_value'].mean()

st.header("Key Performance Indicators")

# Display KPIs using columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")

with col2:
    st.metric(label="Total Orders", value=f"{total_orders:,}")

with col3:
    st.metric(label="Active Customers", value=f"{unique_customers:,}")

with col4:
    st.metric(label="Average Order Value", value=f"${aov:,.2f}")

st.divider()

st.subheader("Platform Architecture")
st.info(
    "**Single Source of Truth**: This dashboard connects directly to the pre-aggregated "
    "SQL Views & Aggregation layer. All metrics perfectly match backend definitions without frontend duplication."
)
