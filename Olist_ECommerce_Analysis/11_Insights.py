import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Business Insights",
    layout="wide"
)

st.title("💡 Automated Business Insights")

# Load Dataset
df = pd.read_csv("data/master_olist.csv")

# ==================================
# Top Revenue State
# ==================================
state_revenue = (
    df.groupby("customer_state")["payment_value"]
    .sum()
    .reset_index()
)

top_state = state_revenue.loc[
    state_revenue["payment_value"].idxmax(),
    "customer_state"
]

# ==================================
# Top Revenue Category
# ==================================
category_revenue = (
    df.groupby("product_category_name")["payment_value"]
    .sum()
    .reset_index()
    .dropna()
)

top_category = category_revenue.loc[
    category_revenue["payment_value"].idxmax(),
    "product_category_name"
]

# ==================================
# Most Popular Payment Method
# ==================================
popular_payment = (
    df["payment_type"]
    .mode()[0]
)

# ==================================
# Peak Revenue Month
# ==================================
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

df["Month"] = (
    df["order_purchase_timestamp"]
    .dt.strftime("%B")
)

monthly_revenue = (
    df.groupby("Month")["payment_value"]
    .sum()
    .reset_index()
)

peak_month = monthly_revenue.loc[
    monthly_revenue["payment_value"].idxmax(),
    "Month"
]

# ==================================
# Average Delivery Time
# ==================================
df["order_delivered_customer_date"] = pd.to_datetime(
    df["order_delivered_customer_date"]
)

df["delivery_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.days

avg_delivery = round(
    df["delivery_days"].mean(),
    1
)

# ==================================
# Display Insights
# ==================================

st.success(
    f"1️⃣ {top_state} generates the highest revenue."
)

st.success(
    f"2️⃣ {popular_payment.title()} is preferred by most customers."
)

st.success(
    f"3️⃣ {top_category} category generates the highest revenue."
)

st.success(
    f"4️⃣ {peak_month} generates maximum revenue."
)

st.success(
    f"5️⃣ Average delivery takes {avg_delivery} days."
)

# ==================================
# Executive Summary
# ==================================

st.markdown("---")

st.subheader("📋 Executive Summary")

summary = f"""
• Highest Revenue State: {top_state}

• Top Revenue Category: {top_category}

• Most Popular Payment Method: {popular_payment.title()}

• Peak Revenue Month: {peak_month}

• Average Delivery Time: {avg_delivery} Days
"""

st.info(summary)