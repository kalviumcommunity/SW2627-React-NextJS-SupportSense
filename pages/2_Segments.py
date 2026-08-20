import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import plotly.graph_objects as go

# Ensure we can import the shared data loader
project_root = Path(__file__).resolve().parent.parent
sql_dir = project_root / 'sql_joins_analysis'
if str(sql_dir) not in sys.path:
    sys.path.insert(0, str(sql_dir))

from src.data_loader import get_customer_summary, get_customer_segments

st.set_page_config(page_title="Segments", page_icon="🧩", layout="wide")

st.title("🧩 Customer Segments Overview")
st.markdown(
    "This page presents a high-level view of each customer segment, "
    "showing how many customers belong to each segment and the total revenue they generate."
)

# Load cached data
df_summary = get_customer_summary()
df_segments = get_customer_segments()

# Show aggregated segment metrics table
st.subheader("Segment Aggregated Metrics")
st.dataframe(df_segments, use_container_width=True)

# Plot segment revenue bar chart (Plotly)
fig = go.Figure(
    data=go.Bar(
        x=df_segments["customer_type"],
        y=df_segments["total_segment_revenue"],
        text=df_segments["customer_count"],
        hovertemplate=(
            "<b>Segment: %{x}</b><br>"
            "Total Revenue: $%{y:,.2f}<br>"
            "Customers: %{text}<extra></extra>"
        ),
        marker_color="steelblue",
    )
)
fig.update_layout(
    title="Revenue by Customer Segment",
    xaxis_title="Customer Segment",
    yaxis_title="Total Revenue (USD)",
    template="plotly_white",
)

st.plotly_chart(fig, width="stretch")

# Show top-5 customers by lifetime value from vw_customer_order_summary
st.subheader("Top Customers by Lifetime Value")
top_customers = df_summary.sort_values(by="lifetime_value", ascending=False).head(5)
st.dataframe(
    top_customers[
        ["customer_id", "customer_name", "customer_type", "total_orders", "lifetime_value"]
    ],
    use_container_width=True
)
