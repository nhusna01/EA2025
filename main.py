import streamlit as st

# Page configuration
st.set_page_config(page_title="Academic")

# Define your pages
home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")
visualise = st.Page('Academic.py', title='Student Coursework', icon=":material/school:")
visual1 = st.Page('Visualization1.py', title='Visualization 1', icon=":material/bar_chart:")
visual2 = st.Page('Visualization2.py', title='Visualization 2', icon=":material/insights:")
visual3 = st.Page('Visualization3.py', title='Visualization 3', icon=":material/analytics:")

# Navigation menu
pg = st.navigation(
    {
        "Menu": [home, visualise],
        "Visualizations": [visual1, visual2, visual3]
    }
)

# Run the navigation
pg.run()
