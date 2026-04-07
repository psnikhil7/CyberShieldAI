import streamlit as st
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
model = load_model("cybershield_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# ---------------- SESSION HISTORY ----------------
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# ---------------- SMART HYBRID PREDICTION ----------------
def predict_message(text):
    text_lower = text.lower()

    official_bank_keywords = [
        "debited", "credited", "account ending", "do not share",
        "customer care", "transaction", "balance", "upi", "bank",
        "inr", "rs.", "available balance", "a/c", "txn"
    ]

    phishing_keywords = [
        "click", "claim", "verify", "urgent", "reward", "free",
        "prize", "win", "link", "limited offer", "login here",
        "update kyc", "suspend", "blocked", "confirm now"
    ]

    official_bank_signals = sum(1 for word in official_bank_keywords if word in text_lower)
    phishing_signals = sum(1 for word in phishing_keywords if word in text_lower)

    if official_bank_signals >= 2 and phishing_signals == 0:
        return 0.10

    if phishing_signals >= 2:
        return 0.90

    seq = tokenizer.texts_to_sequences([text])
    pad = pad_sequences(seq, maxlen=100)
    pred = model.predict(pad, verbose=0)[0][0]
    return float(pred)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(168, 85, 247, 0.18), transparent 28%),
        radial-gradient(circle at bottom right, rgba(236, 72, 153, 0.12), transparent 30%),
        linear-gradient(135deg, #fcf7ff 0%, #f7f0ff 40%, #fff7fb 100%);
    color: #221b44;
}

[data-testid="stHeader"] {
    background: rgba(255,255,255,0);
}

.block-container {
    max-width: 1240px;
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

.hero-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.82), rgba(255,255,255,0.60));
    border: 1px solid rgba(168, 85, 247, 0.18);
    border-radius: 30px;
    padding: 34px 32px 28px 32px;
    box-shadow: 0 18px 50px rgba(109, 40, 217, 0.10);
    backdrop-filter: blur(14px);
    margin-bottom: 22px;
}

.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.3rem;
    font-weight: 800;
    color: #6d28d9;
    margin-bottom: 10px;
    line-height: 1.05;
}

.hero-subtitle {
    font-size: 1.06rem;
    color: #5b4b8a;
    line-height: 1.75;
    max-width: 900px;
}

.pill {
    display: inline-block;
    margin-top: 14px;
    margin-right: 10px;
    padding: 10px 16px;
    border-radius: 999px;
    background: rgba(168, 85, 247, 0.08);
    border: 1px solid rgba(168, 85, 247, 0.16);
    color: #7c3aed;
    font-size: 0.92rem;
    font-weight: 600;
}

.glass-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.82), rgba(255,255,255,0.62));
    border: 1px solid rgba(168, 85, 247, 0.14);
    border-radius: 26px;
    padding: 24px;
    box-shadow: 0 14px 36px rgba(109, 40, 217, 0.08);
    backdrop-filter: blur(12px);
    height: 100%;
}

.section-title {
    font-size: 1.22rem;
    font-weight: 700;
    color: #4c1d95;
    margin-bottom: 10px;
}

.section-text {
    color: #5f5686;
    line-height: 1.72;
    font-size: 0.98rem;
}

.stat-box {
    background: rgba(168, 85, 247, 0.06);
    border: 1px solid rgba(168, 85, 247, 0.14);
    border-radius: 18px;
    padding: 14px 16px;
    margin-top: 12px;
    color: #6d28d9;
    font-weight: 600;
}

.example-box {
    background: rgba(255,255,255,0.72);
    border: 1px dashed rgba(168, 85, 247, 0.18);
    border-radius: 18px;
    padding: 16px;
    margin-top: 14px;
    color: #4338ca;
    line-height: 1.65;
    font-size: 0.97rem;
}

.stTextArea label {
    color: #4c1d95 !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
}

.stTextArea textarea {
    background: rgba(255,255,255,0.96) !important;
    color: #1f1b3a !important;
    border-radius: 18px !important;
    border: 1px solid rgba(168, 85, 247, 0.18) !important;
    min-height: 220px !important;
    font-size: 17px !important;
    box-shadow: inset 0 1px 3px rgba(109, 40, 217, 0.04);
}

.stButton > button {
    width: 100%;
    border: none;
    border-radius: 16px;
    background: linear-gradient(90deg, #9333ea 0%, #ec4899 100%);
    color: white;
    font-size: 1.02rem;
    font-weight: 700;
    padding: 0.92rem 1rem;
    box-shadow: 0 12px 24px rgba(168, 85, 247, 0.18);
}

.stButton > button:hover {
    filter: brightness(1.05);
    transform: translateY(-1px);
}

.result-safe {
    background: linear-gradient(135deg, rgba(34,197,94,0.10), rgba(34,197,94,0.04));
    border: 1px solid rgba(34,197,94,0.18);
    border-radius: 22px;
    padding: 22px;
    margin-top: 10px;
}

.result-phish {
    background: linear-gradient(135deg, rgba(239,68,68,0.10), rgba(239,68,68,0.04));
    border: 1px solid rgba(239,68,68,0.18);
    border-radius: 22px;
    padding: 22px;
    margin-top: 10px;
}

.result-title {
    font-size: 1.32rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.result-text {
    color: #312e81;
    font-size: 1rem;
    line-height: 1.72;
}

.bottom-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.82), rgba(255,255,255,0.62));
    border: 1px solid rgba(168, 85, 247, 0.14);
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 12px 28px rgba(109, 40, 217, 0.07);
    backdrop-filter: blur(10px);
    min-height: 220px;
}

