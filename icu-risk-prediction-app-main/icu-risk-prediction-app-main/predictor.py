import pandas as pd
import streamlit as st
import time
from utils import explain_risk_factors

def streamlit_predict_custom_input(clf):
    st.subheader("🧾 Patient Vital Signs Input")

    with st.form("icu_form"):
        col1, col2 = st.columns(2)

        with col1:
            HR = st.number_input("💓 Heart Rate (bpm)", value=80, step=1)
            BP = st.number_input("🩸 Blood Pressure (mmHg)", value=120, step=1)
            Temp = st.number_input("🌡️ Body Temperature (°F)", value=98.6)

        with col2:
            RespRate = st.number_input("🫁 Respiratory Rate (breaths/min)", value=18, step=1)
            ComorbidityIndex = st.slider("📊 Comorbidity Index", 0, 5, value=2)

        submitted = st.form_submit_button("🚨 Predict ICU Risk")

    if submitted:
        input_df = pd.DataFrame([{
            'HR': HR,
            'BP': BP,
            'Temp': Temp,
            'RespRate': RespRate,
            'ComorbidityIndex': ComorbidityIndex
        }])

        # ICU override rule
        force_icu = (
            HR < 50 or HR > 130 or
            BP < 80 or BP > 180 or
            Temp < 94 or Temp > 105 or
            RespRate < 10 or RespRate > 30 or
            ComorbidityIndex > 3
        )

        with st.spinner("🔍 Predicting ICU Risk... Please wait a few seconds..."):
            time.sleep(3)  # UX delay to simulate real model prediction time

            try:
                if force_icu:
                    prediction = 1
                    prob = 1.0
                else:
                    prediction = clf.predict(input_df.to_numpy())[0]
                    try:
                        prob = clf.predict_proba(input_df.to_numpy())[0][1]
                    except Exception:
                        prob = None

                # Stylish result
                if prediction == 1:
                    st.error("🛑 Prediction: **High ICU Risk**")
                else:
                    st.success("✅ Prediction: **No ICU Risk**")

                if prob is not None:
                    st.info(f"📈 Predicted ICU Risk Probability: **{prob:.2%}**")

                with st.expander("📋 Explanation of Risk Factors"):
                    explain_risk_factors(input_df, prediction, streamlit_mode=True)

                st.success("Prediction complete. You may review the risk level and explanation above.")

            except Exception as e:
                st.error(f"❌ Prediction failed: {str(e)}")
