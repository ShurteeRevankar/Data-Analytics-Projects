import streamlit as st
import pandas as pd
from pathlib import Path


# Path to the dataset
DATA_PATH = Path("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")


@st.cache_data
def load_data():
    """
    Load the HR Analytics dataset.
    The dataset is cached for better performance.
    """

    try:
        df = pd.read_csv(DATA_PATH)
        return df

    except FileNotFoundError:
        st.error(f"Dataset not found!\nExpected location:\n{DATA_PATH}")
        return pd.DataFrame()

    except Exception as e:
        st.error(f"Error loading dataset:\n{e}")
        return pd.DataFrame()


def get_basic_info(df):
    """Return dataset information."""

    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": df.isnull().sum().sum(),
        "Duplicate Rows": df.duplicated().sum()
    }


def get_numerical_columns(df):
    """Return numerical columns."""

    return df.select_dtypes(include=["number"]).columns.tolist()


def get_categorical_columns(df):
    """Return categorical columns."""

    return df.select_dtypes(include=["object"]).columns.tolist()