import streamlit as st
import pandas as pd
import plotly.express as px

from utils.styles import load_css, section_title

# PAGE CONFIG

st.set_page_config(
    page_title="Rating Analytics",
    page_icon="⭐",
    layout="wide"
)

load_css()

# LOAD DATA

if "featured_df" not in st.session_state:

    st.warning("Please upload a dataset from the Home page.")

    st.stop()

df = st.session_state.featured_df.copy()

# TITLE

section_title("⭐ Rating Analytics")

st.markdown(
    "Analyze business ratings, customer reviews and identify highly-rated businesses."
)

st.divider()

# KPI CARDS

avg_rating = round(df["Google Rating"].mean(), 2)
highest_rating = df["Google Rating"].max()
lowest_rating = df["Google Rating"].min()
high_rated = (df["High Rated"] == "Yes").sum()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("⭐ Average Rating", avg_rating)

with c2:
    st.metric("🏆 Highest Rating", highest_rating)

with c3:
    st.metric("📉 Lowest Rating", lowest_rating)

with c4:
    st.metric("🌟 High Rated Businesses", high_rated)

st.divider()

# RATING DISTRIBUTION

section_title("⭐ Rating Distribution")

fig = px.histogram(
    df,
    x="Google Rating",
    nbins=20,
    color_discrete_sequence=["#0F62FE"]
)

fig.update_layout(
    xaxis_title="Google Rating",
    yaxis_title="Number of Businesses",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# RATING VS REVIEWS

section_title("📈 Rating vs Total Reviews")

fig = px.scatter(
    df,
    x="Google Rating",
    y="Total Reviews",
    color="Rating Category",
    hover_name="Business Name",
    size="Total Reviews",
)

fig.update_layout(
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# HIGH RATED VS LOW RATED

section_title("🏅 High Rated vs Others")

rating_counts = (
    df["High Rated"]
    .value_counts()
    .rename(index={1: "High Rated", 0: "Others"})
    .reset_index()
)

rating_counts.columns = ["Category", "Businesses"]

fig = px.pie(
    rating_counts,
    names="Category",
    values="Businesses",
    hole=0.45
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

# AVERAGE RATING BY CATEGORY

section_title("🏪 Average Rating by Category")

category = (
    df.groupby("Category")["Google Rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    category,
    x="Google Rating",
    y="Category",
    orientation="h",
    text_auto=".2f",
    color="Google Rating",
)

fig.update_layout(
    template="plotly_white",
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig, use_container_width=True)

# AVERAGE RATING BY CITY

section_title("🏙 Average Rating by City")

city = (
    df.groupby("City")["Google Rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    city,
    x="City",
    y="Google Rating",
    text_auto=".2f",
    color="Google Rating"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

# TOP RATED BUSINESSES

section_title("🏆 Top Rated Businesses")

top = (
    df.sort_values(
        ["Google Rating", "Total Reviews"],
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top[
        [
            "Business Name",
            "Category",
            "City",
            "Google Rating",
            "Total Reviews",
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# KEY INSIGHTS

section_title("💡 Key Insights")

st.info(f"""
• Average business rating is **{avg_rating}**.

• **{high_rated}** businesses are classified as High Rated.

• Categories shown above have the highest average customer ratings.

• Businesses with higher review counts generally have more reliable ratings.

• Use these insights to identify well-performing business segments.
""")