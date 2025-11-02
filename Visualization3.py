import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="AV Accident Dashboard", layout="wide")
st.title("AV Accident Dashboard")

# =========================
# Load Dataset Section
# =========================
st.markdown("---")
st.header("Load Dataset")

DATA_URL = "https://raw.githubusercontent.com/nhusna01/EA2025/main/processed_av_accident_data.csv"

try:
    df = pd.read_csv(DATA_URL)
    st.success("Dataset loaded successfully from GitHub!")
except Exception as e:
    st.error(f"Failed to load dataset. Error: {e}")
    df = None

# Display preview
if df is not None:
    st.markdown("**Data Preview**")
    st.dataframe(df.head(), use_container_width=True)

# =========================
# Objective 3 Section
# =========================
# ---- Objective 3 Section ----
st.markdown("---")
st.header("Objective 3")

st.markdown("""
This objective focuses on examining how **environmental, operational, and cluster-based factors**
(such as weather, roadway type, surface condition, lighting, and mileage) contribute to 
the occurrence and severity of AV accidents.
""")

# --- Interactive Objective Cards (3.1, 3.2, 3.3) ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("**Objective 3.1**", expanded=True):
        st.markdown("**Analyze how pre-crash vehicle speed varies under different weather conditions.**")

with col2:
    with st.expander("**Objective 3.2**", expanded=True):
        st.markdown("**Examine accident severity distribution across collision types.**")

with col3:
    with st.expander("**Objective 3.3**", expanded=True):
        st.markdown("**Evaluate how roadway type, lighting, and surface conditions interact with weather to influence accidents.**")
        
# =========================
# Visualizations Section
# =========================
# ---- Visualizations ----
st.markdown("---")
st.header("Visualizations")

# ----------------- 3.1 Violin Plot: Speed Distribution by Weather -----------------
st.subheader("3.1 Violin Plot: Speed Distribution by Weather")
if "Weather" in df.columns and "SV Precrash Speed (MPH)" in df.columns:
    fig = px.violin(
        df,
        x='Weather',
        y='SV Precrash Speed (MPH)',
        color='Weather',
        box=True,
        points='all',
        title='Speed Distribution Across Weather Conditions',
        color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF']
    )
    fig.update_layout(xaxis_title='Weather', yaxis_title='Pre-Crash Speed (MPH)', plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

    st.info("**Insight:** Most vehicles travel faster in clear weather, while speeds drop in rain or fog. "
            "The wider violin shapes in clear weather indicate more high-speed variability. "
            "Some outliers reveal high speeds even in adverse weather, suggesting risky driving behavior.")

# ----------------- 3.2 Pie Chart: Accident Severity by Collision Type -----------------
st.subheader("3.2 Pie Chart: Accident Severity by Collision Type")
if "Crash_With" in df.columns and "Severity" in df.columns:
    crash_data = df.groupby(['Crash_With']).size().reset_index(name='Count')

    fig = px.pie(
        crash_data,
        names='Crash_With',
        values='Count',
        title='Accident Proportion by Collision Type',
        color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF']
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("**Insight:** Rear-end and vehicle-to-vehicle collisions occur most frequently, making them the dominant crash types. "
            "Less frequent types like pedestrian or object collisions still contribute to injury-related cases. "
            "This suggests operational focus should prioritize high-frequency collision patterns.")

# ----------------- 3.3 Radar Chart: Environmental Factors by Weather -----------------
st.subheader("3.3 Radar Chart: Environmental Factors by Weather")

required_cols = ['Weather', 'Roadway_Type', 'Roadway_Surface', 'Lighting']
if all(col in df.columns for col in required_cols):
    radar_data = df.groupby(required_cols).size().reset_index(name='Incident_Count')
    top_weather = radar_data.groupby('Weather')['Incident_Count'].sum().nlargest(3).index
    radar_data = radar_data[radar_data['Weather'].isin(top_weather)]

    axes = ['Roadway_Type', 'Roadway_Surface', 'Lighting']
    traces = []
    for i, weather in enumerate(top_weather):
        subset = radar_data[radar_data['Weather'] == weather]
        values = [subset.groupby(axis)['Incident_Count'].sum().max() if not subset.empty else 0 for axis in axes]
        values.append(values[0])

        traces.append(go.Scatterpolar(
            r=values,
            theta=axes + [axes[0]],
            fill='toself',
            name=weather,
            opacity=0.7
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        title='Environmental Factors by Weather',
        color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF'],
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("**Insight:** Clear weather shows more incidents on urban roads with dry surfaces and proper lighting. "
            "Rainy conditions shift accidents toward wet surfaces and lower visibility areas. "
            "This indicates weather significantly alters how road and lighting factors contribute to accidents.")
