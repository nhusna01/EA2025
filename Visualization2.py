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

# ---- Custom Metrics Aligned with Objective 2 ----
st.markdown("### Key Metrics Overview")

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

metrics = [
    ("Total Manufacturers", total_manufacturers, "Unique vehicle manufacturers involved in accidents."),
    ("Total Vehicle Models", total_models, "Distinct vehicle models involved in accidents."),
    ("Top Manufacturer by Accidents", top_manufacturer_display, "Manufacturer with the highest number of accidents."),
    ("Top Operating Entity by Accidents", top_entity_display, "Operating entity with the highest number of accidents.")
]

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
                {label} <span title="{help_text}" style="cursor:help; color:#2563EB;">❓</span>
            </div>
            <div style="font-size:26px; font-weight:800; color:#000;">{value}</div>
        </div>
    """, unsafe_allow_html=True)


# ---- Visualization Section ----
st.markdown("---")
st.header("Visualizations")

# ---- Visualization: Make Distribution by Severity (Histogram + Box) ----
st.subheader("2.1 Make Distribution by Severity (Histogram with Box Plot)")

# Check if required columns exist
required_cols = ['Make', 'Severity']
if all(col in df.columns for col in required_cols):
    fig = px.histogram(
        df,
        x='Make',
        color='Severity',
        marginal='box',  # Optional box plot above
        title='Make Distribution by Severity',
        hover_data=['Make', 'Model', 'Model Year', 'Mileage', 'Cluster ID', 'Severity'],
        color_discrete_sequence=[
            '#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#FF00FF'
        ]
    )

    # Layout improvements
    fig.update_layout(
        plot_bgcolor='#FFFFFF',
        title_font=dict(size=22, color='black', family='Arial Black'),
        xaxis_title='Make',
        yaxis_title='Number of Incidents',
        xaxis=dict(title_font=dict(size=16, color='black'),
                   tickfont=dict(size=12, color='black')),
        yaxis=dict(title_font=dict(size=16, color='black'),
                   tickfont=dict(size=12, color='black')),
        legend_title_font=dict(size=14, color='black'),
        legend_font=dict(size=12),
        margin=dict(l=50, r=30, t=80, b=50)
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Add interpretation text
    st.markdown("""
    <div style='background-color:#F8F9FA; padding:15px; border-radius:10px; border:1px solid #DDD;'>
        <span style='color:black; font-weight:bold; font-size:14pt;'>
        **Interpretation:** The histogram shows the distribution of incidents across different vehicle makes, 
        colored by severity. This allows us to see which makes are involved in the most incidents and how severity 
        is distributed among them.
        </span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Required columns ('Make', 'Severity') not found in dataset.")


# ----------------- 2.2 Stacked Bar: Accident Distribution by Model Year -----------------
st.subheader("2.2 Accident Distribution by Model Year and Severity (Stacked Bar)")
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
        color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF'],
        title='Accident Distribution by Model Year and Severity'
    )
    fig2.update_layout(
        xaxis_title='Model Year',
        yaxis_title='Number of Incidents',
        plot_bgcolor='white',
        title_font=dict(size=18, color='black', family='Arial Black')
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("**Interpretation:** This stacked bar chart shows how accident severity varies across vehicle model years. It highlights which model years have higher counts and severe incidents.")
else:
    st.warning("Required columns for Stacked Bar not found.")

# ----------------- 2.3 Violin Plot: Severity by Air Bag Deployment -----------------
st.subheader("2.3 Severity Distribution by Air Bag Deployment (Violin Plot)")
if "Air_Bag" in df.columns and "Severity" in df.columns:
    fig3 = px.violin(
        df,
        x='Air_Bag',
        y='Severity',
        color='Air_Bag',
        color_discrete_sequence=['#FF0000','#FF7F00','#FFFF00','#00FF00','#00FFFF','#0000FF','#FF00FF'],
        box=True,
        points='all',
        title='Severity Distribution by Air Bag Deployment'
    )
    fig3.update_traces(opacity=0.8, line=dict(width=1.5), marker=dict(size=4, opacity=0.6))
    fig3.update_layout(
        xaxis_title='Air Bag Deployment Status',
        yaxis_title='Severity',
        plot_bgcolor='white',
        title_font=dict(size=18, family='Arial Black', color='black'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        showlegend=True,
        legend_title_text='Air Bag Status'
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("**Interpretation:** This violin plot shows severity distribution for vehicles with and without airbags. Wider areas indicate higher concentration of incidents for each severity level.")
else:
    st.warning("Required columns for Violin Plot not found.")
