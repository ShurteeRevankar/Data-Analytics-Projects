import streamlit as st

from utils.data_loader import load_data, get_basic_info
from utils.preprocessing import preprocess_data

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👨‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main-title{
    font-size:40px;
    font-weight:bold;
    color:#2563EB;
}

.sub-title{
    font-size:18px;
    color:gray;
}

.metric-card{
    background-color:#F8FAFC;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.image(
    "https://img.icons8.com/color/96/conference-call.png",
    width=90
)

st.sidebar.title("HR Analytics")

st.sidebar.info("""
Professional HR Analytics Dashboard

Built using

• Streamlit

• Python

• Plotly

• Machine Learning
""")

# -----------------------------
# Load Dataset
# -----------------------------
df = load_data()

if df.empty:
    st.stop()

df = preprocess_data(df)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<p class="main-title">👨‍💼 HR Analytics Dashboard</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Employee Attrition Analysis & Workforce Insights</p>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Dataset Information
# -----------------------------
info = get_basic_info(df)

total_employees = len(df)
employees_left = df["Attrition"].eq("Yes").sum()
active_employees = total_employees - employees_left
attrition_rate = (employees_left / total_employees) * 100

avg_salary = df["MonthlyIncome"].mean()
avg_age = df["Age"].mean()
avg_experience = df["TotalWorkingYears"].mean()

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "👥 Total Employees",
    f"{total_employees:,}"
)

col2.metric(
    "✅ Active Employees",
    f"{active_employees:,}"
)

col3.metric(
    "❌ Employees Left",
    f"{employees_left:,}"
)

st.write("")

col4, col5, col6 = st.columns(3)

col4.metric(
    "📉 Attrition Rate",
    f"{attrition_rate:.2f}%"
)

col5.metric(
    "💰 Avg Monthly Income",
    f"${avg_salary:,.0f}"
)

col6.metric(
    "🎂 Average Age",
    f"{avg_age:.1f}"
)

st.write("")

col7, col8 = st.columns(2)

col7.metric(
    "💼 Avg Experience",
    f"{avg_experience:.1f} Years"
)

col8.metric(
    "📊 Dataset Columns",
    info["Columns"]
)

st.divider()

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("📄 Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)

# -----------------------------
# Dataset Information
# -----------------------------
st.subheader("📌 Dataset Information")

info_col1, info_col2, info_col3, info_col4 = st.columns(4)

info_col1.metric("Rows", info["Rows"])
info_col2.metric("Columns", info["Columns"])
info_col3.metric("Missing Values", info["Missing Values"])
info_col4.metric("Duplicates", info["Duplicate Rows"])

st.divider()

# -----------------------------
# Quick Insights
# -----------------------------
st.subheader("📈 Project Objectives")

st.markdown("""
- Analyze employee attrition patterns.
- Explore workforce demographics.
- Compare salaries across departments.
- Study employee satisfaction.
- Identify key attrition factors.
- Predict employee attrition using Machine Learning.
""")

st.success("Use the pages in the left sidebar to explore detailed HR analytics.")

