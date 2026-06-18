import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(
    page_title="RansomSense",
    page_icon="🛡️",
    layout="wide"
)


BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data" / "processed"

@st.cache_resource
def load_models():
    model = joblib.load(MODELS_DIR / "severity_model.pkl")
    preprocessor = joblib.load(MODELS_DIR / "preprocessor.pkl")
    return model, preprocessor


@st.cache_data
def load_dataset():
    return pd.read_csv(DATA_DIR / "cleaned_ransomware_dataset.csv")


model, preprocessor = load_models()
df = load_dataset()

st.title("🛡️ RansomSense")

st.caption(
    "AI-Powered Cybersecurity Risk Assessment Platform"
)

st.write(
    """
Predict the severity of ransomware attacks using Machine Learning.
Enter the attack information below and receive an AI-generated
severity prediction.
"""
)

st.sidebar.header("About")

st.sidebar.info(
    """
RansomSense predicts the severity of ransomware attacks using
Machine Learning models trained on historical ransomware incidents.
"""
)

st.sidebar.markdown("---")

st.sidebar.write("Developed by Hlakulo R. Hlungwani")


industries = sorted(df["Industry"].dropna().unique())
countries = sorted(df["Country"].dropna().unique())
vectors = sorted(df["Attack_Vector"].dropna().unique())
groups = sorted(df["Ransomware_Group"].dropna().unique())


st.header("Attack Information")

col1, col2 = st.columns(2)

with col1:

    industry = st.selectbox(
        "Industry",
        industries
    )

    country = st.selectbox(
        "Country",
        countries
    )

    attack_vector = st.selectbox(
        "Attack Vector",
        vectors
    )

with col2:

    ransomware_group = st.selectbox(
        "Ransomware Group",
        groups
    )

    attack_date = st.date_input(
        "Attack Date"
    )

    ransom_amount = st.number_input(
        "Ransom Amount (USD)",
        min_value=0.0,
        value=100000.0,
        step=10000.0
    )

st.markdown("---")


if st.button("Predict Severity", use_container_width=True):

    try:

        input_data = pd.DataFrame({

            "Industry": [industry],
            "Country": [country],
            "Attack_Date": [attack_date],
            "Ransomware_Group": [ransomware_group],
            "Attack_Vector": [attack_vector],
            "Ransom_Amount_USD": [ransom_amount]

        })

        input_data["Attack_Date"] = pd.to_datetime(input_data["Attack_Date"])

        input_data["Attack_Year"] = input_data["Attack_Date"].dt.year
        input_data["Attack_Month"] = input_data["Attack_Date"].dt.month
        input_data["Attack_Day"] = input_data["Attack_Date"].dt.day
        input_data["Attack_DayOfWeek"] = input_data["Attack_Date"].dt.dayofweek

        input_data = input_data.drop("Attack_Date", axis=1)

        processed = preprocessor.transform(input_data)

        prediction = model.predict(processed)[0]

        # Prevent impossible values
        prediction = max(0, min(prediction, 10))

        st.markdown("## Prediction Results")

        metric_col, progress_col = st.columns([1, 2])

        with metric_col:

            st.metric(
                "Severity Score",
                f"{prediction:.2f}/10"
            )

        with progress_col:

            st.progress(prediction / 10)

        # Risk Level

        if prediction < 2:

            st.success("🟢 Very Low Risk")

            recommendation = "Routine monitoring is sufficient."

        elif prediction < 4:

            st.success("🟢 Low Risk")

            recommendation = "Maintain current security controls."

        elif prediction < 6:

            st.info("🟡 Moderate Risk")

            recommendation = "Increase monitoring and investigate indicators."

        elif prediction < 8:

            st.warning("🟠 High Risk")

            recommendation = "Immediate investigation recommended."

        else:

            st.error("🔴 Critical Risk")

            recommendation = "Immediate incident response required."

        st.markdown("### Recommendation")

        st.write(recommendation)

        st.markdown("---")

        st.subheader("Prediction Summary")

        summary = pd.DataFrame({

            "Field": [
                "Industry",
                "Country",
                "Attack Vector",
                "Ransomware Group",
                "Attack Date",
                "Ransom Amount (USD)",
                "Predicted Severity"
            ],

            "Value": [
                industry,
                country,
                attack_vector,
                ransomware_group,
                attack_date,
                f"${ransom_amount:,.2f}",
                f"{prediction:.2f}/10"
            ]

        })

        st.table(summary)

    except Exception as e:

        st.error("Prediction failed.")

        st.exception(e)


st.markdown("---")

st.caption("🛡️ RansomSense | AI-Powered Ransomware Intelligence Platform")