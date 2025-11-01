import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="AV Accident Dashboard", layout="wide")

# ---- Load dataset ----
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

csv_url = "https://raw.githubusercontent.com/nhusna01/EA2025/main/processed_av_accident_data.csv"
df = load_data(csv_url)

# ---- Initialize session_state ----
if "page" not in st.session_state:
    st.session_state.page = "Menu"

# ---- Function to change pages ----
def go_to(page_name):
    st.session_state.page = page_name

# ---- MENU PAGE ----
if st.session_state.page == "Menu":
    st.title("Menu Page")
    st.write("Welcome to the AV Accident Data Dashboard!")

    st.subheader("Dataset Preview")
    st.dataframe(df)

    st.subheader("Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Accidents", len(df))
    col2.metric(
        "Total Fatalities",
        df["Number_of_Casualties"].sum() if "Number_of_Casualties" in df.columns else "N/A"
    )
    col3.metric(
        "Average Vehicles",
        f"{df['Number_of_Vehicles'].mean():.2f}" if "Number_of_Vehicles" in df.columns else "N/A"
    )
    col4.metric(
        "Average Speed Limit",
        f"{df['Speed_Limit'].mean():.2f}" if "Speed_Limit" in df.columns else "N/A"
    )

    st.subheader("Select the Visualizations")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Visualization 1"):
            go_to("Visualization 1")

# ---- Visualization 1 ----
elif st.session_state.page == "Visualization 1":
    st.title("Visualization 1: AV Accident Analysis")

    ## --- 1.1 Box Plot: Pre-crash Speed vs Severity ---
    st.subheader("1.1 Pre-crash Speed vs Severity")
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
        fig1.update_layout(title_font=dict(size=20, color='black', family="Arial Black"), plot_bgcolor='white')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(
            "**Interpretation:** Higher pre-crash speeds are associated with greater accident severity."
        )
    else:
        st.warning("Columns 'Severity' or 'SV Precrash Speed (MPH)' not found.")

    ## --- 1.2 Grouped Bar: Severity by Lighting ---
    st.subheader("1.2 Severity by Lighting Conditions")
    if "Severity" in df.columns and "Lighting" in df.columns:
        counts = df.groupby(['Severity', 'Lighting']).size().reset_index(name='Count')
        fig2 = px.bar(
            counts,
            x='Severity',
            y='Count',
            color='Lighting',
            barmode='group',
            title='Severity by Lighting',
            color_discrete_sequence=['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#FF00FF']
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
        st.markdown(
            "**Interpretation:** Lighting conditions affect accident severity. Bar labels show counts clearly."
        )
    else:
        st.warning("Columns 'Severity' or 'Lighting' not found.")

    ## --- 1.3 Correlation Heatmap ---
    st.subheader("1.3 Correlation Heatmap")
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
            title="Correlation Heatmap"
        )
        fig3.update_layout(title_font=dict(size=18, color='black', family="Arial Black"), plot_bgcolor='white')
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown(
            "**Interpretation:** Brighter warm colors indicate stronger positive correlations."
        )
    else:
        st.warning("Required numeric columns not found.")

    # --- Back to Menu Button ---
    if st.button("⬅ Back to Menu"):
        go_to("Menu")
