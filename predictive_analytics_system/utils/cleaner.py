"""
utils/cleaner.py

Cleaning functions for Google Maps Business Analytics Dashboard
"""

import pandas as pd
import numpy as np

# REMOVE DUPLICATES

def remove_duplicates(df):
    """
    Remove duplicate rows.
    """
    return df.drop_duplicates().reset_index(drop=True)

# CONVERT NUMERIC COLUMNS

def convert_numeric_columns(df):
    """
    Convert known numeric columns safely.
    """

    numeric_columns = [
        "Google Rating",
        "Total Reviews",
        "Latitude",
        "Longitude",
        "Pincode"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df

# CLEAN TEXT COLUMNS

def clean_text_columns(df):
    """
    Clean all object/string columns.
    """

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for col in text_columns:

        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    return df

# FILL MISSING VALUES

def fill_missing_values(df):
    """
    Fill missing values according to data type.
    """

    for column in df.columns:
        # Numeric Columns
        if pd.api.types.is_numeric_dtype(df[column]):
            median = df[column].median()
            df[column] = df[column].fillna(median)
        # Text Columns
        else:
            mode = df[column].mode()
            if not mode.empty:
                df[column] = df[column].fillna(mode.iloc[0])
            else:
                df[column] = df[column].fillna("Unknown")
    return df

# CLEAN RATINGS

def clean_ratings(df):
    if "Google Rating" in df.columns:
        df["Google Rating"] = (
            df["Google Rating"]
            .clip(lower=0, upper=5)
        )
    return df


# CLEAN REVIEWS

def clean_reviews(df):
    if "Total Reviews" in df.columns:
        df["Total Reviews"] = (
            df["Total Reviews"]
            .clip(lower=0)
        )
    return df

# CLEAN COORDINATES

def clean_coordinates(df):
    if "Latitude" in df.columns:
        df = df[
            df["Latitude"].between(-90, 90)
            | df["Latitude"].isna()
        ]

    if "Longitude" in df.columns:
        df = df[
            df["Longitude"].between(-180, 180)
            | df["Longitude"].isna()
        ]

    return df.reset_index(drop=True)


# STANDARDIZE BUSINESS STATUS

def clean_business_status(df):
    
    if "Business Status" in df.columns:
        df["Business Status"] = (
            df["Business Status"]
            .str.title()
        )
    return df


# REMOVE EMPTY BUSINESS NAMES

def remove_empty_businesses(df):

    if "Business Name" in df.columns:
        df = df[
            df["Business Name"].str.strip() != ""
        ]
    return df.reset_index(drop=True)


# MAIN CLEANING FUNCTION

def clean_dataset(df):
    """
    Complete cleaning pipeline.
    """
    df = df.copy()
    
    # Remove duplicates
    df = remove_duplicates(df)

    # Convert numeric columns
    df = convert_numeric_columns(df)

    # Clean text
    df = clean_text_columns(df)

    # Fill missing values
    df = fill_missing_values(df)

    # Ratings
    df = clean_ratings(df)

    # Reviews
    df = clean_reviews(df)

    # Coordinates
    df = clean_coordinates(df)

    # Business Status
    df = clean_business_status(df)

    # Remove empty businesses
    df = remove_empty_businesses(df)

    return df