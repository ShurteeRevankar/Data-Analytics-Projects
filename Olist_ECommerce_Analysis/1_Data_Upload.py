import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Data Upload",
    layout="wide"
)

st.title("📂 Data Upload & Overview")

# Load Dataset
df = pd.read_csv("data/master_olist.csv")

# Shape
st.subheader("Dataset Shape")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

# Dataset Preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Column Names
st.subheader("Column Names")
st.write(list(df.columns))

# Data Types
st.subheader("Data Types")
st.dataframe(
    pd.DataFrame(
        {
            "Column": df.columns,
            "Data Type": df.dtypes.values
        }
    )
)

