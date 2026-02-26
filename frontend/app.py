import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

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
if st.button("Check Fraud", disabled=(amount == 0)):

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
            # 1️⃣ DECISION (EXECUTIVE STYLE)
            # --------------------------------------------------
            st.markdown(
                f"<h2 style='margin-bottom:0;'>{decision_icon} {decision}</h2>",
                unsafe_allow_html=True
            )

            # --------------------------------------------------
            # 2️⃣ EXECUTIVE METRICS ROW
            # --------------------------------------------------
            col1, col2, col3 = st.columns(3)

            col1.markdown("**Risk Tier**")
            col1.markdown(f"<h3>{risk}</h3>", unsafe_allow_html=True)

            col2.markdown("**Fraud Probability**")
            col2.markdown(f"<h3>{fraud_prob_pct}%</h3>", unsafe_allow_html=True)

            col3.markdown("**Confidence (Safe)**")
            col3.markdown(f"<h3>{confidence_safe}%</h3>", unsafe_allow_html=True)

            # --------------------------------------------------
            # 3️⃣ RISK FACTORS
            # --------------------------------------------------
            st.markdown("### 🔍 Risk Factors Identified")

            reasons = []

            if amount >= 100000:
                reasons.append("• High transaction amount detected")
            if hour < 6 or hour > 22:
                reasons.append("• Unusual transaction timing")

            if risk == "HIGH":
                reasons.append("• Strong fraud indicators detected")
            elif risk == "MEDIUM":
                reasons.append("• Moderate anomaly patterns detected")
            else:
                reasons.append("• No significant anomaly patterns detected")

            for r in reasons:
                st.write(r)

            # --------------------------------------------------
            # 4️⃣ RECOMMENDED ACTION
            # --------------------------------------------------
            st.markdown("### ➡ Recommended Action")

            if risk == "LOW":
                st.success(action)
            elif risk == "MEDIUM":
                st.warning(action)
            else:
                st.error(action)

        else:
            st.error(f"API Error ({response.status_code})")
            st.code(response.text)

    except requests.exceptions.ConnectionError:
        st.error("❌ Backend API not running")
    except requests.exceptions.Timeout:
        st.error("⏱ Request timed out")
    except Exception as e:
        st.error("Unexpected error occurred")
        st.code(str(e))

# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------
st.divider()
st.caption(
    "⚠️ This output is generated by a machine learning model and is intended "
    "as a decision-support tool. Final decisions should follow business and compliance policies."
)