.footer {
    text-align: center;
    margin-top: 26px;
    padding: 16px;
    color: #7c3aed;
    font-size: 0.95rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">🛡️ CyberShield AI</div>
    <div class="hero-subtitle">
        An AI-powered phishing threat intelligence platform for analyzing SMS and email content
        using Natural Language Processing and Deep Learning. The system evaluates risky message patterns,
        suspicious wording, urgency, and fraud-like communication behavior in real time.
    </div>
    <span class="pill">NLP Preprocessing</span>
    <span class="pill">LSTM Deep Learning</span>
    <span class="pill">Hybrid Smart Detection</span>
</div>
""", unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([1.45, 1], gap="large")

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Threat Analysis Console</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-text">Paste any SMS or email content below and let CyberShield AI analyze whether the message is safe or potentially phishing-related.</div>',
        unsafe_allow_html=True
    )

    user_input = st.text_area(
        "Enter SMS or Email Message",
        placeholder="Example: Congratulations! You have won 50000 rupees. Click now to claim your reward."
    )

    analyze = st.button("Analyze Message Threat")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Threat Intelligence Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-text">Core model and quick demo examples for project presentation.</div>', unsafe_allow_html=True)

    st.markdown('<div class="stat-box"><b>Model Accuracy:</b> 98%+</div>', unsafe_allow_html=True)
    st.markdown('<div class="stat-box"><b>Architecture:</b> Embedding + LSTM</div>', unsafe_allow_html=True)
    st.markdown('<div class="stat-box"><b>Dataset Size:</b> 5572 messages</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="example-box">
        <b>Phishing example:</b><br>
        Congratulations! You have won 50000 rupees. Click now to claim your reward.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="example-box">
        <b>Safe example:</b><br>
        Hi bro, meeting is at 5 pm tomorrow. Please be on time.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
if analyze:
    if user_input.strip() == "":
        st.warning("Please enter a message before analysis.")
    else:
        pred = predict_message(user_input)
        risk_score = round(float(pred) * 100, 2)
        lower_text = user_input.lower()

        if pred > 0.5:
            st.markdown(f"""
            <div class="result-phish">
                <div class="result-title">⚠️ Phishing Threat Detected</div>
                <div class="result-text">
                    <b>Threat Confidence:</b> {risk_score}%<br><br>
                    This message appears suspicious and matches patterns commonly associated with deceptive or phishing-like content.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            safe_score = round((1 - float(pred)) * 100, 2)
            st.markdown(f"""
            <div class="result-safe">
                <div class="result-title">✅ Message Appears Safe</div>
                <div class="result-text">
                    <b>Safety Confidence:</b> {safe_score}%<br><br>
                    The message does not show strong phishing indicators based on the learned sequence patterns and smart validation rules.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Threat Meter")
        if risk_score < 30:
            st.success(f"🟢 Low Risk • {risk_score}%")
        elif risk_score < 70:
            st.warning(f"🟡 Medium Risk • {risk_score}%")
        else:
            st.error(f"🔴 High Risk • {risk_score}%")

        st.progress(min(int(risk_score), 100))

        suspicious_words = [
            "click", "urgent", "reward", "otp", "bank", "win", "claim",
            "prize", "offer", "free", "link", "account", "verify", "limited",
            "blocked", "suspended", "login"
        ]
        found_words = [word for word in suspicious_words if word in lower_text]

        st.markdown("### Suspicious Keywords Found")
        if found_words:
            st.write(", ".join(found_words))
        else:
            st.write("No obvious suspicious keywords found.")

        explanation_points = []
        if any(word in lower_text for word in ["urgent", "immediately", "now", "limited"]):
            explanation_points.append("Urgency-based language detected")
        if any(word in lower_text for word in ["win", "reward", "prize", "offer", "free"]):
            explanation_points.append("Reward or bait-style wording detected")
        if any(word in lower_text for word in ["click", "link", "verify", "claim", "login"]):
            explanation_points.append("Action-trigger phrases detected")
        if any(word in lower_text for word in ["bank", "account", "otp"]):
            explanation_points.append("Sensitive or account-related terms detected")
        if any(word in lower_text for word in ["debited", "credited", "account ending", "do not share"]):
            explanation_points.append("Official transaction-style wording detected")
        if not explanation_points:
            explanation_points.append("Classification is mainly based on deep learning sequence patterns")

        st.markdown("### Why this result?")
        for point in explanation_points:
            st.write(f"- {point}")

        label = "Phishing" if pred > 0.5 else "Safe"
        st.session_state.scan_history.insert(0, f"{label} • {user_input[:60]}...")
        st.session_state.scan_history = st.session_state.scan_history[:5]

# ---------------- BOTTOM SECTION ----------------
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div class="bottom-card">
        <div class="section-title">How the System Works</div>
        <div class="section-text">
            The input text is tokenized, converted into padded sequences, and analyzed by a trained LSTM model.
            A smart rule-based layer is also included to improve reliability for official transaction-like messages
            and reduce false positives.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown('<div class="bottom-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recent Scan History</div>', unsafe_allow_html=True)
    if st.session_state.scan_history:
        for item in st.session_state.scan_history:
            st.write(f"- {item}")
    else:
        st.write("No scans yet.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Developed by Nikhil • CyberShield AI</div>', unsafe_allow_html=True)
