import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Data Cleaning",
    layout="wide"
)

st.title("🧹Data Cleaning")

# Load Dataset
if "df" not in st.session_state:
    st.warning("Please upload the dataset from the Data Upload page first.")
    st.stop()

df = st.session_state["df"]
# ---------------------------
# Missing Values
# ---------------------------
st.subheader("Missing Values")

missing_df = pd.DataFrame({
    "Column Name": df.columns,
    "Missing Count": df.isnull().sum().values
})

st.dataframe(missing_df, use_container_width=True)

# ---------------------------
# Duplicates
# ---------------------------
st.subheader("Duplicate Records")

duplicate_count = df.duplicated().sum()

st.metric(
    label="Duplicate Rows",
    value=duplicate_count
)

# ---------------------------
# Data Quality Score
# ---------------------------
st.subheader("Data Quality Score")

total_cells = df.shape[0] * df.shape[1]
missing_cells = df.isnull().sum().sum()

missing_percentage = (missing_cells / total_cells) * 100

quality_score = round(100 - missing_percentage, 2)

st.metric(
    label="Data Quality Score",
    value=f"{quality_score}%"
)

# ---------------------------
# Cleaning Buttons
# ---------------------------
st.subheader("Cleaning Actions")

col1, col2 = st.columns(2)

with col1:
    if st.button("Remove Missing Values"):
        cleaned_df = df.dropna()
        st.success(
            f"Missing values removed. New Shape: {cleaned_df.shape}"
        )

with col2:
    if st.button("Remove Duplicates"):
        cleaned_df = df.drop_duplicates()
        st.success(
            f"Duplicates removed. New Shape: {cleaned_df.shape}"
        )

# ---------------------------
# Dataset Summary
# ---------------------------
st.subheader("Dataset Summary")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])