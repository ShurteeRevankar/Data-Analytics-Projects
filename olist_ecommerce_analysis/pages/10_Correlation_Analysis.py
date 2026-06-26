import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Correlation Analysis",
    layout="wide"
)

st.title("📊 Correlation Analysis")

# Load Dataset
df = pd.read_csv("data/master_olist.csv")

# Select Numeric Columns
corr_columns = [
    "price",
    "freight_value",
    "payment_value"
]

corr_df = df[corr_columns]

# Correlation Matrix
correlation_matrix = corr_df.corr()

# Heatmap
st.subheader("Correlation Heatmap")

fig = px.imshow(
    correlation_matrix,
    text_auto=True,
    aspect="auto",
    title="Correlation Between Price, Freight and Payment Value",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig, use_container_width=True)

# Correlation Table
st.subheader("Correlation Matrix")

st.dataframe(
    correlation_matrix,
    use_container_width=True
)

# Insights
price_payment_corr = correlation_matrix.loc[
    "price",
    "payment_value"
]

price_freight_corr = correlation_matrix.loc[
    "price",
    "freight_value"
]

st.subheader("📌 Insights")

st.success(
    f"Payment Value and Product Price correlation: "
    f"{price_payment_corr:.2f}"
)

st.info(
    f"Price and Freight Value correlation: "
    f"{price_freight_corr:.2f}"
)

# Automated Interpretation
if price_payment_corr > 0.7:
    st.success(
        "Strong positive correlation detected between Product Price and Payment Value."
    )
elif price_payment_corr > 0.4:
    st.warning(
        "Moderate positive correlation detected between Product Price and Payment Value."
    )
else:
    st.error(
        "Weak correlation detected between Product Price and Payment Value."
    )