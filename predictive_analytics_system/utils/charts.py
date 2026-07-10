import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# BAR CHART

def bar_chart(
    df,
    x,
    y,
    title="",
    color=None,
    orientation="v"
):

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        orientation=orientation,
        title=title,
        template="plotly_white"
    )

    fig.update_layout(
        height=450,
        title_x=0.5
    )

    return fig


# PIE CHART

def pie_chart(
    df,
    names,
    values,
    title=""
):

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.45,
        title=title
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        height=450
    )

    return fig


# HISTOGRAM

def histogram(
    df,
    column,
    title=""
):

    fig = px.histogram(
        df,
        x=column,
        nbins=20,
        title=title,
        template="plotly_white"
    )

    fig.update_layout(
        title_x=0.5,
        height=450
    )

    return fig


# SCATTER PLOT

def scatter_chart(
    df,
    x,
    y,
    color=None,
    size=None,
    title=""
):

    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        title=title,
        template="plotly_white"
    )

    fig.update_layout(
        title_x=0.5,
        height=500
    )

    return fig


# BOX PLOT

def box_plot(
    df,
    x,
    y,
    title=""
):

    fig = px.box(
        df,
        x=x,
        y=y,
        title=title,
        template="plotly_white"
    )

    fig.update_layout(
        title_x=0.5,
        height=450
    )

    return fig


# LINE CHART

def line_chart(
    df,
    x,
    y,
    color=None,
    title=""
):

    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        markers=True,
        title=title,
        template="plotly_white"
    )

    fig.update_layout(
        title_x=0.5,
        height=450
    )

    return fig


# CORRELATION HEATMAP

def correlation_heatmap(df):

    numeric = df.select_dtypes(include="number")

    corr = numeric.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Blues",
        title="Correlation Heatmap"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        height=600
    )

    return fig


# TOP CATEGORIES

def top_categories(
    df,
    column,
    top_n=10
):

    temp = (
        df[column]
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    temp.columns = [column, "Count"]

    return bar_chart(
        temp,
        x=column,
        y="Count",
        title=f"Top {top_n} {column}"
    )


# RATING DISTRIBUTION

def rating_distribution(df):

    temp = (
        df["Google Rating"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    temp.columns = ["Rating", "Count"]

    return bar_chart(
        temp,
        x="Rating",
        y="Count",
        title="Google Rating Distribution"
    )


# WEBSITE AVAILABILITY

def website_availability(df):

    if "Website Available" not in df.columns:
        return None

    temp = (
        df["Website Available"]
        .value_counts()
        .reset_index()
    )

    temp.columns = ["Website", "Count"]

    return pie_chart(
        temp,
        names="Website",
        values="Count",
        title="Website Availability"
    )


# BUSINESS STATUS

def business_status(df):

    if "Business Status" not in df.columns:
        return None

    temp = (
        df["Business Status"]
        .value_counts()
        .reset_index()
    )

    temp.columns = ["Status", "Count"]

    return pie_chart(
        temp,
        names="Status",
        values="Count",
        title="Business Status"
    )


# REVIEWS VS RATING

def reviews_vs_rating(df):

    return scatter_chart(
        df,
        x="Total Reviews",
        y="Google Rating",
        color="Category",
        title="Reviews vs Google Rating"
    )


# MAP SCATTER

def business_map(df):

    if "Latitude" not in df.columns:
        return None

    if "Longitude" not in df.columns:
        return None

    fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Business Name",
        hover_data=[
            "Category",
            "Google Rating"
        ],
        zoom=9,
        height=600
    )

    fig.update_layout(
        map_style="open-street-map",
        margin=dict(
            l=0,
            r=0,
            t=40,
            b=0
        )
    )

    return fig