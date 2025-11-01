import streamlit as st
import pandas as pd


# --- CSV File Path (from GitHub Raw Link) ---
csv_url = "https://raw.githubusercontent.com/nhusna01/EC2025/refs/heads/main/processed_av_accident_data.csv"

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
    st.write("Select a visualization page below:")

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

elif st.session_state.page == "Visualization 1":
    st.title("Visualization 1")
    st.write("Example content for Visualization 1")
    visualization1 = ["Mathematics", "Physics", "Computer Science"]
    for course in visualization1:
        st.write("- " + course)
    
    # Display dataset
    st.write("Dataset preview:")
    st.dataframe(df.head())

    if st.button("⬅ Back to Menu"):
        go_to("Menu")

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

    # Display dataset
    st.write("Dataset preview:")
    st.dataframe(df.head())

    if st.button("⬅ Back to Menu"):
        go_to("Menu")

elif st.session_state.page == "Visualization 3":
    st.title("Visualization 3")
    st.write("Example content for Visualization 3")
    visualization3 = {
        "Mathematics": 88,
        "Physics": 92,
        "Computer Science": 97
    }
    for subject, score in visualization3.items():
        st.write(f"{subject}: {score}")



  
