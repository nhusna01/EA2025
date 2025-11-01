import streamlit as st
import pandas as pd

# --- CSV File Path (from GitHub Raw Link) ---
csv_url = "https://raw.githubusercontent.com/nhusna01/EC2025/refs/heads/main/processed_av_accident_data.csv"

# Set the title for the Streamlit app
st.title("AV Accident Data Survey")

# Initialize session_state to store current page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Function to change pages
def go_to(page_name):
    st.session_state.page = page_name

# ---- Navigation Buttons ----
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

# ---- PAGE CONTENT ----
if st.session_state.page == "Home":
    st.title(" Home Page")
    st.write("Welcome to the AV Accident Data Dashboard!")

elif st.session_state.page == "Visualization 1":
    st.title("Visualization 1 Page")
    visualization1 = ["Mathematics", "Physics", "Computer Science"]
    st.write("List of courses (example):")
    for course in visualization1:
        st.write("- " + course)

elif st.session_state.page == "Visualization 2":
    st.title("Visualization 2 Page")
    visualization2 = {
        "Mathematics": 90,
        "Physics": 85,
        "Computer Science": 95
    }
    st.write("Example results:")
    for subject, score in visualization2.items():
        st.write(f"{subject}: {score}")

elif st.session_state.page == "Visualization 3":
    st.title("Visualization 3 Page")
    visualization3 = {
        "Mathematics": 88,
        "Physics": 92,
        "Computer Science": 97
    }
    st.write("Example results:")
    for subject, score in visualization3.items():
        st.write(f"{subject}: {score}")

# ---- Metrics ----
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="PLO 2", value="3.3", help="PLO 2: Cognitive Skill")
col2.metric(label="PLO 3", value="3.5", help="PLO 3: Digital Skill")
col3.metric(label="PLO 4", value="4.0", help="PLO 4: Interpersonal Skill")
col4.metric(label="PLO 5", value="4.3", help="PLO 5: Communication Skill")
