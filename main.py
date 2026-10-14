from pathlib import Path

import pandas as pd

import functions as fn

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "students.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "student_results.csv"


def print_section(title):
    """Print a clearly visible section heading."""
    print("\n" + "=" * 75)
    print(title.upper())
    print("=" * 75)


def main():
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", None)

    print("=" * 75)
    print("        STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 75)

    # ---- Step 2: Read the data ----------------------------------------
    raw_df = fn.load_data(DATA_FILE)
    print_section("1. Dataset overview")
    print(f"File           : {DATA_FILE.name}")
    print(f"Records        : {len(raw_df)}")
    print(f"Columns        : {', '.join(raw_df.columns)}")
    print("\nFirst 5 records:")
    print(raw_df.head().to_string(index=False))

    df = fn.clean_data(raw_df)
    removed = len(raw_df) - len(df)
    print(f"\nRecords removed during cleaning: {removed}")

    # ---- Step 3: Process the data -------------------------------------
    df = fn.process_students(df)
    print_section("2. Student results (totals, averages, grades, pass/fail)")
    result_cols = ["Rank", "Student_ID", "Name", "Department", "Total",
                   "Average", "Grade", "Result", "Attendance"]
    print(df.sort_values("Rank")[result_cols].to_string(index=False))

    print("\nGrading rule : A+ >= 90, A >= 80, B >= 70, C >= 60, D >= 50, E >= 40 (average marks)")
    print(f"Pass rule    : at least {fn.PASS_MARK} marks in EVERY subject (otherwise Fail, grade F)")

    # ---- Step 4: Analysis ---------------------------------------------
    print_section("3. Overall class statistics")
    for label, value in fn.overall_statistics(df).items():
        print(f"{label:<24}: {value}")

    print_section("4. Subject-wise performance")
    subject_df = fn.subject_analysis(df)
    print(subject_df.to_string(index=False))
    best_subject = subject_df.iloc[0]
    weakest_subject = subject_df.iloc[-1]
    print(f"\nBest subject (highest average)  : {best_subject['Subject']} ({best_subject['Average']})")
    print(f"Weakest subject (lowest average): {weakest_subject['Subject']} ({weakest_subject['Average']})")

    print_section("5. Top 5 performing students")
    print(fn.top_performers(df, n=5).to_string(index=False))

    print_section("6. Grade distribution")
    print(fn.grade_distribution(df).to_string(index=False))

    print_section("7. Department-wise analysis")
    print(fn.department_analysis(df).to_string(index=False))

    print_section("8. Students who failed")
    failed = fn.failed_students(df)
    print(failed.to_string(index=False) if not failed.empty else "No students failed.")

    print_section("9. Low attendance students (below 75%)")
    low_att = fn.low_attendance_students(df)
    print(low_att.to_string(index=False) if not low_att.empty else "No low-attendance students.")
    print(f"\nCorrelation between attendance and average marks: "
          f"{fn.attendance_marks_correlation(df)}")

    # ---- Save results -------------------------------------------------
    OUTPUT_DIR.mkdir(exist_ok=True)
    df.sort_values("Rank").to_csv(OUTPUT_FILE, index=False)
    print_section("10. Output saved")
    print(f"Processed results saved to: {OUTPUT_FILE.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
