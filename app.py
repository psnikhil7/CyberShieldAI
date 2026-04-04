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

    # Safe official bank alert
    if official_bank_signals >= 2 and phishing_signals == 0:
        return 0.10

    # Strong phishing-style message
    if phishing_signals >= 2:
        return 0.90

    # Otherwise use ML model
    seq = tokenizer.texts_to_sequences([text])
    pad = pad_sequences(seq, maxlen=100)
    pred = model.predict(pad, verbose=0)[0][0]
    return float(pred)

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(0, 198, 255, 0.12), transparent 20%),
        radial-gradient(circle at 90% 10%, rgba(0, 114, 255, 0.14), transparent 22%),
        radial-gradient(circle at 50% 100%, rgba(0, 255, 170, 0.08), transparent 25%),
        linear-gradient(135deg, #030711 0%, #081120 45%, #02050d 100%);
    color: #ffffff;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

.hero-box {
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(0, 198, 255, 0.22);
    border-radius: 28px;
    padding: 34px 34px 26px 34px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    backdrop-filter: blur(12px);
    margin-bottom: 22px;
}

.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.05;
    margin-bottom: 10px;
    color: #f3fbff;
    text-shadow: 0 0 10px rgba(0,198,255,0.25), 0 0 24px rgba(0,114,255,0.18);
}

.hero-sub {
    font-size: 1.1rem;
    color: #bfd0f2;
    line-height: 1.7;
    max-width: 900px;
}

.section-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.28);
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f2f7ff;
    margin-bottom: 10px;
}

.card-text {
    color: #b8c7e4;
    line-height: 1.7;
    font-size: 0.98rem;
}

.metric-pill {
    display: inline-block;
    background: rgba(0,198,255,0.10);
    border: 1px solid rgba(0,198,255,0.20);
    color: #dff8ff;
    padding: 10px 16px;
    border-radius: 999px;
    margin-right: 10px;
    margin-top: 8px;
    font-size: 0.92rem;
    font-weight: 600;
}

.stTextArea label {
    color: #e9f2ff !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}

.stTextArea textarea {
    background: rgba(6, 14, 28, 0.95) !important;
    color: #ffffff !important;
    border-radius: 18px !important;
    border: 1px solid rgba(0,198,255,0.25) !important;
    font-size: 17px !important;
    min-height: 220px !important;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
}

.stButton > button {
    width: 100%;
    border-radius: 16px;
    border: none;
    background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
    color: white;
    font-weight: 700;
    font-size: 1.05rem;
    padding: 0.9rem 1rem;
    box-shadow: 0 8px 25px rgba(0,198,255,0.28);
}

.stButton > button:hover {
    filter: brightness(1.08);
    transform: translateY(-1px);
}

.result-safe {
    background: linear-gradient(135deg, rgba(0,255,140,0.12), rgba(0,255,140,0.05));
    border: 1px solid rgba(0,255,140,0.30);
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0,255,140,0.08);
    margin-top: 10px;
}

.result-phish {
    background: linear-gradient(135deg, rgba(255,70,70,0.14), rgba(255,70,70,0.05));
    border: 1px solid rgba(255,70,70,0.32);
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(255,70,70,0.10);
    margin-top: 10px;
}

