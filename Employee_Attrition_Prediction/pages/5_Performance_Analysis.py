import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Performance Analysis",
    page_icon="⭐",
    layout="wide"
)

st.title("⭐ Performance Analysis")
st.markdown("Analyze employee performance, satisfaction and work-life balance.")

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------
df = load_data()

if df.empty:
    st.stop()

df = preprocess_data(df)

# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------
st.sidebar.header("Filters")

department = st.sidebar.multiselect(
    "Department",
    sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

job_role = st.sidebar.multiselect(
    "Job Role",
    sorted(df["JobRole"].unique()),
    default=sorted(df["JobRole"].unique())
)

gender = st.sidebar.multiselect(
    "Gender",
    sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["JobRole"].isin(job_role)) &
    (df["Gender"].isin(gender))
]

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------
avg_performance = filtered_df["PerformanceRating"].mean()
avg_job_satisfaction = filtered_df["JobSatisfaction"].mean()
avg_env = filtered_df["EnvironmentSatisfaction"].mean()
avg_worklife = filtered_df["WorkLifeBalance"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("⭐ Avg Performance", f"{avg_performance:.2f}")
c2.metric("😊 Job Satisfaction", f"{avg_job_satisfaction:.2f}")
c3.metric("🏢 Environment", f"{avg_env:.2f}")
c4.metric("⚖️ Work-Life Balance", f"{avg_worklife:.2f}")

st.divider()

# ----------------------------------------------------
# Performance Rating Distribution
# ----------------------------------------------------
fig1 = px.histogram(
    filtered_df,
    x="PerformanceRating",
    color="PerformanceRating",
    title="Performance Rating Distribution"
)

# ----------------------------------------------------
# Performance by Department
# ----------------------------------------------------
dept = (
    filtered_df.groupby("Department")["PerformanceRating"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    dept,
    x="Department",
    y="PerformanceRating",
    color="PerformanceRating",
    title="Average Performance by Department"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------------------
# Job Satisfaction
# ----------------------------------------------------
job_sat = (
    filtered_df.groupby("JobRole")["JobSatisfaction"]
    .mean()
    .sort_values()
    .reset_index()
)

fig3 = px.bar(
    job_sat,
    x="JobSatisfaction",
    y="JobRole",
    orientation="h",
    color="JobSatisfaction",
    title="Average Job Satisfaction by Job Role"
)

# ----------------------------------------------------
# Environment Satisfaction
# ----------------------------------------------------
env = (
    filtered_df.groupby("Department")["EnvironmentSatisfaction"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    env,
    x="Department",
    y="EnvironmentSatisfaction",
    color="EnvironmentSatisfaction",
    title="Environment Satisfaction by Department"
)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.plotly_chart(fig4, use_container_width=True)

# ----------------------------------------------------
# Work Life Balance
# ----------------------------------------------------
worklife = (
    filtered_df.groupby("Department")["WorkLifeBalance"]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    worklife,
    x="Department",
    y="WorkLifeBalance",
    color="WorkLifeBalance",
    title="Work-Life Balance by Department"
)

# ----------------------------------------------------
# Performance vs Salary
# ----------------------------------------------------
fig6 = px.scatter(
    filtered_df,
    x="MonthlyIncome",
    y="PerformanceRating",
    color="Department",
    size="TotalWorkingYears",
    hover_data=["JobRole"],
    title="Performance vs Monthly Income"
)

col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.plotly_chart(fig6, use_container_width=True)

# ----------------------------------------------------
# Training Analysis
# ----------------------------------------------------
training = (
    filtered_df.groupby("TrainingTimesLastYear")
    .size()
    .reset_index(name="Employees")
)

fig7 = px.bar(
    training,
    x="TrainingTimesLastYear",
    y="Employees",
    color="Employees",
    title="Training Sessions Last Year"
)

# ----------------------------------------------------
# Performance by Overtime
# ----------------------------------------------------
fig8 = px.box(
    filtered_df,
    x="OverTime",
    y="PerformanceRating",
    color="OverTime",
    title="Performance Rating by Overtime"
)

col7, col8 = st.columns(2)

with col7:
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.plotly_chart(fig8, use_container_width=True)

# ----------------------------------------------------
# High Performers
# ----------------------------------------------------
st.subheader("🏆 High Performing Employees")

top = (
    filtered_df.sort_values(
        by=[
            "PerformanceRating",
            "MonthlyIncome"
        ],
        ascending=False
    )[
        [
            "JobRole",
            "Department",
            "PerformanceRating",
            "MonthlyIncome",
            "YearsAtCompany",
            "JobSatisfaction"
        ]
    ]
    .head(10)
)

st.dataframe(top, use_container_width=True)

# ----------------------------------------------------
# Key Insights
# ----------------------------------------------------
st.subheader("📌 Performance Insights")

best_department = (
    filtered_df.groupby("Department")["PerformanceRating"]
    .mean()
    .idxmax()
)

best_role = (
    filtered_df.groupby("JobRole")["PerformanceRating"]
    .mean()
    .idxmax()
)

st.success(f"""
### Key Findings

- 🏆 Best Performing Department: **{best_department}**
- 👨‍💼 Best Performing Job Role: **{best_role}**
- ⭐ Average Performance Rating: **{avg_performance:.2f}**
- 😊 Average Job Satisfaction: **{avg_job_satisfaction:.2f}**
- ⚖️ Average Work-Life Balance: **{avg_worklife:.2f}**
""")

# ----------------------------------------------------
# Download Data
# ----------------------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Performance Data",
    data=csv,
    file_name="performance_analysis.csv",
    mime="text/csv"
)