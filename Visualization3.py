import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---- Page Setup ----
st.markdown("---")
st.title("Visualization 3: Examine Environmental, Operational, and Cluster-Based Factors Contributing to Incident Occurrence")

# ---- Objective & Rationale ----
st.markdown("""
### 🎯 Objective 3
**Examine Environmental, Operational, and Cluster-Based Factors Contributing to Incident Occurrence**

### 🧩 Rationale
This objective focuses on investigating how **roadway type, surface condition, weather, lighting, mileage,** and **temporal clusters** relate to accident frequency and distribution.  
The integration of cluster data enables the detection of **spatial or situational trends**, supporting **infrastructure planning, operational policy adjustments,** and **adaptive vehicle design enhancements**.
""")

# ---- Sidebar Filters ----
st.sidebar.header("Filters for Objective 3")

weather_filter = st.sidebar.multiselect(
    "Select Weather Conditions:",
    options=sorted(df["Weather"].dropna().unique()) if "Weather" in df.columns else [],
    default=None,
    placeholder="Filter by weather..."
)

cluster_filter = st.sidebar.multiselect(
    "Select Cluster IDs:",
    options=sorted(df["Cluster ID"].dropna().unique()) if "Cluster ID" in df.columns else [],
    default=None,
    placeholder="Filter by cluster..."
)

severity_filter = st.sidebar.multiselect(
    "Select Severity Levels:",
    options=sorted(df["Severity"].dropna().unique()) if "Severity" in df.columns else [],
    default=None,
    placeholder="Filter by severity..."
)

# Apply filters dynamically
filtered_df = df.copy()
if weather_filter:
    filtered_df = filtered_df[filtered_df["Weather"].isin(weather_filter)]
if cluster_filter:
    filtered_df = filtered_df[filtered_df["Cluster ID"].isin(cluster_filter)]
if severity_filter:
    filtered_df = filtered_df[filtered_df["Severity"].isin(severity_filter)]

# ---- Visualization Section ----
st.markdown("---")
st.header("Visualizations")

# ----------------- 3.1 Violin Plot: Speed Distribution by Weather -----------------
st.subheader("3.1 Pre-Crash Speed Distribution by Weather Condition")

if "Weather" in df.columns and "SV Precrash Speed (MPH)" in df.columns:
    fig1 = px.violin(
        filtered_df,
        x='Weather',
        y='SV Precrash Speed (MPH)',
        color='Weather',
        box=True,
        points='all',
        color_discrete_sequence=px.colors.qualitative.Bold,
        title='Speed Distribution Across Different Weather Conditions'
    )
    fig1.update_layout(
        xaxis_title='Weather',
        yaxis_title='Precrash Speed (MPH)',
        title_font=dict(size=22, family='Arial Black', color='black'),
        plot_bgcolor='white'
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""
    <div style='background-color:#F8F9FA; padding:12px; border-radius:10px; border:1px solid #DDD;'>
    <b>Interpretation:</b> This plot shows how vehicle pre-crash speeds vary under different weather conditions. 
    Adverse weather (e.g., rain or fog) tends to increase variability in pre-crash speeds, revealing operational risk patterns under environmental constraints.
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Required columns for Violin Plot not found.")


# ----------------- 3.2 Pie Chart: Accident Distribution by Roadway Surface -----------------
st.subheader("3.2 Proportion of Accidents by Roadway Surface Type")

if "Roadway_Surface" in df.columns and "Severity" in df.columns:
    surface_counts = filtered_df.groupby(['Roadway_Surface', 'Severity']).size().reset_index(name='Count')

    fig2 = px.pie(
        surface_counts,
        names='Roadway_Surface',
        values='Count',
        color='Roadway_Surface',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        title='Distribution of Incidents by Roadway Surface Condition'
    )
    fig2.update_layout(
        title_font=dict(size=22, family='Arial Black', color='black'),
        legend_title_text='Roadway Surface Type',
        showlegend=True
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
    <div style='background-color:#F8F9FA; padding:12px; border-radius:10px; border:1px solid #DDD;'>
    <b>Interpretation:</b> This pie chart highlights how different roadway surface types (e.g., dry, wet, icy) 
    contribute to overall accident frequency. A higher proportion on wet or slippery surfaces may indicate 
    environmental and operational vulnerabilities influencing incident occurrence.
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Required columns for Pie Chart not found.")


# ----------------- 3.3 Radar Chart: Environmental Factors by Cluster -----------------
st.subheader("3.3 Radar Chart: Environmental Factors Across Clusters")

required_cols = ['Cluster ID', 'Weather', 'Roadway_Type', 'Lighting']
if all(col in df.columns for col in required_cols):
    radar_data = filtered_df.groupby(required_cols).size().reset_index(name='Incident_Count')

    # Let user choose number of clusters to display
    top_n_clusters = st.slider("Select number of top clusters to display:", 2, 5, 3)
    top_clusters = radar_data.groupby('Cluster ID')['Incident_Count'].sum().nlargest(top_n_clusters).index
    radar_data = radar_data[radar_data['Cluster ID'].isin(top_clusters)]

    axes = ['Weather', 'Roadway_Type', 'Lighting']
    cluster_categories = radar_data['Cluster ID'].unique()
    colors = px.colors.qualitative.Bold

    traces = []
    for i, cluster in enumerate(cluster_categories):
        subset = radar_data[radar_data['Cluster ID'] == cluster]
        values = [subset.groupby(axis)['Incident_Count'].sum().sum() for axis in axes]
        values.append(values[0])  # close the radar loop
        traces.append(go.Scatterpolar(
            r=values,
            theta=axes + [axes[0]],
            fill='toself',
            name=f"Cluster {cluster}",
            line=dict(color=colors[i % len(colors)], width=2),
            opacity=0.7
        ))

    fig3 = go.Figure(data=traces)
    fig3.update_layout(
        polar=dict(radialaxis=dict(visible=True, showgrid=True, gridcolor='lightgray')),
        title='Environmental Factor Patterns Across Clusters',
        title_font=dict(size=22, family='Arial Black', color='black'),
        showlegend=True,
        legend_title_text='Cluster ID',
        plot_bgcolor='white'
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <div style='background-color:#F8F9FA; padding:12px; border-radius:10px; border:1px solid #DDD;'>
    <b>Interpretation:</b> The radar chart compares how environmental and roadway conditions 
    contribute to incidents across different clusters. Each cluster represents a distinct 
    situational pattern — such as weather severity or roadway lighting — enabling deeper 
    understanding of context-specific accident risks.
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning(f"Required columns {required_cols} not found in the dataset.")

