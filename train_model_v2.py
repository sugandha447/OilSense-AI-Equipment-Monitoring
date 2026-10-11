import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==========================================
# LOAD DATASET
# ==========================================

print("=" * 60)
print("OilSense AI Model Training V2")
print("=" * 60)

data = pd.read_csv("dataset/scada_pipeline.csv")

print("\nDataset Loaded Successfully")
print("Rows :", len(data))
print("Columns :", len(data.columns))

# ==========================================
# REMOVE UNUSED COLUMNS
# ==========================================

drop_columns = [
    "timestamp",
    "segment_id",
    "event_type"
]

for col in drop_columns:
    if col in data.columns:
        data.drop(columns=col, inplace=True)

print("\nRemaining Columns")
print(data.columns.tolist())

# ==========================================
# SAVE LABEL ENCODERS
# ==========================================

encoders = {}

categorical_columns = [
    "valve_status",
    "pump_state",
    "compressor_state"
]

for col in categorical_columns:

    if col in data.columns:

        encoder = LabelEncoder()

        data[col] = encoder.fit_transform(
            data[col].astype(str)
        )

        encoders[col] = encoder

# ==========================================
# FEATURES AND TARGET
# ==========================================

X = data.drop("target", axis=1)

y = data["target"]

print("\nFeatures Used")

for feature in X.columns:
    print("✓", feature)

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

print("\nTraining Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

# ==========================================
# RANDOM FOREST V2
# ==========================================

model = RandomForestClassifier(

    n_estimators=300,

    max_depth=12,

    min_samples_split=4,

    min_samples_leaf=2,

    random_state=42,

    n_jobs=-1

)

print("\nTraining Model...")

model.fit(X_train, y_train)

print("Training Complete.")
# ==========================================
# MODEL EVALUATION
# ==========================================

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"Accuracy : {accuracy*100:.2f}%")

print("\nClassification Report\n")

print(classification_report(y_test, prediction))

print("\nConfusion Matrix\n")

print(confusion_matrix(y_test, prediction))

# ==========================================
# FEATURE IMPORTANCE
# ==========================================

importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

print("\n" + "=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

print(importance)

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(model, "model.pkl")

joblib.dump(encoders, "encoders.pkl")

joblib.dump(list(X.columns), "feature_columns.pkl")

print("\nModel Saved Successfully")

print("Encoders Saved Successfully")

print("Feature Columns Saved Successfully")

print("\nTraining Finished.")

print("=" * 60)
