import streamlit as st
import sys
from pathlib import Path
from src.data_loader import get_daily_revenue

# Need to ensure sql_joins_analysis is in path to import the previously built chart logic
project_root = Path(__file__).resolve().parent.parent
sql_dir = project_root / 'sql_joins_analysis'
if str(sql_dir) not in sys.path:
    sys.path.insert(0, str(sql_dir))

from dashboard.charts.interactive_charts import create_metric_chart

st.set_page_config(page_title="Trends", page_icon="📈", layout="wide")

st.title("📈 Daily Metric Trends")
st.markdown(
    "Explore key metrics over time. Switch metrics using the dropdown on the top-left of the chart. "
    "Drag the slider below the chart to filter by date range. Anomalies (>1.5 Std Dev) are automatically highlighted in red."
)

# Load cached data
df_daily = get_daily_revenue()

# Re-use the Plotly interactive chart from Task 2.46
fig = create_metric_chart(df_daily)

# Render chart in Streamlit
st.plotly_chart(fig, width='stretch')
