import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="AV Accident Dashboard", layout="wide")

st.title("AV Accident Dashboard")

# ---- Load Dataset Section ----
st.markdown("---")
st.header("Load Dataset")

# ---- Dataset URL ----
DATA_URL = "https://raw.githubusercontent.com/nhusna01/EA2025/main/processed_av_accident_data.csv"

# ---- Load the dataset ----
try:
    df = pd.read_csv(DATA_URL)
    st.success("Dataset loaded successfully from GitHub!")
except Exception as e:
    st.error(f"Failed to load dataset. Error: {e}")
    df = None

# ---- Display dataset preview ----
if df is not None:
    st.markdown("Data Preview")
    st.dataframe(df.head(), use_container_width=True)

# ---- Optional styling for neat layout ----
st.markdown("""
<style>
    [data-testid="stDataFrame"] {
        border: 1px solid #e3e3e3;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ---- Objective 2 Section ----

st.markdown("---")
st.header("Objective 2")

st.markdown("""
This dashboard aims to **evaluate the safety performance and reliability** of autonomous vehicles (AVs) across different manufacturers, models, model years, and operational entities for each visualization.
""")

# --- Interactive Objective Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("**Objective 2.1**", expanded=True):
        st.markdown("""
        **Compare accident frequency and severity across different AV manufacturers.**  
        Identify which companies show higher reliability and lower incident rates.
        """)

with col2:
    with st.expander("**Objective 2.2**", expanded=True):
        st.markdown("""
        **Examine performance variations between models and production years.**  
        Detect safety improvements or regressions across AV generations.
        """)

with col3:
    with st.expander("**Objective 2.3**", expanded=True):
        st.markdown("""
        **Evaluate the role of airbag deployment during a collision.**  
        Understand how airbag deployment influences severity levels.
        """)

# --- Optional Styling for Expanders ---
st.markdown("""
<style>
    .stExpander {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }
    .stExpander:hover {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# ---- Page Title for Visualization 2 ----
st.markdown("---")
st.markdown(
    """
    <h3 style='font-size:26px; color_discrete_sequence=[
            '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
        ]; font-weight:600;'>
        Visualization 2: Autonomous Vehicle Accident Analysis
    </h3>
    """,
    unsafe_allow_html=True
)

# ---- Custom Metrics with 'help' icon ----
st.markdown("Key Metrics Overview")

# --- Compute Key Metrics ---
total_manufacturers = df["Make"].nunique() if "Make" in df.columns else "N/A"
total_models = df["Model"].nunique() if "Model" in df.columns else "N/A"

# Top manufacturer by number of accidents
if "Make" in df.columns:
    top_manufacturer = df["Make"].value_counts().idxmax()
    top_manufacturer_count = df["Make"].value_counts().max()
    top_manufacturer_display = f"{top_manufacturer_count}"
else:
    top_manufacturer_display = "N/A"

# Top operational entity by accidents
if "Operating Entity" in df.columns:
    top_entity = df["Operating Entity"].value_counts().idxmax()
    top_entity_count = df["Operating Entity"].value_counts().max()
    top_entity_display = f"{top_entity_count}"
else:
    top_entity_display = "N/A"

# --- Metric Display Setup ---
metrics = [
    ("Total Manufacturers", total_manufacturers, "Number of unique vehicle manufacturers involved in accidents."),
    ("Total Vehicle Models", total_models, "Count of distinct autonomous vehicle models in the dataset."),
    ("Top Manufacturer by Accidents", top_manufacturer_display, "Manufacturer with the highest recorded accident count: Jaguar."),
    ("Top Operating Entity by Accidents", top_entity_display, "Operational entity involved in the most accidents: Waymo LLC.")
]

# --- Display Metrics in 4 Columns ---
cols = st.columns(4)
for col, (label, value, help_text) in zip(cols, metrics):
    col.markdown(f"""
        <div style="
            background-color:#F8F9FA; 
            border:1px solid #DDD; 
            border-radius:10px; 
            padding:15px; 
            text-align:center;
            min-height:120px;
            display:flex;
            flex-direction:column;
            justify-content:center;
        ">
            <div style="font-size:16px; font-weight:700; color:#1E293B; margin-bottom:8px; line-height:1.2em;">
                {label} <span title="{help_text}" style="cursor:help; color:#2563EB;">🛈</span>
            </div>
            <div style="font-size:26px; font-weight:800; color:#000;">{value}</div>
        </div>
    """, unsafe_allow_html=True)



# ---- Visualization Section ----
st.markdown("---")
st.header("Visualizations")

# --- 2.1 Histogram + Box Plot: Make Distribution by Severity ---
st.subheader("2.1 Distribution of Vehicle Makes by Accident Severity")
if "Make" in df.columns and "Severity" in df.columns:
    fig1 = px.histogram(
        df,
        x="Make",
        color="Severity",
        marginal="box",
        title="Distribution of Vehicle Makes by Severity",
        hover_data=['Make', 'Model', 'Model Year', 'Mileage', 'Cluster ID', 'Severity'],
        color_discrete_sequence=[
            '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
        ]
    )
    fig1.update_layout(
        title_font=dict(size=18, color='black', family="Arial Black"),
        xaxis_title='Vehicle Make',
        yaxis_title='Number of Incidents',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray', tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        margin=dict(l=50, r=30, t=80, b=50)
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.info("**Insight:** The histogram shows which vehicle makes are most frequently involved in incidents and how severity levels vary among them. Certain manufacturers display higher accident frequencies or more severe outcomes, suggesting potential performance or operational variations.")
else:
    st.warning("Columns 'Make' or 'Severity' not found in dataset.")


# --- 2.2 Stacked Bar Chart: Accident Distribution by Model Year and Severity ---
st.subheader("2.2 Accident Distribution by Model Year and Severity")
if "Model Year" in df.columns and "Severity" in df.columns:
    df_counts = df.groupby(['Model Year', 'Severity']).size().reset_index(name='Count')
    df_counts['Model Year'] = df_counts['Model Year'].astype(str)
    df_counts = df_counts.sort_values('Model Year')

    fig2 = px.bar(
        df_counts,
        x='Model Year',
        y='Count',
        color='Severity',
        barmode='relative',
        title='Accident Distribution by Model Year and Severity',
        color_discrete_sequence=[
            '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
        ]
    )
    fig2.update_traces(text=df_counts['Count'], textposition='outside')
    fig2.update_layout(
        plot_bgcolor='white',
        title_font=dict(size=18, color='black', family="Arial Black"),
        xaxis_title='Model Year',
        yaxis_title='Number of Incidents',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.info("**Insight:** This stacked bar chart highlights how accident severity differs across vehicle model years. Certain years show higher frequencies of severe incidents, indicating that production year may influence vehicle reliability and safety performance.")
else:
    st.warning("Columns 'Model Year' or 'Severity' not found in dataset.")


# --- 2.3 Density Plot: Severity by Air Bag Deployment ---
st.subheader("2.3 Severity Distribution by Air Bag Deployment Status")
if "Air_Bag" in df.columns and "Severity" in df.columns:
    fig3 = px.violin(
        df,
        x="Air_Bag",
        y="Severity",
        color="Air_Bag",
        box=True,
        points="all",
        title="Severity Distribution by Air Bag Deployment",
        color_discrete_sequence=[
            '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
        ]
    )
    fig3.update_traces(opacity=0.85, line=dict(width=1.5), marker=dict(size=4, opacity=0.6))
    fig3.update_layout(
        title_font=dict(size=18, color='black', family="Arial Black"),
        plot_bgcolor='white',
        xaxis_title='Air Bag Deployment Status',
        yaxis_title='Severity',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        showlegend=True,
        legend_title_text='Air Bag Deployment'
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.info("**Insight:** The density plot visualizes how accident severity distributes between vehicles with and without airbag deployment. Wider sections show higher concentrations of incidents, indicating that airbag activation relates closely to the severity of collisions.")
else:
    st.warning("Columns 'Air_Bag' or 'Severity' not found in dataset.")
