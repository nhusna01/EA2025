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
st.markdown("---")
st.header("Objective 3")

st.markdown("""
**Objective 3:**  
Examine how **environmental, operational, and cluster-based factors** contribute to autonomous vehicle incident occurrence.

This involves evaluating:
- Weather, roadway type, surface condition, lighting  
- Pre-crash speed, severity, and incident clusters  
""")

# =========================
# Visualizations Section
# =========================
st.markdown("---")
st.header("Visualizations")

# ------------------ 3.1 Violin Plot ------------------
st.subheader("3.1 Violin Plot: Speed Distribution by Weather")

if "Weather" in df.columns and "SV Precrash Speed (MPH)" in df.columns:
    fig1 = px.violin(
        df,
        x='Weather',
        y='SV Precrash Speed (MPH)',
        color='Weather',
        box=True,
        points='all',
        title='Speed Distribution Across Different Weather Conditions',
        color_discrete_sequence=[
            '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
        ]
    )
    fig1.update_layout(
        xaxis_title='Weather',
        yaxis_title='Precrash Speed (MPH)',
        plot_bgcolor='white',
        title_font=dict(size=20, family='Arial Black')
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Required columns for Violin Plot are missing.")

# ------------------ 3.2 Pie Chart ------------------
st.subheader("3.2 Pie Chart: Accident Severity by Collision Type")

if "Crash_With" in df.columns and "Severity" in df.columns:
    crash_severity_counts = df.groupby(['Crash_With', 'Severity']).size().reset_index(name='Count')
    fig2 = px.pie(
        crash_severity_counts,
        names='Crash_With',
        values='Count',
        title='Distribution of Collision Types by Severity',
        color='Crash_With',
        color_discrete_sequence=[
            '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
        ]
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Required columns for Pie Chart are missing.")

# ------------------ 3.3 Radar Chart ------------------
st.subheader("3.3 Radar Chart: Environmental Factors by Weather")

required_cols = ['Weather', 'Roadway_Type', 'Roadway_Surface', 'Lighting']
if all(col in df.columns for col in required_cols):

    radar_data = df.groupby(required_cols).size().reset_index(name='Incident_Count')
    top_weather = radar_data.groupby('Weather')['Incident_Count'].sum().nlargest(3).index
    radar_data = radar_data[radar_data['Weather'].isin(top_weather)]

    axes = ['Roadway_Type', 'Roadway_Surface', 'Lighting']
    weather_categories = radar_data['Weather'].unique()
    colors = ['#FF0000', '#FF7F00', '#FFFF00']

    fig3 = go.Figure()

    for i, weather in enumerate(weather_categories):
        subset = radar_data[radar_data['Weather'] == weather]
        values = []
        for axis in axes:
            grouped = subset.groupby(axis)['Incident_Count'].sum()
            val = grouped.max() if not grouped.empty else 0
            values.append(val)
        values.append(values[0])  # Close radar chart

        fig3.add_trace(go.Scatterpolar(
            r=values,
            theta=axes + [axes[0]],
            fill='toself',
            name=weather,
            line=dict(color=colors[i % len(colors)], width=2)
        ))

    fig3.update_layout(
        title="Radar Chart: Incident Distribution by Weather & Environmental Factors",
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning(f"Required columns {required_cols} are missing.")

