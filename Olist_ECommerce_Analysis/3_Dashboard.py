import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide"
)

st.title("📊 Executive Dashboard")

# Load Dataset
df = pd.read_csv("data/master_olist.csv")



# Convert Date
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

# Create Year and Month
df["Year"] = df["order_purchase_timestamp"].dt.year
df["Month"] = df["order_purchase_timestamp"].dt.month_name()

# Sidebar Filters
st.sidebar.header("Filters")

selected_states = st.sidebar.multiselect(
    "State",
    sorted(df["customer_state"].dropna().unique())
)

selected_years = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].unique())
)

# Filter Data
filtered_df = df.copy()

if selected_states:
    filtered_df = filtered_df[
        filtered_df["customer_state"].isin(selected_states)
    ]

if selected_years:
    filtered_df = filtered_df[
        filtered_df["Year"].isin(selected_years)
    ]




# -----------------------------
# KPI Calculations
# -----------------------------

revenue = filtered_df["payment_value"].sum()

orders = filtered_df["order_id"].nunique()

customers = filtered_df["customer_unique_id"].nunique()

avg_order_value = revenue / orders

# -----------------------------
# KPI Cards
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Revenue",
        value=f"R$ {revenue:,.2f}"
    )

with col2:
    st.metric(
        label="📦 Orders",
        value=f"{orders:,}"
    )

with col3:
    st.metric(
        label="👥 Customers",
        value=f"{customers:,}"
    )

with col4:
    st.metric(
        label="🛒 Avg Order Value",
        value=f"R$ {avg_order_value:,.2f}"
    )

st.markdown("---")

# Dataset Overview
st.subheader("Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

st.markdown("---")

st.subheader("Sample Data")
st.dataframe(df.head(), use_container_width=True)