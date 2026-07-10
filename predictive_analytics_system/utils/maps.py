import pandas as pd
import plotly.express as px

# PREPARE MAP DATA

def prepare_map_data(df):
    """
    Prepare dataframe for mapping.
    """
    
    map_df = df.copy()

    if "Latitude" not in map_df.columns or "Longitude" not in map_df.columns:
        return pd.DataFrame()

    map_df["Latitude"] = pd.to_numeric(
        map_df["Latitude"],
        errors="coerce"
    )

    map_df["Longitude"] = pd.to_numeric(
        map_df["Longitude"],
        errors="coerce"
    )

    map_df = map_df.dropna(
        subset=["Latitude", "Longitude"]
    )

    return map_df

# BUSINESS LOCATION MAP

def business_location_map(df):
    """
    Scatter map of businesses.
    """

    df = prepare_map_data(df)

    if df.empty:
        return None

    hover = []

    for col in [
        "Business Name",
        "Category",
        "Google Rating",
        "Total Reviews",
        "City"
    ]:
        if col in df.columns:
            hover.append(col)

    fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Business Name" if "Business Name" in df.columns else None,
        hover_data=hover,
        color="Google Rating" if "Google Rating" in df.columns else None,
        zoom=9,
        height=600,
    )

    fig.update_layout(
        map_style="open-street-map",
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig


# DENSITY MAP

def density_map(df):
    """
    Density heat map.
    """

    df = prepare_map_data(df)

    if df.empty:
        return None

    fig = px.density_map(
        df,
        lat="Latitude",
        lon="Longitude",
        z="Google Rating" if "Google Rating" in df.columns else None,
        radius=15,
        zoom=9,
        height=600,
    )

    fig.update_layout(
        map_style="open-street-map",
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig

# CATEGORY MAP

def category_map(df):
    """
    Color businesses by category.
    """

    df = prepare_map_data(df)

    if df.empty:
        return None

    if "Category" not in df.columns:
        return business_location_map(df)

    hover = []

    for col in [
        "Business Name",
        "Category",
        "Google Rating",
        "Total Reviews",
    ]:
        if col in df.columns:
            hover.append(col)

    fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Category",
        hover_name="Business Name",
        hover_data=hover,
        zoom=9,
        height=600,
    )

    fig.update_layout(
        map_style="carto-positron",
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig


# RATING MAP

def rating_map(df):
    """
    Bubble map by rating.
    """

    df = prepare_map_data(df)

    if df.empty:
        return None

    fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Google Rating",
        size="Total Reviews" if "Total Reviews" in df.columns else None,
        hover_name="Business Name",
        zoom=9,
        height=600,
    )

    fig.update_layout(
        map_style="carto-positron",
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig


# CITY FILTER

def filter_city(df, city):
    """
    Filter dataframe by city.
    """

    if city == "All":
        return df

    if "City" not in df.columns:
        return df

    return df[df["City"] == city]


# CATEGORY FILTER

def filter_category(df, category):
    """
    Filter dataframe by category.
    """

    if category == "All":
        return df

    if "Category" not in df.columns:
        return df

    return df[df["Category"] == category]


# AVAILABLE CITIES

def get_cities(df):

    if "City" not in df.columns:
        return ["All"]

    cities = sorted(df["City"].dropna().unique())

    return ["All"] + list(cities)


# AVAILABLE CATEGORIES

def get_categories(df):

    if "Category" not in df.columns:
        return ["All"]

    categories = sorted(df["Category"].dropna().unique())

    return ["All"] + list(categories)