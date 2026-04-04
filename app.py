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

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(147, 51, 234, 0.10), transparent 25%),
        radial-gradient(circle at bottom right, rgba(168, 85, 247, 0.12), transparent 25%),
        linear-gradient(135deg, #faf7ff 0%, #f5f0ff 50%, #ffffff 100%);
    color: #1e1b4b;
}

[data-testid="stHeader"] {
    background: rgba(255,255,255,0);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

.hero-box, .section-card {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(147, 51, 234, 0.15);
    border-radius: 28px;
    padding: 28px;
    box-shadow: 0 10px 30px rgba(147, 51, 234, 0.08);
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.4rem;
    font-weight: 800;
    color: #6d28d9;
    margin-bottom: 10px;
}

.hero-sub {
    font-size: 1.08rem;
    color: #4338ca;
    line-height: 1.7;
    max-width: 900px;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #4c1d95;
    margin-bottom: 10px;
}

.card-text {
    color: #4338ca;
    line-height: 1.7;
    font-size: 0.98rem;
}

.metric-pill {
    display: inline-block;
    background: rgba(147, 51, 234, 0.08);
    border: 1px solid rgba(147, 51, 234, 0.15);
    color: #6d28d9;
    padding: 10px 16px;
    border-radius: 999px;
    margin-right: 10px;
    margin-top: 8px;
    font-size: 0.92rem;
    font-weight: 600;
}

.stTextArea label {
    color: #4c1d95 !important;
    font-weight: 600 !important;
}

.stTextArea textarea {
    background: rgba(255,255,255,0.95) !important;
    color: #1e1b4b !important;
    border-radius: 18px !important;
    border: 1px solid rgba(147, 51, 234, 0.20) !important;
    font-size: 17px !important;
    min-height: 220px !important;
}

.stButton > button {
    width: 100%;
    border-radius: 16px;
    border: none;
    background: linear-gradient(90deg, #9333ea 0%, #7c3aed 100%);
    color: white;
    font-weight: 700;
    font-size: 1.05rem;
    padding: 0.9rem 1rem;
    box-shadow: 0 8px 25px rgba(147, 51, 234, 0.18);
}

.small-stat {
    background: rgba(147, 51, 234, 0.06);
    border: 1px solid rgba(147, 51, 234, 0.15);
    border-radius: 18px;
    padding: 16px;
    margin-top: 12px;
    color: #5b21b6;
}

.sample-box {
    background: rgba(255,255,255,0.75);
    border: 1px dashed rgba(147, 51, 234, 0.20);
    border-radius: 18px;
    padding: 16px;
    margin-top: 12px;
    color: #4338ca;
}

.result-safe {
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.18);
    border-radius: 22px;
    padding: 24px;
    margin-top: 10px;
}

.result-phish {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.18);
    border-radius: 22px;
    padding: 24px;
    margin-top: 10px;
}

.result-title {
    font-size: 1.4rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.result-text {
    font-size: 1rem;
    color: #312e81;
    line-height: 1.7;
}

.footer {
    text-align: center;
    margin-top: 28px;
    padding: 20px;
    color: #6d28d9;
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
        Natural Language Processing and Deep Learning.
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
    st.markdown('<div class="card-text">Paste any SMS or email content below and let CyberShield AI analyze it.</div>', unsafe_allow_html=True)

    user_input = st.text_area(
        "Enter SMS or Email Message",
        placeholder="Example: Congratulations! You have won 50000 rupees. Click now to claim your reward."
    )

    analyze = st.button("Analyze Message Threat")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="section-card">
        <div class="card-title">Threat Intelligence Panel</div>
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

        if pred > 0.5:
            st.markdown(f"""
            <div class="result-phish">
                <div class="result-title">⚠️ Phishing Threat Detected</div>
                <div class="result-text">
                    <b>Threat Confidence:</b> {risk_score}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            safe_score = round((1 - float(pred)) * 100, 2)
            st.markdown(f"""
            <div class="result-safe">
                <div class="result-title">✅ Message Appears Safe</div>
                <div class="result-text">
                    <b>Safety Confidence:</b> {safe_score}%
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

        label = "Phishing" if pred > 0.5 else "Safe"
        st.session_state.scan_history.insert(0, f"{label} • {user_input[:60]}...")
        st.session_state.scan_history = st.session_state.scan_history[:5]

# ---------------- BOTTOM ----------------
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="section-card">
        <div class="card-title">How the System Works</div>
        <div class="card-text">
            Uses NLP preprocessing, tokenization, sequence padding, LSTM prediction,
            and smart rule-based validation.
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
