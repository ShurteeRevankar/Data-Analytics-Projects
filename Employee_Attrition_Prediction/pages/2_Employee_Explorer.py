import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Employee Explorer",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Employee Explorer")
st.markdown("Search, filter and explore employee information.")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
df = load_data()

if df.empty:
    st.stop()

df = preprocess_data(df)

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🔍 Filter Employees")

department = st.sidebar.multiselect(
    "Department",
    options=sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

job_role = st.sidebar.multiselect(
    "Job Role",
    options=sorted(df["JobRole"].unique()),
    default=sorted(df["JobRole"].unique())
)

gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

marital = st.sidebar.multiselect(
    "Marital Status",
    options=sorted(df["MaritalStatus"].unique()),
    default=sorted(df["MaritalStatus"].unique())
)

attrition = st.sidebar.multiselect(
    "Attrition",
    options=sorted(df["Attrition"].unique()),
    default=sorted(df["Attrition"].unique())
)

# --------------------------------------------------
# Salary Filter
# --------------------------------------------------
salary_range = st.sidebar.slider(
    "Monthly Income",
    int(df["MonthlyIncome"].min()),
    int(df["MonthlyIncome"].max()),
    (
        int(df["MonthlyIncome"].min()),
        int(df["MonthlyIncome"].max())
    )
)

# --------------------------------------------------
# Age Filter
# --------------------------------------------------
age_range = st.sidebar.slider(
    "Age",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (
        int(df["Age"].min()),
        int(df["Age"].max())
    )
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------
filtered_df = df[
    (df["Department"].isin(department)) &
    (df["JobRole"].isin(job_role)) &
    (df["Gender"].isin(gender)) &
    (df["MaritalStatus"].isin(marital)) &
    (df["Attrition"].isin(attrition)) &
    (df["MonthlyIncome"].between(*salary_range)) &
    (df["Age"].between(*age_range))
]

# --------------------------------------------------
# Search
# --------------------------------------------------
search = st.text_input(
    "🔎 Search by Job Role or Department"
)

if search:

    filtered_df = filtered_df[
        filtered_df["JobRole"].str.contains(
            search,
            case=False,
            na=False
        ) |
        filtered_df["Department"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# --------------------------------------------------
# KPIs
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Employees", len(filtered_df))
c2.metric("Avg Age", f"{filtered_df['Age'].mean():.1f}")
c3.metric("Avg Salary", f"${filtered_df['MonthlyIncome'].mean():,.0f}")
c4.metric(
    "Attrition %",
    f"{(filtered_df['Attrition']=='Yes').mean()*100:.2f}%"
)

st.divider()

# --------------------------------------------------
# Choose Columns
# --------------------------------------------------
st.subheader("📋 Employee Records")

selected_columns = st.multiselect(
    "Select Columns",
    options=df.columns.tolist(),
    default=[
        "Age",
        "Gender",
        "Department",
        "JobRole",
        "MonthlyIncome",
        "TotalWorkingYears",
        "YearsAtCompany",
        "Attrition"
    ]
)

st.dataframe(
    filtered_df[selected_columns],
    use_container_width=True,
    height=500
)

# --------------------------------------------------
# Statistics
# --------------------------------------------------
with st.expander("📈 Summary Statistics"):

    st.dataframe(
        filtered_df.describe(),
        use_container_width=True
    )

# --------------------------------------------------
# Download
# --------------------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "employee_data.csv",
    "text/csv"
)