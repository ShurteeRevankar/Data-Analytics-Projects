import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Analysis",
    layout="wide"
)

st.title("📈 Sales Analysis")

# Load Data
if "df" not in st.session_state:
    st.warning("Please upload the dataset from the Data Upload page first.")
    st.stop()

df = st.session_state["df"]


# Convert Date
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

# Create Year and Month Columns
df["Year"] = df["order_purchase_timestamp"].dt.year
df["Month"] = df["order_purchase_timestamp"].dt.month_name()

# Sidebar Filters
st.sidebar.header("Sales Filters")

selected_states = st.sidebar.multiselect(
    "State",
    sorted(df["customer_state"].dropna().unique())
)

selected_years = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].unique())
)

# Create Filtered Dataset
filtered_df = df.copy()

# Apply State Filter
if selected_states:
    filtered_df = filtered_df[
        filtered_df["customer_state"].isin(selected_states)
    ]

# Apply Year Filter
if selected_years:
    filtered_df = filtered_df[
        filtered_df["Year"].isin(selected_years)
    ]

    

# Convert Date Column
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

# Create Month-Year Column
df["Month"] = df["order_purchase_timestamp"].dt.strftime("%Y-%m")

# Monthly Revenue
monthly_revenue = (
    filtered_df.groupby("Month")["payment_value"]
    .sum()
    .reset_index()
)

# Revenue Trend Chart
st.subheader("Monthly Revenue Trend")

fig = px.line(
    monthly_revenue,
    x="Month",
    y="payment_value",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig, use_container_width=True)

# KPI Summary
peak_month = monthly_revenue.loc[
    monthly_revenue["payment_value"].idxmax(),
    "Month"
]

peak_revenue = monthly_revenue["payment_value"].max()

st.subheader("Key Insights")

st.info(f"📌 Peak sales occurred in {peak_month}.")
st.info(f"📌 Highest monthly revenue was R$ {peak_revenue:,.2f}.")

growth = (
    (monthly_revenue["payment_value"].iloc[-1]
     - monthly_revenue["payment_value"].iloc[0])
    / monthly_revenue["payment_value"].iloc[0]
) * 100

st.success(
    f"Revenue changed by {growth:.2f}% between the first and last month."
)