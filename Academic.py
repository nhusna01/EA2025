import streamlit as st
import pandas as pd

# -------------------------------
# Page Title
# -------------------------------
st.title("Student Coursework Dashboard")
st.markdown("Upload and view student coursework data.")

# -------------------------------
# Upload Section
# -------------------------------
st.subheader(" Upload Coursework File")
uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

# -------------------------------
# 📄 Display Uploaded File
# -------------------------------
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Clean column names
        df.columns = df.columns.str.strip()

        st.success("File uploaded successfully!")
        st.write("### 📄 Preview of Uploaded Data:")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error reading the file: {e}")
else:
    st.info("Please upload a CSV file to view its contents.")
