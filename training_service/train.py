print("🚀 train.py started")

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from feature_engineering import preprocess

print("📥 Reading CSV...")

df = pd.read_csv("training_service/creditcard_2023.csv")
print("✅ CSV loaded. Shape:", df.shape)

print("🧹 Preprocessing data...")
df = preprocess(df)
print("✅ After preprocessing:", df.shape)

X = df.drop("is_fraud", axis=1)
y = df["is_fraud"]

print("✂️ Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print("🤖 Training model...")
model = RandomForestClassifier(
    n_estimators=50,   # smaller for fast test
    max_depth=8,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)
print("✅ Model trained")

print("📊 Evaluating model...")
preds = model.predict(X_test)
probs = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, preds))
print("ROC-AUC:", roc_auc_score(y_test, probs))

print("💾 Saving model...")
joblib.dump(model, "artifacts/fraud_model.pkl")

print("🎉 DONE. Model saved in artifacts/")