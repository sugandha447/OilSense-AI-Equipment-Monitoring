# ==========================================================
# OilSense AI Based Crude Oil Refinery Equipment Monitoring
# Indian Oil Corporation Limited (IOCL)
# Flask Backend - Professional Version
# ==========================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file
)

import pandas as pd
import numpy as np
import joblib
import os

from datetime import datetime
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
# ==========================================================
# Flask Application
# ==========================================================

app = Flask(__name__)

app.secret_key = "OilSense_AI_IOCL_2026"

# ==========================================================
# Login Credentials
# ==========================================================

USERNAME = "admin"
PASSWORD = "admin123"

# ==========================================================
# Load AI Files
# ==========================================================

try:

    model = joblib.load("model.pkl")

    encoders = joblib.load("encoders.pkl")

    feature_columns = joblib.load("feature_columns.pkl")

    print("✓ AI Model Loaded Successfully")

except Exception as e:

    print("Model Loading Error :", e)

# ==========================================================
# Prediction History File
# ==========================================================

HISTORY_FILE = "prediction_history.csv"

history_columns = [

    "Date",

    "Pressure",

    "Flow Rate",

    "Temperature",

    "Pump Speed",

    "Energy",

    "Prediction",

    "Confidence",

    "Health",

    "Severity",

    "Risk",

    "Recommendation"

]

# ==========================================================
# Create CSV if Missing
# ==========================================================

if not os.path.exists(HISTORY_FILE):

    pd.DataFrame(

        columns=history_columns

    ).to_csv(

        HISTORY_FILE,

        index=False

    )

# ==========================================================
# Repair Empty CSV
# ==========================================================
try:

    test = pd.read_csv(HISTORY_FILE)

    # If columns don't match, recreate the file
    if list(test.columns) != history_columns:

        pd.DataFrame(
            columns=history_columns
        ).to_csv(
            HISTORY_FILE,
            index=False
        )

except Exception:

    pd.DataFrame(
        columns=history_columns
    ).to_csv(
        HISTORY_FILE,
        index=False
    )

# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
def home():

    if "user" in session:

        return redirect(url_for("dashboard"))

    return render_template("login.html")

# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["POST"])

def login():

    username = request.form.get("username")

    password = request.form.get("password")

    if username == USERNAME and password == PASSWORD:

        session["user"] = username

        return redirect(url_for("dashboard"))

    return render_template(

        "login.html",

        error="Invalid Username or Password"

    )

# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")

def logout():

    session.clear()

    return redirect(url_for("home"))
# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect(url_for("home"))

    # -----------------------------
    # Load Prediction History
    # -----------------------------

    try:

        history = pd.read_csv(HISTORY_FILE)

    except Exception:

        history = pd.DataFrame(columns=history_columns)

    # -----------------------------
    # Last 10 Records
    # -----------------------------

    latest_history = history.tail(10)

    # -----------------------------
    # Chart Data
    # -----------------------------

    pressure_data = latest_history["Pressure"].tolist() \
        if "Pressure" in latest_history.columns else []

    temperature_data = latest_history["Temperature"].tolist() \
        if "Temperature" in latest_history.columns else []

    energy_data = latest_history["Energy"].tolist() \
        if "Energy" in latest_history.columns else []

    labels = list(range(1, len(pressure_data) + 1))

    # -----------------------------
    # Fault Statistics
    # -----------------------------

    if "Prediction" in latest_history.columns:

        normal_count = len(
            latest_history[
                latest_history["Prediction"] == "Normal Operation"
            ]
        )

        fault_count = len(
            latest_history[
                latest_history["Prediction"] == "Fault Detected"
            ]
        )

    else:

        normal_count = 0
        fault_count = 0

    # -----------------------------
    # Dashboard
    # -----------------------------

    return render_template(

        "dashboard.html",

        prediction=None,
        confidence=None,
        recommendation=None,

        health=None,
        severity=None,
        risk=None,

        prediction_time=None,

        status_color="",

        pressure=None,
        flow_rate=None,
        temperature=None,
        pump_speed=None,
        energy=None,

        history=latest_history.to_dict(orient="records"),

        chart_labels=labels,

        pressure_chart=pressure_data,

        temperature_chart=temperature_data,

        energy_chart=energy_data,

        normal_count=normal_count,

        fault_count=fault_count

    )
