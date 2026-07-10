import pickle
import pandas as pd
import numpy as np
import os

# Paths

MODEL_PATH = "models/best_model.pkl"
ENCODER_PATH = "models/encoder.pkl"

# Load Model

def load_model():

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Model file not found. Please train the model first."
        )

    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

    return model


# Load Encoder

def load_encoder():

    if not os.path.exists(ENCODER_PATH):
        raise FileNotFoundError(
            "Encoder file not found. Please train the model first."
        )

    with open(ENCODER_PATH, "rb") as file:
        encoder = pickle.load(file)

    return encoder


# Prediction Function

def predict_business(
        category,
        city,
        rating,
        reviews,
        website
):

    # Load saved objects

    model = load_model()
    encoder = load_encoder()



    # Create Input DataFrame

    input_data = pd.DataFrame({
        "Category": [category],
        "City": [city],
        "Google Rating": [rating],
        "Total Reviews": [reviews],
        "Website Available": [website]
    })

    # Identify categorical columns

    categorical_columns = [
        "Category",
        "City",
        "Website Available"
    ]

    # Encode categorical variables

    for col in categorical_columns:

        if col in encoder:
            le = encoder[col]
            value = input_data[col].astype(str)

            # Handle unseen values

            if "Unknown" not in le.classes_:
                le.classes_ = np.append(
                    le.classes_,
                    "Unknown"
                )


            value = value.apply(

                lambda x:
                x if x in le.classes_
                else "Unknown"
            )
            input_data[col] = le.transform(value)



    # Prediction

    prediction = model.predict(
        input_data
    )


    # Probability

    if hasattr(model, "predict_proba"):

        probability = model.predict_proba(
            input_data
        )

        confidence = max(
            probability[0]
        ) * 100

    else:

        confidence = None

    # Return Result

    return {

        "prediction": prediction[0],
        "confidence": round(
            confidence,
            2
        ) if confidence else None

    }