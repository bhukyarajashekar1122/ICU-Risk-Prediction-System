def explain_risk_factors(input_df, prediction, streamlit_mode=False):
    hr = input_df['HR'].iloc[0]
    bp = input_df['BP'].iloc[0]
    rr = input_df['RespRate'].iloc[0]
    ci = input_df['ComorbidityIndex'].iloc[0]
    temp = input_df['Temp'].iloc[0]

    reasons = []

    # Heart Rate
    if hr < 60:
        reasons.append(f"🔻 Low Heart Rate: {hr} bpm (below 60)")
    elif hr > 100:
        reasons.append(f"🔺 High Heart Rate: {hr} bpm (above 100)")

    # Blood Pressure
    if bp < 90:
        reasons.append(f"🔻 Low Blood Pressure: {bp} mmHg (below 90)")
    elif bp > 140:
        reasons.append(f"🔺 High Blood Pressure: {bp} mmHg (above 140)")

    # Respiratory Rate
    if rr < 12:
        reasons.append(f"🔻 Low Respiratory Rate: {rr} breaths/min (below 12)")
    elif rr > 20:
        reasons.append(f"🔺 High Respiratory Rate: {rr} breaths/min (above 20)")

    # Temperature
    if temp < 95:
        reasons.append(f"❄️ Low Body Temperature: {temp}°F (below 95)")
    elif temp > 100.4:
        reasons.append(f"🌡️ High Body Temperature: {temp}°F (above 100.4)")

    # Comorbidity Index
    if ci < 1:
        reasons.append(f"🔻 Low Comorbidity Index: {ci} (may indicate missing data)")
    elif ci > 2:
        reasons.append(f"⚠️ High Comorbidity Index: {ci} (above 2)")

    # Streamlit display only
    import streamlit as st

    st.markdown("### 🧠 Explanation of Risk Factors")

    if prediction == 1:
        if reasons:
            st.error("🛑 ICU likely required due to:")
            for r in reasons:
                st.markdown(f"- {r}")
        else:
            st.error("🛑 ICU risk predicted, but no critical vitals explicitly triggered.")
    else:
        if reasons:
            st.warning("⚠️ Some vitals are outside normal range, but overall ICU risk is not predicted:")
            for r in reasons:
                st.markdown(f"- {r}")
        else:
            st.success("✅ All vital signs appear to be within safe clinical ranges.")
