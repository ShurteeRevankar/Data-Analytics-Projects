import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="State Analysis",
    layout="wide"
)

st.title("🗺️ State Analysis")

# Load Dataset
if "df" not in st.session_state:
    st.warning("Please upload the dataset from the Data Upload page first.")
    st.stop()

df = st.session_state["df"]

# =========================
# Revenue by State
# =========================

revenue_state = (
    df.groupby("customer_state")["payment_value"]
    .sum()
    .reset_index()
    .sort_values("payment_value", ascending=False)
)

st.subheader("Revenue by State")

fig1 = px.bar(
    revenue_state,
    x="customer_state",
    y="payment_value",
    title="Revenue by State",
    labels={
        "customer_state": "State",
        "payment_value": "Revenue (R$)"
    }
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# Orders by State
# =========================

orders_state = (
    df.groupby("customer_state")["order_id"]
    .nunique()
    .reset_index()
    .sort_values("order_id", ascending=False)
)

st.subheader("Orders by State")

fig2 = px.bar(
    orders_state,
    x="customer_state",
    y="order_id",
    title="Orders by State",
    labels={
        "customer_state": "State",
        "order_id": "Number of Orders"
    }
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# KPI Cards
# =========================

top_revenue_state = revenue_state.iloc[0]
top_orders_state = orders_state.iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Top Revenue State",
        top_revenue_state["customer_state"]
    )

with col2:
    st.metric(
        "Top Orders State",
        top_orders_state["customer_state"]
    )

# =========================
# Insights
# =========================

st.subheader("📌 Insights")

st.info(
    f"🏆 {top_revenue_state['customer_state']} - Sao Paulo contributes the highest revenue "
    f"with R$ {top_revenue_state['payment_value']:,.2f}."
)

if len(revenue_state) > 1:
    second_state = revenue_state.iloc[1]

    st.info(
        f"🥈 {second_state['customer_state']} - Rio de Janero follows with "
        f"R$ {second_state['payment_value']:,.2f}."
    )