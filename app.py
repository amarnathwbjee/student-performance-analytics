"""
app.py
Streamlit web interface for the Student Performance Analytics System.
Reuses the functions in functions.py. Run with: streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st

import functions as fn

DATA_FILE = Path(__file__).resolve().parent / "data" / "students.csv"

st.set_page_config(page_title="Student Performance Analytics", layout="wide")
st.title("Student Performance Analytics System")
st.caption("Python | NumPy | Pandas | EWB Courses")


@st.cache_data
def get_processed_data(source):
    """Load, clean and process the data (cached for speed)."""
    raw = fn.load_data(source)
    cleaned = fn.clean_data(raw)
    return fn.process_students(cleaned)


# Optional: let the user upload their own CSV with the same columns
uploaded = st.sidebar.file_uploader("Upload a student CSV (optional)", type="csv")
st.sidebar.write("Without an upload, the sample dataset (20 students) is used.")

try:
    df = get_processed_data(uploaded if uploaded is not None else DATA_FILE)
except ValueError as error:
    st.error(str(error))
    st.stop()

stats = fn.overall_statistics(df)

# ---- Key numbers -------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total students", stats["Total students"])
col2.metric("Passed", stats["Students passed"])
col3.metric("Pass %", f"{stats['Pass percentage']}%")
col4.metric("Class average", stats["Overall class average"])

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Student results", "Subject analysis", "Top performers", "Departments", "Attention needed"]
)

with tab1:
    department = st.selectbox("Filter by department", ["All"] + sorted(df["Department"].unique()))
    view = df if department == "All" else df[df["Department"] == department]
    columns = ["Rank", "Student_ID", "Name", "Department", "Total", "Average",
               "Grade", "Result", "Attendance"]
    st.dataframe(view.sort_values("Rank")[columns], hide_index=True)
    st.subheader("Grade distribution")
    st.bar_chart(fn.grade_distribution(df).set_index("Grade"))

with tab2:
    subject_df = fn.subject_analysis(df)
    st.dataframe(subject_df, hide_index=True)
    st.bar_chart(subject_df.set_index("Subject")["Average"])
    st.success(f"Best subject: {subject_df.iloc[0]['Subject']} ({subject_df.iloc[0]['Average']})")

with tab3:
    count = st.slider("Number of top students", 3, 10, 5)
    st.dataframe(fn.top_performers(df, n=count), hide_index=True)
    st.write(f"Highest average: **{stats['Highest average']}**")

with tab4:
    dept_df = fn.department_analysis(df)
    st.dataframe(dept_df, hide_index=True)
    st.bar_chart(dept_df.set_index("Department")["Avg_Marks"])

with tab5:
    st.subheader("Students who failed")
    failed = fn.failed_students(df)
    if failed.empty:
        st.write("No students failed.")
    else:
        st.dataframe(failed, hide_index=True)
    st.subheader(f"Low attendance (below {fn.MIN_ATTENDANCE}%)")
    st.dataframe(fn.low_attendance_students(df), hide_index=True)
    st.write(f"Correlation between attendance and average marks: "
             f"**{fn.attendance_marks_correlation(df)}**")
             