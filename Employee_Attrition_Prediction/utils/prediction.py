import joblib
import pandas as pd
from pathlib import Path

# ----------------------------------------------------
# Load Saved Files
# ----------------------------------------------------
MODEL_PATH = Path("models/attrition_model.pkl")
ENCODER_PATH = Path("models/label_encoders.pkl")
FEATURE_PATH = Path("models/feature_columns.pkl")

model = joblib.load(MODEL_PATH)
label_encoders = joblib.load(ENCODER_PATH)
feature_columns = joblib.load(FEATURE_PATH)


# ----------------------------------------------------
# Prediction Function
# ----------------------------------------------------
def predict_attrition(employee_data):
    """
    Predict employee attrition.

    Parameters
    ----------
    employee_data : dict

    Returns
    -------
    prediction : int
    probability : float
    """

    # Convert dictionary to DataFrame
    input_df = pd.DataFrame([employee_data])

    # Encode categorical columns
    for column, encoder in label_encoders.items():

        if column in input_df.columns:

            value = str(input_df.loc[0, column])

            # Handle unseen values safely
            if value in encoder.classes_:

                input_df[column] = encoder.transform([value])

            else:
                # Use first known class if unseen
                input_df[column] = encoder.transform(
                    [encoder.classes_[0]]
                )

    # Add any missing columns
    for col in feature_columns:

        if col not in input_df.columns:
            input_df[col] = 0

    # Keep same column order as training
    input_df = input_df[feature_columns]

    # Prediction
    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0][1]

    return prediction, probability


# ----------------------------------------------------
# Risk Message
# ----------------------------------------------------
def prediction_message(prediction, probability):

    if prediction == 1:

        if probability >= 0.80:
            return (
                "🔴 High Risk",
                "This employee has a high probability of leaving the organization."
            )

        return (
            "🟠 Medium Risk",
            "This employee has a moderate probability of leaving the organization."
        )

    return (
        "🟢 Low Risk",
        "This employee is likely to stay in the organization."
    )