
import streamlit as st
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- LOAD FILES ----------------
model = load_model("cybershield_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 255, 255, 0.10), transparent 25%),
            radial-gradient(circle at top right, rgba(0, 102, 255, 0.12), transparent 25%),
            linear-gradient(135deg, #050816 0%, #0b1023 45%, #03060f 100%);
        color: white;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        text-align: center;
        font-weight: 700;
        color: #eaf6ff;
        text-shadow: 0 0 10px rgba(0,255,255,0.45), 0 0 25px rgba(0,102,255,0.35);
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .sub-title {
        text-align: center;
        font-size: 1.05rem;
        color: #b9c7e6;
        margin-bottom: 30px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(0, 255, 255, 0.18);
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.35);
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }

    .stTextArea textarea {
        background: rgba(10, 16, 35, 0.95) !important;
        color: #ffffff !important;
        border-radius: 16px !important;
        border: 1px solid rgba(0, 255, 255, 0.25) !important;
        font-size: 16px !important;
    }

    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid rgba(0,255,255,0.35);
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.75rem 1rem;
        box-shadow: 0 0 20px rgba(0,198,255,0.25);
    }

    .stButton > button:hover {
        transform: scale(1.01);
        border: 1px solid rgba(255,255,255,0.35);
    }

    .safe-box {
        background: rgba(0, 255, 128, 0.10);
        border: 1px solid rgba(0, 255, 128, 0.45);
        padding: 18px;
        border-radius: 18px;
        color: #d8ffe8;
        margin-top: 15px;
        box-shadow: 0 0 18px rgba(0,255,128,0.12);
    }

    .phish-box {
        background: rgba(255, 59, 59, 0.10);
        border: 1px solid rgba(255, 59, 59, 0.45);
        padding: 18px;
        border-radius: 18px;
        color: #ffe3e3;
        margin-top: 15px;
        box-shadow: 0 0 18px rgba(255,59,59,0.14);
    }

    .footer {
        text-align: center;
        margin-top: 35px;
        color: #8ca0c8;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ----------------
st.markdown('<div class="main-title">🛡️ CyberShield AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-Time Phishing Detection Dashboard</div>', unsafe_allow_html=True)

# ---------------- PREDICTION FUNCTION ----------------
def predict_message(text):
    seq = tokenizer.texts_to_sequences([text])
    pad = pad_sequences(seq, maxlen=100)
    pred = model.predict(pad, verbose=0)[0][0]
    return pred

# ---------------- INPUT SECTION ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.write("### Analyze SMS or Email Content")
user_input = st.text_area(
    "Paste your message below:",
    height=180,
    placeholder="Example: Congratulations! You have won 50000 rupees. Click this link now to claim your prize."
)
analyze = st.button("Analyze Threat")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- OUTPUT SECTION ----------------
if analyze:
    if user_input.strip() == "":
        st.warning("Please enter a message first.")
    else:
        pred = predict_message(user_input)

        if pred > 0.5:
            confidence = round(float(pred) * 100, 2)
            st.markdown(
                f"""
                <div class="phish-box">
                    <h3>⚠️ Phishing Detected</h3>
                    <p><b>Threat Confidence:</b> {confidence}%</p>
                    <p>This message contains suspicious patterns often seen in fraudulent or deceptive content.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.progress(min(int(confidence), 100))
        else:
            confidence = round((1 - float(pred)) * 100, 2)
            st.markdown(
                f"""
                <div class="safe-box">
                    <h3>✅ Safe Message</h3>
                    <p><b>Safety Confidence:</b> {confidence}%</p>
                    <p>No strong phishing indicators were detected in this message.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.progress(min(int(confidence), 100))

# ---------------- INFO SECTION ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.write("### How it Works")
st.write("This system uses NLP preprocessing, tokenization, padding, and a deep learning LSTM model to classify text messages as safe or phishing.")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown('<div class="footer">Developed by Nikhil And Team </div>', unsafe_allow_html=True)
