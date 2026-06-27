import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
from datetime import datetime
import hashlib

# Get base directory of the app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="SegmentPro — Customer Intelligence Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Persistent storage file for authentication
AUTH_FILE = ".streamlit/auth_session.json"

# Create .streamlit directory if it doesn't exist
os.makedirs(".streamlit", exist_ok=True)

def save_auth_session():
    auth_data = {
        "authenticated": st.session_state.authenticated,
        "username": st.session_state.username
    }
    with open(AUTH_FILE, "w") as f:
        json.dump(auth_data, f)

def load_auth_session():
    if os.path.exists(AUTH_FILE):
        try:
            with open(AUTH_FILE, "r") as f:
                auth_data = json.load(f)
                return auth_data.get("authenticated", False), auth_data.get("username", None)
        except:
            return False, None
    return False, None

def clear_auth_session():
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)

# Initialize session state
if 'authenticated' not in st.session_state:
    auth_state, username = load_auth_session()
    st.session_state.authenticated = auth_state
    st.session_state.username = username
if 'username' not in st.session_state:
    st.session_state.username = None
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'show_signin' not in st.session_state:
    st.session_state.show_signin = False
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    if username in st.session_state.users:
        return False, "Username already exists"
    st.session_state.users[username] = {
        "email": email,
        "password": hash_password(password)
    }
    return True, "Account created successfully!"

def login_user(username, password):
    if username not in st.session_state.users:
        return False, "Username not found"
    if st.session_state.users[username]["password"] != hash_password(password):
        return False, "Incorrect password"
    return True, "Login successful!"


