import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="AV Accident Dashboard", layout="wide")

# ---- Load Dataset ----
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# Load data directly from GitHub
csv_url = "https://raw.githubusercontent.com/nhusna01/EA2025/main/processed_av_accident_data.csv"
df = load_data(csv_url)

# ---- Page Title ----
st.title("Visualization 1: Autonomous Vehicle Accident Analysis")

# ---- Dataset Summary ----
st.markdown("---")
st.header("📊 Dataset Summary")

# ---- Custom CSS to center metrics ----
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #F8F9FA;
        border: 1px solid #DADCE0;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        justify-content: center;
    }
    [data-testid="stMetricLabel"] {
        text-align: center !important;
        font-weight: 600 !important;
        color: #2C3E50 !important;
    }
    [data-testid="stMetricValue"] {
        text-align: center !important;
        font-size: 24px !important;
        font-weight: bold !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown(
        """
        <div style="background-color:#F8F9FA; padding:20px; border-radius:10px; border:1px solid #DDD;">
        <h4 style="color:#2C3E50;">Data Overview</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display dataset preview
    st.dataframe(df.head(), use_container_width=True)

    # ---- Metrics Summary (Centered Style) ----
    col1, col2, col3, col4 = st.columns(4)

    total_records = len(df)
    unique_severity = df["Severity"].nunique() if "Severity" in df.columns else "N/A"
    avg_speed = f"{df['SV Precrash Speed (MPH)'].mean():.2f}" if "SV Precrash Speed (MPH)" in df.columns else "N/A"
    avg_limit = f"{df['Posted Speed Limit (MPH)'].mean():.2f}" if "Posted Speed Limit (MPH)" in df.columns else "N/A"

    col1.metric(
        label="Total Accident Records",
        value=total_records,
        help="Total number of accident cases recorded in the dataset.",
        border=True
    )
    col2.metric(
        label="Unique Severity Levels",
        value=unique_severity,
        help="Number of distinct severity categories found (POD (Fatal), Serious, Moderate, Minor).",
        border=True
    )
    col3.metric(
        label="Average Pre-Crash Speed (MPH)",
        value=avg_speed,
        help="Mean pre-crash vehicle speed across all records.",
        border=True
    )
    col4.metric(
        label="Average Posted Speed Limit (MPH)",
        value=avg_limit,
        help="Mean posted speed limit for all accident locations.",
        border=True
    )


# ---- Objectives Section ----
st.markdown("---")
st.header("Objectives")

st.markdown("""
This dashboard aims to **analyze Autonomous Vehicle (AV) accident data** to uncover meaningful insights on accident trends.

**Key objectives:**
1. Examine the relationship between **pre-crash speed** and **accident severity**.  
2. Understand how **lighting conditions** influence accident outcomes.  
3. Identify correlations between **vehicle speed, mileage, and posted speed limits**.
""")

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
    st.info(" **Insight:** Higher pre-crash speeds are associated with greater accident severity.")
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
    st.info("**Insight:** Lighting conditions influence accident severity — poor visibility often leads to more severe outcomes.")
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
    st.info(" **Insight:** Stronger warm colors indicate stronger positive correlations between the numeric variables.")
else:
    st.warning("Required numeric columns not found for correlation analysis.")
