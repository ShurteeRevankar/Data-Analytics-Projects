import pandas as pd


def preprocess_data(df):
    """
    Perform preprocessing and feature engineering
    """

    # Create a copy
    df = df.copy()

    # -------------------------
    # Remove duplicate records
    # -------------------------
    df.drop_duplicates(inplace=True)

    # -------------------------
    # Handle Missing Values
    # -------------------------
    numeric_cols = df.select_dtypes(include=["number"]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)

    for col in categorical_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)

    # -------------------------
    # Age Group
    # -------------------------
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[18, 25, 35, 45, 60],
        labels=["18-25", "26-35", "36-45", "46-60"]
    )

    # -------------------------
    # Income Category
    # -------------------------
    df["IncomeCategory"] = pd.qcut(
        df["MonthlyIncome"],
        q=3,
        labels=["Low", "Medium", "High"]
    )

    # -------------------------
    # Experience Level
    # -------------------------
    df["ExperienceLevel"] = pd.cut(
        df["TotalWorkingYears"],
        bins=[-1, 5, 10, 20, 40],
        labels=["0-5 Years", "6-10 Years", "11-20 Years", "20+ Years"]
    )

    # -------------------------
    # Distance Category
    # -------------------------
    df["DistanceCategory"] = pd.cut(
        df["DistanceFromHome"],
        bins=[0, 5, 15, 30],
        labels=["Near", "Medium", "Far"],
        include_lowest=True
    )

    # -------------------------
    # Overtime Flag
    # -------------------------
    df["OvertimeFlag"] = df["OverTime"].map({
        "Yes": 1,
        "No": 0
    })

    # -------------------------
    # Attrition Flag
    # -------------------------
    df["AttritionFlag"] = df["Attrition"].map({
        "Yes": 1,
        "No": 0
    })

    # -------------------------
    # High Performer
    # -------------------------
    df["HighPerformer"] = (
        df["PerformanceRating"] >= 4
    ).astype(int)

    # -------------------------
    # Long Tenure Employee
    # -------------------------
    df["LongTenure"] = (
        df["YearsAtCompany"] >= 10
    ).astype(int)

    # -------------------------
    # Save processed dataset
    # -------------------------
    df.to_csv(
        "data/hr_cleaned.csv",
        index=False
    )

    return df