import streamlit as st

st.set_page_config(
    page_title="Academic"
)
visualise = st.Page('Academic.py', title='Student Coursework', icon=":material/school:")

home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [home, visualise]
        }
    )

pg.run()
