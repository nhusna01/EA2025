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

# Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Accidents", total_accidents)
    col2.metric("Total Fatalities", total_fatalities)
    col3.metric("Average Vehicles Involved", f"{avg_vehicles:.2f}" if isinstance(avg_vehicles, float) else avg_vehicles)
    col4.metric("Average Speed Limit", f"{avg_speed:.2f}" if isinstance(avg_speed, float) else avg_speed)

    # Display severity count as a table
    if severity_count is not None:
        st.write("Accidents by Severity:")
        st.dataframe(severity_count)
        
    st.write("Select a visualization page below:")

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

# ---- Visualization 1 (unchanged) ----
elif st.session_state.page == "Visualization 1":
    st.title("Visualization 1")
    st.write("Example content for Visualization 1")
    visualization1 = ["Mathematics", "Physics", "Computer Science"]
    for course in visualization1:
        st.write("- " + course)

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
