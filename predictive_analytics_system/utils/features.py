import pandas as pd
import numpy as np


# CREATE FEATURES

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates additional business features.
    """

    df = df.copy()

    # Convert Numeric Columns
    numeric_cols = [
        "Google Rating",
        "Total Reviews",
        "Latitude",
        "Longitude"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Google Rating
    if "Google Rating" in df.columns:

        df["High Rated"] = np.where(
            df["Google Rating"] >= 4.5,
            "Yes",
            "No"
        )

        df["Rating Category"] = pd.cut(
            df["Google Rating"],
            bins=[0, 2, 3, 4, 4.5, 5],
            labels=[
                "Poor",
                "Average",
                "Good",
                "Very Good",
                "Excellent"
            ],
            include_lowest=True
        )

    # Total Reviews

    if "Total Reviews" in df.columns:

        df["Popular Business"] = np.where(
            df["Total Reviews"] >= 100,
            "Yes",
            "No"
        )

        df["Business Size"] = pd.cut(
            df["Total Reviews"],
            bins=[-1, 10, 50, 100, 500, 1000000],
            labels=[
                "Very Small",
                "Small",
                "Medium",
                "Large",
                "Very Large"
            ]
        )

    # Website

    if "Website" in df.columns:

        df["Website Available"] = np.where(
            df["Website"].fillna("").astype(str).str.strip() == "",
            "No",
            "Yes"
        )

    # Phone Number

    phone_columns = [
        "Phone",
        "Phone Number",
        "Contact Number"
    ]

    for col in phone_columns:

        if col in df.columns:

            df["Phone Available"] = np.where(
                df[col].fillna("").astype(str).str.strip() == "",
                "No",
                "Yes"
            )

            break

    # Coordinates

    if {"Latitude", "Longitude"}.issubset(df.columns):

        df["Coordinates Available"] = np.where(
            df["Latitude"].notna() &
            df["Longitude"].notna(),
            "Yes",
            "No"
        )

    # Business Status

    if "Business Status" in df.columns:

        df["Business Status"] = (
            df["Business Status"]
            .astype(str)
            .str.title()
        )

    # Opportunity Score

    if (
        "Google Rating" in df.columns
        and "Total Reviews" in df.columns
    ):

        df["Opportunity Score"] = (
            df["Google Rating"] * 20
            +
            np.log1p(df["Total Reviews"]) * 10
        ).round(2)

    # Missing Value Count

    df["Missing Values"] = df.isna().sum(axis=1)

    # Row ID

    df["Business ID"] = range(
        1,
        len(df) + 1
    )

    return df