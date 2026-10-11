# 🛢 OilSense - AI-Based Refinery Monitoring System

## 📌 Project Description
OilSense is an AI-powered industrial monitoring system for crude oil refinery equipment using SCADA-like sensor data.

It predicts equipment faults using Machine Learning (Random Forest).

---

## ⚙ Features

- Real-time dashboard for industrial sensors
- AI-based fault prediction system
- SCADA-style monitoring UI
- Prediction history stored in SQLite
- Model analytics (Accuracy, Precision, Recall, F1-score)
- Industrial-grade UI design

---

## 🧠 Machine Learning Model

- Algorithm: Random Forest Classifier
- Input Features:
  - Pressure
  - Flow Rate
  - Temperature
  - Valve Status
  - Pump State
  - Pump Speed
  - Compressor State
  - Energy Consumption
  - Alarm Triggered

- Output:
  - Normal / Fault Prediction

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python train_model.py
python app.py