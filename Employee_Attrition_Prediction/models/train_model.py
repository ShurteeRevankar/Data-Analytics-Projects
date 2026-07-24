import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# -----------------------------------------
# Paths
# -----------------------------------------
DATA_PATH = Path("data/hr_cleaned.csv")

MODEL_PATH = Path("models/attrition_model.pkl")
ENCODER_PATH = Path("models/label_encoders.pkl")
FEATURE_PATH = Path("models/feature_columns.pkl")

# -----------------------------------------
# Load Dataset
# -----------------------------------------
print("Loading Dataset...")

df = pd.read_csv(DATA_PATH)

# -----------------------------------------
# Drop Unnecessary Columns
# -----------------------------------------
drop_columns = [
    "EmployeeCount",
    "EmployeeNumber",
    "Over18",
    "StandardHours"
]

df.drop(columns=drop_columns, inplace=True, errors="ignore")

# -----------------------------------------
# Target Variable
# -----------------------------------------
y = df["AttritionFlag"]

X = df.drop(
    columns=[
        "Attrition",
        "AttritionFlag"
    ],
    errors="ignore"
)

# -----------------------------------------
# Label Encoding
# -----------------------------------------
label_encoders = {}

categorical_columns = X.select_dtypes(
    include="object"
).columns

for column in categorical_columns:

    encoder = LabelEncoder()

    X[column] = encoder.fit_transform(
        X[column].astype(str)
    )

    label_encoders[column] = encoder

# -----------------------------------------
# Save Feature Names
# -----------------------------------------
feature_columns = X.columns.tolist()

# -----------------------------------------
# Train Test Split
# -----------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# -----------------------------------------
# Model
# -----------------------------------------
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

print("Training Model...")

model.fit(X_train, y_train)

# -----------------------------------------
# Prediction
# -----------------------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\nModel Accuracy")
print("----------------------")
print(f"{accuracy:.4f}")

print("\nClassification Report")
print("----------------------")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix")
print("----------------------")
print(confusion_matrix(y_test, y_pred))

# -----------------------------------------
# Save Files
# -----------------------------------------
MODEL_PATH.parent.mkdir(
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)

joblib.dump(
    label_encoders,
    ENCODER_PATH
)

joblib.dump(
    feature_columns,
    FEATURE_PATH
)

print("\nFiles Saved Successfully")

print("✔ attrition_model.pkl")
print("✔ label_encoders.pkl")
print("✔ feature_columns.pkl")