.result-title {
    font-size: 1.4rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.result-text {
    font-size: 1rem;
    color: #e9efff;
    line-height: 1.7;
}

.sample-box {
    background: rgba(255,255,255,0.04);
    border: 1px dashed rgba(255,255,255,0.16);
    border-radius: 18px;
    padding: 16px;
    margin-top: 12px;
    color: #dbe7ff;
    font-size: 0.96rem;
    line-height: 1.6;
}

.small-stat {
    background: rgba(0,198,255,0.08);
    border: 1px solid rgba(0,198,255,0.18);
    border-radius: 18px;
    padding: 16px;
    margin-top: 12px;
    color: #eaf7ff;
}

.footer {
    text-align: center;
    margin-top: 28px;
    padding: 20px;
    color: #8fa5d1;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">🛡️ CyberShield AI</div>
    <div class="hero-sub">
        AI-Powered Phishing Threat Intelligence Platform for analyzing SMS and email content using
        Natural Language Processing and Deep Learning. The system identifies suspicious wording,
        deceptive urgency, reward bait, and fraud-like message behavior in real time.
    </div>
    <div>
        <span class="metric-pill">NLP Preprocessing</span>
        <span class="metric-pill">LSTM Deep Learning</span>
        <span class="metric-pill">Hybrid Smart Detection</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- LAYOUT ----------------
left, right = st.columns([1.45, 1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Threat Analysis Console</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-text">Paste any SMS or email content below and let CyberShield AI evaluate whether the message appears safe or potentially phishing-related.</div>',
        unsafe_allow_html=True
    )

    user_input = st.text_area(
        "Enter SMS or Email Message",
        placeholder="Example: Congratulations! You have won 50000 rupees. Click the link now to claim your reward."
    )

    analyze = st.button("Analyze Message Threat")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="section-card">
        <div class="card-title">Threat Intelligence Panel</div>
        <div class="card-text">
            The system checks for suspicious features such as urgency, fake rewards, risky action phrases,
            fraud-oriented communication style, and official transaction-message patterns.
        </div>
        <div class="small-stat"><b>Model Accuracy:</b> 98%+</div>
        <div class="small-stat"><b>Architecture:</b> Embedding + LSTM</div>
        <div class="small-stat"><b>Dataset Size:</b> 5572 messages</div>
       <div class="sample-box">
    <b>Phishing example:</b><br>
    Congratulations! You have won 50000 rupees. Click now to claim your reward.
</div>

<div class="sample-box">
    <b>Safe example:</b><br>
    Hi bro, meeting is at 5 pm tomorrow. Please be on time.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
if analyze:
    if user_input.strip() == "":
        st.warning("Please enter a message before analysis.")
    else:
        pred = predict_message(user_input)
        risk_score = round(float(pred) * 100, 2)
        lower_text = user_input.lower()

        suspicious_words = [
            "click", "urgent", "reward", "otp", "bank", "win", "claim",
            "prize", "offer", "free", "link", "account", "verify", "limited",
            "blocked", "suspended", "login"
        ]
        found_words = [word for word in suspicious_words if word in lower_text]

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
            explanation_points.append("Classification is based mainly on learned text patterns from the deep learning model")

        if pred > 0.5:
            st.markdown(f"""
            <div class="result-phish">
                <div class="result-title">⚠️ Phishing Threat Detected</div>
                <div class="result-text">
                    <b>Threat Confidence:</b> {risk_score}%<br><br>
                    This message appears suspicious and contains patterns commonly associated with
                    phishing, deceptive intent, or fraudulent communication.
                </div>
            </div>
            """, unsafe_allow_html=True)
            display_score = risk_score
        else:
            safe_score = round((1 - float(pred)) * 100, 2)
            st.markdown(f"""
            <div class="result-safe">
                <div class="result-title">✅ Message Appears Safe</div>
                <div class="result-text">
                    <b>Safety Confidence:</b> {safe_score}%<br><br>
                    The system did not detect strong phishing indicators in this message. Based on the
                    learned sequence patterns and smart rule validation, it appears to be non-malicious.
                </div>
            </div>
            """, unsafe_allow_html=True)
            display_score = risk_score

        st.markdown("### Threat Meter")
        if display_score < 30:
            st.success(f"🟢 Low Risk • {display_score}%")
        elif display_score < 70:
            st.warning(f"🟡 Medium Risk • {display_score}%")
        else:
            st.error(f"🔴 High Risk • {display_score}%")

        st.progress(min(int(display_score), 100))

        st.markdown("### Suspicious Keywords Found")
        if found_words:
            st.write(", ".join(found_words))
        else:
            st.write("No obvious suspicious keywords found.")

        st.markdown("### Why this result?")
        for point in explanation_points:
            st.write(f"- {point}")

        label = "Phishing" if pred > 0.5 else "Safe"
        st.session_state.scan_history.insert(0, f"{label} • {user_input[:60]}...")
        st.session_state.scan_history = st.session_state.scan_history[:5]

# ---------------- BOTTOM SECTION ----------------
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="section-card">
        <div class="card-title">How the System Works</div>
        <div class="card-text">
            The message is cleaned and tokenized, converted into padded sequences, and processed by a
            trained LSTM network. A smart rule-based validation layer is also added to improve reliability
            for official transaction alerts and reduce false positives.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Recent Scan History</div>', unsafe_allow_html=True)
    if st.session_state.scan_history:
        for item in st.session_state.scan_history:
            st.write(f"- {item}")
    else:
        st.write("No scans yet.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Developed by Nikhil • CyberShield AI</div>', unsafe_allow_html=True)
