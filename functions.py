"""
functions.py
Reusable calculation and processing functions for the
Student Performance Analytics System.
"""

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------
# Configuration (grading rule and pass condition)
# ----------------------------------------------------------------------
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer_Science"]
REQUIRED_COLUMNS = ["Student_ID", "Name", "Department"] + SUBJECTS + ["Attendance"]

PASS_MARK = 40          # minimum marks required in EVERY subject to pass
MIN_ATTENDANCE = 75     # attendance % below this is flagged as low

# Grade rule based on average marks (checked from highest to lowest)
GRADE_RULES = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (40, "E"),
]
GRADE_ORDER = ["A+", "A", "B", "C", "D", "E", "F"]   # F = failed the pass condition


# ----------------------------------------------------------------------
# Step 1 & 2: Load and validate data
# ----------------------------------------------------------------------
def load_data(file_path):
    """Read the student CSV file into a Pandas DataFrame and validate columns."""
    df = pd.read_csv(file_path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")
    return df


def clean_data(df):
    """Remove duplicate IDs, convert numeric columns and drop incomplete rows."""
    df = df.drop_duplicates(subset="Student_ID").copy()
    numeric_cols = SUBJECTS + ["Attendance"]
    for col in numeric_cols:                       # loop over columns
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=numeric_cols).reset_index(drop=True)
    return df


# ----------------------------------------------------------------------
# Step 3: Process data
# ----------------------------------------------------------------------
def calculate_total_and_average(df):
    """Add Total and Average marks per student using NumPy."""
    marks = df[SUBJECTS].to_numpy()                # 2D NumPy array
    df["Total"] = np.sum(marks, axis=1)
    df["Average"] = np.round(np.mean(marks, axis=1), 2)
    return df


def add_pass_fail(df):
    """
    Pass condition: student must score >= PASS_MARK in every subject.
    Adds 'Result' (Pass/Fail) and 'Failed_Subjects' columns.
    """
    marks = df[SUBJECTS].to_numpy()
    passed = np.all(marks >= PASS_MARK, axis=1)
    df["Result"] = np.where(passed, "Pass", "Fail")

    failed_subjects = []
    for _, row in df.iterrows():                   # loop to list failed subjects
        failed = [s for s in SUBJECTS if row[s] < PASS_MARK]
        failed_subjects.append(", ".join(failed) if failed else "-")
    df["Failed_Subjects"] = failed_subjects
    return df


def get_grade(average, result):
    """Return grade for one student. Failed students always receive 'F'."""
    if result == "Fail":
        return "F"
    for minimum, grade in GRADE_RULES:
        if average >= minimum:
            return grade
    return "F"


def add_grades(df):
    """Assign a grade to every student using the grading rule."""
    grades = []
    for average, result in zip(df["Average"], df["Result"]):   # loop
        grades.append(get_grade(average, result))
    df["Grade"] = grades
    return df


def add_rank(df):
    """Rank students by average marks (1 = best)."""
    df["Rank"] = df["Average"].rank(method="min", ascending=False).astype(int)
    return df


def process_students(df):
    """Run the complete processing pipeline."""
    df = calculate_total_and_average(df)
    df = add_pass_fail(df)
    df = add_grades(df)
    df = add_rank(df)
    return df


# ----------------------------------------------------------------------
# Step 4: Analysis
# ----------------------------------------------------------------------
def overall_statistics(df):
    """Return key class-level statistics as a dictionary."""
    best = df.loc[df["Average"].idxmax()]
    worst = df.loc[df["Average"].idxmin()]
    passed = int(np.sum(df["Result"] == "Pass"))
    total_students = len(df)
    return {
        "Total students": total_students,
        "Students passed": passed,
        "Students failed": total_students - passed,
        "Pass percentage": round(passed / total_students * 100, 2),
        "Overall class average": round(float(np.mean(df["Average"])), 2),
        "Highest average": f"{best['Name']} ({best['Average']})",
        "Lowest average": f"{worst['Name']} ({worst['Average']})",
        "Highest total marks": int(df["Total"].max()),
        "Lowest total marks": int(df["Total"].min()),
        "Average attendance %": round(float(np.mean(df["Attendance"])), 2),
    }


def subject_analysis(df):
    """Subject-wise average, highest, lowest, spread, pass % and topper."""
    rows = []
    for subject in SUBJECTS:                       # loop over subjects
        scores = df[subject].to_numpy()
        rows.append({
            "Subject": subject,
            "Average": round(float(np.mean(scores)), 2),
            "Highest": int(np.max(scores)),
            "Lowest": int(np.min(scores)),
            "Median": float(np.median(scores)),
            "Std_Dev": round(float(np.std(scores)), 2),
            "Pass_%": round(float(np.sum(scores >= PASS_MARK) / len(scores) * 100), 2),
            "Topper": df.loc[df[subject].idxmax(), "Name"],
        })
    return pd.DataFrame(rows).sort_values("Average", ascending=False).reset_index(drop=True)


def top_performers(df, n=5):
    """Return the top n students by average marks."""
    columns = ["Rank", "Student_ID", "Name", "Department", "Total", "Average", "Grade"]
    return df.sort_values("Average", ascending=False).head(n)[columns]


def department_analysis(df):
    """Department-wise student count, average marks and pass percentage."""
    temp = df.assign(Passed=(df["Result"] == "Pass").astype(int))
    summary = temp.groupby("Department").agg(
        Students=("Student_ID", "count"),
        Avg_Marks=("Average", "mean"),
        Avg_Attendance=("Attendance", "mean"),
        Passed=("Passed", "sum"),
    )
    summary["Pass_%"] = summary["Passed"] / summary["Students"] * 100
    return summary.round(2).sort_values("Avg_Marks", ascending=False).reset_index()


def grade_distribution(df):
    """Count of students per grade."""
    counts = df["Grade"].value_counts().reindex(GRADE_ORDER, fill_value=0)
    return counts.rename_axis("Grade").reset_index(name="Students")


def low_attendance_students(df):
    """Students whose attendance is below MIN_ATTENDANCE."""
    columns = ["Student_ID", "Name", "Department", "Attendance", "Average", "Result"]
    return df[df["Attendance"] < MIN_ATTENDANCE][columns]


def failed_students(df):
    """Students who did not satisfy the pass condition."""
    columns = ["Student_ID", "Name", "Department", "Average", "Failed_Subjects"]
    return df[df["Result"] == "Fail"][columns]


def attendance_marks_correlation(df):
    """Pearson correlation between attendance and average marks (NumPy)."""
    return round(float(np.corrcoef(df["Attendance"], df["Average"])[0, 1]), 3)