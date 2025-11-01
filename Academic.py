import streamlit as st
import pandas as pd
import plotly.express as px

# --- CSV File Path (raw GitHub link) ---
csv_url = "https://raw.githubusercontent.com/nhusna01/EA2025/main/processed_av_accident_data.csv"

# ---- Initialize session_state ----
if "page" not in st.session_state:
    st.session_state.page = "Menu"

# ---- Function to change pages ----
def go_to(page_name):
    st.session_state.page = page_name

# ---- Load dataset ----
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# ---- PAGE CONTENT ----
if st.session_state.page == "Menu":
    st.title("Menu Page")
    st.write("Welcome to the AV Accident Data Dashboard!")

    # --- Dataset preview ---
    st.subheader("Dataset Preview")
    st.dataframe(df)

    # --- Metrics ---
    st.subheader("AV Accident Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Accidents", len(df))
    col2.metric("Total Fatalities", df["Number_of_Casualties"].sum() if "Number_of_Casualties" in df.columns else "N/A")
    col3.metric("Average Vehicles", f"{df['Number_of_Vehicles'].mean():.2f}" if "Number_of_Vehicles" in df.columns else "N/A")
    col4.metric("Average Speed Limit", f"{df['Speed_Limit'].mean():.2f}" if "Speed_Limit" in df.columns else "N/A")

    # --- Navigation Buttons ---
    st.subheader("Select the Visualizations")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Visualization 1"):
            go_to("Visualization 1")
    with col2:
        if st.button("Visualization 2"):
            go_to("Visualization 2")
    with col3:
        if st.button("Visualization 3"):
            go_to("Visualization 3")

# ---- Visualization 1 ----
elif st.session_state.page == "Visualization 1":
    st.title("Visualization 1: Pre-crash Speed vs Severity")


    # --- Plotly Box Plot ---
    df_plot = df  # fallback to df if processed data not defined
    if "Severity" in df_plot.columns and "SV Precrash Speed (MPH)" in df_plot.columns:
        fig = px.box(
            df_plot,
            x="Severity",
            y="SV Precrash Speed (MPH)",
            color="Severity",
            title="Pre-crash Speed vs Severity",
            color_discrete_sequence=[
                '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
            ]
        )
        fig.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=1)
        fig.update_layout(title_font=dict(size=20, color='black', family="Arial Black"), plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            **Interpretation:**  
            Higher pre-crash speeds are strongly associated with greater accident severity.
            Bold colors highlight severity differences clearly.
            """
        )
    else:
        st.warning("Columns 'Severity' or 'SV Precrash Speed (MPH)' not found in dataset.")




    import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Load dataset ----
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

csv_url = "https://raw.githubusercontent.com/nhusna01/EA2025/main/processed_av_accident_data.csv"
df = load_data(csv_url)

# ---- Page navigation ----
if "page" not in st.session_state:
    st.session_state.page = "Menu"

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
    col2.metric("Total Fatalities", df["Number_of_Casualties"].sum() if "Number_of_Casualties" in df.columns else "N/A")
    col3.metric("Average Vehicles", f"{df['Number_of_Vehicles'].mean():.2f}" if "Number_of_Vehicles" in df.columns else "N/A")
    col4.metric("Average Speed Limit", f"{df['Speed_Limit'].mean():.2f}" if "Speed_Limit" in df.columns else "N/A")

    st.subheader("Go to Visualizations")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Visualization 1"):
            go_to("Visualization 1")
    with col2:
        if st.button("Visualization 2"):
            go_to("Visualization 2")
    with col3:
        if st.button("Correlation Heatmap"):
            go_to("Correlation Heatmap")

# ---- Visualization 1 (existing) ----
elif st.session_state.page == "Visualization 1":
    st.title("Visualization 1: Pre-crash Speed vs Severity")

    st.write("Example content for Visualization 1:")
    for course in ["Mathematics", "Physics", "Computer Science"]:
        st.write("- " + course)

    # Plotly Box Plot
    if "Severity" in df.columns and "SV Precrash Speed (MPH)" in df.columns:
        fig = px.box(
            df,
            x="Severity",
            y="SV Precrash Speed (MPH)",
            color="Severity",
            title="Pre-crash Speed vs Severity",
            color_discrete_sequence=[
                '#FF0000', '#FF7F00', '#FFD700', '#32CD32', '#00FFFF', '#0000FF', '#FF00FF'
            ]
        )
        fig.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=1)
        fig.update_layout(title_font=dict(size=20, color='black', family="Arial Black"), plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            "**Interpretation:** Higher pre-crash speeds are strongly associated with greater accident severity."
        )
    else:
        st.warning("Columns 'Severity' or 'SV Precrash Speed (MPH)' not found in dataset.")

    if st.button("⬅ Back to Menu"):
        go_to("Menu")

# ---- Visualization 2 (placeholder) ----
elif st.session_state.page == "Visualization 2":
    st.title("Visualization 2")
    st.write("Example content for Visualization 2")
    for subject, score in {"Mathematics": 90, "Physics": 85, "Computer Science": 95}.items():
        st.write(f"{subject}: {score}")

    if st.button("⬅ Back to Menu"):
        go_to("Menu")

# ---- Correlation Heatmap ----
elif st.session_state.page == "Correlation Heatmap":
    st.title("Correlation Heatmap: Mileage, Speed Limit, Precrash Speed")

    # Select numeric continuous variables only
    corr_vars = df[['Mileage', 'Posted Speed Limit (MPH)', 'SV Precrash Speed (MPH)']].copy()
    for col in corr_vars.columns:
        corr_vars[col] = pd.to_numeric(corr_vars[col], errors='coerce')
    corr_vars = corr_vars.dropna()

    # Compute correlation matrix
    corr_matrix = corr_vars.corr(method='pearson')

    # Plotly heatmap
    fig = px.imshow(
        corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        color_continuous_scale=['#FFFF00', '#FF7F00', '#FF0000'],  # Yellow → Orange → Red
        text_auto=".2f",
        aspect="auto",
        title="Correlation Heatmap"
    )
    fig.update_layout(
        title_font=dict(size=18, color='black', family="Arial Black"),
        plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "**I**


    if st.button("⬅ Back to Menu"):
        go_to("Menu")

# ---- Visualization 2 ----
elif st.session_state.page == "Visualization 2":
    st.title("Visualization 2")
    st.write("Example content for Visualization 2")
    for subject, score in {"Mathematics": 90, "Physics": 85, "Computer Science": 95}.items():
        st.write(f"{subject}: {score}")

    if st.button("⬅ Back to Menu"):
        go_to("Menu")

# ---- Visualization 3 ----
elif st.session_state.page == "Visualization 3":
    st.title("Visualization 3")
    st.write("Example content for Visualization 3")
    for subject, score in {"Mathematics": 88, "Physics": 92, "Computer Science": 97}.items():
        st.write(f"{subject}: {score}")

    if st.button("⬅ Back to Menu"):
        go_to("Menu")
