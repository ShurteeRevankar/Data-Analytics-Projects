import streamlit as st
import pandas as pd


# PAGE CONFIG

st.set_page_config(
    page_title="Business Search",
    page_icon="🔍",
    layout="wide"
)

# TITLE

st.title("🔍 Business Search")

st.markdown(
    """
Search and filter businesses from your Google Maps dataset.

You can search by:

- Business Name
- Category
- City
- Area
- Rating
- Website Availability
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


# DETECT COLUMNS

def find_column(keyword):
    for col in df.columns:
        if keyword.lower() in col.lower():
            return col
    return None


name_col = find_column("business")
category_col = find_column("category")
city_col = find_column("city")
area_col = find_column("area")
rating_col = find_column("rating")
website_col = find_column("website")

# SEARCH FILTERS

st.subheader("🔎 Search Filters")

col1, col2 = st.columns(2)

with col1:
    search_text = st.text_input(
        "Search Business Name"
    )

with col2:
    rating_filter = st.slider(
        "Minimum Rating",
        0.0,
        5.0,
        0.0
    )

filtered_df = df.copy()


# BUSINESS NAME SEARCH

if search_text and name_col:

    filtered_df = filtered_df[
        filtered_df[name_col]
        .astype(str)
        .str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

# CATEGORY FILTER

if category_col:

    categories = sorted(
        df[category_col]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.multiselect(
        "Select Category",
        categories
    )

    if selected_category:

        filtered_df = filtered_df[
            filtered_df[category_col]
            .isin(selected_category)
        ]

# LOCATION FILTER

col3, col4 = st.columns(2)

with col3:
    if city_col:

        cities = sorted(
            df[city_col]
            .dropna()
            .unique()
            .tolist()
        )

        selected_city = st.multiselect(
            "Select City",
            cities
        )

        if selected_city:
            filtered_df = filtered_df[
                filtered_df[city_col]
                .isin(selected_city)
            ]


with col4:
    if area_col:
        areas = sorted(
            df[area_col]
            .dropna()
            .unique()
            .tolist()
        )

        selected_area = st.multiselect(
            "Select Area",
            areas
        )

        if selected_area:

            filtered_df = filtered_df[
                filtered_df[area_col]
                .isin(selected_area)
            ]

# RATING FILTER

if rating_col:

    filtered_df[rating_col] = pd.to_numeric(
        filtered_df[rating_col],
        errors="coerce"
    )

    filtered_df = filtered_df[
        filtered_df[rating_col] >= rating_filter
    ]


# WEBSITE FILTER

if website_col:
    website_option = st.selectbox(
        "Website Availability",
        [
            "All",
            "Available",
            "Not Available"
        ]
    )


    if website_option != "All":
        if website_option == "Available":
            filtered_df = filtered_df[
                ~filtered_df[website_col]
                .astype(str)
                .str.lower()
                .isin(
                    [
                        "no",
                        "false",
                        "nan",
                        "none"
                    ]
                )
            ]

        else:
            filtered_df = filtered_df[
                filtered_df[website_col]
                .astype(str)
                .str.lower()
                .isin(
                    [
                        "no",
                        "false",
                        "nan",
                        "none"
                    ]
                )
            ]


# RESULTS

st.divider()

st.subheader("📊 Search Results")


c1, c2 = st.columns(2)


with c1:

    st.metric(
        "Businesses Found",
        len(filtered_df)
    )


with c2:

    if rating_col:

        st.metric(
            "Average Rating",
            round(
                filtered_df[rating_col].mean(),
                2
            )
            if len(filtered_df)
            else 0
        )


st.dataframe(
    filtered_df,
    use_container_width=True
)


# BUSINESS DETAILS

st.divider()

st.subheader("🏢 View Business Details")


if len(filtered_df) > 0 and name_col:
    selected_business = st.selectbox(
        "Select Business",
        filtered_df[name_col].astype(str)
    )


    business_details = filtered_df[
        filtered_df[name_col]
        .astype(str)
        ==
        selected_business
    ]
    
    st.dataframe(
        business_details.T,
        use_container_width=True
    )

# DOWNLOAD RESULTS

st.divider()

st.subheader("📥 Download Search Results")


csv = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Results",
    data=csv,
    file_name="business_search_results.csv",
    mime="text/csv"
)