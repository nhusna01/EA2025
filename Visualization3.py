import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="AV Accident Dashboard", layout="wide")

# ---- Load Dataset ----
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# Load data directly from GitHub
csv_url = "https://raw.githubusercontent.com/nhusna01/EA2025/main/processed_av_accident_data.csv"
df = load_data(csv_url)

# ---- Page Setup ----
st.markdown("---")
st.title("Visualization 3: Examine Environmental, Operational, and Cluster-Based Factors Contributing to Incident Occurrence")

# ---- Objective & Rationale ----
st.markdown("""
### Objective 3
**Examine Environmental, Operational, and Cluster-Based Factors Contributing to Incident Occurrence**

### Rationale
This objective focuses on investigating how **roadway type, surface condition, weather, lighting, mileage,** and **temporal clusters** relate to accident frequency and distribution.  
The integration of cluster data enables the detection of **spatial or situational trends**, supporting **infrastructure planning, operational policy adjustments,** and **adaptive vehicle design enhancements**.
""")

# ---- Visualization Section ----
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
            color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF'],
            title='Speed Distribution Across Different Weather Conditions'
        )
        fig.update_layout(
            xaxis_title='Weather',
            yaxis_title='Precrash Speed (MPH)',
            title_font=dict(size=22, family='Arial Black', color='black'),
            plot_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "**Interpretation:** The violin plot shows how pre-crash speeds differ across weather conditions. Wider areas indicate higher data concentration, revealing risky speed patterns under adverse weather."
        )
    else:
        st.warning("Required columns for Violin Plot not found.")

    # ----------------- 3.2 Pie Chart: Accident Severity by Collision Type -----------------
    st.subheader("3.2 Pie Chart: Accident Severity by Collision Type")
    if "Crash_With" in df.columns and "Severity" in df.columns:
        crash_severity_counts = df.groupby(['Crash_With', 'Severity']).size().reset_index(name='Count')
        fig = px.pie(
            crash_severity_counts,
            names='Crash_With',
            values='Count',
            color='Crash_With',
            color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF'],
            title='Distribution of Accident Severity by Collision Type'
        )
        fig.update_layout(
            title_font=dict(size=22, family='Arial Black', color='black'),
            legend_title_text='Collision Type',
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "**Interpretation:** The pie chart shows the proportion of incidents by collision type. Larger segments indicate more frequent collision categories, revealing key accident risk sources."
        )
    else:
        st.warning("Required columns for Pie Chart not found.")


    # 3.3 Radar Chart: Environmental Factors by Weather
    st.subheader("3.3 Radar Chart: Environmental Factors by Weather")

    # ---- Check required columns exist ----
    required_cols = ['Weather', 'Roadway_Type', 'Roadway_Surface', 'Lighting']
    if all(col in df.columns for col in required_cols):

        # Aggregate data
        radar_data = df.groupby(required_cols).size().reset_index(name='Incident_Count')

        # Take top 3 weather conditions by total incidents
        top_weather = radar_data.groupby('Weather')['Incident_Count'].sum().nlargest(3).index
        radar_data = radar_data[radar_data['Weather'].isin(top_weather)]

        axes = ['Roadway_Type', 'Roadway_Surface', 'Lighting']
        weather_categories = radar_data['Weather'].unique()
        rainbow_colors = ['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF']

        traces = []
        for i, weather in enumerate(weather_categories):
            subset = radar_data[radar_data['Weather'] == weather]
            values = []
            for axis in axes:
                grouped = subset.groupby(axis)['Incident_Count'].sum()
                val = grouped.max() if not grouped.empty else 0
                values.append(val)
            values.append(values[0])  # close the loop

            trace = go.Scatterpolar(
                r=values,
                theta=axes + [axes[0]],
                fill='toself',
                name=weather,
                line=dict(color=rainbow_colors[i % len(rainbow_colors)], width=2),
                opacity=0.7
            )
            traces.append(trace)

        fig = go.Figure(data=traces)
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, showgrid=True, gridcolor='darkgray'),
                angularaxis=dict(showgrid=True)
            ),
            title='Radar Chart: Incident Distribution Across Environmental Factors by Weather',
            title_font=dict(size=22, family='Arial Black', color='black'),
            showlegend=True,
            legend_title_text='Weather Condition',
            plot_bgcolor='white'
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            "**Interpretation:** This radar chart compares how road type, surface, and lighting influence accident occurrences under different weather conditions. Larger areas indicate higher incident counts."
        )

    else:
        st.warning(f"Required columns {required_cols} not found in the dataset.")
