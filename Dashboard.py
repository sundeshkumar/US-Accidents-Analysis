import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="US Accidents Analysis", layout="wide")

st.title("🚦 US Accidents Analysis Dashboard")
st.markdown("This dashboard provides insights into accident trends, hotspots, and environmental factors.")

# --- 1. DATA LOADING (Cached for performance) ---
@st.cache_data
def load_data():
    # REPLACE with your actual file name
    # We use a sample for speed in the dashboard. If you have the full file, use that.
    df = pd.read_csv(r"C:\Users\sunde\Desktop\Data Mining Project\US_Accidents_March23.csv", nrows=100000) 
    
    # Quick date conversion if not already saved as datetime
    if 'Start_Time' in df.columns:
        df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
        df['Year'] = df['Start_Time'].dt.year
        df['Hour'] = df['Start_Time'].dt.hour
    return df

# Load the data
with st.spinner('Loading data...'):
    df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
selected_state = st.sidebar.selectbox("Select State", sorted(df['State'].unique()))

# Filter the dataset based on selection
df_filtered = df[(df['Year'] == selected_year) & (df['State'] == selected_state)]

# --- KEY METRICS ROW ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Accidents", f"{len(df_filtered):,}")
col2.metric("Most Common City", df_filtered['City'].mode()[0] if not df_filtered.empty else "N/A")
col3.metric("Avg Severity", f"{df_filtered['Severity'].mean():.2f}")

st.markdown("---")

# --- CHART 1: ACCIDENT HOTSPOTS (MAP) ---
st.header(f"📍 Accident Hotspots in {selected_state} ({selected_year})")
if not df_filtered.empty:
    # Rename for Streamlit Map compatibility
    map_data = df_filtered[['Start_Lat', 'Start_Lng']].rename(columns={'Start_Lat': 'lat', 'Start_Lng': 'lon'})
    st.map(map_data)
else:
    st.write("No data available for this selection.")

st.markdown("---")

# --- CHART 2: TIME PATTERNS (LINE CHART) ---
st.header("📈 Accidents Over Time")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Hourly Trend (Rush Hour)")
    hourly_counts = df_filtered['Hour'].value_counts().sort_index()
    fig_hour = px.line(x=hourly_counts.index, y=hourly_counts.values, 
                       labels={'x': 'Hour of Day', 'y': 'Accident Count'},
                       title="Accidents by Hour")
    st.plotly_chart(fig_hour, use_container_width=True)

with col_right:
    st.subheader("Monthly Trend")
    # Group by month
    monthly_counts = df_filtered.set_index('Start_Time').resample('M').size()
    fig_month = px.line(x=monthly_counts.index, y=monthly_counts.values,
                        labels={'x': 'Date', 'y': 'Accident Count'},
                        title="Accidents by Month")
    st.plotly_chart(fig_month, use_container_width=True)

st.markdown("---")

# --- CHART 3: ENVIRONMENTAL FACTORS (BAR CHART) ---
st.header("🌧️ Impact of Weather")
weather_counts = df_filtered['Weather_Condition'].value_counts().head(10)
fig_weather = px.bar(x=weather_counts.values, y=weather_counts.index, orientation='h',
                     labels={'x': 'Count', 'y': 'Condition'},
                     title="Top 10 Weather Conditions for Accidents",
                     color=weather_counts.values, color_continuous_scale='Viridis')
st.plotly_chart(fig_weather, use_container_width=True)

st.markdown("---")

# --- CHART 4: MODEL PERFORMANCE (CONFUSION MATRIX) ---
st.header("🤖 Prediction Model Performance")
st.write("This heatmap shows how well the Random Forest model predicted Accident Severity (Class 1-4).")

# NOTE: Since the model runs in a separate notebook, we usually load a saved image or CSV here.
# For this demo, we will simulate the Confusion Matrix data to show you how to code the visualization.
# You can replace this with your actual 'cm' array from Week 4.

# Example Data (Replace this list with your actual confusion matrix values)
import numpy as np
dummy_cm = np.array([[50, 10, 0, 0], 
                     [5, 400, 20, 5], 
                     [0, 30, 150, 10], 
                     [0, 5, 20, 60]])

fig_cm = px.imshow(dummy_cm, 
                   labels=dict(x="Predicted Severity", y="Actual Severity", color="Count"),
                   x=['1', '2', '3', '4'],
                   y=['1', '2', '3', '4'],
                   text_auto=True, aspect="auto", color_continuous_scale='Blues')

fig_cm.update_layout(title="Confusion Matrix (Model Accuracy)")
st.plotly_chart(fig_cm, use_container_width=True)

# Add a small conclusion box
st.info("Insight: The model is most accurate at predicting Severity 2 accidents (the majority class), but struggles slightly with distinguishing between Severity 3 and 4.")