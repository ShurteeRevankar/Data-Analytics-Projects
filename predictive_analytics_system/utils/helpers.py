import pandas as pd
import numpy as np


# KPI CALCULATIONS

def calculate_kpis(df):
    """
    Calculate dashboard KPIs.
    """

    kpis = {}

    # Total Businesses
    kpis["total_businesses"] = len(df)

    # Average Rating
    if "Google Rating" in df.columns:
        kpis["average_rating"] = round(
            pd.to_numeric(df["Google Rating"], errors="coerce").mean(),
            2,
        )
    else:
        kpis["average_rating"] = 0

    # Total Reviews
    if "Total Reviews" in df.columns:
        kpis["total_reviews"] = int(
            pd.to_numeric(df["Total Reviews"], errors="coerce").fillna(0).sum()
        )
    else:
        kpis["total_reviews"] = 0

    # Website Availability
    if "Website" in df.columns:

        website = (
            df["Website"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        available = website.ne("").sum()

        kpis["website_percentage"] = round(
            available / len(df) * 100,
            2,
        )

    else:
        kpis["website_percentage"] = 0

    # High Rated Businesses
    if "Google Rating" in df.columns:

        ratings = pd.to_numeric(
            df["Google Rating"],
            errors="coerce"
        )

        kpis["high_rated"] = int(
            (ratings >= 4.5).sum()
        )

    else:

        kpis["high_rated"] = 0

    # Popular Businesses
    if "Total Reviews" in df.columns:

        reviews = pd.to_numeric(
            df["Total Reviews"],
            errors="coerce"
        )

        kpis["popular_businesses"] = int(
            (reviews >= 100).sum()
        )

    else:

        kpis["popular_businesses"] = 0

    return kpis


# TOP CATEGORIES

def top_categories(df, top_n=10):

    if "Category" not in df.columns:
        return pd.DataFrame()

    return (
        df["Category"]
        .value_counts()
        .head(top_n)
        .reset_index()
        .rename(columns={
            "index": "Category",
            "Category": "Businesses"
        })
    )


# TOP CITIES

def top_cities(df, top_n=10):

    if "City" not in df.columns:
        return pd.DataFrame()

    return (
        df["City"]
        .value_counts()
        .head(top_n)
        .reset_index()
        .rename(columns={
            "index": "City",
            "City": "Businesses"
        })
    )


# RATING DISTRIBUTION

def rating_distribution(df):

    if "Google Rating" not in df.columns:
        return pd.DataFrame()

    rating = pd.to_numeric(
        df["Google Rating"],
        errors="coerce"
    )

    return (
        rating
        .value_counts()
        .sort_index()
        .reset_index()
        .rename(columns={
            "index": "Rating",
            "Google Rating": "Count"
        })
    )


# REVIEW STATISTICS

def review_statistics(df):

    if "Total Reviews" not in df.columns:
        return {}

    reviews = pd.to_numeric(
        df["Total Reviews"],
        errors="coerce"
    )

    return {

        "Minimum": int(reviews.min()),

        "Maximum": int(reviews.max()),

        "Average": round(reviews.mean(), 2),

        "Median": round(reviews.median(), 2),

        "Total": int(reviews.sum())

    }


# WEBSITE AVAILABILITY

def website_statistics(df):

    if "Website" not in df.columns:
        return {}

    website = df["Website"].fillna("").astype(str)

    yes = website.str.strip().ne("").sum()

    no = len(df) - yes

    return {

        "Available": int(yes),

        "Not Available": int(no),

        "Percentage": round(
            yes / len(df) * 100,
            2,
        )

    }


# FILTER DATAFRAME

def filter_dataframe(df,
                     city=None,
                     category=None,
                     rating=None):

    data = df.copy()

    if city and "City" in data.columns:
        data = data[data["City"] == city]

    if category and "Category" in data.columns:
        data = data[data["Category"] == category]

    if rating and "Google Rating" in data.columns:
        data = data[
            pd.to_numeric(
                data["Google Rating"],
                errors="coerce"
            ) >= rating
        ]

    return data


# DOWNLOAD DATA

def dataframe_to_csv(df):

    return df.to_csv(index=False).encode("utf-8")


# DATASET SUMMARY

def dataset_summary(df):

    return {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Missing Values": int(df.isna().sum().sum()),

        "Duplicate Rows": int(df.duplicated().sum()),

        "Memory (MB)": round(
            df.memory_usage(deep=True).sum() / 1024**2,
            2,
        )

    }


# FORMAT LARGE NUMBERS

def format_number(number):

    if number >= 1_000_000:

        return f"{number/1_000_000:.1f}M"

    elif number >= 1_000:

        return f"{number/1_000:.1f}K"

    else:

        return str(number)