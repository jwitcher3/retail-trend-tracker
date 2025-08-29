# Retail Trend Tracker Dashboard (Streamlit)

import streamlit as st
import pandas as pd
import plotly.express as px

# Load trend data from CSV
@st.cache_data
def load_data():
    return pd.read_csv("trends.csv", parse_dates=["date"])

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
segment = st.sidebar.selectbox("Select Segment", df['segment'].unique())
region = st.sidebar.selectbox("Select Region", df['region'].unique())

# Filtered data
filtered_df = df[(df['segment'] == segment) & (df['region'] == region)]

# Melt for Plotly
melted = filtered_df.melt(
    id_vars=['date'],
    value_vars=[col for col in df.columns if col not in ['date', 'isPartial', 'country', 'segment', 'region']],
    var_name='Trend',
    value_name='Interest'
)

# App layout
st.title("📈 Retail Trend Tracker Dashboard")
st.markdown(f"Showing **{segment}** trends in **{region}**")

fig = px.line(
    melted,
    x='date',
    y='Interest',
    color='Trend',
    title=f"{region} {segment} Trends (Google Trends)"
)
fig.update_layout(xaxis_title='Date', yaxis_title='Google Trends Interest')
st.plotly_chart(fig, use_container_width=True)
