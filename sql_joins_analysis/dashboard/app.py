import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# Add project root to sys path to import src modules
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.database import setup_database
from dashboard.charts.interactive_charts import create_metric_chart
from dashboard.filters.dashboard_filters import render_sidebar
from src.utils import extract_queries
from sqlalchemy import text

# Setup Page Config
st.set_page_config(page_title="SupportSense Analytics", page_icon="📈", layout="wide")

@st.cache_resource
def init_db():
    """Initializes the in-memory SQLite DB and runs the SQL Aggregation logic."""
    data_dir = project_root / 'data'
    sql_dir = project_root / 'database'
    engine = setup_database(data_dir)
    
    # Materialize aggregations needed for the dashboard
    aggs = ['agg_daily_revenue']
    for agg in aggs:
        sql_file = sql_dir / 'aggregations' / f"{agg}.sql"
        queries = extract_queries(sql_file)
        with engine.begin() as conn:
            for q in queries:
                conn.execute(text(q))
    return engine

def main():
    st.title("📈 SupportSense Business Analytics")
    st.markdown(
        "Interactive exploration layer built on top of pre-aggregated SQL data. "
        "This ensures that frontend metrics perfectly match backend SQL definitions."
    )
    
    render_sidebar()
    
    # Initialize DB (cached so it doesn't run on every UI interaction)
    engine = init_db()
    
    # Load Data directly from the SQL Aggregation table
    df_daily = pd.read_sql("SELECT * FROM agg_daily_revenue ORDER BY aggregation_date", engine)
    
    st.subheader("Daily Metric Trends")
    
    # Create the Plotly chart
    fig = create_metric_chart(df_daily)
    
    # Render chart in Streamlit
    st.plotly_chart(fig, width='stretch')
    
    # Export Chart to HTML as required by Task 11
    output_dir = project_root / 'output'
    output_dir.mkdir(exist_ok=True)
    export_path = output_dir / 'interactive_chart.html'
    fig.write_html(str(export_path))
    
    st.success(f"✅ Interactive chart exported successfully for offline viewing at: `{export_path.relative_to(project_root.parent)}`")

if __name__ == "__main__":
    main()
