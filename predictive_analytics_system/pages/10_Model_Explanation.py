import streamlit as st

# Page Configuration

st.set_page_config(
    page_title="Model Explanation",
    page_icon="📑",
    layout="wide"
)


# Title

st.title("📑 Model Explanation")

st.markdown("""
This page explains the Machine Learning model used in the 
Google Maps Business Analytics application.
""")


# Model Overview

st.subheader("🤖 Machine Learning Model")

st.write("""
The application uses a **Random Forest Classifier** to analyze
business characteristics and predict business opportunities.

Random Forest is selected because:

- Handles numerical and categorical data well
- Reduces overfitting compared to a single decision tree
- Provides feature importance
- Works effectively on business datasets
""")


# Workflow

st.subheader("⚙️ Model Workflow")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.info("""
    **1. Data Input**

    Google Maps business dataset
    uploaded by user
    """)

with col2:
    st.info("""
    **2. Data Processing**

    Cleaning, encoding,
    feature engineering
    """)

with col3:
    st.info("""
    **3. Model Training**

    Random Forest learns
    business patterns
    """)

with col4:
    st.info("""
    **4. Prediction**

    Opportunity category
    prediction
    """)


# Features

st.subheader("📊 Features Used For Prediction")

features = [
    "Category",
    "City",
    "Area / Locality",
    "Pincode",
    "Google Rating",
    "Total Reviews",
    "Latitude",
    "Longitude",
    "Business Status",
    "Business Size",
    "Rating Category",
    "Website Availability"
]


for feature in features:
    st.write("✅", feature)



# Target Variable

st.subheader("🎯 Prediction Target")

st.write("""
The model predicts business opportunity based on:

- Customer engagement
- Ratings
- Reviews
- Online presence
- Business characteristics

Output:

**High Opportunity Business**
or

**Low Opportunity Business**
""")


# Model Evaluation

st.subheader("📈 Model Performance")

metric1, metric2, metric3 = st.columns(3)


with metric1:
    st.metric(
        "Algorithm",
        "Random Forest"
    )

with metric2:
    st.metric(
        "Task",
        "Classification"
    )

with metric3:
    st.metric(
        "Evaluation",
        "Accuracy Score"
    )


st.info("""
Model performance metrics are generated during training
and stored with the trained model.
""")


# Feature Importance

st.subheader("⭐ Feature Importance")

st.write("""
Feature importance shows which factors contribute most
to identifying business opportunities.

Typical important features:

1. Google Rating
2. Total Reviews
3. Website Availability
4. Business Category
5. Location
""")


# Business Use Case

st.subheader("💼 Business Application")

st.success("""
This model helps businesses identify:

- Locations with growth potential
- Businesses needing digital presence
- High-performing categories
- Market opportunities
""")
