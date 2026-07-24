import streamlit as st
import pandas as pd

from utils.prediction import predict_attrition

st.set_page_config(
    page_title="Attrition Prediction",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Employee Attrition Prediction")
st.markdown("Predict whether an employee is likely to leave the organization.")

st.divider()

st.subheader("Employee Information")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", 18, 60, 30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    department = st.selectbox(
        "Department",
        [
            "Human Resources",
            "Research & Development",
            "Sales"
        ]
    )
    education = st.selectbox(
        "Education",
        [1, 2, 3, 4, 5]
    )
    education_field = st.selectbox(
        "Education Field",
        [
            "Life Sciences",
            "Medical",
            "Marketing",
            "Technical Degree",
            "Human Resources",
            "Other"
        ]
    )
    business_travel = st.selectbox(
        "Business Travel",
        [
            "Non-Travel",
            "Travel_Rarely",
            "Travel_Frequently"
        ]
    )
    marital_status = st.selectbox(
        "Marital Status",
        [
            "Single",
            "Married",
            "Divorced"
        ]
    )

with col2:
    job_role = st.selectbox(
        "Job Role",
        [
            "Healthcare Representative",
            "Human Resources",
            "Laboratory Technician",
            "Manager",
            "Manufacturing Director",
            "Research Director",
            "Research Scientist",
            "Sales Executive",
            "Sales Representative"
        ]
    )

    job_level = st.slider("Job Level", 1, 5, 2)
    monthly_income = st.number_input(
        "Monthly Income",
        1000,
        25000,
        6000
    )

    total_working_years = st.slider(
        "Total Working Years",
        0,
        40,
        8
    )

    years_at_company = st.slider(
        "Years at Company",
        0,
        40,
        5
    )

    years_current_role = st.slider(
        "Years in Current Role",
        0,
        20,
        3
    )

    years_since_promotion = st.slider(
        "Years Since Last Promotion",
        0,
        15,
        1
    )

with col3:

    overtime = st.selectbox(
        "OverTime",
        [
            "No",
            "Yes"
        ]
    )

    job_satisfaction = st.slider(
        "Job Satisfaction",
        1,
        4,
        3
    )

    environment = st.slider(
        "Environment Satisfaction",
        1,
        4,
        3
    )

    worklife = st.slider(
        "Work-Life Balance",
        1,
        4,
        3
    )

    performance = st.slider(
        "Performance Rating",
        3,
        4,
        3
    )

    distance = st.slider(
        "Distance From Home",
        1,
        30,
        5
    )

    training = st.slider(
        "Training Times Last Year",
        0,
        6,
        2
    )

st.divider()

if st.button("🔮 Predict Attrition", use_container_width=True):

    employee = {
        "Age": age,
        "BusinessTravel": business_travel,
        "DailyRate": 800,
        "Department": department,
        "DistanceFromHome": distance,
        "Education": education,
        "EducationField": education_field,
        "EnvironmentSatisfaction": environment,
        "Gender": gender,
        "HourlyRate": 60,
        "JobInvolvement": 3,
        "JobLevel": job_level,
        "JobRole": job_role,
        "JobSatisfaction": job_satisfaction,
        "MaritalStatus": marital_status,
        "MonthlyIncome": monthly_income,
        "MonthlyRate": 15000,
        "NumCompaniesWorked": 2,
        "OverTime": overtime,
        "PercentSalaryHike": 15,
        "PerformanceRating": performance,
        "RelationshipSatisfaction": 3,
        "StockOptionLevel": 1,
        "TotalWorkingYears": total_working_years,
        "TrainingTimesLastYear": training,
        "WorkLifeBalance": worklife,
        "YearsAtCompany": years_at_company,
        "YearsInCurrentRole": years_current_role,
        "YearsSinceLastPromotion": years_since_promotion,
        "YearsWithCurrManager": 3,
        "AgeGroup": "26-35",
        "IncomeCategory": "Medium",
        "ExperienceLevel": "6-10 Years",
        "DistanceCategory": "Medium",
        "OvertimeFlag": 1 if overtime == "Yes" else 0,
        "HighPerformer": 1 if performance == 4 else 0,
        "LongTenure": 1 if years_at_company >= 10 else 0
    }

    prediction, probability = predict_attrition(employee)

    st.divider()

    st.subheader("Prediction Result")

    if prediction == 1:

        st.error("⚠️ High Risk of Attrition")

        if probability is not None:
            st.metric(
                "Probability",
                f"{probability*100:.2f}%"
            )

        st.warning("""
### Recommendations

- Improve employee engagement
- Conduct one-on-one meetings
- Review compensation
- Improve work-life balance
- Provide career growth opportunities
""")

    else:

        st.success("✅ Low Risk of Attrition")

        if probability is not None:
            st.metric(
                "Probability",
                f"{(1-probability)*100:.2f}%"
            )

        st.info("""
### Recommendations

- Continue employee recognition
- Maintain career development
- Encourage training
- Maintain healthy work environment
""")

st.divider()

st.caption("HR Analytics Dashboard | Attrition Prediction using Machine Learning")