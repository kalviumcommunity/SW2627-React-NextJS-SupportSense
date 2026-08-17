import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Data Explorer", layout="wide")

st.title("Data Explorer with Interactive Filters")

# Generate sample data to demonstrate the filters
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(100)]
    segments = ['Enterprise', 'Mid-Market', 'SMB']
    
    data = {
        'date': np.random.choice(dates, 500),
        'segment': np.random.choice(segments, 500, p=[0.2, 0.3, 0.5]),
        'revenue': np.random.uniform(1000, 50000, 500).round(2),
        'region': np.random.choice(['North America', 'Europe', 'Asia'], 500)
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# --- Task 5: Implement Filter Reset ---
if st.sidebar.button("Reset Filters"):
    st.rerun()

st.sidebar.header("Filters")

# --- Task 1: Implement Three Different Widget Types & Task 3: Meaningful Defaults ---

# Widget 1: Date range picker
min_date = df['date'].min().date()
max_date = df['date'].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Widget 2: Multi-select for segments
all_segments = df["segment"].unique().tolist()
selected_segments = st.sidebar.multiselect(
    "Segments",
    options=all_segments,
    default=all_segments
)

# Widget 3: Revenue slider
min_rev_val = int(df["revenue"].min())
max_rev_val = int(df["revenue"].max())
min_rev, max_rev = st.sidebar.slider(
    "Revenue Range",
    min_value=min_rev_val,
    max_value=max_rev_val,
    value=(min_rev_val, max_rev_val)
)

# --- Task 2: Wire Widgets to Filter the DataFrame ---
# Ensure date_range has two elements (start and end)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = date_range[0], date_range[0]

# Apply all filters to create filtered DataFrame
filtered_df = df[
    (df["date"] >= pd.Timestamp(start_date)) &
    (df["date"] <= pd.Timestamp(end_date)) &
    (df["segment"].isin(selected_segments)) &
    (df["revenue"] >= min_rev) &
    (df["revenue"] <= max_rev)
]

# --- Task 4: Handle Empty Filter Combinations ---
if len(filtered_df) == 0:
    st.warning("No data matches the current filters. Try broadening your selection.")
    st.stop()

# All downstream charts and metrics read from filtered_df
st.write(f"Showing **{len(filtered_df):,}** of **{len(df):,}** records")
st.dataframe(filtered_df.head(20), use_container_width=True)

# Add a simple chart to show interactivity downstream
st.subheader("Revenue by Segment")
if not filtered_df.empty:
    chart_data = filtered_df.groupby('segment')['revenue'].sum().reset_index()
    st.bar_chart(chart_data, x='segment', y='revenue')
