import os
import pandas as pd
import streamlit as st

# SAMPLE DATASET PATH

SAMPLE_DATASET = "data/sample_google_maps.csv"

# LOAD UPLOADED DATASET

def load_dataset(uploaded_file):
    """
    Load CSV or Excel dataset.
    """
    
    if uploaded_file is None:
        return None
    try:
        file_name = uploaded_file.name.lower()
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:

            st.error("Unsupported file format.")
            return None
        return df

    except Exception as e:
        st.error(f"Error loading dataset:\n{e}")
        return None


# LOAD SAMPLE DATASET

def load_sample_dataset():
    """
    Loads the sample dataset stored inside data folder.
    """
    try:
        if os.path.exists(SAMPLE_DATASET):
            return pd.read_csv(SAMPLE_DATASET)
        st.warning("Sample dataset not found.")
        return None
    except Exception as e:
        st.error(f"Unable to load sample dataset.\n{e}")
        return None


# FILE INFORMATION

def get_file_information(df):
    """
    Returns dataset information.
    """
    memory = round(
        df.memory_usage(deep=True).sum() / 1024 / 1024,
        2,
    )
    info = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "memory": f"{memory} MB",
        "duplicates": int(df.duplicated().sum())
    }

    return info


# COLUMN INFORMATION

def get_column_information(df):
    """
    Returns information about every column.
    """
    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isna().sum().values,
        "Unique Values": df.nunique().values
    })
    return column_info


# NUMERIC COLUMNS

def get_numeric_columns(df):
    """
    Returns numeric columns.
    """
    return df.select_dtypes(include=["number"]).columns.tolist()


# CATEGORICAL COLUMNS

def get_categorical_columns(df):
    """
    Returns categorical columns.
    """

    return df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


# DATA PREVIEW

def preview_dataset(df, rows=10):
    """
    Returns first few rows.
    """

    return df.head(rows)


# MISSING VALUE SUMMARY

def missing_summary(df):
    """
    Returns missing value summary.
    """
    summary = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isna().sum(),
        "Missing %": (
            df.isna().sum() / len(df) * 100
        ).round(2)

    })

    return summary.sort_values(
        "Missing %",
        ascending=False
    )


# DOWNLOAD DATAFRAME

def dataframe_to_csv(df):
    """
    Converts dataframe to CSV bytes.
    """

    return df.to_csv(
        index=False
    ).encode("utf-8")


# DOWNLOAD BUTTON

def download_dataset(df, filename="cleaned_dataset.csv"):
    """
    Creates a Streamlit download button.
    """

    st.download_button(
        label="📥 Download Cleaned Dataset",
        data=dataframe_to_csv(df),
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )


# DATASET SUMMARY

def dataset_summary(df):
    """
    Returns overall dataset summary.
    """

    summary = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isna().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Numeric Columns": len(
            get_numeric_columns(df)
        ),
        "Categorical Columns": len(
            get_categorical_columns(df)
        )
    }
    return summary