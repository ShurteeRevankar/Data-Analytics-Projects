import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="HR Report",
    page_icon="📄",
    layout="wide"
)

st.title("📄 HR Analytics Report")
st.markdown("Summary of workforce analytics and key business insights.")

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------
df = load_data()

if df.empty:
    st.stop()

df = preprocess_data(df)

# ----------------------------------------------------
# KPI Calculations
# ----------------------------------------------------
total_emp = len(df)
active_emp = len(df[df["Attrition"] == "No"])
left_emp = len(df[df["Attrition"] == "Yes"])

attrition_rate = left_emp / total_emp * 100

avg_age = df["Age"].mean()
avg_salary = df["MonthlyIncome"].mean()
avg_exp = df["TotalWorkingYears"].mean()

male = len(df[df["Gender"] == "Male"])
female = len(df[df["Gender"] == "Female"])

# ----------------------------------------------------
# Executive Summary
# ----------------------------------------------------
st.header("📌 Executive Summary")

st.info(f"""
The HR Analytics Dashboard contains data for **{total_emp} employees**.

The overall attrition rate is **{attrition_rate:.2f}%**.

The average employee age is **{avg_age:.1f} years** while the average monthly salary is **${avg_salary:,.0f}**.

This dashboard helps HR teams identify employee trends, monitor workforce performance, analyze salary distribution, and predict employee attrition using Machine Learning.
""")

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------
st.header("📊 Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Employees", total_emp)
c2.metric("Active", active_emp)
c3.metric("Attrition", left_emp)
c4.metric("Attrition Rate", f"{attrition_rate:.2f}%")

c5, c6, c7, c8 = st.columns(4)

c5.metric("Average Salary", f"${avg_salary:,.0f}")
c6.metric("Average Age", f"{avg_age:.1f}")
c7.metric("Average Experience", f"{avg_exp:.1f} Years")
c8.metric("Departments", df["Department"].nunique())

st.divider()

# ----------------------------------------------------
# Department Summary
# ----------------------------------------------------
st.header("🏢 Department Summary")

dept = (
    df.groupby("Department")
      .agg(
          Employees=("Department", "count"),
          AverageSalary=("MonthlyIncome", "mean"),
          Attrition=("AttritionFlag", "sum")
      )
      .reset_index()
)

st.dataframe(
    dept,
    use_container_width=True
)

# ----------------------------------------------------
# Job Role Summary
# ----------------------------------------------------
st.header("👨‍💼 Job Role Summary")

role = (
    df.groupby("JobRole")
      .agg(
          Employees=("JobRole", "count"),
          AverageSalary=("MonthlyIncome", "mean"),
          AverageExperience=("TotalWorkingYears", "mean")
      )
      .sort_values(
          by="Employees",
          ascending=False
      )
      .reset_index()
)

st.dataframe(
    role,
    use_container_width=True
)

# ----------------------------------------------------
# Workforce Statistics
# ----------------------------------------------------
st.header("📈 Workforce Statistics")

stats = pd.DataFrame({

    "Metric":[
        "Male Employees",
        "Female Employees",
        "Average Age",
        "Average Salary",
        "Average Experience",
        "Maximum Salary",
        "Minimum Salary"
    ],

    "Value":[
        male,
        female,
        round(avg_age,1),
        round(avg_salary,2),
        round(avg_exp,1),
        df["MonthlyIncome"].max(),
        df["MonthlyIncome"].min()
    ]

})

st.table(stats)

# ----------------------------------------------------
# Key Business Insights
# ----------------------------------------------------
st.header("💡 Key Insights")

highest_salary_department = (
    df.groupby("Department")["MonthlyIncome"]
      .mean()
      .idxmax()
)

highest_attrition_department = (
    df[df["Attrition"]=="Yes"]["Department"]
      .value_counts()
      .idxmax()
)

highest_paid_role = (
    df.groupby("JobRole")["MonthlyIncome"]
      .mean()
      .idxmax()
)

st.success(f"""
### Workforce Insights

• Highest Paying Department: **{highest_salary_department}**

• Highest Paying Job Role: **{highest_paid_role}**

• Highest Attrition Department: **{highest_attrition_department}**

• Overall Attrition Rate: **{attrition_rate:.2f}%**

• Total Employees: **{total_emp}**
""")

# ----------------------------------------------------
# Recommendations
# ----------------------------------------------------
st.header("🎯 Recommendations")

st.markdown("""
### Employee Retention
- Improve employee engagement.
- Conduct regular feedback sessions.
- Recognize high-performing employees.

### Salary Strategy
- Review compensation for critical roles.
- Benchmark salaries against industry standards.

### Career Development
- Increase learning opportunities.
- Provide leadership development programs.

### Work-Life Balance
- Encourage flexible work policies.
- Monitor overtime regularly.
""")

# ----------------------------------------------------
# Dataset Preview
# ----------------------------------------------------
st.header("📂 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# ----------------------------------------------------
# Download Dataset
# ----------------------------------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Cleaned Dataset",
    csv,
    "hr_cleaned.csv",
    "text/csv"
)

st.divider()

st.caption("HR Analytics Dashboard | ReadyNest Internship | Developed using Streamlit, Python & Machine Learning")