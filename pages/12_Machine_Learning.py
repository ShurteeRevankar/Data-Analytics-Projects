import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

st.set_page_config(
    page_title="Machine Learning",
    layout="wide"
)

st.title("🤖 Machine Learning: Payment Value Prediction")

# =====================================
# Load Dataset
# =====================================

if "df" not in st.session_state:
    st.warning("Please upload the dataset from the Data Upload page first.")
    st.stop()

df = st.session_state["df"]

# Select Required Columns
ml_df = df[
    ["price", "freight_value", "payment_value"]
].dropna()

# =====================================
# Features & Target
# =====================================

X = ml_df[["price", "freight_value"]]

y = ml_df["payment_value"]

# =====================================
# Train Test Split
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================
# Model Training
# =====================================

model = LinearRegression()

model.fit(X_train, y_train)

# =====================================
# Predictions
# =====================================

y_pred = model.predict(X_test)

# =====================================
# Evaluation Metrics
# =====================================

r2 = r2_score(y_test, y_pred)

mae = mean_absolute_error(y_test, y_pred)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

# =====================================
# KPI Cards
# =====================================

st.subheader("📊 Model Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "R² Score",
        f"{r2:.3f}"
    )

with col2:
    st.metric(
        "MAE",
        f"{mae:.2f}"
    )

with col3:
    st.metric(
        "RMSE",
        f"{rmse:.2f}"
    )

st.markdown("---")

# =====================================
# Actual vs Predicted
# =====================================

results = pd.DataFrame({
    "Actual": y_test,
    "Predicted": y_pred
})

fig = px.scatter(
    results,
    x="Actual",
    y="Predicted",
    title="Actual vs Predicted Payment Value"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# Sample Predictions
# =====================================

st.subheader("Prediction Samples")

st.dataframe(
    results.head(20),
    use_container_width=True
)

# =====================================
# Business Insights
# =====================================

st.subheader("📌 Insights")

st.success(
    f"The model explains {r2*100:.1f}% of the variation in payment value."
)

st.info(
    "Price and freight value are strong predictors of total payment value."
)

st.info(
    "Higher-priced products generally result in higher payment values."
)