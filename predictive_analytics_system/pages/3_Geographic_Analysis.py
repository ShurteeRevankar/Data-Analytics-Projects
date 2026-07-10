import streamlit as st
import pandas as pd
import plotly.express as px

from utils.styles import load_css, section_title

# PAGE CONFIG

st.set_page_config(
    page_title="Geographic Analysis",
    page_icon="🌍",
    layout="wide"
)

load_css()

# LOAD DATA

if "featured_df" not in st.session_state:
    st.warning("⚠ Please upload a dataset from the Home page.")
    st.stop()

df = st.session_state.featured_df.copy()

# FILTER VALID COORDINATES

df = df.dropna(subset=["Latitude", "Longitude"])

# PAGE TITLE

section_title("🌍 Geographic Analysis")

st.write(
    "Explore business distribution across cities and locations."
)
st.divider()

# KPI CARDS

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Businesses", len(df))

with k2:
    st.metric("Cities", df["City"].nunique())

with k3:
    st.metric("Areas", df["Area/Locality"].nunique())

with k4:
    if "Coordinates Available" in df.columns:
        coordinates = (df["Coordinates Available"] == "Yes").sum()
    else:
        coordinates = len(df)

    st.metric(
        "📍 Coordinates Available",
        coordinates
    )

st.divider()

# INTERACTIVE MAP

section_title("📍 Business Locations")

fig = px.scatter_map(
    df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Business Name",
    hover_data=[
        "Category",
        "City",
        "Google Rating",
        "Total Reviews"
    ],
    color="Google Rating",
    zoom=8,
    height=600
)

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# BUSINESSES BY CITY

col1, col2 = st.columns(2)

with col1:
    section_title("🏙 Businesses by City")
    city = (
        df["City"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    city.columns = ["City", "Businesses"]

    fig = px.bar(
        city,
        x="City",
        y="Businesses",
        text="Businesses",
        color="Businesses"
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:
    section_title("📌 Businesses by Area")
    area = (
        df["Area/Locality"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    area.columns = ["Area", "Businesses"]

    fig = px.bar(
        area,
        x="Area",
        y="Businesses",
        text="Businesses",
        color="Businesses"
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# TOP LOCATIONS

section_title("⭐ Top Business Locations")

top_locations = (
    df.groupby("City")
      .agg(
          Businesses=("Business Name", "count"),
          Average_Rating=("Google Rating", "mean"),
          Total_Reviews=("Total Reviews", "sum")
      )
      .sort_values(
          "Businesses",
          ascending=False
      )
      .reset_index()
)

st.dataframe(
    top_locations,
    use_container_width=True,
    hide_index=True
)

st.divider()

# HEATMAP

section_title("🔥 Business Density Map")

heat = px.density_map(
    df,
    lat="Latitude",
    lon="Longitude",
    z=None,
    radius=18,
    zoom=8,
    height=600
)

heat.update_layout(
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(
    heat,
    use_container_width=True
)

st.divider()

# KEY INSIGHTS

section_title("💡 Key Insights")

c1, c2 = st.columns(2)

with c1:

    st.info(f"""
**Top City**

{city.iloc[0]['City']}

Businesses: **{city.iloc[0]['Businesses']}**
""")

with c2:

    st.info(f"""
**Top Area**

{area.iloc[0]['Area']}

Businesses: **{area.iloc[0]['Businesses']}**
""")