import streamlit as st
import pandas as pd
import plotly.express as px


# PAGE CONFIG

st.set_page_config(
    page_title="Opportunity Finder",
    page_icon="🎯",
    layout="wide"
)


# TITLE

st.title("🎯 Opportunity Finder")

st.markdown(
    """
Find businesses with growth opportunities using:

- ⭐ Rating performance
- 📝 Customer review volume
- 🌐 Online presence
- 📍 Location potential
- 📊 Business performance indicators
"""
)


# LOAD DATA

if (
    "featured_df" not in st.session_state
    or st.session_state.featured_df is None
):
    st.warning(
        "⚠️ Please upload and process dataset from Home page first."
    )
    st.stop()
df = st.session_state.featured_df.copy()


# CREATE OPPORTUNITY FEATURES

st.subheader("⚙️ Opportunity Calculation")


# Website column detection

website_col = None

for col in df.columns:

    if "website" in col.lower():

        website_col = col
        break


# Rating column

rating_col = None

for col in df.columns:

    if "rating" in col.lower():
        rating_col = col
        break


# Review column

review_col = None

for col in df.columns:

    if "review" in col.lower():
        review_col = col
        break


if rating_col is None or review_col is None:

    st.error(
        "Required columns (Rating / Reviews) not found."
    )
    st.stop()


# Convert numeric

df[rating_col] = pd.to_numeric(
    df[rating_col],
    errors="coerce"
)


df[review_col] = pd.to_numeric(
    df[review_col],
    errors="coerce"
)


# Fill missing

df[rating_col] = df[rating_col].fillna(0)
df[review_col] = df[review_col].fillna(0)


# OPPORTUNITY SCORE

df["Opportunity Score"] = (

    df[rating_col] * 10
    +
    (100 / (df[review_col] + 1))

)


# Website opportunity

if website_col:

    df["Website Opportunity"] = (

        df[website_col]
        .astype(str)
        .str.lower()
        .isin(
            [
                "no",
                "false",
                "nan",
                "none",
                "not available"
            ]
        )
    )
else:
    df["Website Opportunity"] = False


# Overall opportunity

df["Growth Opportunity"] = (
    (df["Opportunity Score"] > 
     df["Opportunity Score"].median())
    |
    df["Website Opportunity"]
)


# KPI CARDS

st.divider()

st.subheader("📊 Opportunity Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Total Businesses",
        len(df)
    )


with c2:

    st.metric(
        "Growth Opportunities",
        int(
            df["Growth Opportunity"].sum()
        )
    )


with c3:

    st.metric(
        "Website Opportunities",
        int(
            df["Website Opportunity"].sum()
        )
    )


with c4:

    st.metric(
        "Average Opportunity Score",
        round(
            df["Opportunity Score"].mean(),
            2
        )
    )


# FILTERS

st.divider()

st.subheader("🔎 Find Opportunities")

col1, col2 = st.columns(2)


with col1:

    min_rating = st.slider(
        "Minimum Rating",
        0.0,
        5.0,
        4.0
    )

with col2:

    min_reviews = st.slider(
        "Maximum Reviews",
        0,
        int(df[review_col].max()),
        1000
    )


opportunity_df = df[
    (df[rating_col] >= min_rating)
    &
    (df[review_col] <= min_reviews)
]


# TOP OPPORTUNITIES

st.divider()

st.subheader("🏆 Top Business Opportunities")

top_df = (
    opportunity_df
    .sort_values(
        "Opportunity Score",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_df,
    use_container_width=True
)

# VISUALIZATION

st.divider()

st.subheader("📈 Rating vs Reviews")

fig = px.scatter(
    df,
    x=review_col,
    y=rating_col,
    size="Opportunity Score",
    hover_name=df.columns[0],
    title="Businesses with Growth Potential"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# WEBSITE OPPORTUNITY

if website_col:
    st.divider()
    st.subheader(
        "🌐 Digital Presence Opportunities"
    )

    website_df = df[
        df["Website Opportunity"]
    ]

    st.write(
        f"{len(website_df)} businesses can improve by creating an online presence."
    )

    st.dataframe(
        website_df.head(20),
        use_container_width=True
    )


# DOWNLOAD

st.divider()
st.subheader("📥 Export Opportunity Report")

csv = top_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Opportunity Report",
    data=csv,
    file_name="business_opportunity_report.csv",
    mime="text/csv"
)