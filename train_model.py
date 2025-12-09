# train_model.py
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("dataset.csv")

required_cols = ["has_https", "num_digits", "num_special", "label"]
for c in required_cols:
    if c not in df.columns:
        raise ValueError(f"dataset.csv missing column: {c}")

# Convert label to numeric
df["label"] = df["label"].map({"legit": 0, "phishing": 1})

X = df[["has_https", "num_digits", "num_special"]]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model training completed successfully!")
print("Training accuracy:", model.score(X_train, y_train))
print("Testing accuracy:", model.score(X_test, y_test))