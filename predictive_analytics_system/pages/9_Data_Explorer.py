import streamlit as st
import pandas as pd


# PAGE CONFIG

st.set_page_config(
    page_title="Data Explorer",
    page_icon="📁",
    layout="wide"
)


# TITLE

st.title("📁 Data Explorer")
st.write(
    "Explore your processed Google Maps Business dataset."
)


# LOAD DATA FROM HOME

if (
    "featured_df" not in st.session_state
    or st.session_state.featured_df is None
):
    st.warning(
        "Please upload and process dataset from Home page first."
    )
    st.stop()


df = st.session_state.featured_df.copy()


# DATASET SUMMARY

st.subheader("📊 Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Rows",
        df.shape[0]
    )

with col2:
    st.metric(
        "Columns",
        df.shape[1]
    )

with col3:
    st.metric(
        "Missing Values",
        df.isnull().sum().sum()
    )

with col4:
    st.metric(
        "Duplicates",
        df.duplicated().sum()
    )


# PREVIEW

st.divider()
st.subheader("👀 Data Preview")


rows = st.slider(
    "Rows to display",
    5,
    50,
    10
)

st.dataframe(
    df.head(rows),
    use_container_width=True
)

# COLUMN INFORMATION

st.divider()
st.subheader("🧾 Column Information")

column_info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isnull().sum().values,
    "Unique Values": [
        df[col].nunique()
        for col in df.columns
    ]
})

st.dataframe(
    column_info,
    use_container_width=True,
    hide_index=True
)

# FILTER DATA

st.divider()
st.subheader("🔎 Filter Data")

filter_column = st.selectbox(
    "Select Column",
    df.columns
)

values = st.multiselect(
    "Select Values",
    df[filter_column].dropna().unique()
)

filtered_df = df.copy()

if values:

    filtered_df = filtered_df[
        filtered_df[filter_column].isin(values)
    ]

st.write(
    f"Records Found: {len(filtered_df)}"
)

st.dataframe(
    filtered_df,
    use_container_width=True
)


# DOWNLOAD

st.divider()

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Data",
    data=csv,
    file_name="business_data_explorer.csv",
    mime="text/csv"
)