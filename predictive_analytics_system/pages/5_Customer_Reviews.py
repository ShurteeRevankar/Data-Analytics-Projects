# CUSTOMER REVIEWS

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.styles import load_css, section_title

# PAGE CONFIG

st.set_page_config(
    page_title="Customer Reviews",
    page_icon="📝",
    layout="wide"
)

load_css()

# LOAD DATA

if "featured_df" not in st.session_state:
    st.warning("⚠ Please upload and process a dataset from the Home page.")
    st.stop()

df = st.session_state.featured_df

# PAGE TITLE

section_title("📝 Customer Reviews")

st.markdown(
    "Analyze customer review patterns, review distribution, and businesses with the highest and lowest engagement."
)

st.divider()

# KPI CARDS

total_reviews = int(df["Total Reviews"].sum())
avg_reviews = round(df["Total Reviews"].mean(), 1)
max_reviews = int(df["Total Reviews"].max())
review_groups = df["Review Group"].nunique()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("📝 Total Reviews", f"{total_reviews:,}")

with c2:
    st.metric("📊 Average Reviews", avg_reviews)

with c3:
    st.metric("🏆 Highest Reviews", f"{max_reviews:,}")

with c4:
    st.metric("📂 Review Groups", review_groups)

st.divider()

# REVIEW DISTRIBUTION

col1, col2 = st.columns(2)

with col1:

    section_title("📈 Review Distribution")

    fig = px.histogram(
        df,
        x="Total Reviews",
        nbins=25,
        title="Distribution of Customer Reviews"
    )

    fig.update_layout(height=400)

    st.plotly_chart(fig, use_container_width=True)

with col2:

    section_title("📊 Review Groups")

    review_group = (
        df["Review Group"]
        .value_counts()
        .reset_index()
    )

    review_group.columns = ["Review Group", "Businesses"]

    fig = px.pie(
        review_group,
        names="Review Group",
        values="Businesses",
        hole=0.45
    )

    fig.update_layout(height=400)

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# REVIEWS BY CATEGORY

section_title("🏪 Reviews by Category")

category_reviews = (
    df.groupby("Category")["Total Reviews"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    category_reviews,
    x="Category",
    y="Total Reviews",
    color="Total Reviews",
    text="Total Reviews"
)

fig.update_layout(
    xaxis_title="Category",
    yaxis_title="Total Reviews",
    height=450
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# MOST REVIEWED BUSINESSES

section_title("🏆 Top 10 Most Reviewed Businesses")

top_reviews = (
    df.sort_values(
        "Total Reviews",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_reviews[
        [
            "Business Name",
            "Category",
            "City",
            "Google Rating",
            "Total Reviews",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

st.divider()

# LEAST REVIEWED BUSINESSES

section_title("📉 Least Reviewed Businesses")

least_reviews = (
    df.sort_values(
        "Total Reviews",
        ascending=True
    )
    .head(10)
)

st.dataframe(
    least_reviews[
        [
            "Business Name",
            "Category",
            "City",
            "Google Rating",
            "Total Reviews",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

st.divider()

# KEY INSIGHTS

section_title("💡 Key Insights")

st.info(f"""
• Total customer reviews collected: **{total_reviews:,}**
• Average reviews per business: **{avg_reviews}**
• Business with the highest engagement has **{max_reviews:,} reviews**
• Businesses are classified into **{review_groups} review groups**, making it easier to identify high- and low-engagement businesses.
""")