import streamlit as st

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from utils.charts import (
    gender_distribution,
    department_distribution,
    job_role_distribution,
    age_distribution,
)

# ----------------------------------
# Page Config
# ----------------------------------
st.set_page_config(
    page_title="HR Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 HR Overview")
st.markdown("Explore workforce demographics and key HR metrics.")

# ----------------------------------
# Load Data
# ----------------------------------
df = load_data()

if df.empty:
    st.stop()

df = preprocess_data(df)

# ----------------------------------
# Sidebar Filters
# ----------------------------------
st.sidebar.header("🔎 Filters")

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

job_role = st.sidebar.multiselect(
    "Job Role",
    sorted(df["JobRole"].unique()),
    default=sorted(df["JobRole"].unique())
)

overtime = st.sidebar.multiselect(
    "OverTime",
    sorted(df["OverTime"].unique()),
    default=sorted(df["OverTime"].unique())
)

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["Gender"].isin(gender)) &
    (df["JobRole"].isin(job_role)) &
    (df["OverTime"].isin(overtime))
]

# ----------------------------------
# KPIs
# ----------------------------------
total_emp = len(filtered_df)
left_emp = filtered_df["Attrition"].eq("Yes").sum()
active_emp = total_emp - left_emp
attrition_rate = (left_emp / total_emp * 100) if total_emp else 0

avg_age = filtered_df["Age"].mean()
avg_income = filtered_df["MonthlyIncome"].mean()
avg_exp = filtered_df["TotalWorkingYears"].mean()

st.subheader("📌 Workforce KPIs")

c1, c2, c3 = st.columns(3)

c1.metric("👥 Total Employees", f"{total_emp:,}")
c2.metric("✅ Active Employees", f"{active_emp:,}")
c3.metric("❌ Employees Left", f"{left_emp:,}")

c4, c5, c6 = st.columns(3)

c4.metric("📉 Attrition Rate", f"{attrition_rate:.2f}%")
c5.metric("💰 Avg Monthly Income", f"${avg_income:,.0f}")
c6.metric("🎂 Average Age", f"{avg_age:.1f}")

st.metric("💼 Avg Experience", f"{avg_exp:.1f} Years")

st.divider()

# ----------------------------------
# Charts Row 1
# ----------------------------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        gender_distribution(filtered_df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        department_distribution(filtered_df),
        use_container_width=True
    )

# ----------------------------------
# Charts Row 2
# ----------------------------------
col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        job_role_distribution(filtered_df),
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        age_distribution(filtered_df),
        use_container_width=True
    )

st.divider()

# ----------------------------------
# Dataset Preview
# ----------------------------------
st.subheader("📄 Employee Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)

# ----------------------------------
# Download Button
# ----------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "filtered_hr_data.csv",
    "text/csv"
)