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

# ---- Objectives Section ----

st.markdown("---")
st.header("Objectives")

st.markdown("""
This dashboard aims to **analyze Autonomous Vehicle (AV) accident data** and uncover key insights into accident patterns and contributing factors.
""")

# --- Interactive Objective Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("**Objective 1.1**", expanded=True):
        st.markdown("""
        **Analyze the relationship between pre-crash speed and accident severity.**  
        Explore how varying speeds contribute to the severity levels of autonomous vehicle crashes.
        """)

with col2:
    with st.expander("**Objective 1.2**", expanded=True):
        st.markdown("""
        **Examine the influence of lighting conditions on accident outcomes.**  
        Understand how visibility factors, such as day, night, or dusk, affect crash frequency.
        """)

with col3:
    with st.expander("**Objective 1.3**", expanded=True):
        st.markdown("""
        **Identify correlations between vehicle speed, mileage, and posted speed limits.**  
        Detect operational patterns that may reveal safety or performance risks.
        """)

# Optional: Subtle styling
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

# ---- Page Title ----
st.markdown("---")
st.markdown(
    """
    <h3 style='font-size:26px; color_discrete_sequence=[
            '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
        ]; font-weight:600;'>
        Visualization 1: Autonomous Vehicle Accident Analysis
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
    top_manufacturer_display = f"{top_manufacturer} ({top_manufacturer_count})"
else:
    top_manufacturer_display = "N/A"

# Top operational entity by accidents
if "Operating Entity" in df.columns:
    top_entity = df["Operating Entity"].value_counts().idxmax()
    top_entity_count = df["Operating Entity"].value_counts().max()
    top_entity_display = f"{top_entity} ({top_entity_count})"
else:
    top_entity_display = "N/A"

# --- Metric Display Setup ---
metrics = [
    ("Total Manufacturers", total_manufacturers, "Number of unique vehicle manufacturers involved in accidents."),
    ("Total Vehicle Models", total_models, "Count of distinct autonomous vehicle models in the dataset."),
    ("Top Manufacturer by Accidents", top_manufacturer_display, "Manufacturer with the highest recorded accident count."),
    ("Top Operating Entity by Accidents", top_entity_display, "Operational entity involved in the most accidents.")
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
st.header(" Visualizations")

# --- 1.1 Box Plot: Pre-crash Speed vs Severity ---
st.subheader("1.1  Distribution of Pre-Crash Speed Across Accident Severity Levels")
if "Severity" in df.columns and "SV Precrash Speed (MPH)" in df.columns:
    fig1 = px.box(
        df,
        x="Severity",
        y="SV Precrash Speed (MPH)",
        color="Severity",
        title="Pre-crash Speed vs Severity",
        color_discrete_sequence=[
            '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
        ]
    )
    fig1.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=1)
    fig1.update_layout(
        title_font=dict(size=18, color='black', family="Arial Black"),
        plot_bgcolor='white'
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.info(" **Insight:** Higher pre-crash speeds are associated with greater accident severity. Outliers detected the highest among POD severity as SV Precrash Speed (MPH) increased compared to minor and moderate")
else:
    st.warning("Columns 'Severity' or 'SV Precrash Speed (MPH)' not found in dataset.")

# --- 1.2 Grouped Bar: Severity by Lighting ---
st.subheader("1.2 Impact of Lighting Conditions on Accident Severity")
if "Severity" in df.columns and "Lighting" in df.columns:
    counts = df.groupby(['Severity', 'Lighting']).size().reset_index(name='Count')
    fig2 = px.bar(
        counts,
        x='Severity',
        y='Count',
        color='Lighting',
        barmode='group',
        title='Accident Severity Distribution under Various Lighting Conditions',
        color_discrete_sequence=[
            '#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#FF00FF'
        ]
    )
    fig2.update_traces(text=counts['Count'], textposition='outside')
    fig2.update_layout(
        plot_bgcolor='white',
        title_font=dict(size=18, color='black', family="Arial Black"),
        xaxis_title='Severity',
        yaxis_title='Count of Incidents',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.info("**Insight:** Lighting conditions influence accident severity, while poor visibility often leads to more severe outcomes. Among those lighting shows, accident occurrences cause POD severity at the highest compared to serious injuries.")
else:
    st.warning("Columns 'Severity' or 'Lighting' not found in dataset.")

# --- 1.3 Correlation Heatmap ---
st.subheader("1.3 Correlation Between Key Driving Parameters")
required_cols = ['Mileage', 'Posted Speed Limit (MPH)', 'SV Precrash Speed (MPH)']
if all(col in df.columns for col in required_cols):
    corr_vars = df[required_cols].apply(pd.to_numeric, errors='coerce').dropna()
    corr_matrix = corr_vars.corr(method='pearson')
    fig3 = px.imshow(
        corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        color_continuous_scale=['#FFFF00', '#FF7F00', '#FF0000'],
        text_auto=".2f",
        aspect="auto",
        title="Correlation Matrix of Driving Variables"
    )
    fig3.update_layout(
        title_font=dict(size=18, color='black', family="Arial Black"),
        plot_bgcolor='white'
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.info(" **Insight:** Stronger warm colors indicate stronger positive correlations between the numeric variables. Posted Speed Limit shows strong positive relationships with SV Precrash Speed, meanwhile mileage contribute weak correlation towards both speed variables.")
else:
    st.warning("Required numeric columns not found for correlation analysis.")
