import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📘 Student Coursework Dashboard")
st.markdown("Manage, track, and analyze student coursework interactively.")

# -----------------------------------
# ✅ Upload CSV File
# -----------------------------------
st.subheader("📂 Upload Coursework File")
uploaded_file = st.file_uploader("Upload CSV (Columns: Course, Assignment, Due_Date, Status, Grade)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Clean column names (remove extra spaces and lowercase)
    df.columns = df.columns.str.strip()

    # Check required columns
    required_columns = ["Course", "Assignment", "Due_Date", "Status", "Grade"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
    else:
        # Convert date
        df["Due_Date"] = pd.to_datetime(df["Due_Date"], errors="coerce")

        st.success("✅ File uploaded successfully!")
        st.dataframe(df, use_container_width=True)

        # -----------------------------------
        # ✅ Key Metrics
        # -----------------------------------
        st.markdown("---")
        st.subheader("📊 Coursework Overview")

        total_tasks = len(df)
        completed_tasks = df[df["Status"] == "Completed"].shape[0]
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        avg_grade = df["Grade"].mean() if "Grade" in df.columns else 0

        metric_cols = st.columns(4)
        metric_cols[0].metric("📁 Total Assignments", total_tasks)
        metric_cols[1].metric("✅ Completed (%)", f"{completion_rate:.2f}%")
        metric_cols[2].metric("✔ Completed Tasks", completed_tasks)
        metric_cols[3].metric("🎯 Average Grade", f"{avg_grade:.2f}")

        # -----------------------------------
        # ✅ Filter Section
        # -----------------------------------
        st.markdown("---")
        st.subheader("🎯 Filter Coursework")

        col1, col2, col3 = st.columns(3)

        with col1:
            course_filter = st.selectbox("Filter by Course", ["All"] + df["Course"].unique().tolist())
        with col2:
            status_filter = st.selectbox("Filter by Status", ["All"] + df["Status"].unique().tolist())
        with col3:
            grade_filter = st.slider("Minimum Grade", 0, 100, 0)

        filtered_df = df.copy()
        if course_filter != "All":
            filtered_df = filtered_df[filtered_df["Course"] == course_filter]
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        filtered_df = filtered_df[filtered_df["Grade"] >= grade_filter]

        st.dataframe(filtered_df, use_container_width=True)

        # -----------------------------------
        # ✅Progress Chart
        # -----------------------------------
        st.markdown("---")
        st.subheader("📈 Coursework Completion by Course")

        course_progress = df.groupby("Course")["Status"].apply(lambda x: (x == "Completed").mean() * 100).reset_index()
        course_progress.columns = ["Course", "Completion (%)"]

        fig = px.bar(course_progress, x="Course", y="Completion (%)", text="Completion (%)",
                     title="Completion Percentage by Course", range_y=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        # -----------------------------------
        # ✅ Download Section
        # -----------------------------------
        st.markdown("---")
        st.subheader("📥 Download Filtered Coursework")
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv_data, "coursework_filtered.csv", "text/csv")

else:
    st.info("📌 Please upload a CSV file to continue.")
