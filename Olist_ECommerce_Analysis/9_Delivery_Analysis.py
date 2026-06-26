import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Delivery Analysis",
    layout="wide"
)

st.title("🚚 Delivery Analysis")

# Load Dataset
df = pd.read_csv("data/master_olist.csv")

# Convert Date Columns
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

df["order_delivered_customer_date"] = pd.to_datetime(
    df["order_delivered_customer_date"]
)

# Create Delivery Days
df["delivery_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.days

# Remove invalid values
delivery_df = df[df["delivery_days"] >= 0]

# KPI
avg_delivery = round(
    delivery_df["delivery_days"].mean(),
    2
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Average Delivery Days",
        avg_delivery
    )

with col2:
    st.metric(
        "Total Delivered Orders",
        delivery_df["order_id"].nunique()
    )

st.markdown("---")

# Histogram
st.subheader("Delivery Time Distribution")

fig = px.histogram(
    delivery_df,
    x="delivery_days",
    nbins=30,
    title="Distribution of Delivery Days"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Summary Statistics
st.subheader("Delivery Statistics")

stats_df = pd.DataFrame({
    "Metric": [
        "Average",
        "Minimum",
        "Maximum",
        "Median"
    ],
    "Value": [
        delivery_df["delivery_days"].mean(),
        delivery_df["delivery_days"].min(),
        delivery_df["delivery_days"].max(),
        delivery_df["delivery_days"].median()
    ]
})

st.dataframe(
    stats_df,
    use_container_width=True
)

# Insights
st.subheader("📌 Insights")

st.success(
    f"Average delivery takes {avg_delivery} days."
)

st.info(
    f"Fastest delivery took {delivery_df['delivery_days'].min()} days."
)

st.info(
    f"Longest delivery took {delivery_df['delivery_days'].max()} days."
)