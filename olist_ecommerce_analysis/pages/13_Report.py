import streamlit as st
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="Report Generator",
    layout="wide"
)

st.title("📄 Business Report Generator")

# Load Dataset
df = pd.read_csv("data/master_olist.csv")

# ============================
# KPI Calculations
# ============================

revenue = df["payment_value"].sum()
orders = df["order_id"].nunique()
customers = df["customer_unique_id"].nunique()
avg_order_value = revenue / orders

# ============================
# Top State
# ============================

top_state = (
    df.groupby("customer_state")["payment_value"]
    .sum()
    .idxmax()
)

# ============================
# Top Category
# ============================

top_category = (
    df.groupby("product_category_name")["payment_value"]
    .sum()
    .idxmax()
)

# ============================
# Payment Method
# ============================

popular_payment = df["payment_type"].mode()[0]

# ============================
# Delivery Time
# ============================

df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

df["order_delivered_customer_date"] = pd.to_datetime(
    df["order_delivered_customer_date"]
)

df["delivery_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.days

avg_delivery = round(
    df["delivery_days"].mean(),
    2
)

# ============================
# Generate PDF
# ============================

def generate_pdf():

    pdf_file = "Olist_Business_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Olist Business Intelligence Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "Executive Summary",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            "This report summarizes key business performance metrics and insights from the Olist E-Commerce dataset.",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            "KPIs",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Revenue: R$ {revenue:,.2f}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Orders: {orders:,}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Customers: {customers:,}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Average Order Value: R$ {avg_order_value:,.2f}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            "Sales Analysis",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            "Sales performance shows strong revenue generation across multiple states and product categories.",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            "Category Analysis",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Top Revenue Category: {top_category}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            "State Analysis",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Top Revenue State: {top_state}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            "Insights",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Most customers prefer {popular_payment.title()} payments.",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Average delivery time is {avg_delivery} days.",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            "Recommendations",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            "1. Focus marketing efforts on top-performing states.<br/>"
            "2. Increase inventory for best-selling categories.<br/>"
            "3. Promote digital payment adoption.<br/>"
            "4. Improve logistics to reduce delivery time.",
            styles["BodyText"]
        )
    )

    doc.build(content)

    return pdf_file

# ============================
# Generate Report Button
# ============================

if st.button("Generate PDF Report"):

    pdf_path = generate_pdf()

    with open(pdf_path, "rb") as pdf_file:

        st.download_button(
            label="⬇️ Download Report",
            data=pdf_file,
            file_name="Olist_Business_Report.pdf",
            mime="application/pdf"
        )

    st.success("Report generated successfully!")