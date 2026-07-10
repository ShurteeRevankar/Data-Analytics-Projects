import streamlit as st
import pandas as pd
import plotly.express as px

from utils.styles import load_css, section_title
from utils.helpers import calculate_kpis

# PAGE CONFIG

st.set_page_config(
    page_title="Business Overview",
    page_icon="📊",
    layout="wide"
)

load_css()

# LOAD DATA

if "featured_df" not in st.session_state:
    st.warning("⚠ Please upload a dataset from the Home page.")
    st.stop()
    
df = st.session_state.featured_df

# PAGE TITLE

section_title("📊 Business Overview")
st.caption(
    "Overall summary of the uploaded Google Maps Business dataset."
)
st.divider()


# KPI CARDS

kpi = calculate_kpis(df)
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(
        "🏢 Businesses",
        f"{kpi['total_businesses']:,}"
    )

with c2:
    st.metric(
        "⭐ Avg Rating",
        kpi["average_rating"]
    )

with c3:
    st.metric(
        "📝 Reviews",
        f"{kpi['total_reviews']:,}"
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "🌐 Website %",
        f"{kpi['website_percentage']}%"
    )

with c5:
    st.metric(
        "🏆 High Rated",
        kpi["high_rated"]
    )

with c6:
    st.metric(
        "🔥 Popular",
        kpi["popular_businesses"]
    )

st.divider()


# CATEGORY & AREA / LOCALITY

left, right = st.columns(2)

# TOP CATEGORIES

with left:

    section_title("🏪 Top Categories")

    category = (
        df["Category"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    category.columns = ["Category", "Businesses"]

    fig = px.bar(
        category,
        x="Businesses",
        y="Category",
        orientation="h",
        color="Businesses",
        text="Businesses",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        height=420,
        xaxis_title="Number of Businesses",
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# TOP AREAS / LOCALITIES

with right:

    section_title("📍 Top Areas / Localities")

    locality = (
        df["Area/Locality"]
        .fillna("Unknown")
        .value_counts()
        .head(10)
        .reset_index()
    )

    locality.columns = ["Area/Locality", "Businesses"]

    fig = px.bar(
        locality,
        x="Businesses",
        y="Area/Locality",
        orientation="h",
        color="Businesses",
        text="Businesses",
        color_continuous_scale="Greens"
    )

    fig.update_layout(
        height=420,
        xaxis_title="Number of Businesses",
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# BUSINESS STATUS & WEBSITE

left, right = st.columns(2)

with left:

    section_title("🏢 Business Status")

    status = (
        df["Business Status"]
        .value_counts()
        .reset_index()
    )

    status.columns = ["Status", "Count"]

    fig = px.pie(
        status,
        names="Status",
        values="Count",
        hole=0.55
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    section_title("🌐 Website Availability")

    website = (
        df["Has Website"]
        .value_counts()
        .reset_index()
    )

    website.columns = ["Website", "Count"]

    fig = px.pie(
        website,
        names="Website",
        values="Count",
        hole=0.55
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# TOP BUSINESSES

section_title("🏆 Top 10 Businesses")

top = (
    df
    .sort_values(
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
            "Business Status"
        ]
    ],

    use_container_width=True,
    hide_index=True

)

st.divider()

st.caption(
    "Business Overview • Google Maps Business Analytics Dashboard"
)