import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Category Analysis",
    layout="wide"
)

st.title("📦 Product Category Analysis")

# Load Dataset
if "df" not in st.session_state:
    st.warning("Please upload the dataset from the Data Upload page first.")
    st.stop()

df = st.session_state["df"]


# Sidebar Filter
st.sidebar.header("Category Filters")

selected_categories = st.sidebar.multiselect(
    "Select Category",
    sorted(df["product_category_name"].dropna().unique())
)


category_translation = {
    "cama_mesa_banho": "Bed, Bath & Home",
    "beleza_saude": "Beauty & Health",
    "informatica_acessorios": "Computers & Accessories",
    "moveis_decoracao": "Furniture & Decor",
    "relogios_presentes": "Watches & Gifts",
    "esporte_lazer": "Sports & Leisure",
    "utilidades_domesticas": "Home & Kitchen",
    "automotivo": "Automotive",
    "ferramentas_jardim": "Garden & Tools",
    "cool_stuff": "Lifestyle Products"
}

df["product_category_name"] = (
    df["product_category_name"]
    .replace(category_translation)
)


st.caption(
    "Product categories translated from Portuguese to English for readability."
)

# Create Filtered Dataset
filtered_df = df.copy()

# Apply Filter
if selected_categories:
    filtered_df = filtered_df[
        filtered_df["product_category_name"].isin(selected_categories)
    ]

    

# Category Revenue Analysis
category_sales = (
    filtered_df.groupby("product_category_name")["payment_value"]
    .sum()
    .reset_index()
)

# Remove Null Categories
category_sales = category_sales.dropna()

# Top 10 Categories
top_categories = (
    category_sales
    .sort_values("payment_value", ascending=False)
    .head(10)
)

# Bar Chart
st.subheader("Top 10 Revenue Generating Categories")

fig = px.bar(
    top_categories,
    x="payment_value",
    y="product_category_name",
    orientation="h",
    title="Top 10 Categories by Revenue",
    labels={
        "payment_value": "Revenue",
        "product_category_name": "Category"
    }
)

fig.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig, use_container_width=True)

# Category Table
st.subheader("Top Categories Table")
st.dataframe(top_categories, use_container_width=True)

# Insights
highest_category = category_sales.loc[
    category_sales["payment_value"].idxmax()
]

lowest_category = category_sales.loc[
    category_sales["payment_value"].idxmin()
]

st.subheader("Insights")

st.success(
    f"🏆 Highest Revenue Category: "
    f"{highest_category['product_category_name']} "
    f"(R$ {highest_category['payment_value']:,.2f})"
)

st.warning(
    f"📉 Lowest Revenue Category: "
    f"{lowest_category['product_category_name']} "
    f"(R$ {lowest_category['payment_value']:,.2f})"
)