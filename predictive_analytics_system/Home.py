# GOOGLE MAPS BUSINESS ANALYTICS DASHBOARD

import streamlit as st
import pandas as pd

# UTILS

from utils.loader import (
    load_dataset,
    load_sample_dataset,
    get_file_information,
)

from utils.validators import validate_dataset

from utils.cleaner import clean_dataset

from utils.features import create_features

from utils.helpers import calculate_kpis

from utils.styles import (
    load_css,
    hero_section,
    section_title,
    success_card,
    warning_card,
    error_card,
)

# PAGE CONFIG

st.set_page_config(
    page_title="Google Maps Business Analytics",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# LOAD CSS

load_css()

# SESSION STATE

if "raw_df" not in st.session_state:
    st.session_state.raw_df = None

if "clean_df" not in st.session_state:
    st.session_state.clean_df = None

if "featured_df" not in st.session_state:
    st.session_state.featured_df = None

# Dataset available for all pages
if "data" not in st.session_state:
    st.session_state.data = None

if "processed" not in st.session_state:
    st.session_state.processed = False

# HERO SECTION

hero_section(
    "📍 Google Maps Business Analytics Dashboard",
    """
Upload any Google Maps Business dataset.

The dashboard automatically validates,
cleans,
creates new features,
and prepares the dataset
for advanced analytics.
""",
)

# DATASET UPLOAD GUIDELINES

section_title("📌 Dataset Upload Guidelines")

st.info(
    """
**Upload a Google Maps Business dataset (CSV/Excel) containing:**

### Required Columns
✅ Business Name  
✅ Category  
✅ Google Rating (0-5)  
✅ Total Reviews  

### Recommended Columns
📍 City / Area  
📍 Address / Pincode  
📞 Contact Number  
🌐 Website Availability  
📌 Latitude & Longitude  
📊 Business Status  

### Dataset Requirements
✔ First row should contain column names  
✔ Each row = one business  
✔ Ratings and reviews should be numeric  

After upload, the dashboard will automatically **validate, clean, 
create features, and generate business insights.**
"""
)

st.divider()

# SIDEBAR

st.sidebar.title("⚙ Dashboard")

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV / Excel File",
    type=["csv", "xlsx", "xls"],
)

st.sidebar.markdown("---")


# LOAD DATASET

df = None

if uploaded_file is not None:

    df = load_dataset(uploaded_file)

# WAIT FOR DATA

if df is None:

    st.info("👈 Upload a dataset from the sidebar to begin.")

    st.stop()

# STORE RAW DATA

st.session_state.raw_df = df.copy()

# Share dataset with all pages
st.session_state.data = df.copy()


# DATASET INFORMATION

section_title("📊 Dataset Information")

info = get_file_information(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Rows",
        info["rows"]
    )

with col2:
    st.metric(
        "Columns",
        info["columns"]
    )

with col3:
    st.metric(
        "Memory Usage",
        info["memory"]
    )

with col4:
    st.metric(
        "Duplicate Rows",
        info["duplicates"]
    )

st.divider()

# DATASET VALIDATION

section_title("✅ Dataset Validation")

validation = validate_dataset(df)

if validation["valid"]:

    success_card(
        "✅ Dataset Validation Passed",
        "Required columns were detected successfully. "
        "The dataset is ready for preprocessing."
    )

else:

    error_card(
        "❌ Dataset Validation Failed",
        "Some required columns are missing."
    )

    st.error("Missing Columns")

    st.write(validation["missing_columns"])

    st.stop()

st.divider()

# CLEAN DATASET

section_title("🧹 Dataset Cleaning")

with st.spinner("Cleaning dataset..."):

    clean_df = clean_dataset(df.copy())

st.session_state.clean_df = clean_df

success_card(
    "Dataset Cleaned Successfully",
    "Missing values, duplicate records and invalid "
    "entries have been processed."
)

st.divider()

# FEATURE ENGINEERING

section_title("⚙️ Feature Engineering")

with st.spinner("Creating business features..."):

    featured_df = create_features(clean_df.copy())

st.session_state.featured_df = featured_df

success_card(
    "Feature Engineering Completed",
    "Business intelligence features have been created successfully."
)

st.divider()

# KPI CALCULATIONS

kpis = calculate_kpis(featured_df)

# KPI DASHBOARD

section_title("📈 Dashboard KPIs")

k1, k2, k3 = st.columns(3)

with k1:

    st.metric(
        "🏢 Total Businesses",
        f"{kpis['total_businesses']:,}"
    )

with k2:

    st.metric(
        "⭐ Average Rating",
        kpis["average_rating"]
    )

with k3:

    st.metric(
        "📝 Total Reviews",
        f"{kpis['total_reviews']:,}"
    )

k4, k5, k6 = st.columns(3)

with k4:

    st.metric(
        "🌐 Website Availability",
        f"{kpis['website_percentage']}%"
    )

with k5:

    st.metric(
        "🏆 High Rated Businesses",
        kpis["high_rated"]
    )

with k6:

    st.metric(
        "🔥 Popular Businesses",
        kpis["popular_businesses"]
    )

st.divider()

# CLEANED DATASET PREVIEW

section_title("📋 Cleaned Dataset Preview")

preview_rows = st.slider(
    "Number of rows to preview",
    min_value=5,
    max_value=min(100, len(featured_df)),
    value=10,
)

st.dataframe(
    featured_df.head(preview_rows),
    use_container_width=True,
)

st.divider()

# COLUMN SUMMARY

section_title("🔍 Column Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.subheader("Column Names")

    st.write(featured_df.columns.tolist())

with summary_col2:

    summary_df = pd.DataFrame(
        {
            "Column": featured_df.columns,
            "Data Type": featured_df.dtypes.astype(str).values,
            "Missing Values": featured_df.isna().sum().values,
        }
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
    )

st.divider()

# DOWNLOAD DATASET

section_title("📥 Download Processed Dataset")

csv = featured_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Processed Dataset (CSV)",
    data=csv,
    file_name="processed_google_maps_business.csv",
    mime="text/csv",
    use_container_width=True,
)

st.divider()

# STORE FINAL DATASET

st.session_state.featured_df = featured_df
st.session_state.processed = True

# PROCESS COMPLETED

success_card(
    "🎉 Processing Completed Successfully",
    """
Your dataset has been successfully:

✔ Validated

✔ Cleaned

✔ Feature Engineered

✔ Processed

You can now explore the remaining pages of the dashboard from the sidebar.
"""
)

st.divider()

# ABOUT PROJECT

section_title("ℹ️ About This Dashboard")

st.markdown(
    """
### Google Maps Business Analytics Dashboard

This application helps analyze Google Maps Business datasets by providing:

- 📊 Business Overview
- ⭐ Rating Analytics
- 🌍 Geographic Analysis
- 💻 Online Presence Analysis
- 📝 Customer Review Insights
- 🤖 Business Prediction
- 🎯 Opportunity Finder
- 🔍 Business Search
- 📂 Data Explorer
- 📖 Model Explanation

---

### Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- Scikit-learn

---

Developed as part of the **ReadyNest Internship Project**.
"""
)

st.divider()

# FOOTER

st.caption(
    "© 2026 Google Maps Business Analytics Dashboard | Built with Streamlit"
)
