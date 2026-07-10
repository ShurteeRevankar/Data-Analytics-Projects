# GOOGLE MAPS BUSINESS ANALYTICS
# ML MODEL TRAINING

import pandas as pd
import numpy as np
import os
import pickle


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


print("="*70)
print(" GOOGLE MAPS BUSINESS ANALYTICS MODEL TRAINING ")
print("="*70)

# 1. LOAD DATASET

DATA_PATH = "data/google_maps.csv"


df = pd.read_csv(DATA_PATH)


print("\nDataset Loaded Successfully!")
print("Dataset Shape :", df.shape)

# 2. DATA CHECK

print("\nColumns Available:")
print(df.columns.tolist())

# 3. CREATE TARGET VARIABLE

print("\nCreating Target Variable...")


def business_score(row):

    rating = row["Google Rating"]
    reviews = row["Total Reviews"]


    if rating >= 4.5 and reviews >= 100:

        return "High"


    elif rating >= 4.0:

        return "Medium"


    else:

        return "Low"


df["Business Potential"] = df.apply(
    business_score,
    axis=1
)

print("\nTarget Distribution")
print(
    df["Business Potential"].value_counts()
)

# 4. SELECT FEATURES

features = [

    "Category",
    "City",
    "Google Rating",
    "Total Reviews",
    "Website Available"

]


X = df[features].copy()
y = df["Business Potential"]

print("\nFeatures Selected:")

for col in features:
    print("-", col)


# 5. HANDLE MISSING VALUES

print("\nHandling Missing Values...")

for col in X.columns:

    # categorical columns
    if X[col].dtype in ["object", "string"]:

        X[col] = X[col].fillna("Unknown")

    # numerical columns
    else:

        X[col] = X[col].fillna(
            X[col].median()
        )


print("Missing Values Handled!")


# 6. ENCODING
# ============================================================


print("\nEncoding Categorical Features...")

encoder = {}

categorical_columns = [
    "Category",
    "City",
    "Website Available"
]

for col in categorical_columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(
        X[col].astype(str)
    )

    encoder[col] = le

print("Encoding Completed!")


# 7. TRAIN TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Data :", X_train.shape)
print("Testing Data  :", X_test.shape)


# 8. TRAIN MODEL

print("\nTraining Random Forest Model...")

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

print("Model Training Completed!")


# 9. MODEL EVALUATION

y_pred = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n")
print("="*50)

print("MODEL PERFORMANCE")

print("="*50)

print(
    "Accuracy :",
    round(
        accuracy*100,
        2
    ),
    "%"
)

print("\nClassification Report")

print(
    classification_report(
        y_test,
        y_pred
    )
)

print("\nConfusion Matrix")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# 10. SAVE MODEL + ENCODER

MODEL_PATH = "models"

os.makedirs(
    MODEL_PATH,
    exist_ok=True
)

with open(
    "models/best_model.pkl",
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )

with open(
    "models/encoder.pkl",
    "wb"
) as file:


    pickle.dump(
        encoder,
        file
    )

print("\n")
print("="*70)

print("MODEL SAVED SUCCESSFULLY")

print("="*70)
