import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("="*60)
print(" OilSense AI Model Training ")
print("="*60)

# ==========================================
# Load Dataset
# ==========================================

data = pd.read_csv("dataset/scada_pipeline.csv")

print("\nDataset Loaded Successfully")
print("Rows :", data.shape[0])
print("Columns :", data.shape[1])

# ==========================================
# Remove Unwanted Columns
# ==========================================

drop_columns = [

    "timestamp",

    "segment_id",

    "event_type"

]

for col in drop_columns:

    if col in data.columns:

        data.drop(columns=col, inplace=True)

print("\nFeatures Used")

print(data.columns)

# ==========================================
# Split Features
# ==========================================

X = data.drop("target", axis=1)

y = data["target"]

# ==========================================
# Train Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)
# ==========================================
# Build AI Model
# ==========================================

print("\nTraining Random Forest Model...")

model = RandomForestClassifier(

    n_estimators=200,

    max_depth=12,

    random_state=42,

    n_jobs=-1

)

model.fit(X_train, y_train)

print("Training Completed")

# ==========================================
# Model Testing
# ==========================================

prediction = model.predict(X_test)

accuracy = accuracy_score(

    y_test,

    prediction

)

print()

print("="*60)

print("MODEL ACCURACY :", round(accuracy*100,2), "%")

print("="*60)

# ==========================================
# Save Model
# ==========================================

joblib.dump(

    model,

    "model.pkl"

)

print()

print("Model Saved Successfully")

print()

print("="*60)

print(" OilSense AI Model Ready ")

print("="*60)