# ══════════════════════════════════════════════════════════════
#  DUSK AURORA THEME — ORGANIC HIGH-TECH UI
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Cabinet+Grotesk:wght@800;900&family=Space+Mono&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-void:    #0a0b16;
        --bg-base:    #0f1026;
        --bg-card:    rgba(255, 255, 255, 0.02);
        --bg-hover:   rgba(255, 255, 255, 0.05);
        --border-dim: rgba(255, 255, 255, 0.04);
        --border-mid: rgba(255, 255, 255, 0.12);

        /* Sunset Dusk Palette */
        --peach:       #ffb088;
        --coral:       #ff6b6b;
        --emerald:     #66ddaa;
        --mint:        #a7f3d0;
        --orchid:      #bd93f9;
        --lavender:    #e8dff5;
        --sage:        #8bebff;

        /* Glow & Shadows */
        --glow-peach:   0 0 40px rgba(255, 176, 136, 0.12), 0 0 80px rgba(255, 176, 136, 0.04);
        --glow-emerald: 0 0 40px rgba(102, 221, 170, 0.12), 0 0 80px rgba(102, 221, 170, 0.04);
        --glow-coral:   0 0 40px rgba(255, 107, 107, 0.15);
        --shadow-deep:   0 24px 64px rgba(0,0,0,0.5);

        /* Typography Colors */
        --text-primary:   #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted:     #475569;

        /* Gradients */
        --grad-dusk:   linear-gradient(135deg, #ffb088 0%, #ff6b6b 50%, #bd93f9 100%);
        --grad-aurora: linear-gradient(135deg, #ffb088, #66ddaa);
        --grad-coral:  linear-gradient(135deg, #ff6b6b, #ff8c69);
        --grad-emerald: linear-gradient(135deg, #66ddaa, #059669);
        --grad-base:   linear-gradient(160deg, #070814 0%, #0e0f2b 50%, #070814 100%);

        /* Radius */
        --r-sm:  12px;
        --r-md:  20px;
        --r-lg:  28px;
        --r-full:9999px;
    }

    /* ── Global Reset ── */
    * { font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    h1, h2, h3, .brand-name, .hero-title { font-family: 'Cabinet Grotesk', sans-serif !important; }
    code, .mono { font-family: 'Space Mono', monospace !important; }

    .stApp {
        background: var(--bg-void) !important;
        color: var(--text-primary) !important;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    div[data-testid="stDecoration"] { display: none; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-void); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--peach), var(--emerald));
        border-radius: 3px;
    }

    /* ══ KEYFRAMES ══ */
    @keyframes fadeUp   { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
    @keyframes fadeDown { from{opacity:0;transform:translateY(-20px)} to{opacity:1;transform:translateY(0)} }
    @keyframes pulseGlow {
        0%,100%{ box-shadow: 0 0 20px rgba(255,176,136,0.08), 0 0 50px rgba(255,176,136,0.03); }
        50%    { box-shadow: 0 0 35px rgba(255,176,136,0.18), 0 0 70px rgba(255,176,136,0.06); }
    }
    @keyframes floatOrb {
        0%,100%{ transform:translateY(0) scale(1); opacity:0.5; }
        50%    { transform:translateY(-15px) scale(1.03); opacity:0.7; }
    }
    @keyframes borderShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ══ BACKGROUND ORB EFFECTS ══ */
    .stApp::before {
        content:'';
        position: fixed;
        inset: 0;
        background-image:
            radial-gradient(circle at 10% 20%, rgba(255, 176, 136, 0.03) 0%, transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(102, 221, 170, 0.03) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
    }

    /* ══ DUSK HERO ══ */
    .dusk-hero {
        min-height: 55vh;
        background: var(--grad-base);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 80px 24px 60px 24px;
        position: relative;
        overflow: hidden;
        border-radius: 0 0 var(--r-lg) var(--r-lg);
        margin: -6rem -6rem 0 -6rem;
        border-bottom: 1px solid var(--border-dim);
    }
    .dusk-hero::before {
        content:'';
        position: absolute;
        inset: 0;
        background:
            radial-gradient(ellipse at 25% 40%, rgba(255,176,136,0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 75% 60%, rgba(102,221,170,0.05) 0%, transparent 50%);
        animation: floatOrb 10s ease-in-out infinite;
        pointer-events: none;
    }

    /* Hero badge */
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 18px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: var(--r-full);
        color: var(--peach);
        font-size: 0.72em;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 24px;
        animation: fadeDown 0.5s ease-out;
        position: relative; z-index: 2;
    }

    /* Hero icon */
    .hero-icon-wrap {
        position: relative;
        width: 100px; height: 100px;
        margin: 0 auto 28px;
        animation: fadeUp 0.6s ease-out;
        z-index: 2;
    }
    .hero-icon-inner {
        width: 100%; height: 100%;
        border-radius: var(--r-md);
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.8em;
        animation: pulseGlow 4s ease-in-out infinite;
        backdrop-filter: blur(10px);
    }

    /* Hero title */
    .hero-title {
        font-size: clamp(2.5em, 6vw, 4.8em);
        font-weight: 900;
        background: var(--grad-dusk);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -2px;
        line-height: 1.1;
        margin-bottom: 12px;
        position: relative; z-index: 2;
        background-size: 200% auto;
        animation: fadeUp 0.7s ease-out, borderShift 4s ease-in-out infinite;
    }
    .hero-sub {
        font-size: 1.1em;
        color: var(--text-secondary);
        font-weight: 400;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        animation: fadeUp 0.8s ease-out;
        position: relative; z-index: 2;
    }
    .hero-desc {
        font-size: 0.92em;
        color: var(--text-secondary);
        max-width: 500px;
        margin: 0 auto 36px;
        line-height: 1.8;
        opacity: 0.85;
        animation: fadeUp 0.9s ease-out;
        position: relative; z-index: 2;
    }

    /* Feature chips */
    .feature-chips {
        display: flex;
        gap: 8px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 28px;
        position: relative; z-index: 2;
        animation: fadeUp 1s ease-out;
    }
    .chip {
        padding: 7px 16px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: var(--r-full);
        color: var(--text-secondary);
        font-size: 0.78em;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: default;
    }
    .chip:hover {
        background: rgba(255,255,255,0.05);
        border-color: rgba(255,176,136,0.3);
        color: var(--peach);
        transform: translateY(-2px);
    }

    /* ── DASHBOARD NAVBAR ── */
    .dash-nav {
        background: rgba(10,11,22,0.85);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-dim);
        border-radius: var(--r-md);
        padding: 16px 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        animation: fadeDown 0.4s ease-out;
        position: relative;
    }
    .dash-nav::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: var(--grad-dusk);
        background-size: 200% auto;
        animation: borderShift 4s ease-in-out infinite;
        border-radius: var(--r-md) var(--r-md) 0 0;
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .nav-logo {
        width: 38px; height: 38px;
        border-radius: var(--r-sm);
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1em;
    }
    .brand-name {
        font-size: 1.35em;
        font-weight: 800;
        background: var(--grad-dusk);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    .nav-user {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .user-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.02);
        border: 1px solid var(--border-dim);
        border-radius: var(--r-full);
        padding: 6px 14px 6px 6px;
    }
    .user-avatar {
        width: 28px; height: 28px;
        border-radius: 50%;
        background: var(--grad-dusk);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.85em;
        font-weight: 800;
        color: white;
    }
    .user-name {
        font-weight: 600;
        font-size: 0.85em;
        color: var(--text-primary);
    }

    /* ── PAGE HEADER ── */
    .page-header {
        text-align: center;
        margin-bottom: 36px;
        animation: fadeUp 0.4s ease-out;
    }
    .page-header h1 {
        font-size: 2.1em;
        font-weight: 800;
        background: var(--grad-dusk);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }
    .page-header p { color: var(--text-secondary); font-size: 0.9em; opacity: 0.8; }

    /* ── GLASS CARDS ── */
    .glass {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-dim);
        border-radius: var(--r-md);
        padding: 24px;
        transition: all 0.35s ease;
        position: relative;
        overflow: hidden;
    }
    .glass:hover {
        border-color: rgba(255, 176, 136, 0.2);
        background: var(--bg-hover);
        box-shadow: var(--glow-peach);
        transform: translateY(-2px);
    }

    /* ── STAT CARDS ── */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 14px;
        margin: 16px 0;
    }
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border-dim);
        border-radius: var(--r-md);
        padding: 24px 20px;
        text-align: center;
        transition: all 0.35s ease;
        position: relative;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        border-radius: var(--r-md) var(--r-md) 0 0;
    }
    .stat-card.peach::before   { background: var(--grad-dusk); }
    .stat-card.emerald::before { background: var(--grad-emerald); }
    .stat-card.coral::before   { background: var(--grad-coral); }
    .stat-card.orchid::before  { background: var(--orchid); }
    .stat-card:hover {
        transform: translateY(-3px);
        background: var(--bg-hover);
    }
    .stat-card.peach:hover    { border-color: rgba(255, 176, 136, 0.2); box-shadow: var(--glow-peach); }
    .stat-card.emerald:hover  { border-color: rgba(102, 221, 170, 0.2); box-shadow: var(--glow-emerald); }
    .stat-card.coral:hover    { border-color: rgba(255, 107, 107, 0.2); }
    .stat-card.orchid:hover   { border-color: rgba(189, 147, 249, 0.2); }
    .stat-icon { font-size: 1.45em; margin-bottom: 10px; }
    .stat-value {
        font-size: 1.85em;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }
    .stat-label {
        font-size: 0.65em;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        opacity: 0.7;
    }

    /* ── METRIC BOXES ── */
    .metric-box {
        background: var(--bg-card);
        border: 1px solid var(--border-dim);
        border-radius: var(--r-md);
        padding: 18px 24px;
        transition: all 0.3s ease;
        position: relative;
    }
    .metric-box:hover {
        border-color: rgba(255, 176, 136, 0.2);
        transform: translateY(-1px);
        box-shadow: var(--glow-peach);
    }
    .metric-label {
        font-size: 0.65em;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: var(--text-secondary);
        margin-bottom: 6px;
        font-weight: 700;
        opacity: 0.7;
    }
    .metric-value {
        font-size: 1.6em;
        font-weight: 800;
        color: var(--text-primary);
        letter-spacing: -0.5px;
    }

    /* ── SEGMENT RESULT ── */
    .seg-result {
        border-radius: var(--r-md);
        padding: 40px 32px;
        text-align: center;
        animation: fadeUp 0.4s ease-out;
        position: relative;
        overflow: hidden;
    }
    .seg-result::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--grad-dusk);
        background-size: 200% auto;
        animation: borderShift 3s ease-in-out infinite;
    }
    .seg-emoji {
        font-size: 3.5em;
        margin-bottom: 14px;
        filter: drop-shadow(0 4px 16px rgba(255,176,136,0.25));
    }
    .seg-name {
        font-size: 1.95em;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: 6px;
    }
    .seg-type {
        font-size: 0.78em;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: var(--peach);
        margin-bottom: 14px;
    }
    .seg-detail {
        color: var(--text-secondary);
        max-width: 440px;
        margin: 0 auto;
        font-size: 0.9em;
        line-height: 1.7;
    }

    /* ── STRATEGY BOX ── */
    .strategy {
        background: rgba(255,255,255,0.01);
        border: 1px solid rgba(255,176,136,0.12);
        border-radius: var(--r-md);
        padding: 24px 28px;
        margin: 16px 0;
        position: relative;
    }
    .strategy::before {
        content: '';
        position: absolute;
        top: 0; bottom: 0; left: 0;
        width: 3px;
        background: var(--grad-dusk);
        border-radius: 3px 0 0 3px;
    }
    .strategy h4 {
        color: var(--peach);
        font-size: 0.72em;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 8px;
        font-weight: 700;
    }
    .strategy p {
        color: var(--text-primary);
        font-size: 0.95em;
        font-weight: 500;
        line-height: 1.6;
    }

    /* ── RECOMMENDATION ACTION ITEMS ── */
    .rec-item {
        background: var(--bg-card);
        border: 1px solid var(--border-dim);
        border-radius: var(--r-sm);
        padding: 16px 20px;
        margin: 6px 0;
        display: flex;
        align-items: center;
        gap: 14px;
        transition: all 0.3s ease;
    }
    .rec-item:hover {
        border-color: rgba(255, 176, 136, 0.15);
        transform: translateX(4px);
        background: var(--bg-hover);
    }
    .rec-icon {
        width: 38px; height: 38px;
        border-radius: var(--r-sm);
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1em;
        flex-shrink: 0;
    }
    .rec-text { color: var(--text-primary); font-size: 0.9em; line-height: 1.5; }

    /* ── EMPTY PROMPT ── */
    .prompt-empty {
        background: var(--bg-card);
        border: 1px dashed var(--border-mid);
        border-radius: var(--r-md);
        padding: 48px 32px;
        text-align: center;
    }
    .prompt-icon { font-size: 3em; margin-bottom: 16px; opacity: 0.4; }
    .prompt-text { color: var(--text-secondary); font-size: 0.98em; line-height: 1.8; }

    /* ── ABOUT BOX ── */
    .about-card {
        background: var(--bg-card);
        border: 1px solid var(--border-dim);
        border-radius: var(--r-md);
        padding: 28px;
        transition: all 0.3s ease;
    }
    .about-card:hover { border-color: rgba(255, 176, 136, 0.12); }
    .about-card h3 {
        color: var(--peach);
        font-size: 1.1em;
        margin-bottom: 14px;
        font-weight: 700;
    }
    .about-card li { color: var(--text-secondary); margin-bottom: 8px; line-height: 1.7; font-size: 0.9em; }
    .about-card p { color: var(--text-secondary); line-height: 1.7; font-size: 0.9em; }

    /* ── STREAMLIT OVERRIDES ── */

    /* Sliders */
    .stSlider label { color: var(--text-primary) !important; font-weight: 600 !important; font-size: 0.88em !important; }
    .stSlider [role="slider"] {
        background: linear-gradient(135deg, var(--peach), var(--coral)) !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 0 10px rgba(255,176,136,0.3) !important;
    }

    /* Forms */
    div[data-testid="stForm"] {
        background: rgba(15, 16, 38, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid var(--border-dim) !important;
        border-radius: var(--r-md) !important;
        padding: 36px 28px !important;
        box-shadow: var(--shadow-deep) !important;
        position: relative;
    }
    div[data-testid="stForm"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: var(--grad-dusk);
        background-size: 200% auto;
        animation: borderShift 3s ease-in-out infinite;
        border-radius: var(--r-md) var(--r-md) 0 0;
    }
    button[data-testid="stFormSubmitButton"] {
        background: linear-gradient(135deg, var(--peach), var(--coral)) !important;
        border: none !important;
        color: #070814 !important;
        box-shadow: 0 4px 16px rgba(255,176,136,0.2) !important;
        font-weight: 700 !important;
        border-radius: var(--r-sm) !important;
        padding: 10px 20px !important;
    }
    button[data-testid="stFormSubmitButton"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,176,136,0.35) !important;
        filter: brightness(1.05);
    }

    /* Buttons */
    .stButton > button {
        border-radius: var(--r-sm) !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: 1px solid var(--border-dim) !important;
        background: rgba(255,255,255,0.01) !important;
        color: var(--text-primary) !important;
    }
    .stButton > button:hover {
        border-color: rgba(255,176,136,0.2) !important;
        background: rgba(255,176,136,0.03) !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, var(--peach), var(--coral)) !important;
        border: none !important;
        color: #070814 !important;
        box-shadow: 0 4px 16px rgba(255,176,136,0.2) !important;
        font-weight: 700 !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(255,176,136,0.3) !important;
    }

    /* Inputs */
    .stTextInput input {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: var(--r-sm) !important;
        color: var(--text-primary) !important;
        padding: 11px 16px !important;
    }
    .stTextInput input:focus {
        border-color: var(--peach) !important;
        box-shadow: 0 0 10px rgba(255,176,136,0.06) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.01);
        border-radius: var(--r-md);
        padding: 4px;
        gap: 2px;
        border: 1px solid var(--border-dim);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--r-sm);
        color: var(--text-secondary);
        font-weight: 600;
        padding: 10px 18px;
    }
    .stTabs [data-baseweb="tab"]:hover { color: var(--peach); }
    .stTabs [aria-selected="true"] {
        background: rgba(255,176,136,0.05) !important;
        color: var(--peach) !important;
        border-color: transparent !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { background: var(--peach) !important; }

    /* Expanders */
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.01) !important;
        border: 1px solid var(--border-dim) !important;
        border-radius: var(--r-md) !important;
    }

    /* Alerts */
    .stAlert { border-radius: var(--r-sm) !important; }

    /* Footer style */
    .site-footer {
        text-align: center;
        padding: 30px 24px;
        color: var(--text-secondary);
        font-size: 0.8em;
        opacity: 0.8;
        border-top: 1px solid var(--border-dim);
        margin-top: 40px;
    }
    .site-footer span {
        background: var(--grad-dusk);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  LANDING & AUTH PAGES
# ══════════════════════════════════════════════════════════════

def show_landing_page():
    st.markdown("""
    <div class="dusk-hero">
        <div style="position:relative;z-index:2;">
            <div class="hero-badge">🔮 Intelligent Analytics</div>
            <div class="hero-icon-wrap">
                <div class="hero-icon-inner">🛍️</div>
            </div>
            <h1 class="hero-title">SegmentPro</h1>
            <p class="hero-sub">Customer Intelligence Platform</p>
            <p class="hero-desc">
                Harness K-Means Clustering models to profile and target customer behavior groups dynamically.
            </p>
            <div class="feature-chips">
                <span class="chip">🔮 Predictive ML</span>
                <span class="chip">📈 Interactive Visualizations</span>
                <span class="chip">💡 Playbook Recommendations</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1.5])
    with col2:
        if st.button("🔓  Sign In", key="nav_signin_landing", use_container_width=True, type="primary"):
            st.session_state.show_signin = True
            st.rerun()
    with col3:
        if st.button("📝  Sign Up", key="nav_signup_landing", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()


def show_signin_modal():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form(key="signin_form", clear_on_submit=False):
            st.markdown("""
            <div class="auth-head" style="margin-bottom: 20px; text-align: center;">
                <h2 style="font-size: 1.8em; margin-bottom: 4px;">Welcome Back</h2>
                <p style="color: var(--text-secondary); font-size: 0.88em; margin-bottom: 0;">Sign in to your account</p>
            </div>
            """, unsafe_allow_html=True)

            username = st.text_input("👤 Username", placeholder="Enter username", key="signin_user")
            password = st.text_input("🔐 Password", type="password", placeholder="Enter password", key="signin_pass")

            submit = st.form_submit_button("Sign In →", use_container_width=True)
            if submit:
                if username and password:
                    success, message = login_user(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.show_signin = False
                        save_auth_session()
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter both username and password")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📝 Create an Account", use_container_width=True, key="switch_to_signup_from_signin"):
            st.session_state.show_signin = False
            st.session_state.show_signup = True
            st.rerun()


def show_signup_modal():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form(key="signup_form", clear_on_submit=False):
            st.markdown("""
            <div class="auth-head" style="margin-bottom: 20px; text-align: center;">
                <h2 style="font-size: 1.8em; margin-bottom: 4px;">Create Account</h2>
                <p style="color: var(--text-secondary); font-size: 0.88em; margin-bottom: 0;">Join SegmentPro today</p>
            </div>
            """, unsafe_allow_html=True)

            new_username = st.text_input("👤 Username", placeholder="Choose username", key="signup_user")
            new_email    = st.text_input("📧 Email",    placeholder="Enter email address",  key="signup_email")
            new_password = st.text_input("🔐 Password", type="password", placeholder="Password (min 6 chars)", key="signup_pass")
            confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password", key="signup_pass_confirm")

            submit = st.form_submit_button("Sign Up →", use_container_width=True)
            if submit:
                if not new_username or not new_email or not new_password:
                    st.error("Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    success, message = register_user(new_username, new_email, new_password)
                    if success:
                        st.success(message)
                        st.session_state.show_signup = False
                        st.session_state.show_signin = True
                        st.rerun()
                    else:
                        st.error(message)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Sign In", use_container_width=True, key="switch_to_signin"):
            st.session_state.show_signup = False
            st.session_state.show_signin = True
            st.rerun()


# ══════════════════════════════════════════════════════════════
#  MODEL & DATA LOADING
# ══════════════════════════════════════════════════════════════

@st.cache_resource
def load_model():
    try:
        model_path = os.path.join(BASE_DIR, 'models', 'kmeans_model.pkl')
        info_path  = os.path.join(BASE_DIR, 'models', 'model_info.json')
        model = joblib.load(model_path)
        with open(info_path) as f:
            info = json.load(f)
        return model, info
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        return None, None

@st.cache_data
def load_dataset():
    try:
        dataset_path = os.path.join(BASE_DIR, 'dataset', 'Mall_Customers.csv')
        df = pd.read_csv(dataset_path)
        return df
    except Exception as e:
        st.error(f"Failed to load dataset: {str(e)}")
        return None


# ══════════════════════════════════════════════════════════════
#  ROUTING: LANDING vs DASHBOARD
# ══════════════════════════════════════════════════════════════

if not st.session_state.authenticated:
    if not st.session_state.show_signin and not st.session_state.show_signup:
        show_landing_page()
    elif st.session_state.show_signin:
        show_signin_modal()
    elif st.session_state.show_signup:
        show_signup_modal()
    st.stop()


# ══════════════════════════════════════════════════════════════
#  AUTHENTICATED DASHBOARD
# ══════════════════════════════════════════════════════════════

user_initial = st.session_state.username[0].upper() if st.session_state.username else "U"

# ── Navbar ──
st.markdown(f"""
<div class="dash-nav">
    <div class="nav-brand">
        <div class="nav-logo">🛍️</div>
        <div class="brand-name">SegmentPro</div>
    </div>
    <div class="nav-user">
        <div class="user-pill">
            <div class="user-avatar">{user_initial}</div>
            <span class="user-name">{st.session_state.username}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Logout ──
logout_col1, logout_col2 = st.columns([5, 1])
with logout_col2:
    if st.button("🚪 Logout", key="navbar_logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        clear_auth_session()
        st.rerun()

# ── Load Model ──
try:
    kmeans, model_info = load_model()
    model_loaded = kmeans is not None
    if not model_loaded:
        st.error("Error: Failed to load KMeans model. Check 'models/kmeans_model.pkl'.")
except Exception as e:
    kmeans = None
    model_loaded = False
    st.error(f"Error: {e}")

# ── Load Dataset ──
dataset = load_dataset()

# ── Page Header ──
st.markdown("""
<div class="page-header">
    <h1>🛍️ Customer Segmentation Dashboard</h1>
    <p>Real-time customer clustering analysis based on unsupervised machine learning</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Input Controls ──
slider_col1, slider_col2 = st.columns(2)
with slider_col1:
    income = st.slider(
        "💰 Annual Income (k₹)",
        min_value=10, max_value=150, value=60, step=5,
        help="Select annual income in thousands"
    )
with slider_col2:
    spending = st.slider(
        "🛍️ Spending Score (1–100)",
        min_value=1, max_value=100, value=50,
        help="Shopping activity and frequency score"
    )

st.markdown("---")

# ── Profile Metrics ──
income_level  = "High"   if income  >= 100 else "Medium" if income  >= 50 else "Low"
spending_level= "High"   if spending >= 60  else "Medium" if spending >= 40 else "Low"

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Annual Income</div>
        <div class="metric-value" style="color:var(--peach);">₹{income}k</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Spending Score</div>
        <div class="metric-value" style="color:var(--coral);">{spending}/100</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Profile Class</div>
        <div class="metric-value" style="color:var(--emerald);">{income_level} / {spending_level}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Predict Button ──
btn_c1, btn_c2, btn_c3 = st.columns([1, 2, 1])
with btn_c2:
    predict_btn = st.button(
        "🔮  Analyze & Profile Customer",
        use_container_width=True,
        key="find_segment_main",
        type="primary"
    )

st.markdown("---")

# ── Segment Definitions ──
segments = {
    0: {
        "name": "Premium Customer", "emoji": "💎",
        "desc": "High income, high spender",
        "strategy": "Send VIP offers, luxury brand promotions, and exclusive early-access invites.",
        "color": "#ffb088",
        "details": "Your most valuable customers — high purchasing power and strong engagement.",
        "gradient": "linear-gradient(135deg, rgba(255,176,136,0.06), rgba(255,107,107,0.02))",
        "border": "rgba(255,176,136,0.2)"
    },
    1: {
        "name": "Careful Spender", "emoji": "💰",
        "desc": "High income, low spender",
        "strategy": "Send value-for-money deals, quality comparisons, and smart savings alerts.",
        "color": "#66ddaa",
        "details": "Price-conscious high earners who value quality and meaningful discounts.",
        "gradient": "linear-gradient(135deg, rgba(102,221,170,0.06), rgba(167,243,208,0.02))",
        "border": "rgba(102,221,170,0.2)"
    },
    2: {
        "name": "Impulsive Buyer", "emoji": "🛍️",
        "desc": "Low income, high spender",
        "strategy": "Send flash sale alerts, limited-time offers, and trending product notifications.",
        "color": "#ff6b6b",
        "details": "Enthusiastic shoppers with limited income — highly responsive to promotions.",
        "gradient": "linear-gradient(135deg, rgba(255,107,107,0.06), rgba(255,140,105,0.02))",
        "border": "rgba(255,107,107,0.2)"
    },
    3: {
        "name": "Budget Customer", "emoji": "💚",
        "desc": "Low income, low spender",
        "strategy": "Send heavy discount coupons, clearance sale alerts, and budget bundle offers.",
        "color": "#8bebff",
        "details": "Cost-conscious customers seeking the best value for every rupee.",
        "gradient": "linear-gradient(135deg, rgba(139,235,255,0.06), rgba(102,221,170,0.02))",
        "border": "rgba(139,235,255,0.2)"
    },
    4: {
        "name": "Average Customer", "emoji": "📊",
        "desc": "Medium income, medium spender",
        "strategy": "Send loyalty points, regular newsletters, and seasonal promotion offers.",
        "color": "#bd93f9",
        "details": "Balanced customers with moderate income and steady spending habits.",
        "gradient": "linear-gradient(135deg, rgba(189,147,249,0.06), rgba(232,223,245,0.02))",
        "border": "rgba(189,147,249,0.2)"
    }
}

# ══════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔮 Find Segment",
    "📈 Visualizations",
    "📊 Data Analysis",
    "💡 Recommendations",
    "ℹ️ About"
])

# ── TAB 1: Segment Finder ──
with tab1:
    st.markdown("### 🔮 Customer Segment Results")
    st.markdown("---")

    if predict_btn and model_loaded:
        input_data = np.array([[income, spending]])
        cluster    = kmeans.predict(input_data)[0]
        seg        = segments.get(cluster, {})

        st.markdown(f"""
        <div class="seg-result" style="background:{seg['gradient']}; border:1px solid {seg['border']};">
            <div class="seg-emoji">{seg['emoji']}</div>
            <div class="seg-name" style="color:{seg['color']};">{seg['name']}</div>
            <div class="seg-type">{seg['desc']}</div>
            <div class="seg-detail">{seg['details']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        d1, d2, d3 = st.columns(3)
        with d1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Assigned Segment</div>
                <div class="metric-value" style="font-size:1.05em;color:{seg['color']};">{seg['emoji']} {seg['name']}</div>
            </div>""", unsafe_allow_html=True)
        with d2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Behavior profile</div>
                <div class="metric-value" style="font-size:1.05em;">{seg['desc']}</div>
            </div>""", unsafe_allow_html=True)
        with d3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Cluster number</div>
                <div class="metric-value" style="font-size:1.05em; color:var(--peach);">K-Means Group {cluster}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"""
        <div class="strategy">
            <h4>📢 Recommended Marketing Strategy</h4>
            <p>{seg['strategy']}</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔍 Detailed Segment Analytics"):
            ac1, ac2 = st.columns(2)
            with ac1:
                st.metric("Cluster Number", cluster)
            with ac2:
                st.metric("Estimated Segment Size", "~40 customers")
            st.markdown(f"""
            **Customer Characteristics:**
            - Income Level: {'High' if income >= 100 else 'Medium' if income >= 50 else 'Low'}
            - Spending Behavior: {'Frequent' if spending >= 60 else 'Moderate' if spending >= 40 else 'Minimal'}
            - Purchase Power Index: {income * (spending / 100):.0f}k
            """)

    elif not predict_btn:
        st.markdown("""
        <div class="prompt-empty">
            <div class="prompt-icon">🔮</div>
            <div class="prompt-text">Adjust the sliders above and click <strong>"Analyze & Profile Customer"</strong> to discover your customer profile.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📌 Example Segments")
        ex1, ex2 = st.columns(2)
        with ex1:
            st.markdown("""
            <div class="glass" style="padding: 20px;">
                <h4 style="color:var(--peach); font-size:1em; margin-bottom:8px;">💎 Premium Customer</h4>
                <p style="color:var(--text-secondary); font-size:0.85em; margin:0;">Income: ₹120k+ · Score: 80+<br>VIP and luxury product marketing</p>
            </div>""", unsafe_allow_html=True)
        with ex2:
            st.markdown("""
            <div class="glass" style="padding: 20px;">
                <h4 style="color:var(--emerald); font-size:1em; margin-bottom:8px;">💰 Careful Spender</h4>
                <p style="color:var(--text-secondary); font-size:0.85em; margin:0;">Income: ₹100k+ · Score: &lt;40<br>High-end value-focused deals</p>
            </div>""", unsafe_allow_html=True)


# ── TAB 2: Visualizations ──
with tab2:
    st.markdown("### 📈 Visualizations & Insights")

    images_path = os.path.join(BASE_DIR, 'images')
    clusters_img = os.path.join(images_path, 'clusters.png')

    if os.path.exists(clusters_img):
        st.markdown("#### 🎯 Customer Clusters")
        st.image(clusters_img, caption='2D Plot — Customer Segments (Income vs Spending Score)', use_container_width=True)
        st.markdown("---")

        st.markdown("""
        <div class="stat-grid">
            <div class="stat-card peach">
                <div class="stat-icon">👥</div>
                <div class="stat-value">200</div>
                <div class="stat-label">Total Customers</div>
            </div>
            <div class="stat-card emerald">
                <div class="stat-icon">🎯</div>
                <div class="stat-value">5</div>
                <div class="stat-label">Clusters</div>
            </div>
            <div class="stat-card coral">
                <div class="stat-icon">📐</div>
                <div class="stat-value">2</div>
                <div class="stat-label">Features</div>
            </div>
            <div class="stat-card orchid">
                <div class="stat-icon">⚙️</div>
                <div class="stat-value">K=5</div>
                <div class="stat-label">Optimal K</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📈 Detailed Analysis")
        viz1, viz2 = st.columns(2)
        with viz1:
            st.markdown("##### 📉 Elbow Method")
            elbow_img = os.path.join(images_path, 'elbow_curve.png')
            if os.path.exists(elbow_img):
                st.image(elbow_img, caption='Elbow Curve — Optimal K=5', use_container_width=True)
        with viz2:
            st.markdown("##### 📊 Feature Distributions")
            dist_img = os.path.join(images_path, 'distributions.png')
            if os.path.exists(dist_img):
                st.image(dist_img, caption='Income & Spending Score Distributions', use_container_width=True)
    else:
        st.warning("⚠️ Visualization images not found in the images/ folder.")


# ── TAB 3: Data Analysis ──
with tab3:
    st.markdown("### 📊 Data Analysis")

    if dataset is not None:
        st.markdown(f"""
        <div class="stat-grid">
            <div class="stat-card peach">
                <div class="stat-icon">📋</div>
                <div class="stat-value">{len(dataset)}</div>
                <div class="stat-label">Total Records</div>
            </div>
            <div class="stat-card emerald">
                <div class="stat-icon">📊</div>
                <div class="stat-value">{len(dataset.columns)}</div>
                <div class="stat-label">Columns</div>
            </div>
            <div class="stat-card coral">
                <div class="stat-icon">💰</div>
                <div class="stat-value">₹{dataset['Annual Income (k$)'].mean():.0f}k</div>
                <div class="stat-label">Avg Income</div>
            </div>
            <div class="stat-card orchid">
                <div class="stat-icon">🛍️</div>
                <div class="stat-value">{dataset['Spending Score (1-100)'].mean():.0f}</div>
                <div class="stat-label">Avg Spending</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        with st.expander("📋 View Dataset Sample", expanded=False):
            st.dataframe(dataset.head(10), use_container_width=True)

        st.markdown("### 📈 Statistical Summary")
        s1, s2 = st.columns(2)
        with s1:
            st.markdown("**Income Statistics (k₹)**")
            st.write(dataset['Annual Income (k$)'].describe())
        with s2:
            st.markdown("**Spending Score Statistics**")
            st.write(dataset['Spending Score (1-100)'].describe())

        st.markdown("---")
        st.markdown("### 🔍 Segment Distribution")
        if 'Cluster' in dataset.columns:
            cluster_counts = dataset['Cluster'].value_counts().sort_index()
            st.bar_chart(cluster_counts)
    else:
        st.warning("Dataset not available!")


# ── TAB 4: Recommendations ──
with tab4:
    st.markdown("### 💡 Personalized Recommendations")

    if predict_btn and model_loaded:
        input_data = np.array([[income, spending]])
        cluster    = kmeans.predict(input_data)[0]

        recommendations = {
            0: {
                "title": "💎 Premium Customer Playbook",
                "tips": [
                    ("🎁", "Exclusive Early Access to new premium collections"),
                    ("✨", "VIP Membership with priority customer service"),
                    ("💳", "Premium loyalty points on every purchase"),
                    ("🛍️", "Invitations to exclusive appreciation events"),
                    ("📦", "Complimentary shipping on all orders"),
                ],
                "target": "High-value customer retention"
            },
            1: {
                "title": "💰 Careful Spender Playbook",
                "tips": [
                    ("💰", "Smart Deals — best price alerts & comparisons"),
                    ("📊", "Detailed quality vs. price analysis reports"),
                    ("🏷️", "Bulk discount offers for larger purchases"),
                    ("📧", "Curated newsletter of best-value items"),
                    ("🎯", "Early notification of seasonal sales events"),
                ],
                "target": "Increase purchase frequency"
            },
            2: {
                "title": "🛍️ Impulsive Buyer Playbook",
                "tips": [
                    ("⚡", "Daily flash sales and limited-time deals"),
                    ("🎪", "Exclusive limited-edition drops"),
                    ("🔔", "Instant push alerts for trending products"),
                    ("🎁", "Attractive bundle deals and combos"),
                    ("⭐", "Curated 'Hot This Week' collections"),
                ],
                "target": "Maximize purchase frequency"
            },
            3: {
                "title": "💚 Budget Customer Playbook",
                "tips": [
                    ("🏷️", "Consistent budget-friendly daily deals"),
                    ("📱", "Exclusive discount codes and vouchers"),
                    ("💵", "Best bang-for-buck product bundles"),
                    ("🎯", "Student / Senior special discounts"),
                    ("💳", "Flexible payment plans and EMI options"),
                ],
                "target": "Build loyalty and repeat purchases"
            },
            4: {
                "title": "📊 Average Customer Playbook",
                "tips": [
                    ("🎟️", "Earn and redeem loyalty points easily"),
                    ("🎁", "Targeted seasonal promotions"),
                    ("📧", "Personalized product recommendations"),
                    ("🤝", "Referral rewards for bringing friends"),
                    ("⭐", "Growing member benefits with engagement"),
                ],
                "target": "Gradual value increase"
            }
        }

        rec = recommendations.get(cluster, {})
        st.markdown(f"#### {rec.get('title')}")
        st.markdown(f"""
        <div class="strategy">
            <h4>🎯 Goal</h4>
            <p>{rec.get('target')}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 📌 Action Items")
        for icon, text in rec.get('tips', []):
            st.markdown(f"""
            <div class="rec-item">
                <div class="rec-icon">{icon}</div>
                <div class="rec-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="prompt-empty">
            <div class="prompt-icon">💡</div>
            <div class="prompt-text">Click <strong>"Analyze & Profile Customer"</strong> first to unlock personalized recommendations.</div>
        </div>
        """, unsafe_allow_html=True)


# ── TAB 5: About ──
with tab5:
    st.markdown("### ℹ️ About This Application")

    ab1, ab2 = st.columns([2, 1])
    with ab1:
        st.markdown("""
        <div class="about-card">
            <h3>🛍️ Customer Segmentation Analysis</h3>
            <p>
                This application uses <strong>K-Means Clustering</strong> to segment customers into
                distinct groups based on their purchasing behavior and income levels, enabling
                targeted marketing strategies for each segment.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <h3>🚀 Key Features</h3>
            <ul>
                <li><strong>🔮 Segment Finder</strong> — Real-time customer classification</li>
                <li><strong>📈 Visual Analytics</strong> — Interactive cluster visualizations</li>
                <li><strong>📊 Data Exploration</strong> — Comprehensive dataset statistics</li>
                <li><strong>💡 Smart Recommendations</strong> — Tailored marketing strategies</li>
                <li><strong>🎯 Actionable Insights</strong> — Data-driven business decisions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card">
            <h3>👥 The 5 Customer Segments</h3>
            <ul>
                <li><strong>💎 Premium</strong> — High income, high spenders</li>
                <li><strong>💰 Careful</strong> — High income, low spenders</li>
                <li><strong>🛍️ Impulsive</strong> — Low income, high spenders</li>
                <li><strong>💚 Budget</strong> — Low income, low spenders</li>
                <li><strong>📊 Average</strong> — Medium income & spending</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with ab2:
        st.markdown("""
        <div class="about-card" style="text-align:center;">
            <h3>📋 Project Info</h3>
            <p><strong>Company:</strong> SkillCraft Technology</p>
            <p><strong>Program:</strong> ML Internship</p>
            <p><strong>Task:</strong> #02 — K-Means Clustering</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="about-card" style="text-align:center;">
            <h3>📊 Statistics</h3>
            <div class="stat-grid" style="grid-template-columns:1fr 1fr; gap:10px; margin-top:14px;">
                <div class="stat-card peach" style="padding:14px;">
                    <div class="stat-value" style="font-size:1.3em;">200</div>
                    <div class="stat-label" style="font-size:0.65em;">Customers</div>
                </div>
                <div class="stat-card emerald" style="padding:14px;">
                    <div class="stat-value" style="font-size:1.3em;">5</div>
                    <div class="stat-label" style="font-size:0.65em;">Clusters</div>
                </div>
                <div class="stat-card coral" style="padding:14px;">
                    <div class="stat-value" style="font-size:1.3em;">2</div>
                    <div class="stat-label" style="font-size:0.65em;">Features</div>
                </div>
                <div class="stat-card orchid" style="padding:14px;">
                    <div class="stat-value" style="font-size:1.3em;">K=5</div>
                    <div class="stat-label" style="font-size:0.65em;">Optimal</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    with st.expander("🔧 Technical Stack"):
        st.markdown("""
        - **Language:** Python 3.x
        - **ML Library:** Scikit-learn (K-Means)
        - **Data Processing:** Pandas, NumPy
        - **Web Framework:** Streamlit
        - **Visualization:** Matplotlib, Seaborn
        - **Model Serialization:** Joblib
        """)

    with st.expander("📚 Learn More"):
        st.markdown("""
        - **K-Means Clustering:** Unsupervised learning algorithm for grouping similar data points
        - **Elbow Method:** Technique to find optimal cluster count by plotting inertia
        - **Customer Segmentation:** Market strategy to group customers for targeted marketing
        - **Personalization:** Tailor offerings based on each customer's predicted segment
        """)


# ── Footer ──
st.markdown("---")
st.markdown("""
<div class="site-footer">
    Built with ❤️ using <span>Streamlit</span> · SkillCraft Technology Internship<br>
    <span style="font-size:0.85em;">© 2026 SegmentPro — Customer Intelligence Platform v7.0</span>
</div>
""", unsafe_allow_html=True)