# ==========================================================
# AI PREDICTION
# ==========================================================

@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect(url_for("home"))

    # --------------------------------------------------
    # Read Form Data
    # --------------------------------------------------

    pressure = float(request.form["pressure"])
    flow_rate = float(request.form["flow_rate"])
    temperature = float(request.form["temperature"])

    valve_status = int(request.form["valve_status"])
    pump_state = int(request.form["pump_state"])

    pump_speed = float(request.form["pump_speed"])

    compressor_state = int(request.form["compressor_state"])

    energy = float(request.form["energy"])

    alarm = int(request.form["alarm"])

    # --------------------------------------------------
    # Prepare Input Data
    # --------------------------------------------------

    input_data = pd.DataFrame([{

        "pressure": pressure,

        "flow_rate": flow_rate,

        "temperature": temperature,

        "valve_status": valve_status,

        "pump_state": pump_state,

        "pump_speed": pump_speed,

        "compressor_state": compressor_state,

        "energy_consumption": energy,

        "alarm_triggered": alarm

    }])

    # Ensure column order matches training

    input_data = input_data.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # --------------------------------------------------
    # AI Prediction
    # --------------------------------------------------

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0]

    confidence = round(float(np.max(probability)) * 100, 2)

        # --------------------------------------------------
    # Equipment Health
    # --------------------------------------------------

    if prediction == 0:
        health = confidence
    else:
        health = max(5, 100 - confidence)

    health = round(health, 1)

    # --------------------------------------------------
    # Severity & Risk
    # --------------------------------------------------

    if prediction == 0:

        severity = "LOW"
        risk = "SAFE"

    else:

        if confidence < 80:

            severity = "MEDIUM"
            risk = "WARNING"

        elif confidence < 95:

            severity = "HIGH"
            risk = "DANGER"

        else:

            severity = "CRITICAL"
            risk = "EMERGENCY"

    # --------------------------------------------------
    # Prediction Text
    # --------------------------------------------------

    if prediction == 0:

        prediction_text = "Normal Operation"

        status_color = "green"

    else:

        prediction_text = "Fault Detected"

        status_color = "red"
            # --------------------------------------------------
    # Smart Recommendation Engine
    # --------------------------------------------------

    if prediction == 0:

        recommendation = (
            "✔ Equipment is operating normally.\n"
            "✔ Continue routine monitoring.\n"
            "✔ Preventive maintenance is recommended as per schedule."
        )

    else:

        recommendations = []

        if pressure > 90:
            recommendations.append(
                "✔ High pressure detected. Inspect the pipeline and pressure valves."
            )

        if temperature > 35:
            recommendations.append(
                "✔ High temperature detected. Check the cooling system."
            )

        if flow_rate < 15:
            recommendations.append(
                "✔ Low flow rate detected. Inspect pipelines for blockage."
            )

        if pump_speed > 1500:
            recommendations.append(
                "✔ Pump speed is too high. Inspect pump bearings."
            )

        if energy > 40:
            recommendations.append(
                "✔ High energy consumption detected. Inspect motor efficiency."
            )

        if alarm == 1:
            recommendations.append(
                "✔ Alarm signal detected. Verify the alarm source immediately."
            )

        if len(recommendations) == 0:
            recommendations.append(
                "✔ Schedule preventive maintenance."
            )

        recommendation = "\n".join(recommendations)

    # --------------------------------------------------
    # Prediction Time
    # --------------------------------------------------

    prediction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # --------------------------------------------------
    # Load History
    # --------------------------------------------------

    try:
        history = pd.read_csv(HISTORY_FILE)

    except Exception:
        history = pd.DataFrame(columns=history_columns)

    # --------------------------------------------------
    # Save Current Prediction
    # --------------------------------------------------

    history.loc[len(history)] = [

        prediction_time,

        pressure,

        flow_rate,

        temperature,

        pump_speed,

        energy,

        prediction_text,

        confidence,

        health,

        severity,

        risk,

        recommendation

    ]

    history.to_csv(HISTORY_FILE, index=False)

    # --------------------------------------------------
    # Prepare Charts
    # --------------------------------------------------

    latest_history = history.tail(10)

    pressure_chart = latest_history["Pressure"].tolist()

    temperature_chart = latest_history["Temperature"].tolist()

    energy_chart = latest_history["Energy"].tolist()

    labels = list(range(1, len(pressure_chart) + 1))

    normal_count = len(
        latest_history[
            latest_history["Prediction"] == "Normal Operation"
        ]
    )

    fault_count = len(
        latest_history[
            latest_history["Prediction"] == "Fault Detected"
        ]
    )
        # --------------------------------------------------
    # Return Dashboard
    # --------------------------------------------------

    return render_template(

        "dashboard.html",

        prediction=prediction_text,

        confidence=confidence,

        health=health,

        severity=severity,

        risk=risk,

        recommendation=recommendation,

        prediction_time=prediction_time,

        status_color=status_color,

        pressure=pressure,

        flow_rate=flow_rate,

        temperature=temperature,

        pump_speed=pump_speed,

        energy=energy,

        history=latest_history.to_dict(orient="records"),

        chart_labels=labels,

        pressure_chart=pressure_chart,

        temperature_chart=temperature_chart,

        energy_chart=energy_chart,

        normal_count=normal_count,

        fault_count=fault_count

    )
