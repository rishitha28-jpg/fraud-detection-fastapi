import pandas as pd

def preprocess(df):
    df = df.copy()

    # --------- TARGET COLUMN ----------
    # Your dataset uses 'Class' as fraud label
    target_col = "Class"

    # --------- CREATE HOUR FEATURE ----------
    if "Time" in df.columns:
        df["hour"] = (df["Time"] // 3600) % 24
    else:
        df["hour"] = 0  # safe default

    # --------- SELECT NUMERIC FEATURES ----------
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c != target_col]

    # Keep first 7 numeric features (industry safe)
    selected_features = numeric_cols[:7]

    # Final dataframe
    df = df[selected_features + [target_col]]

    # Rename target
    df.rename(columns={target_col: "is_fraud"}, inplace=True)

    return df