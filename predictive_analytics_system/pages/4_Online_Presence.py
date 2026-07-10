import streamlit as st
import pandas as pd
import plotly.express as px

from utils.styles import load_css, section_title

# PAGE CONFIG

st.set_page_config(
    page_title="Online Presence",
    page_icon="💻",
    layout="wide"
)

load_css()

# LOAD DATA

if "featured_df" not in st.session_state:
    st.warning("Please upload and process a dataset from the Home page.")
    st.stop()

df = st.session_state.featured_df


# PAGE TITLE

section_title("💻 Online Presence")

st.markdown(
    """
Analyze the online presence of businesses based on
website availability, ratings and customer reviews.
"""
)

st.divider()

# KPI CARDS

total_businesses = len(df)
website_count = df["Has Website"].sum()
no_website = total_businesses - website_count
website_percentage = round((website_count / total_businesses) * 100, 2)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Businesses", total_businesses)

with col2:
    st.metric("Has Website", website_count)

with col3:
    st.metric("No Website", no_website)

with col4:
    st.metric("Website Availability", f"{website_percentage}%")

st.divider()

# WEBSITE DISTRIBUTION

col1, col2 = st.columns(2)

with col1:

    section_title("🌐 Website Availability")

    website_df = (
        df["Website Available"]
        .value_counts()
        .reset_index()
    )

    website_df.columns = ["Website", "Count"]

    fig = px.pie(
        website_df,
        names="Website",
        values="Count",
        hole=0.45
    )

    st.plotly_chart(fig, use_container_width=True)

# WEBSITE VS NO WEBSITE

with col2:

    section_title("📊 Website Comparison")

    compare = pd.DataFrame({
        "Status": ["Has Website", "No Website"],
        "Businesses": [website_count, no_website]
    })

    fig = px.bar(
        compare,
        x="Status",
        y="Businesses",
        color="Status",
        text="Businesses"
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# RATING COMPARISON

section_title("⭐ Average Rating Comparison")

rating_df = (
    df.groupby("Website Available")["Google Rating"]
    .mean()
    .reset_index()
)

fig = px.bar(
    rating_df,
    x="Website Available",
    y="Google Rating",
    color="Website Available",
    text_auto=".2f"
)

fig.update_layout(
    xaxis_title="",
    yaxis_title="Average Rating",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# REVIEW COMPARISON

section_title("📝 Average Reviews Comparison")

review_df = (
    df.groupby("Website Available")["Total Reviews"]
    .mean()
    .reset_index()
)

fig = px.bar(
    review_df,
    x="Website Available",
    y="Total Reviews",
    color="Website Available",
    text_auto=".0f"
)

fig.update_layout(
    xaxis_title="",
    yaxis_title="Average Reviews",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# CATEGORIES WITHOUT WEBSITE

section_title("🚫 Categories Lacking Websites")

no_site = (
    df[df["Has Website"] == 0]
    .groupby("Category")
    .size()
    .reset_index(name="Businesses")
    .sort_values("Businesses", ascending=False)
    .head(10)
)

fig = px.bar(
    no_site,
    x="Category",
    y="Businesses",
    color="Businesses",
    text="Businesses"
)

fig.update_layout(
    xaxis_title="Category",
    yaxis_title="Businesses"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# BUSINESSES WITHOUT WEBSITE

section_title("📋 Top Businesses Without Website")

display_df = (
    df[df["Has Website"] == 0]
    [
        [
            "Business Name",
            "Category",
            "City",
            "Google Rating",
            "Total Reviews"
        ]
    ]
    .sort_values(
        ["Google Rating", "Total Reviews"],
        ascending=False
    )
    .head(15)
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# KEY INSIGHTS

section_title("💡 Key Insights")

st.info(f"""
• **{website_percentage}%** of businesses have a website.
• **{no_website} businesses** do not have an online website.
• Businesses with websites generally receive better customer engagement.
• Categories shown above present the greatest opportunity for improving online presence.
""")