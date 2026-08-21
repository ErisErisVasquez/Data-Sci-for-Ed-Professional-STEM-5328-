
EPISD TAPR: AI-Assisted Data Exploration
This repository contains the reproducible analysis for a graduate-level data science assignment examining STAAR End-of-Course (EOC) performance and student-group context in El Paso Independent School District (EPISD) during 2023–2024 and 2024–2025.

Research question
How does STAAR EOC performance differ among students in El Paso Independent School District based on English Learner and At-Risk classification compared with overall district and state performance?

The final analysis focuses most directly on students reported by TAPR as EB/EL (Current & Monitored). At-Risk and Economically Disadvantaged data are used as district-level context, not as proof that those classifications caused the observed test outcomes.

Data sources
Texas Education Agency, 2023–24 TAPR Reports

Texas Education Agency, 2024–25 TAPR Reports

EPISD district number: 071902

District TAPR and Texas State TAPR files for both school years

The project stores only the manually transcribed values needed for the four selected charts. This makes the analysis auditable without redistributing the full TAPR PDFs.

Method
For EOC performance, the TAPR tables report Approaches Grade Level or Above. The complementary rate was calculated as:

Did Not Meet Grade Level (%) = 100 - Approaches Grade Level or Above (%)
This is not the complement of Meets Grade Level or Above. TAPR percentages are displayed as whole numbers, so derived values retain that rounding.

Population charts compare the percentage of total student membership classified as:

EB Students/EL

At-Risk

Economically Disadvantaged

Because EPISD and Texas have very different total enrollments, percentages—not raw counts—are the primary comparison.

Main findings
EPISD EB/EL students had the highest Did Not Meet rate in English I: 48% in 2023–24 and 47% in 2024–25.

Algebra I increased from 23% to 26% Did Not Meet, while U.S. History decreased from 11% to 10%.

EPISD's EB/EL membership share exceeded Texas by 13.5 percentage points in 2023–24 and 11.8 points in 2024–25.

EPISD's At-Risk share exceeded Texas by 8.1 points in 2023–24 and 7.2 points in 2024–25.

EPISD's Economically Disadvantaged share exceeded Texas by 12.9 points in 2023–24 and 10.8 points in 2024–25.

What this analysis cannot establish
The aggregate TAPR tables do not identify how many students belong simultaneously to the EB/EL, At-Risk, and Economically Disadvantaged groups.

The At-Risk totals do not separate students by the specific criterion that qualified them, such as attendance-related criteria.

Two annual district-level observations are not enough to estimate a meaningful correlation between population composition and test performance.

These comparisons are descriptive and observational. They do not show that EB/EL status, poverty, attendance, or any other classification caused a difference in STAAR performance.

The selected Never EB/EL – All Grades table was not used because its broad subject aggregates are not directly comparable with the specific English I, Algebra I, and U.S. History EOC assessments.

Repository structure
data/
  eoc_eb_el_performance.csv
  student_membership.csv
src/
  analyze_tapr.py
figures/
  generated PNG charts
outputs/
  generated summary tables
requirements.txt
Run the analysis
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/analyze_tapr.py
The script validates the input percentages, calculates the derived rates and percentage-point gaps, writes summary CSV files, and regenerates all four charts.

Responsible use of AI
AI assistance was used to help locate relevant TAPR fields, structure the extracted values, generate and check Python code, and improve chart presentation. The source values, formulas, terminology, and limitations should be verified against the original TAPR reports before submission or reuse.