import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="Attrition Analysis",
    page_icon="📉",
    layout="wide"
)

st.title("📉 Employee Attrition Analysis")
st.markdown("Analyze the factors contributing to employee attrition.")

# ------------------------------------
# Load Data
# ------------------------------------
df = load_data()

if df.empty:
    st.stop()

df = preprocess_data(df)

# ------------------------------------
# Sidebar Filters
# ------------------------------------
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

overtime = st.sidebar.multiselect(
    "OverTime",
    sorted(df["OverTime"].unique()),
    default=sorted(df["OverTime"].unique())
)

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["Gender"].isin(gender)) &
    (df["OverTime"].isin(overtime))
]

# ------------------------------------
# KPI Cards
# ------------------------------------
total = len(filtered_df)
left = filtered_df["Attrition"].eq("Yes").sum()
stayed = total - left
rate = (left / total * 100) if total > 0 else 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Employees", total)
c2.metric("Employees Left", left)
c3.metric("Employees Stayed", stayed)
c4.metric("Attrition Rate", f"{rate:.2f}%")

st.divider()

# ------------------------------------
# Attrition by Department
# ------------------------------------
dept = (
    filtered_df.groupby(["Department", "Attrition"])
    .size()
    .reset_index(name="Employees")
)

fig1 = px.bar(
    dept,
    x="Department",
    y="Employees",
    color="Attrition",
    barmode="group",
    title="Attrition by Department"
)

# ------------------------------------
# Attrition by Gender
# ------------------------------------
gender_df = (
    filtered_df.groupby(["Gender", "Attrition"])
    .size()
    .reset_index(name="Employees")
)

fig2 = px.bar(
    gender_df,
    x="Gender",
    y="Employees",
    color="Attrition",
    barmode="group",
    title="Attrition by Gender"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------
# Attrition by Job Role
# ------------------------------------
job = (
    filtered_df.groupby(["JobRole", "Attrition"])
    .size()
    .reset_index(name="Employees")
)

fig3 = px.bar(
    job,
    x="Employees",
    y="JobRole",
    color="Attrition",
    orientation="h",
    title="Attrition by Job Role"
)

# ------------------------------------
# Attrition by Overtime
# ------------------------------------
ot = (
    filtered_df.groupby(["OverTime", "Attrition"])
    .size()
    .reset_index(name="Employees")
)

fig4 = px.bar(
    ot,
    x="OverTime",
    y="Employees",
    color="Attrition",
    barmode="group",
    title="Attrition by Overtime"
)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.plotly_chart(fig4, use_container_width=True)

# ------------------------------------
# Attrition by Age Group
# ------------------------------------
age = (
    filtered_df.groupby(["AgeGroup", "Attrition"])
    .size()
    .reset_index(name="Employees")
)

fig5 = px.bar(
    age,
    x="AgeGroup",
    y="Employees",
    color="Attrition",
    barmode="group",
    title="Attrition by Age Group"
)

# ------------------------------------
# Attrition by Income Category
# ------------------------------------
income = (
    filtered_df.groupby(["IncomeCategory", "Attrition"])
    .size()
    .reset_index(name="Employees")
)

fig6 = px.bar(
    income,
    x="IncomeCategory",
    y="Employees",
    color="Attrition",
    barmode="group",
    title="Attrition by Income Category"
)

col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.plotly_chart(fig6, use_container_width=True)

# ------------------------------------
# Attrition by Years at Company
# ------------------------------------
fig7 = px.histogram(
    filtered_df,
    x="YearsAtCompany",
    color="Attrition",
    nbins=15,
    barmode="overlay",
    title="Attrition by Years at Company"
)

st.plotly_chart(fig7, use_container_width=True)

# ------------------------------------
# Attrition Distribution
# ------------------------------------
fig8 = px.pie(
    filtered_df,
    names="Attrition",
    hole=0.5,
    title="Overall Attrition Distribution"
)

st.plotly_chart(fig8, use_container_width=True)

# ------------------------------------
# Key Insights
# ------------------------------------
st.subheader("📌 Key Insights")

highest_attrition_dept = (
    filtered_df[filtered_df["Attrition"] == "Yes"]["Department"]
    .value_counts()
    .idxmax()
)

highest_attrition_role = (
    filtered_df[filtered_df["Attrition"] == "Yes"]["JobRole"]
    .value_counts()
    .idxmax()
)

st.info(f"""
**Highest Attrition Department:** {highest_attrition_dept}

**Highest Attrition Job Role:** {highest_attrition_role}

**Overall Attrition Rate:** {rate:.2f}%
""")

# ------------------------------------
# Download Data
# ------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Attrition Data",
    csv,
    "attrition_analysis.csv",
    "text/csv"
)