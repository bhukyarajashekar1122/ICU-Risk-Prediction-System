import streamlit as st
import os
import joblib
from predictor import streamlit_predict_custom_input

MODEL_PATH = "xgb_icu_model.pkl.gz"

# ------------------------------
# CSS: Minimal padding and spacing
# ------------------------------
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
        .about-section h3 { margin-top: 1.5rem; }
        .about-section li { margin-bottom: 0.4rem; }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Title
# ------------------------------
st.title("ICU Risk Prediction App")

# ------------------------------
# Load Model (once per session)
# ------------------------------
if "clf" not in st.session_state:
    if os.path.exists(MODEL_PATH):
        st.session_state.clf = joblib.load(MODEL_PATH)
        st.success("Model loaded successfully.")
    else:
        st.error("Trained model file not found. Please upload or train a model.")

# ------------------------------
# Tabs: Predict | About
# ------------------------------
tabs = st.tabs(["Predict ICU Risk", "About the App"])

# ------------------------------
# Tab 1: Predict ICU Risk
# ------------------------------
with tabs[0]:
    st.subheader("Enter Patient Vitals to Predict ICU Risk")

    if "clf" in st.session_state:
        streamlit_predict_custom_input(st.session_state.clf)
    else:
        st.warning("Model is not loaded. Prediction cannot proceed.")

# ------------------------------
# Tab 2: About the App
# ------------------------------
with tabs[1]:
    st.markdown("## About the ICU Risk Prediction App")
    st.markdown("""
<div class="about-section">

### How the Model Works
- Accepts patient vital inputs: Heart Rate, Blood Pressure, Temperature, Respiratory Rate, and Comorbidity Index.
- Predicts whether the patient is likely to require ICU care using a pre-trained XGBoost model.
- Automatically flags extreme vital signs as high risk before prediction.

### Dataset
- Uses a synthetic dataset of 500 patient records.
- Data generated using realistic clinical ranges for vitals.
- ICU risk labels assigned using a rule-based scoring system.

### Model & Training
- Model: XGBoost Classifier – efficient and accurate.
- Trained offline using a custom `run_train.py` script.
- Final model is compressed and saved as `.pkl.gz` for optimized deployment.

### Key Features
- Simple and intuitive UI using Streamlit.
- Predicts ICU risk instantly from vitals.
- Provides explanation for predictions based on medical thresholds.

### Use Case
- Can assist in early triage in hospitals or remote settings.
- Useful in EHR systems or healthcare dashboards for ICU prioritization.

</div>
""", unsafe_allow_html=True)
