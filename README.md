# Student Performance Analytics System

A Python data-analysis project built with **NumPy** and **Pandas** that reads student records from a CSV file, processes them, and prints a clear performance report.

## 1. Project Title
**Student Performance Analytics System**
Student: *<edit: your name, batch and roll number>* | Course: Python with AI, EWB Courses

## 2. Objective
Teachers often need to turn raw marks into useful information. This project automates that: it calculates totals, averages, grades and pass/fail results, compares subjects and departments, and identifies top performers and students who need support.

## 3. Technologies Used
- Python 3.9+
- NumPy (numerical calculations) 
- Pandas (DataFrame loading, grouping, sorting, filtering)
- No other libraries are used.

## 4. Dataset Description
`data/students.csv` holds **20 student records** with these columns:

| Column | Description |
|---|---|
| Student_ID | Unique ID (S001-S020) |
| Name | Student name |
| Department | Computer Science, Electronics, Civil or Mechanical |
| Maths, Physics, Chemistry, English, Computer_Science | Marks out of 100 |
| Attendance | Attendance percentage |

## 5. Implementation
1. **Load**: `load_data()` reads the CSV with Pandas and validates the required columns.
2. **Clean**: `clean_data()` removes duplicate IDs, converts marks to numbers, drops incomplete rows (loop over columns).
3. **Totals & averages**: `calculate_total_and_average()` converts subject marks to a 2D NumPy array and uses `np.sum` and `np.mean` with `axis=1`.
4. **Pass/fail**: `add_pass_fail()` uses `np.all(marks >= 40, axis=1)` and `np.where`; a loop lists the failed subjects.
5. **Grades**: `get_grade()` / `add_grades()` apply the grading rule in a loop.
6. **Ranking**: `add_rank()` ranks students by average.
7. **Analysis**: functions for overall statistics, subject-wise analysis (loop + NumPy `mean`, `median`, `std`), top performers, grade distribution, department-wise `groupby`, low attendance and an attendance-vs-marks correlation (`np.corrcoef`).
8. **Output**: `main.py` prints every section and saves the processed table to `output/student_results.csv`.

### Rules used
- **Grade (by average):** A+ >= 90, A >= 80, B >= 70, C >= 60, D >= 50, E >= 40.
- **Pass condition:** at least 40 marks in *every* subject. Students who fail any subject get grade **F**.
- **Low attendance:** below 75%.

## 6. Key Features
- Total, average, grade, result and rank for every student
- Class statistics: pass count, pass %, class average, highest and lowest performers
- Subject-wise analysis with topper per subject
- Top 5 students
- Grade distribution and department-wise comparison
- Failed-student and low-attendance reports
- Results exported to CSV

## 7. Output / Screenshots
Run `python main.py` and add screenshots to a `screenshots/` folder. Key results from the sample dataset:

- Students passed: **17 of 20 (85%)**
- Overall class average: **70.35**
- Highest average: **Arjun Malhotra (94.6)**
- Best subject: **English (73.0)**; weakest: **Physics (68.4)**
- Best department: **Computer Science (84.16 average)**

## 8. Final Outcome
The program runs end to end without errors and produces a readable report that answers the assignment questions: who has the highest average, which subject is strongest, how many students passed, and what the class average is.

## 9. Challenges & Learning
*<edit: write your own experience here>* Examples: deciding a fair pass rule (every subject vs. average), handling failed students in the grading rule, learning axis-wise NumPy operations, and using `groupby` for department analysis.

## 10. GitHub Repository
*<[edit: paste your final repository link here](https://student-performance-analytics-kgfbzkgzgwiwcxzs2onktq.streamlit.app/#student-performance-analytics-system)>*

## Folder Structure
```
student-performance-analytics/
├── data/students.csv
├── output/                 (created automatically)
├── functions.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup & Run
```bash
git clone <your-repo-link>
cd student-performance-analytics
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```