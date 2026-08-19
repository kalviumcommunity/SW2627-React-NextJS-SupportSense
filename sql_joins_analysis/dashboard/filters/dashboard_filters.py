import streamlit as st

def render_sidebar():
    """Renders the sidebar filters and information for the dashboard."""
    st.sidebar.header("Dashboard Controls")
    
    st.sidebar.info(
        "💡 **Pro Tip**: Use the dropdown directly on the chart to switch metrics "
        "without reloading the page. Use the slider below the chart to zoom into dates."
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Layer Context")
    st.sidebar.text("Engine: SQLite In-Memory")
    st.sidebar.text("Table: agg_daily_revenue")
    st.sidebar.text("Grain: Daily Time-Series")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "This dashboard consumes the **SQL Views & Aggregations** "
        "layer, strictly separating data processing from UI rendering."
    )
