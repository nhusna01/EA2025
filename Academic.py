import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Title
# -------------------------------
st.title("Student Coursework Dashboard")
st.markdown("Manage, track, and analyze student coursework interactively.")

# -------------------------------
#  Upload Coursework CSV
# -------------------------------
st.subheader("Upload Coursework File")
uploaded_file = st.file_uploader("Upload CSV file (Columns: Course, Assignment, Due_Date, Status, Grade)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert date column to datetime
    if "Due_Date" in df.columns:
        df['Due_Date'] = pd.to_datetime(df["Due_Date"])

    st.success(" File uploaded successfully!")
    st.dataframe(df, use_container_width=True)

    # -------------------------------
    # Key Metrics Section
    # -------------------------------
    st.markdown("---")
    st.subheader("Coursework Overview")

    total_tasks = len(df)
    completed_tasks = df[df["Status"] == "Completed"].shape[0]
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    avg_grade = df["Grade"].mean() if "Grade" in df.columns else "N/A"

    metric_cols = st.columns(4)
    metric_cols[0].metric("Total Assignments", total_tasks)
    metric_cols[1].metric("Completed (%)", f"{completion_rate:.2f}%")
    metric_cols[2].metric("Completed Tasks", completed_tasks)
    metric_cols[3].metric("Average Grade", f"{avg_grade:.2f}" if isinstance(avg_grade, float) else "N/A")

    # -------------------------------
    # Filters for Exploration
    # -------------------------------
    st.markdown("---")
    st.subheader(" Filter Coursework")

    col1, col2, col3 = st.columns(3)
    with col1:
        course_filter = st.selectbox("Filter by Course", ["All"] + df["Course"].unique().tolist())
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All"] + df["Status"].unique().tolist())
    with col3:
        grade_filter = st.slider("Filter by Grade (Min)", 0, 100, 0)

    filtered_df = df.copy()
    if course_filter != "All":
        filtered_df = filtered_df[filtered_df["Course"] == course_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]
    filtered_df = filtered_df[filtered_df["Grade"] >= grade_filter]

    st.dataframe(filtered_df, use_container_width=True)

    # -------------------------------
    # Progress Visualization
    # -------------------------------
    st.markdown("---")
    st.subheader("Coursework Progress by Course")

    if "Course" in df.columns and "Status" in df.columns:
        course_progress = df.groupby("Course")["Status"].apply(lambda x: (x == "Completed").mean() * 100).reset_index()
        course_progress.columns = ["Course", "Completion (%)"]

        fig = px.bar(course_progress, x="Course", y="Completion (%)", title="Completion by Course",
                     text="Completion (%)", range_y=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Download Updated File
    # -------------------------------
    st.markdown("---")
    st.subheader(" Download Updated Coursework")

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered Coursework", csv_data, "filtered_coursework.csv", "text/csv")

else:
    st.info("Please upload a CSV file to get started.")
