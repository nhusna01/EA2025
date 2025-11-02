import streamlit as st

# Page Configuration
st.set_page_config(page_title="Student Coursework", page_icon=":material/school:", layout="wide")

# Title Section
st.title("Student Coursework Dashboard")
st.write("Please select a visualization to explore accident data interactively.")

st.markdown("---")

# Interactive Layout with 3 Visualization Cards
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Visualization 1")
        st.write("Explore crash severity trends across various factors.")
        if st.button("Go to Visualization 1", key="vis1"):
            st.switch_page("pages/Visualization1.py")

with col2:
    with st.container(border=True):
        st.subheader("Visualization 2")
        st.write("Analyze injury severity, vehicle types, and collision patterns.")
        if st.button("Go to Visualization 2", key="vis2"):
            st.switch_page("pages/Visualization2.py")

with col3:
    with st.container(border=True):
        st.subheader("Visualization 3")
        st.write("View geographic and environmental crash distributions.")
        if st.button("Go to Visualization 3", key="vis3"):
            st.switch_page("pages/Visualization3.py")

st.markdown("---")

# Optional Interactive Section (Dropdown Navigation)
st.subheader(" Quick Navigation Menu")
nav_selection = st.selectbox(
    "Select a visualization page:",
    ("-- Select --", "Visualization 1", "Visualization 2", "Visualization 3")
)

if nav_selection == "Visualization 1":
    st.switch_page("pages/Visualization1.py")
elif nav_selection == "Visualization 2":
    st.switch_page("pages/Visualization2.py")
elif nav_selection == "Visualization 3":
    st.switch_page("pages/Visualization3.py")
