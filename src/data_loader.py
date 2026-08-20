import sys
from pathlib import Path
import streamlit as st
import pandas as pd
from sqlalchemy import text

# Add sql_joins_analysis to path so we can import its DB setup
project_root = Path(__file__).resolve().parent.parent
sql_dir = project_root / 'sql_joins_analysis'
sys.path.insert(0, str(sql_dir))

from src.database import setup_database
from src.utils import extract_queries

@st.cache_resource
def get_db_engine():
    """Initializes and caches the in-memory SQLite database connection."""
    data_dir = sql_dir / 'data'
    sql_ddl_dir = sql_dir / 'database'
    engine = setup_database(data_dir)
    
    # Materialize aggregations and views needed across the dashboard
    with engine.begin() as conn:
        for view in ['vw_customer_order_summary']:
            queries = extract_queries(sql_ddl_dir / 'views' / f"{view}.sql")
            for q in queries:
                conn.execute(text(q))
                
        for agg in ['agg_daily_revenue', 'agg_customer_segments']:
            queries = extract_queries(sql_ddl_dir / 'aggregations' / f"{agg}.sql")
            for q in queries:
                conn.execute(text(q))
                
    return engine

@st.cache_data
def get_daily_revenue():
    engine = get_db_engine()
    return pd.read_sql("SELECT * FROM agg_daily_revenue ORDER BY aggregation_date", engine)

@st.cache_data
def get_customer_summary():
    engine = get_db_engine()
    return pd.read_sql("SELECT * FROM vw_customer_order_summary", engine)

@st.cache_data
def get_customer_segments():
    engine = get_db_engine()
    return pd.read_sql("SELECT * FROM agg_customer_segments ORDER BY total_segment_revenue DESC", engine)

@st.cache_data
def get_raw_orders():
    engine = get_db_engine()
    return pd.read_sql("SELECT * FROM orders", engine)

@st.cache_data
def get_raw_customers():
    engine = get_db_engine()
    return pd.read_sql("SELECT * FROM customers", engine)
