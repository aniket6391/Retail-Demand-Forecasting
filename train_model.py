import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv("dataset/dashboard_data.csv")

# ==========================================================
# ENCODE ONLY REQUIRED COLUMNS
# ==========================================================

categorical_columns = [
    "Region",
    "Category",
    "Month_Name"
]

encoders = {}

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# ==========================================================
# FEATURES USED BY DASHBOARD
# ==========================================================

feature_columns = [
    "Region",
    "Category",
    "Price",
    "Inventory",
    "Customers",
    "Month_Name"
]

X = df[feature_columns]

y = df["Predicted_Sales"]

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================================
# MODEL
# ==========================================================

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================================================
# EVALUATION
# ==========================================================

pred = model.predict(X_test)

score = r2_score(y_test, pred)

print(f"R² Score : {score:.4f}")

# ==========================================================
# SAVE
# ==========================================================

joblib.dump(model, "models/model.pkl")
joblib.dump(encoders, "models/encoders.pkl")
joblib.dump(feature_columns, "models/features.pkl")

print("Model Saved Successfully")