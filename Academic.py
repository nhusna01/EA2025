import streamlit as st
import pandas as pd

# --- CSV File Path (from GitHub Raw Link) ---
csv_url = "https://raw.githubusercontent.com/nhusna01/EA2025/refs/heads/main/processed_av_accident_data.csv"

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

    # --- Display dataset in Menu page ---
    st.write("Dataset preview:")
    st.dataframe(df)
    
st.title("Av Accident Data")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="PLO 2", value="3.3", help="PLO 2: Cognitive Skill")
col2.metric(label="PLO 3", value="3.5", help="PLO 3: Digital Skill")
col3.metric(label="PLO 4", value="4.0", help="PLO 4: Interpersonal Skill")
col4.metric(label="PLO 5", value="4.3", help="PLO 5: Communication Skill")


        
    st.write("Select a visualization page below:")

if st.session_state.page == "Menu":
    st.title("Menu Page")
    st.write("Welcome to the AV Accident Data Dashboard!")

    # --- Display dataset ---
    st.write("Dataset preview:")
    st.dataframe(df)

    # --- Metrics ---
    st.title("AV Accident Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="PLO 2", value="3.3", help="PLO 2: Cognitive Skill")
    col2.metric(label="PLO 3", value="3.5", help="PLO 3: Digital Skill")
    col3.metric(label="PLO 4", value="4.0", help="PLO 4: Interpersonal Skill")
    col4.metric(label="PLO 5", value="4.3", help="PLO 5: Communication Skill")

    # --- Navigation Buttons ---
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

# ---- Visualization 1 (with Plotly Box Plot) ----
elif st.session_state.page == "Visualization 1":
    st.title("Visualization 1: Pre-crash Speed vs Severity")
    st.write("Example content for Visualization 1:")
    visualization1 = ["Mathematics", "Physics", "Computer Science"]
    for course in visualization1:
        st.write("- " + course)

    # --- Plotly Box Plot ---
    import plotly.express as px

    # Use the processed DataFrame; fallback to df if df_processed_imputed not defined
    try:
        df_plot = df_processed_imputed
    except NameError:
        df_plot = df  # fallback

    if 'Severity' in df_plot.columns and 'SV Precrash Speed (MPH)' in df_plot.columns:
        fig = px.box(
            df_plot,
            x='Severity',
            y='SV Precrash Speed (MPH)',
            title='Pre-crash Speed vs. Severity',
            color='Severity',
            color_discrete_sequence=[
                '#FF0000',  # Red
                '#FF7F00',  # Orange
                '#FFD700',  # Bold Yellow
                '#32CD32',  # Bold Green
                '#00FFFF',  # Cyan
                '#0000FF',  # Blue
                '#FF00FF'   # Magenta
            ]
        )

        # Styling the box plot
        fig.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=1)
        fig.update_layout(title_font=dict(size=20, color='black', family="Arial Black"), plot_bgcolor='white')

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)

        # Interpretation
        st.markdown(
            """
            <div style='font-size:16px; color:black;'>
            <b>Interpretation:</b><br>
            The box plot shows that higher pre-crash speeds are strongly associated with greater accident severity.
            The bold yellow (<span style='color:#FFD700;'>#FFD700</span>) and green (<span style='color:#32CD32;'>#32CD32</span>)
            fills make moderate-to-severe levels stand out, while the vivid color palette ensures clear distinction among severity categories.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Columns 'Severity' or 'SV Precrash Speed (MPH)' not found in the dataset.")

    # --- Back to Menu Button ---
    if st.button("⬅ Back to Menu"):
        go_to("Menu")

# ---- Visualization 2 (unchanged) ----
elif st.session_state.page == "Visualization 2":
    st.title("Visualization 2")
    st.write("Example content for Visualization 2")
    visualization2 = {
        "Mathematics": 90,
        "Physics": 85,
        "Computer Science": 95
    }
    for subject, score in visualization2.items():
        st.write(f"{subject}: {score}")

    if st.button("⬅ Back to Menu"):
        go_to("Menu")

elif st.session_state.page == "Visualization 3":
    st.title("AV Accident Summary")
    st.write("Key Statistics from the AV Accident dataset:")

   
    
    if st.button("⬅ Back to Menu"):
        go_to("Menu")  
