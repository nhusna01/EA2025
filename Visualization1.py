import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="AV Accident Dashboard", layout="wide")

# ---- Load Dataset Section ----
import streamlit as st
import pandas as pd

st.markdown("---")
st.header("Load Dataset")

# Option 1: Upload your own CSV file
uploaded_file = st.file_uploader("Upload your AV Accident dataset (.csv)", type=["csv"])

# Option 2: Use default dataset if no file uploaded
default_path = "AV_Accidents.csv"  # change to your actual file path

if uploaded_file is not None:
    # Read uploaded dataset
    df = pd.read_csv(uploaded_file)
    st.success("✅ Dataset uploaded successfully!")
elif st.checkbox("Use default dataset"):
    try:
        df = pd.read_csv(default_path)
        st.success("✅ Default dataset loaded successfully!")
    except FileNotFoundError:
        st.error("⚠️ Default dataset not found. Please upload a CSV file.")
        df = None
else:
    st.info("Please upload a dataset file or select the checkbox to use the default dataset.")
    df = None

# Display dataset preview
if df is not None:
    st.markdown("### 🔍 Data Preview")
    st.dataframe(df.head(), use_container_width=True)


# Optional styling for neat layout
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
import streamlit as st

st.markdown("---")
st.header("Objectives")

st.markdown("""
This dashboard aims to **analyze Autonomous Vehicle (AV) accident data** and uncover key insights into accident patterns and contributing factors.
""")

# --- Interactive Objective Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("**Objective 1**", expanded=True):
        st.markdown("""
        **Analyze the relationship between pre-crash speed and accident severity.**  
        Explore how varying speeds contribute to the severity levels of autonomous vehicle crashes.
        """)

with col2:
    with st.expander("**Objective 2**", expanded=True):
        st.markdown("""
        **Examine the influence of lighting conditions on accident outcomes.**  
        Understand how visibility factors, such as day, night, or dusk, affect crash frequency.
        """)

with col3:
    with st.expander("**Objective 3**", expanded=True):
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
st.title("Visualization 1: Autonomous Vehicle Accident Analysis")

# ---- Custom Metrics with 'help' icon ----
total_records = len(df)
unique_severity = df["Severity"].nunique() if "Severity" in df.columns else "N/A"
avg_speed = f"{df['SV Precrash Speed (MPH)'].mean():.2f}" if "SV Precrash Speed (MPH)" in df.columns else "N/A"
avg_limit = f"{df['Posted Speed Limit (MPH)'].mean():.2f}" if "Posted Speed Limit (MPH)" in df.columns else "N/A"

metrics = [
    ("Total Accident Records", total_records, "Total number of accident cases recorded in the dataset."),
    ("Unique Severity Levels", unique_severity, "Number of distinct severity categories (POD, Serious, Moderate, Minor)."),
    ("Average Pre-Crash Speed (MPH)", avg_speed, "Mean pre-crash vehicle speed across all records."),
    ("Average Posted Speed Limit (MPH)", avg_limit, "Mean posted speed limit for all accident locations.")
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
