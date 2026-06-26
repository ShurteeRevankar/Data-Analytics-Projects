import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Payment Analysis",
    layout="wide"
)

st.title("💳 Payment Analysis")

# Load Dataset
if "df" not in st.session_state:
    st.warning("Please upload the dataset from the Data Upload page first.")
    st.stop()

df = st.session_state["df"]

# Payment Type Analysis
payment_analysis = (
    df.groupby("payment_type")["order_id"]
    .count()
    .reset_index()
)

# Pie Chart
st.subheader("Payment Method Distribution")

fig = px.pie(
    payment_analysis,
    names="payment_type",
    values="order_id",
    title="Orders by Payment Type",
    hole=0.3
)

st.plotly_chart(fig, use_container_width=True)

# KPI Cards
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Payment Methods",
        payment_analysis["payment_type"].nunique()
    )

with col2:
    most_used = payment_analysis.loc[
        payment_analysis["order_id"].idxmax(),
        "payment_type"
    ]
    
    st.metric(
        "Most Used Method",
        most_used.title()
    )

# Payment Summary Table
st.subheader("Payment Summary")

payment_analysis.columns = [
    "Payment Type",
    "Number of Transactions"
]

st.dataframe(
    payment_analysis,
    use_container_width=True
)

# Insights
st.subheader("📌 Insights")

top_payment = payment_analysis.loc[
    payment_analysis["Number of Transactions"].idxmax()
]

st.success(
    f"💳 Most customers prefer {top_payment['Payment Type'].title()} "
    f"payments with {top_payment['Number of Transactions']:,} transactions."
)

st.info(
    "Credit cards generally dominate online purchases due to convenience and installment options."
)