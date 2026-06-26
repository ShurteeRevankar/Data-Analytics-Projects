import streamlit as st

# ==========================
# Page Configuration
# ==========================

st.set_page_config(
    page_title="AI-Powered E-Commerce BI Platform",
    page_icon="📊",
    layout="wide"
)

# ==========================
# Home Page
# ==========================

st.title("📊 Olist E-Commerce Dashboard")

st.markdown("---")

st.write("""
Welcome to the **Olist Business Intelligence Dashboard**.

This project analyzes:
- 📦 Orders
- 👥 Customers
- 🛒 Products
- 💳 Payments
- 🚚 Deliveries
- 🗺️ States

### Built Using
- Python
- Pandas
- Plotly
- Streamlit
- Power BI
""")

st.success("✅ OLIST E-Commerce Analysis")

st.info(
    """
    📂 **Before exploring the dashboard:**

    1. Open **Data Upload** from the left sidebar.
    2. Upload **master_olist.csv**.
    3. Navigate through the remaining analysis pages.
    """
)

st.sidebar.info("💰 All monetary values are in Brazilian Real (BRL)")