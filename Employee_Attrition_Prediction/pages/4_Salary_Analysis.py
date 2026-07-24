import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Salary Analysis",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Salary Analysis")
st.markdown("Analyze employee salary distribution across departments, job roles and demographics.")

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

gender = st.sidebar.multiselect(
    "Gender",
    sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

education = st.sidebar.multiselect(
    "Education",
    sorted(df["Education"].unique()),
    default=sorted(df["Education"].unique())
)

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["Gender"].isin(gender)) &
    (df["Education"].isin(education))
]

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------
avg_salary = filtered_df["MonthlyIncome"].mean()
max_salary = filtered_df["MonthlyIncome"].max()
min_salary = filtered_df["MonthlyIncome"].min()
total_payroll = filtered_df["MonthlyIncome"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average Salary", f"${avg_salary:,.0f}")
c2.metric("Highest Salary", f"${max_salary:,.0f}")
c3.metric("Lowest Salary", f"${min_salary:,.0f}")
c4.metric("Total Payroll", f"${total_payroll:,.0f}")

st.divider()

# ----------------------------------------------------
# Salary Distribution
# ----------------------------------------------------
fig1 = px.histogram(
    filtered_df,
    x="MonthlyIncome",
    nbins=30,
    title="Monthly Salary Distribution",
    color_discrete_sequence=["royalblue"]
)

# ----------------------------------------------------
# Salary by Department
# ----------------------------------------------------
fig2 = px.box(
    filtered_df,
    x="Department",
    y="MonthlyIncome",
    color="Department",
    title="Salary by Department"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------------------
# Salary by Job Role
# ----------------------------------------------------
salary_role = (
    filtered_df.groupby("JobRole")["MonthlyIncome"]
    .mean()
    .sort_values()
    .reset_index()
)

fig3 = px.bar(
    salary_role,
    x="MonthlyIncome",
    y="JobRole",
    orientation="h",
    color="MonthlyIncome",
    title="Average Salary by Job Role"
)

# ----------------------------------------------------
# Salary by Gender
# ----------------------------------------------------
fig4 = px.box(
    filtered_df,
    x="Gender",
    y="MonthlyIncome",
    color="Gender",
    title="Salary by Gender"
)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.plotly_chart(fig4, use_container_width=True)

# ----------------------------------------------------
# Salary by Education
# ----------------------------------------------------
salary_edu = (
    filtered_df.groupby("Education")["MonthlyIncome"]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    salary_edu,
    x="Education",
    y="MonthlyIncome",
    color="MonthlyIncome",
    title="Average Salary by Education Level"
)

# ----------------------------------------------------
# Salary vs Experience
# ----------------------------------------------------
fig6 = px.scatter(
    filtered_df,
    x="TotalWorkingYears",
    y="MonthlyIncome",
    color="Department",
    size="JobLevel",
    hover_data=["JobRole"],
    title="Salary vs Total Working Years"
)

col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.plotly_chart(fig6, use_container_width=True)

# ----------------------------------------------------
# Salary by Age Group
# ----------------------------------------------------
salary_age = (
    filtered_df.groupby("AgeGroup")["MonthlyIncome"]
    .mean()
    .reset_index()
)

fig7 = px.bar(
    salary_age,
    x="AgeGroup",
    y="MonthlyIncome",
    color="MonthlyIncome",
    title="Average Salary by Age Group"
)

# ----------------------------------------------------
# Salary by Overtime
# ----------------------------------------------------
fig8 = px.box(
    filtered_df,
    x="OverTime",
    y="MonthlyIncome",
    color="OverTime",
    title="Salary by Overtime"
)

col7, col8 = st.columns(2)

with col7:
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.plotly_chart(fig8, use_container_width=True)

# ----------------------------------------------------
# Top 10 Highest Paid Employees
# ----------------------------------------------------
st.subheader("🏆 Top 10 Highest Paid Employees")

top_salary = (
    filtered_df[
        [
            "JobRole",
            "Department",
            "MonthlyIncome",
            "Age",
            "TotalWorkingYears",
            "YearsAtCompany"
        ]
    ]
    .sort_values(
        by="MonthlyIncome",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_salary,
    use_container_width=True
)

# ----------------------------------------------------
# Key Insights
# ----------------------------------------------------
st.subheader("📌 Key Insights")

highest_department = (
    filtered_df.groupby("Department")["MonthlyIncome"]
    .mean()
    .idxmax()
)

highest_role = (
    filtered_df.groupby("JobRole")["MonthlyIncome"]
    .mean()
    .idxmax()
)

st.success(f"""
**Highest Paying Department:** {highest_department}

**Highest Paying Job Role:** {highest_role}

**Average Monthly Salary:** ${avg_salary:,.0f}
""")

# ----------------------------------------------------
# Download Button
# ----------------------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Salary Analysis Data",
    csv,
    "salary_analysis.csv",
    "text/csv"
)