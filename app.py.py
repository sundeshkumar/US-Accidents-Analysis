import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. PAGE CONFIGURATION (Title aur Layout)
st.set_page_config(page_title="US Accidents Dashboard", layout="wide")

st.title("🚗 US Accidents Analysis Dashboard")
st.markdown("""
Yeh dashboard US Accidents data (2016-2023) ko analyze kar raha hai. 
Aap left side se **State** aur **Severity** filter kar sakte hain.
""")

# 2. DATA LOAD KARNA (Cache use kar rahe hain taake fast chale)
@st.cache_data
def load_data():
    try:
        # 1. CHANGE: Rows barha kar 1 Lakh (100,000) kar dein
        df = pd.read_csv(r"C:\Users\sunde\Desktop\Data Mining Project\US_Accidents_March23.csv", nrows=100000)
        
        # Date column fix karna
        if 'Start_Time' in df.columns:
            df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')

        # 2. CHANGE: Missing Values (NaN) ko fix karna (Jadoo ki line)
        # Numerics ko 0 se bhar dein, taake graphs crash na hon
        df_numeric = df.select_dtypes(include=['number'])
        df[df_numeric.columns] = df_numeric.fillna(0)
        
        # Text columns mein agar kuch missing hai to "Unknown" likh dein
        df_text = df.select_dtypes(include=['object'])
        df[df_text.columns] = df_text.fillna("Unknown")

        return df
    except FileNotFoundError:
        return None
# Loading text dikhana
data_load_state = st.text('Loading data... (Thora wait karein)')
df = load_data()
data_load_state.text('Data Loaded Successfully! ✅')

# 3. SIDEBAR FILTERS (User apni marzi ka data dekh sake)
st.sidebar.header("🔍 Filters")

# State Filter
state_list = df['State'].unique()
selected_state = st.sidebar.selectbox("Select State", state_list, index=0)

# Severity Filter
severity_list = df['Severity'].unique()
selected_severity = st.sidebar.multiselect("Select Severity Level", severity_list, default=severity_list)

# Data ko Filter karna based on selection
filtered_df = df[(df['State'] == selected_state) & (df['Severity'].isin(selected_severity))]

# 4. KEY METRICS (Upar 3 dabbay)
col1, col2, col3 = st.columns(3)
col1.metric("Total Accidents", len(filtered_df))
col2.metric("Most Common City", filtered_df['City'].mode()[0] if not filtered_df.empty else "N/A")
col3.metric("Avg Temperature", f"{filtered_df['Temperature(F)'].mean():.1f} °F")

# 5. VISUALIZATIONS (Graphs)

# Row 1: Map aur Time Chart
c1, c2 = st.columns((1, 1))

with c1:
    st.subheader(f"📍 Accident Map ({selected_state})")
    # Agar data hai to map dikhao
    if not filtered_df.empty:
        st.map(filtered_df[['latitude', 'longitude']].dropna())
    else:
        st.write("No data available for this selection.")

with c2:
    st.subheader("⏰ Accidents by Hour (Rush Hour Check)")
    if not filtered_df.empty:
        fig, ax = plt.subplots()
        sns.histplot(filtered_df['Hour'], bins=24, kde=False, color='orange')
        plt.xlabel("Hour of Day")
        plt.ylabel("Accidents")
        st.pyplot(fig)
    else:
        st.write("No data.")

# Row 2: Weather Analysis
st.subheader("🌧️ Weather Conditions during Accidents")
if not filtered_df.empty:
    top_weather = filtered_df['Weather_Condition'].value_counts().head(10)
    st.bar_chart(top_weather)

# Footer
st.markdown("---")
st.markdown("Created for Data Mining Project")