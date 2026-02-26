import streamlit as st
import requests

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
API_URL = "https://fraud-detection-fastapi-ouqr.onrender.com/predict"
HEALTH_URL = "https://fraud-detection-fastapi-ouqr.onrender.com/health"

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Fraud Detection System",
    layout="centered"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("💳 Fraud Detection System")
st.caption("Real-time transaction risk assessment using Machine Learning")

# --------------------------------------------------
# BACKEND HEALTH CHECK (INDUSTRY PRACTICE)
# --------------------------------------------------
with st.spinner("Checking system status..."):
    try:
        health = requests.get(HEALTH_URL, timeout=3)
        if health.status_code == 200:
            st.success("🟢 Fraud Detection API is online")
        else:
            st.warning("🟡 API reachable but unhealthy")
    except Exception:
        st.error("🔴 Backend service is unavailable")

st.divider()

# --------------------------------------------------
# USER INPUTS
# --------------------------------------------------
amount = st.number_input(
    "Transaction Amount (₹)",
    min_value=0.0,
    step=100.0,
    help="Higher transaction amounts may increase fraud risk"
)

hour = st.slider(
    "Transaction Hour (0–23)",
    min_value=0,
    max_value=23,
    help="Late-night transactions are generally higher risk"
)

# --------------------------------------------------
# BUTTON ACTION
# --------------------------------------------------
if st.button("Check Fraud", disabled=(amount <= 0)):

    payload = {
        "amount": amount,
        "hour": hour
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=5)

        if response.status_code == 200:
            result = response.json()

            probability = result["probability"]
            risk = result["risk_level"]

            fraud_prob_pct = round(probability * 100, 1)
            confidence_safe = round((1 - probability) * 100, 1)

            # --------------------------------------------------
            # INDUSTRY DECISION MAPPING
            # --------------------------------------------------
            if risk == "LOW":
                decision = "TRANSACTION APPROVED"
                decision_icon = "🟢"
                action = "Proceed with transaction"
            elif risk == "MEDIUM":
                decision = "REVIEW REQUIRED"
                decision_icon = "🟡"
                action = "Initiate step-up authentication (OTP / manual verification)"
            else:
                decision = "TRANSACTION BLOCKED"
                decision_icon = "🔴"
                action = "Block transaction and escalate to fraud investigation team"

            st.divider()

            # --------------------------------------------------
            # 1️⃣ DECISION (EXECUTIVE VIEW)
            # --------------------------------------------------
            st.markdown(
                f"<h2 style='margin-bottom:0;'>{decision_icon} {decision}</h2>",
                unsafe_allow_html=True
            )

            # --------------------------------------------------
            # 2️⃣ EXECUTIVE METRICS
            # --------------------------------------------------
            col1, col2, col3 = st.columns(3)

            col1.metric("Risk Tier", risk)
            col2.metric("Fraud Probability", f"{fraud_prob_pct}%")
            col3.metric("Confidence (Safe)", f"{confidence_safe}%")

            # --------------------------------------------------
            # 3️⃣ RISK FACTORS (EXPLAINABILITY)
            # --------------------------------------------------
            st.subheader("🔍 Risk Factors Identified")

            reasons = []

            if amount >= 100000:
                reasons.append("⚠ High transaction amount detected")
            else:
                reasons.append("✔ Transaction amount within normal range")

            if hour < 6 or hour > 22:
                reasons.append("⚠ Unusual transaction timing")
            else:
                reasons.append("✔ Transaction timing within normal range")

            if risk == "HIGH":
                reasons.append("❌ Strong fraud indicators detected")
            elif risk == "MEDIUM":
                reasons.append("⚠ Moderate anomaly patterns detected")
            else:
                reasons.append("✔ No significant anomaly patterns detected")

            for r in reasons:
                st.write(r)

            # --------------------------------------------------
            # 4️⃣ RECOMMENDED ACTION
            # --------------------------------------------------
            st.subheader("➡ Recommended Action")

            if risk == "LOW":
                st.success(action)
            elif risk == "MEDIUM":
                st.warning(action)
            else:
                st.error(action)

        else:
            st.error(f"API Error ({response.status_code})")
            st.code(response.text)

    except requests.exceptions.Timeout:
        st.error("⏱ Request timed out")
    except requests.exceptions.ConnectionError:
        st.error("❌ Unable to reach backend service")
    except Exception as e:
        st.error("Unexpected error occurred")
        st.code(str(e))

# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------
st.divider()
st.caption(
    "⚠️ This output is generated by a machine learning model and is intended "
    "as a decision-support tool. Final decisions should follow business, risk, "
    "and compliance policies."
)