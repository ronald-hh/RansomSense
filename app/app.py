import streamlit as st
import pandas as pd
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

print(MODELS_DIR)

model = joblib.load(MODELS_DIR / "severity_model.pkl")
preprocessor = joblib.load(MODELS_DIR / "preprocessor.pkl")

st.set_page_config(
    page_title="RansomSense",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ RansomSense")

st.subheader("AI-Powered Ransomware Severity Prediction")

st.sidebar.title("Navigation")

st.sidebar.info(
    "Enter ransomware attack details to predict severity."
)

industry = st.selectbox(
    "Industry",
    [
        "Healthcare",
        "Finance",
        "Education",
        "Government",
        "Retail",
        "Technology",
        "Manufacturing"
    ]
)

country = st.selectbox(
    "Country",
    [
        "USA",
        "UK",
        "Germany",
        "Canada",
        "South Africa",
        "India",
        "Australia"
    ]
)

attack_vector = st.selectbox(
    "Attack Vector",
    [
        "Phishing",
        "RDP",
        "Software Vulnerability",
        "Malicious Email",
        "USB",
        "Insider Threat"
    ]
)

group = st.text_input(
    "Ransomware Group"
)

attack_date = st.date_input(
    "Attack Date"
)

ransom = st.number_input(
    "Ransom Amount (USD)",
    min_value=0.0
)

if st.button("Predict Severity"):
    input_data = pd.DataFrame({

    "Industry":[industry],

    "Country":[country],

    "Attack_Date":[attack_date],

    "Ransomware_Group":[group],

    "Attack_Vector":[attack_vector],

    "Ransom_Amount_USD":[ransom]

})
    input_data["Attack_Date"] = pd.to_datetime(input_data["Attack_Date"])

    input_data["Attack_Year"] = input_data["Attack_Date"].dt.year
    input_data["Attack_Month"] = input_data["Attack_Date"].dt.month
    input_data["Attack_Day"] = input_data["Attack_Date"].dt.day
    input_data["Attack_DayOfWeek"] = input_data["Attack_Date"].dt.dayofweek

    input_data = input_data.drop("Attack_Date", axis=1)
    processed = preprocessor.transform(input_data)
    prediction = model.predict(processed)[0]
    st.success(f"Predicted Severity Score: {prediction:.2f}/10")