import pandas as pd


REQUIRED_COLUMNS = [
    "Business Name",
    "Category",
    "Google Rating",
    "Total Reviews"
]


# VALIDATE DATASET

def validate_dataset(df: pd.DataFrame):
    """
    Validate uploaded dataset.

    Returns
    -------
    dict
    """

    available_columns = list(df.columns)

    missing_columns = [
        col
        for col in REQUIRED_COLUMNS
        if col not in available_columns
    ]

    return {
        "valid": len(missing_columns) == 0,
        "missing_columns": missing_columns,
        "available_columns": available_columns,
        "total_rows": df.shape[0],
        "total_columns": df.shape[1]
    }


# CHECK REQUIRED COLUMNS

def has_required_columns(df):
    """
    Returns True if all required columns exist.
    """

    return all(col in df.columns for col in REQUIRED_COLUMNS)


# DUPLICATE ROWS

def duplicate_rows(df):
    """
    Returns duplicate row count.
    """

    return int(df.duplicated().sum())


# MISSING VALUE SUMMARY

def missing_values(df):
    """
    Missing value summary.
    """

    summary = pd.DataFrame({

        "Column": df.columns,

        "Missing Values": df.isna().sum().values,

        "Missing Percentage": (
            df.isna().mean() * 100
        ).round(2).values

    })

    return summary.sort_values(
        by="Missing Percentage",
        ascending=False
    )


# NUMERIC COLUMNS

def numeric_columns(df):
    """
    Returns numeric columns.
    """

    return df.select_dtypes(
        include=["number"]
    ).columns.tolist()


# CATEGORICAL COLUMNS

def categorical_columns(df):
    """
    Returns categorical columns.
    """

    return df.select_dtypes(
        include=["object", "string", "category"]
    ).columns.tolist()


# DATASET INFORMATION

def dataset_information(df):
    """
    Returns dataset information.
    """

    memory = round(
        df.memory_usage(deep=True).sum() /
        (1024 * 1024),
        2
    )

    return {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Duplicates": duplicate_rows(df),

        "Missing Values": int(df.isna().sum().sum()),

        "Memory (MB)": memory

    }


# CHECK DATASET READY

def dataset_ready(df):
    """
    Check whether dataset is ready for analysis.
    """

    validation = validate_dataset(df)

    if not validation["valid"]:
        return False

    if duplicate_rows(df) > 0:
        return False

    return True


# VALIDATE NUMERIC COLUMNS

def validate_numeric_columns(df):
    """
    Convert important numeric columns safely.
    """

    numeric_cols = [

        "Google Rating",

        "Total Reviews",

        "Latitude",

        "Longitude"

    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


# VALIDATE TEXT COLUMNS

def validate_text_columns(df):
    """
    Clean text columns.
    """

    text_cols = [
        "Business Name",
        "Category",
        "City",
        "Area/Locality",
        "Business Status"
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )
    return df


# COMPLETE VALIDATION

def run_validation(df):
    """
    Runs all validations.
    """

    df = validate_numeric_columns(df)
    df = validate_text_columns(df)
    validation = validate_dataset(df)

    return {
        "validation": validation,
        "dataset_info": dataset_information(df),
        "missing_summary": missing_values(df),
        "numeric_columns": numeric_columns(df),
        "categorical_columns": categorical_columns(df)
    }