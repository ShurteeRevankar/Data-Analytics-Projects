import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer Analysis",
    layout="wide"
)

st.title("👥 Customer Analysis")

# Load Dataset
if "df" not in st.session_state:
    st.warning("Please upload the dataset from the Data Upload page first.")
    st.stop()

df = st.session_state["df"]

# ===================================
# Customer KPIs
# ===================================

total_customers = df["customer_unique_id"].nunique()

customer_orders = (
    df.groupby("customer_unique_id")["order_id"]
    .nunique()
    .reset_index()
)

repeat_customers = (
    customer_orders[customer_orders["order_id"] > 1]
    .shape[0]
)

# KPI Cards
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Repeat Customers",
        f"{repeat_customers:,}"
    )

st.markdown("---")

# ===================================
# Customer Distribution by State
# ===================================

state_customers = (
    df.groupby("customer_state")["customer_unique_id"]
    .nunique()
    .reset_index()
    .sort_values(
        "customer_unique_id",
        ascending=False
    )
)

st.subheader("Customer Distribution by State")

fig = px.bar(
    state_customers,
    x="customer_state",
    y="customer_unique_id",
    title="Customers by State",
    labels={
        "customer_state": "State",
        "customer_unique_id": "Customers"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================
# Top States Table
# ===================================

st.subheader("Top States")

st.dataframe(
    state_customers.head(10),
    use_container_width=True
)

# ===================================
# Insights
# ===================================

top_state = state_customers.iloc[0]

st.subheader("📌 Insights")

st.success(
    f"🏆 Majority customers come from "
    f"{top_state['customer_state']} with "
    f"{top_state['customer_unique_id']:,} customers."
)

customer_retention = (
    repeat_customers / total_customers
) * 100

st.info(
    f"🔄 Repeat Customer Rate: "
    f"{customer_retention:.2f}%"
)