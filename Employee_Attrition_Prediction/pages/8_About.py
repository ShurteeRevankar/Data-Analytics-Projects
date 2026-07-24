import streamlit as st

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

# ----------------------------------------------------
# Title
# ----------------------------------------------------
st.title("ℹ️ About This Project")
st.markdown("Learn more about the HR Analytics Dashboard.")

st.divider()

# ----------------------------------------------------
# Project Overview
# ----------------------------------------------------
st.header("📌 Project Overview")

st.write("""
The **HR Analytics Dashboard** is an end-to-end data analytics project
developed to help Human Resource departments analyze employee data,
identify workforce trends, monitor attrition, evaluate employee
performance, and support data-driven decision-making.

The project combines **Data Analytics, Business Intelligence, and
Machine Learning** into a single interactive Streamlit application.
""")

# ----------------------------------------------------
# Objectives
# ----------------------------------------------------
st.header("🎯 Project Objectives")

st.markdown("""
- Analyze employee demographics
- Monitor employee attrition
- Study salary distribution
- Evaluate employee performance
- Identify workforce trends
- Predict employee attrition using Machine Learning
- Generate HR reports for decision making
""")

# ----------------------------------------------------
# Dataset Information
# ----------------------------------------------------
st.header("📂 Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.info("""
**Dataset Name**

IBM HR Analytics Employee Attrition Dataset
""")

with col2:
    st.info("""
**Records**

• Employees: 1470

• Features: 35+
""")

st.markdown("""
The dataset contains employee-related information such as:

- Age
- Gender
- Department
- Job Role
- Education
- Monthly Income
- Performance Rating
- Job Satisfaction
- Work-Life Balance
- Overtime
- Attrition
- Experience
- Training History
""")

# ----------------------------------------------------
# Dashboard Features
# ----------------------------------------------------
st.header("📊 Dashboard Modules")

st.markdown("""
✅ Home Dashboard

✅ HR Overview

✅ Employee Explorer

✅ Attrition Analysis

✅ Salary Analysis

✅ Performance Analysis

✅ Attrition Prediction

✅ Report Generator
""")

# ----------------------------------------------------
# Machine Learning
# ----------------------------------------------------
st.header("🤖 Machine Learning")

st.write("""
The application includes a Machine Learning model that predicts
whether an employee is likely to leave the organization based on
employee information.

**Algorithm Used**

- Random Forest Classifier

**Target Variable**

- Attrition

**Model Capabilities**

- Employee Attrition Prediction
- Risk Identification
- HR Decision Support
""")

# ----------------------------------------------------
# Technologies
# ----------------------------------------------------
st.header("🛠 Technology Stack")

tech1, tech2 = st.columns(2)

with tech1:

    st.markdown("""
### Programming

- Python
- SQL

### Libraries

- Pandas
- NumPy
- Scikit-learn
""")

with tech2:

    st.markdown("""
### Visualization

- Plotly
- Streamlit

### Tools

- Power BI
- VS Code
- GitHub
""")

# ----------------------------------------------------
# Project Workflow
# ----------------------------------------------------
st.header("⚙️ Project Workflow")

st.markdown("""
1. Data Collection

⬇️

2. Data Cleaning

⬇️

3. Feature Engineering

⬇️

4. Exploratory Data Analysis

⬇️

5. Dashboard Development

⬇️

6. Machine Learning Model

⬇️

7. Employee Attrition Prediction

⬇️

8. Business Insights & Reporting
""")

# ----------------------------------------------------
# Key Insights
# ----------------------------------------------------
st.header("💡 Business Benefits")

st.success("""
• Improve employee retention

• Identify high attrition departments

• Monitor employee performance

• Optimize salary planning

• Support HR decision making

• Improve workforce planning

• Enhance employee satisfaction
""")

# ----------------------------------------------------
# Internship Information
# ----------------------------------------------------
st.header("🎓 Internship Project")

st.info("""
This project was developed as part of the **ReadyNest Data Analytics Internship**.

The objective was to build a complete end-to-end HR Analytics solution using:

• Python

• Streamlit

• Machine Learning

• Power BI

• Data Visualization
""")

# ----------------------------------------------------
# Developer
# ----------------------------------------------------
st.header("👩‍💻 Developer")

st.markdown("""
**Project Developed By**

**Shrutee Sujit Revankar**

Data Analyst | Data Science Enthusiast

Skills:
- Python
- SQL
- Power BI
- Excel
- Streamlit
- Machine Learning
""")

# ----------------------------------------------------
# Footer
# ----------------------------------------------------
st.divider()

st.caption(
    "© 2026 HR Analytics Dashboard | ReadyNest Internship Project | Built with ❤️ using Streamlit"
)