# ==========================================================
# RUN APPLICATION
# ==========================================================
# ==========================================================
# ABOUT PAGE
# ==========================================================

@app.route("/about")
def about():

    if "user" not in session:
        return redirect(url_for("home"))

    return render_template("about.html")


# ==========================================================
# HISTORY PAGE
# ==========================================================

@app.route("/history")
def history():

    if "user" not in session:
        return redirect(url_for("home"))

    try:
        history = pd.read_csv(HISTORY_FILE)
    except Exception:
        history = pd.DataFrame()

    return render_template(
        "history.html",
        history=history.to_dict(orient="records")
    )
# ==========================================================
# DOWNLOAD HISTORY CSV
# ==========================================================

@app.route("/download_csv")
def download_csv():

    if "user" not in session:
        return redirect(url_for("home"))

    return send_file(
        HISTORY_FILE,
        as_attachment=True,
        download_name="OilSense_Prediction_History.csv"
    )
# ==========================================================
# DOWNLOAD HISTORY CSV
# ==========================================================

@app.route("/download_history")
def download_history():

    if "user" not in session:
        return redirect(url_for("home"))

    return send_file(
        HISTORY_FILE,
        as_attachment=True,
        download_name="OilSense_Prediction_History.csv",
        mimetype="text/csv"
    )
# ==========================================================
# GENERATE PDF REPORT
# ==========================================================

@app.route("/report")
def report():

    if "user" not in session:
        return redirect(url_for("home"))

    try:
        history = pd.read_csv(HISTORY_FILE)

        if history.empty:
            return "No prediction history available."

    except Exception:
        return "Prediction history file not found."

    latest = history.iloc[-1]

    pdf_file = "OilSense_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("<b>OilSense AI Based Crude Oil Refinery Equipment Monitoring System</b>", styles["Title"])
    )

    elements.append(
        Paragraph("Indian Oil Corporation Limited (IOCL)", styles["Heading2"])
    )

    elements.append(
        Paragraph("<br/>Latest AI Prediction Report<br/><br/>", styles["Heading3"])
    )

    data = [

        ["Parameter", "Value"],

        ["Date", str(latest["Date"])],
        ["Pressure", str(latest["Pressure"])],
        ["Flow Rate", str(latest["Flow Rate"])],
        ["Temperature", str(latest["Temperature"])],
        ["Pump Speed", str(latest["Pump Speed"])],
        ["Energy", str(latest["Energy"])],
        ["Prediction", str(latest["Prediction"])],
        ["Confidence", str(latest["Confidence"]) + "%"],
        ["Health", str(latest["Health"]) + "%"],
        ["Severity", str(latest["Severity"])],
        ["Risk", str(latest["Risk"])],
        ["Recommendation", str(latest["Recommendation"])]

    ]

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,1), (-1,-1), colors.beige),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

        ("BOTTOMPADDING", (0,0), (-1,0), 10),

        ("ALIGN", (0,0), (-1,-1), "CENTER")

    ]))

    elements.append(table)

    doc.build(elements)

    return send_file(
        pdf_file,
        as_attachment=True
    )
if __name__ == "__main__":
    app.run(debug=True)