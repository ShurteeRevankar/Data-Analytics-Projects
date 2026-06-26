import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI-Powered E-Commerce BI Platform",
    page_icon="📊",
    layout="wide"
)

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Home"]
)
st.sidebar.info("💰 All monetary values are in Brazilian Real (BRL)")


# Main Page
if page == "Home":
    st.title("📊 Olist E-Commerce Dashboard")
    st.markdown("---")

    st.write("""
    Welcome to the Olist Business Intelligence Dashboard.

    This project analyzes:
    - Orders
    - Customers
    - Products
    - Payments

    Built using:
    - Python
    - Pandas
    - Streamlit
    - Power BI
    """)

    st.success("OLIST E-Commerce Analysis")