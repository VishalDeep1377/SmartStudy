import streamlit as st
import requests
import os
import re
import base64
from dotenv import load_dotenv

load_dotenv()

# ─── Load Custom Logo ──────────────────────────────────────────────────────────
LOGO_HTML = '<div class="nav-icon">📚</div>'
for logo_file in ["logo.png.png", "logo.png", "logo.jpg"]:
    if os.path.exists(logo_file):
        try:
            with open(logo_file, "rb") as f:
                b64_str = base64.b64encode(f.read()).decode()
            LOGO_HTML = f'<img src="data:image/png;base64,{b64_str}" style="width:34px; height:34px; border-radius:8px; object-fit:cover; box-shadow:0 0 12px rgba(6,182,212,0.35);" />'
            break
        except Exception:
            pass

st.set_page_config(
    page_title="Smart Study Notes Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body { font-family: 'Plus Jakarta Sans', sans-serif; }

/* ── Animated Mesh Background ── */
.stApp {
    background: #020817;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

/* Orb blobs */
.stApp::before {
    content: '';
    position: fixed;
    top: -20%;
    left: -10%;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(6,182,212,0.18) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    animation: drift1 18s ease-in-out infinite alternate;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -10%;
    right: -5%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    animation: drift2 22s ease-in-out infinite alternate;
}
@keyframes drift1 { 0% { transform: translate(0,0) scale(1); } 100% { transform: translate(80px,60px) scale(1.15); } }
@keyframes drift2 { 0% { transform: translate(0,0) scale(1); } 100% { transform: translate(-60px,-80px) scale(1.1); } }

/* Additional orb (mid right) via injected div */
.orb-mid {
    position: fixed;
    top: 40%;
    right: 15%;
    width: 450px;
    height: 450px;
    background: radial-gradient(circle, rgba(16,185,129,0.10) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    animation: drift1 26s ease-in-out infinite alternate-reverse;
}

/* ── Hide Streamlit chrome & remove ALL extra bottom padding & scroll gaps ── */
#MainMenu, footer, header, .stDeployButton, 
[data-testid="stToolbar"], 
[data-testid="stBottom"], 
[data-testid="stBottomBlockContainer"],
.stBottom, 
header[data-testid="stHeader"],
footer[data-testid="stFooter"] {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
    position: relative;
    z-index: 1;
}

[data-testid="stMain"], section.main {
    background: transparent !important;
    padding-bottom: 0 !important;
    margin-bottom: 0 !important;
}

.block-container, 
[data-testid="stMainBlockContainer"], 
[data-testid="stAppViewBlockContainer"] {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 1280px !important;
    margin: 0 auto !important;
}

[data-testid="stVerticalBlock"], 
[data-testid="stVerticalBlockBorderWrapper"] {
    gap: 1rem !important;
    padding-bottom: 0 !important;
    margin-bottom: 0 !important;
}

[data-testid="stVerticalBlock"] > div:last-child {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

/* ── Glass Mixin (utility classes) ── */
.glass {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.09);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06);
}
.glass-strong {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(32px) saturate(200%);
    -webkit-backdrop-filter: blur(32px) saturate(200%);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 24px 48px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.08);
}

/* ── Top Nav ── */
.nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(2,8,23,0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    padding: 0 3rem;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.nav-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.nav-icon {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    box-shadow: 0 0 16px rgba(6,182,212,0.35);
}
.nav-title {
    font-size: 0.92rem;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
    letter-spacing: -0.02em;
}
.nav-right { display: flex; gap: 0.5rem; align-items: center; }
.pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    color: rgba(255,255,255,0.4);
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 3px 10px;
    border-radius: 20px;
}
.pill-live {
    font-size: 0.67rem;
    color: #10b981;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.2);
    padding: 3px 10px;
    border-radius: 20px;
    display: flex; align-items: center; gap: 5px;
    font-weight: 600;
}
.pill-live::before {
    content: '';
    width: 6px; height: 6px;
    background: #10b981;
    border-radius: 50%;
    display: inline-block;
    animation: pulse-dot 2s ease infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; } 50% { opacity: 0.4; }
}

/* ── Hero ── */
.hero-wrap {
    padding: 2.5rem 0 1.8rem;
    width: 100%;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(6,182,212,0.1);
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.73rem;
    font-weight: 600;
    color: #06b6d4;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero-h1 {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.1;
    color: #fff;
    margin-bottom: 1rem;
}
.hero-h1 span {
    background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 50%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.45);
    max-width: 520px;
    line-height: 1.65;
    font-weight: 400;
}

/* ── Main content wrapper ── */
.content-wrap {
    padding: 0 0 1.5rem;
    width: 100%;
}

/* ── Section label ── */
.s-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: rgba(255,255,255,0.25);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.65rem;
}

/* ── Sample chips ── */
.stButton > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    letter-spacing: -0.01em !important;
}
.stButton > button:not([kind="primary"]) {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    color: rgba(255,255,255,0.6) !important;
    backdrop-filter: blur(8px) !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(255,255,255,0.09) !important;
    border-color: rgba(255,255,255,0.16) !important;
    color: rgba(255,255,255,0.85) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #06b6d4, #3b82f6) !important;
    border: none !important;
    color: #fff !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(6,182,212,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 28px rgba(6,182,212,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Textarea ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    color: rgba(255,255,255,0.85) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.7 !important;
    resize: vertical !important;
    backdrop-filter: blur(12px) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextArea textarea::placeholder { color: rgba(255,255,255,0.18) !important; }
.stTextArea textarea:focus {
    border-color: rgba(6,182,212,0.5) !important;
    box-shadow: 0 0 0 3px rgba(6,182,212,0.08), 0 0 20px rgba(6,182,212,0.05) !important;
    outline: none !important;
}
.stTextArea > label { display: none !important; }

/* ── Glass Cards ── */
.g-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.06);
    position: relative;
    overflow: hidden;
}
.g-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
}
.g-card-label {
    font-size: 0.67rem;
    font-weight: 700;
    color: rgba(255,255,255,0.3);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.g-card-label .accent { color: #06b6d4; }

/* Summary text */
.sum-text {
    font-size: 0.93rem;
    color: rgba(255,255,255,0.82);
    line-height: 1.78;
    background: rgba(6,182,212,0.05);
    border-left: 2px solid rgba(6,182,212,0.6);
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
}
.model-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: rgba(255,255,255,0.2);
    margin-top: 0.6rem;
}

/* Key points */
.kp {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.88rem;
    color: rgba(255,255,255,0.72);
    line-height: 1.6;
}
.kp:last-child { border-bottom: none; }
.kp-idx {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: rgba(6,182,212,0.6);
    background: rgba(6,182,212,0.08);
    border: 1px solid rgba(6,182,212,0.15);
    border-radius: 4px;
    padding: 1px 6px;
    flex-shrink: 0;
    margin-top: 3px;
}

/* Stats */
.stats-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.75rem;
}
.stat-glass {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.1rem 0.8rem;
    text-align: center;
    backdrop-filter: blur(16px);
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease;
}
.stat-glass:hover { border-color: rgba(255,255,255,0.14); }
.stat-glass.highlight {
    border-color: rgba(16,185,129,0.25);
    background: rgba(16,185,129,0.04);
}
.stat-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: rgba(255,255,255,0.85);
    line-height: 1;
    letter-spacing: -0.03em;
}
.stat-val.c-cyan { color: #06b6d4; }
.stat-val.c-green { color: #10b981; }
.stat-lbl {
    font-size: 0.65rem;
    color: rgba(255,255,255,0.3);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.35rem;
}
.formula {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: rgba(255,255,255,0.18);
    text-align: center;
    margin-top: 0.75rem;
    padding-top: 0.6rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}

/* Empty state */
.empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 390px;
    border: 1px dashed rgba(255,255,255,0.07);
    border-radius: 16px;
    background: rgba(255,255,255,0.02);
    backdrop-filter: blur(12px);
    gap: 0.5rem;
}
.empty-ico {
    width: 48px; height: 48px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}
.empty-t { font-size: 0.9rem; font-weight: 500; color: rgba(255,255,255,0.28); }
.empty-s { font-size: 0.78rem; color: rgba(255,255,255,0.15); }

/* Error */
.err {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    color: rgba(248,113,113,0.9);
    font-size: 0.85rem;
    line-height: 1.55;
    backdrop-filter: blur(12px);
}

/* ── Divider ── */
.div-line {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 2.8rem 0 2rem;
}

/* ── Section header ── */
.sec-h {
    display: flex;
    align-items: flex-end;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.sec-h h2 {
    font-size: 1.35rem;
    font-weight: 700;
    color: rgba(255,255,255,0.88);
    letter-spacing: -0.03em;
}
.sec-avg-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #10b981;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.2);
    padding: 3px 10px;
    border-radius: 6px;
    margin-bottom: 2px;
}

/* ── Test result expanders ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    margin-bottom: 0.75rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
    overflow: hidden !important;
}
[data-testid="stExpander"]:hover {
    border-color: rgba(255,255,255,0.12) !important;
}
[data-testid="stExpander"] > details > summary {
    color: rgba(255,255,255,0.78) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 1rem 1.1rem !important;
}
[data-testid="stExpander"] > details > summary:hover {
    color: #fff !important;
}
[data-testid="stExpander"] > details[open] {
    border-top: 1px solid rgba(255,255,255,0.06);
}

/* ── Obs panel ── */
.obs-glass {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
}
.obs-row {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    padding: 0.6rem 0;
    font-size: 0.875rem;
    line-height: 1.65;
    color: rgba(255,255,255,0.6);
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.obs-row:last-child { border-bottom: none; }
.obs-dot {
    width: 6px; height: 6px;
    background: #06b6d4;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 7px;
    box-shadow: 0 0 8px rgba(6,182,212,0.5);
}
.obs-strong { color: rgba(255,255,255,0.88); font-weight: 600; }

/* ── Test result box ── */
.t-sum {
    font-size: 0.875rem;
    color: rgba(255,255,255,0.72);
    line-height: 1.72;
    padding: 0.75rem 0.9rem;
    background: rgba(6,182,212,0.04);
    border-left: 2px solid rgba(6,182,212,0.4);
    border-radius: 0 7px 7px 0;
}
.t-obs {
    margin-top: 0.9rem;
    padding: 0.75rem 0.9rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    font-size: 0.82rem;
    color: rgba(255,255,255,0.45);
    line-height: 1.65;
}
.t-obs strong { color: rgba(255,255,255,0.55); }

/* Mini stats in test results */
.mini-stats {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.5rem;
    margin-bottom: 0.8rem;
}
.mini-s {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px;
    padding: 0.7rem 0.5rem;
    text-align: center;
}
.mini-v {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem;
    font-weight: 600;
    color: rgba(255,255,255,0.82);
    line-height: 1;
}
.mini-v.g { color: #10b981; }
.mini-v.b { color: #06b6d4; }
.mini-l {
    font-size: 0.6rem;
    color: rgba(255,255,255,0.25);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 0.25rem;
}

/* Footer */
.footer {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: rgba(255,255,255,0.12);
    margin-top: 3rem;
    padding-bottom: 2rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(2,8,23,0.85) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: rgba(255,255,255,0.5) !important; }
/* ── Fix: remove extra scroll space below footer ── */
html, body, .stApp {
    height: 100% !important;
    overflow: hidden !important;      /* kills the outer (second) scrollbar */
}
[data-testid="stAppViewContainer"] {
    height: 100vh !important;
    overflow: hidden !important;
}
[data-testid="stMain"] {
    height: 100vh !important;
    overflow-y: auto !important;      /* only ONE scroll area, ends at footer */
    overflow-x: hidden !important;
}
.stApp::before, .stApp::after, .orb-mid { contain: strict; }

/* ── Mobile Responsive Overrides ── */
@media (max-width: 768px) {
    .nav {
        padding: 0 1rem !important;
        height: 56px !important;
    }
    .nav-left {
        gap: 0.5rem !important;
        max-width: 65% !important;
    }
    .nav-title {
        font-size: 0.82rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    .nav-right .pill {
        display: none !important;
    }
    .nav-right .pill-live {
        display: inline-flex !important;
        font-size: 0.62rem !important;
        padding: 2px 7px !important;
    }
    .hero-wrap {
        padding: 2rem 1rem 1.2rem !important;
    }
    .hero-h1 {
        font-size: 2.1rem !important;
        line-height: 1.15 !important;
    }
    .hero-sub {
        font-size: 0.88rem !important;
    }
    .content-wrap {
        padding: 0 1rem 1rem !important;
    }
    .stats-row {
        grid-template-columns: 1fr 1fr 1fr !important;
        gap: 0.4rem !important;
    }
    .stat-glass {
        padding: 0.7rem 0.3rem !important;
    }
    .stat-val {
        font-size: 1.35rem !important;
    }
    .stat-lbl {
        font-size: 0.55rem !important;
    }
}

@media (max-width: 480px) {
    .hero-h1 {
        font-size: 1.75rem !important;
    }
    .nav-title {
        font-size: 0.76rem !important;
        max-width: 150px !important;
    }
}
</style>

<!-- Orb mid -->
<div class="orb-mid"></div>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────────
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_TOKEN   = os.getenv("HF_TOKEN", "")

SAMPLES = {
    "Climate Change": (
        "Climate change refers to long-term shifts in global temperatures and weather patterns. "
        "While some climate change is natural, scientific evidence shows that since the 1800s, human activities "
        "have been the primary driver. Burning fossil fuels like coal, oil, and gas releases greenhouse gases into "
        "the atmosphere. These gases trap heat from the sun, causing the planet to warm. The effects include rising "
        "sea levels, more frequent and severe weather events, loss of biodiversity, and threats to food and water "
        "security. Addressing climate change requires both mitigation strategies — reducing greenhouse gas emissions "
        "— and adaptation measures to cope with the changes already underway."
    ),
    "Artificial Intelligence": (
        "Artificial Intelligence (AI) is the simulation of human intelligence in machines programmed to think and "
        "learn. AI encompasses a broad range of technologies including machine learning, deep learning, natural "
        "language processing, and computer vision. These technologies power applications from virtual assistants "
        "like Siri and Alexa to recommendation systems on Netflix and Spotify. Machine learning allows systems to "
        "learn from data and improve over time without explicit programming. Deep learning uses neural networks with "
        "many layers to analyze complex patterns. AI is transforming industries including healthcare, finance, "
        "transportation, and education, creating new opportunities while also raising ethical concerns about "
        "privacy, bias, and employment."
    ),
    "DNA & Genetics": (
        "DNA, or deoxyribonucleic acid, is the hereditary material in humans and almost all other organisms. "
        "Nearly every cell in a person's body has the same DNA. Most DNA is located in the cell nucleus, but a "
        "small amount can also be found in the mitochondria. The information in DNA is stored as a code made up of "
        "four chemical bases: adenine (A), guanine (G), cytosine (C), and thymine (T). Human DNA consists of about "
        "3 billion bases, and more than 99 percent of those bases are the same in all people. The sequence of these "
        "bases determines the information available for building and maintaining an organism, similar to the way "
        "letters of the alphabet appear in a certain order to form words and sentences."
    ),
}

# ─── Helpers ─────────────────────────────────────────────────────────────────────
def word_count(text):
    return len(text.split()) if text.strip() else 0

def reduction_pct(orig, summ):
    return ((orig - summ) / orig * 100) if orig > 0 else 0.0

def extract_key_points(original, summary, n=5):
    sentences = re.split(r'(?<=[.!?])\s+', original.strip())
    sentences = [s.strip() for s in sentences if len(s.split()) > 5]
    summ_words = set(re.findall(r'\b\w+\b', summary.lower()))
    stop = {'the','a','an','is','are','was','were','of','in','on','at','to','for',
            'and','but','or','it','its','by','as','with','from','this','that','be',
            'been','have','has','had','do','does','did','not','also','can','will'}
    def score(s):
        ws = re.findall(r'\b\w+\b', s.lower())
        return sum(1 for w in ws if w in summ_words and w not in stop) / max(len(ws), 1)
    ranked = sorted(sentences, key=score, reverse=True)
    seen, pts = set(), []
    for s in ranked:
        k = s[:40]
        if k not in seen:
            seen.add(k); pts.append(s)
        if len(pts) == n:
            break
    return pts or sentences[:n]

def call_hf_api(text, token):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": text,
        "parameters": {"max_length": 130, "min_length": 30, "do_sample": False, "truncation": "only_first"},
    }
    try:
        r = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        if r.status_code == 503:
            return {"error": "Model is loading on HF servers. Please wait 20 seconds and retry."}
        if r.status_code == 401:
            return {"error": "Invalid API token. Check your Hugging Face token in the sidebar."}
        if r.status_code != 200:
            return {"error": f"API error (HTTP {r.status_code}). Please retry."}
        data = r.json()
        if isinstance(data, list) and data:
            return {"summary": data[0].get("summary_text", "")}
        return {"error": "Unexpected API response. Please retry."}
    except requests.Timeout:
        return {"error": "Request timed out. Model may be cold-starting. Please retry."}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def extractive_fallback(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    if len(sentences) <= 2: return text
    words = re.findall(r'\b\w+\b', text.lower())
    stop = {'the','a','an','is','are','was','were','of','in','on','at','to','for',
            'and','but','or','it','its','by','as','with','from','this','that','be',
            'been','have','has','had','do','does','did','not','also','can','will',
            'we','our','they','them','more','most','some','which','while','both'}
    freq = {w: 0 for w in words}
    for w in words:
        if w not in stop and len(w) > 2: freq[w] = freq.get(w, 0) + 1
    def score(s, pos, total):
        ws = re.findall(r'\b\w+\b', s.lower())
        f = sum(freq.get(w, 0) for w in ws) / max(len(ws), 1)
        p = 1.0 if pos == 0 else (0.8 if pos == total - 1 else 0.5)
        return f * p
    scored = sorted(enumerate(sentences), key=lambda x: score(x[1], x[0], len(sentences)), reverse=True)
    top_idx = {i for i, _ in scored[:max(2, len(sentences)//3)]}
    return ' '.join(s for i, s in enumerate(sentences) if i in top_idx)

# ─── Session State ─────────────────────────────────────────────────────────────
if "input_text" not in st.session_state: st.session_state.input_text = ""
if "result"     not in st.session_state: st.session_state.result     = None
if "history"    not in st.session_state: st.session_state.history    = []

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("**⚙ Settings**")
    token_input = st.text_input("HF API Token", value=HF_TOKEN, type="password",
                                 help="Get free token at huggingface.co/settings/tokens")
    if token_input: HF_TOKEN = token_input
    offline = st.checkbox("Offline mode (no API key)", value=False)
    st.markdown("---")
    st.markdown("`facebook/bart-large-cnn`")
    st.markdown("**Vishal Deep** · Mini Project")

# ─── Nav Bar ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="nav">
  <div class="nav-left">
    {LOGO_HTML}
    <span class="nav-title">Smart Study Notes Generator</span>
  </div>
  <div class="nav-right">
    <span class="pill">facebook/bart-large-cnn</span>
    <span class="pill">Hugging Face</span>
    <span class="pill-live">AI · Live</span>
  </div>
</div>

<div class="hero-wrap">
  <div class="hero-eyebrow">✦ Powered by Generative AI</div>
  <h1 class="hero-h1">Summarize any text,<br><span>instantly.</span></h1>
  <p class="hero-sub">Paste a paragraph and get an AI-generated summary, key study points, and compression statistics — powered by Hugging Face BART.</p>
</div>
""", unsafe_allow_html=True)

# ─── Content Wrapper Start ────────────────────────────────────────────────────
st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

# ─── Two-Column Layout ────────────────────────────────────────────────────────
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown('<p class="s-label">Paragraph Input</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("🌍  Climate", use_container_width=True):
        st.session_state.input_text = SAMPLES["Climate Change"]
        st.session_state.result = None
    if c2.button("🤖  AI / ML", use_container_width=True):
        st.session_state.input_text = SAMPLES["Artificial Intelligence"]
        st.session_state.result = None
    if c3.button("🧬  Genetics", use_container_width=True):
        st.session_state.input_text = SAMPLES["DNA & Genetics"]
        st.session_state.result = None

    user_text = st.text_area(
        label="input",
        value=st.session_state.input_text,
        height=235,
        placeholder="Paste or type your paragraph here (minimum 20 words)...",
        label_visibility="collapsed",
    )
    st.session_state.input_text = user_text

    b1, b2 = st.columns([3, 1])
    gen_btn   = b1.button("✨  Generate Summary & Notes", type="primary", use_container_width=True)
    clear_btn = b2.button("Clear", use_container_width=True)

    if clear_btn:
        st.session_state.input_text = ""
        st.session_state.result = None
        st.rerun()

# ─── Processing ───────────────────────────────────────────────────────────────
if gen_btn:
    text = user_text.strip()
    if not text:
        st.session_state.result = {"error": "Please enter a paragraph before generating."}
    elif word_count(text) < 20:
        st.session_state.result = {"error": f"Text too short ({word_count(text)} words). Enter at least 20 words."}
    else:
        with st.spinner("Running BART model..."):
            if offline or not HF_TOKEN:
                summary      = extractive_fallback(text)
                method_label = "Extractive fallback (offline mode)"
            else:
                api_res = call_hf_api(text, HF_TOKEN)
                if "error" in api_res:
                    st.session_state.result = {"error": api_res["error"]}
                    st.rerun()
                summary      = api_res["summary"]
                method_label = "facebook/bart-large-cnn · Hugging Face Inference API"

        owc = word_count(text)
        swc = word_count(summary)
        red = reduction_pct(owc, swc)
        kps = extract_key_points(text, summary)
        entry = {
            "summary": summary, "key_points": kps,
            "owc": owc, "swc": swc, "reduction": red, "method": method_label,
            "snippet": text[:60].strip() + ("..." if len(text) > 60 else ""),
        }
        st.session_state.result = entry
        # prepend to history, keep last 5
        st.session_state.history = [entry] + st.session_state.history[:4]
    st.rerun()

# ─── Output Panel ─────────────────────────────────────────────────────────────
with right:
    res = st.session_state.result

    if res is None:
        st.markdown("""
        <div class="empty">
          <div class="empty-ico">↩</div>
          <div class="empty-t">No output yet</div>
          <div class="empty-s">Enter a paragraph and click Generate</div>
        </div>
        """, unsafe_allow_html=True)

    elif "error" in res:
        st.markdown(f'<div class="err">⚠&nbsp; {res["error"]}</div>', unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="g-card">
          <div class="g-card-label"><span class="accent">◈</span> Summary</div>
          <div class="sum-text">{res['summary']}</div>
          <div class="model-badge">{res['method']}</div>
        </div>
        """, unsafe_allow_html=True)

        kp_html = "".join(
            f'<div class="kp"><span class="kp-idx">0{i+1}</span><span>{p}</span></div>'
            for i, p in enumerate(res['key_points'])
        )
        st.markdown(f"""
        <div class="g-card">
          <div class="g-card-label"><span class="accent">◈</span> Key Points</div>
          {kp_html}
        </div>
        """, unsafe_allow_html=True)

        red_v   = res['reduction']
        red_cls = "c-green" if red_v >= 40 else "c-cyan"
        st.markdown(f"""
        <div class="g-card">
          <div class="g-card-label"><span class="accent">◈</span> Word Count Statistics</div>
          <div class="stats-row">
            <div class="stat-glass">
              <div class="stat-val">{res['owc']}</div>
              <div class="stat-lbl">Original</div>
            </div>
            <div class="stat-glass">
              <div class="stat-val c-cyan">{res['swc']}</div>
              <div class="stat-lbl">Summary</div>
            </div>
            <div class="stat-glass highlight">
              <div class="stat-val {red_cls}">{red_v:.1f}%</div>
              <div class="stat-lbl">Reduced</div>
            </div>
          </div>
          <div class="formula">Reduction % = ((Original &minus; Summary) / Original) &times; 100</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Copy + Download buttons ──────────────────────────────────────
        kp_text = "\n".join(f"  {i+1}. {p}" for i, p in enumerate(res['key_points']))
        notes_txt = (
            f"SMART STUDY NOTES\n{'='*40}\n\n"
            f"SUMMARY\n{'-'*40}\n{res['summary']}\n\n"
            f"KEY POINTS\n{'-'*40}\n{kp_text}\n\n"
            f"STATISTICS\n{'-'*40}\n"
            f"Original Word Count : {res['owc']}\n"
            f"Summary Word Count  : {res['swc']}\n"
            f"Reduction           : {res['reduction']:.1f}%\n"
            f"Formula             : ((Original - Summary) / Original) x 100\n\n"
            f"Model: {res['method']}\n"
            f"Generated by: Smart Study Notes Generator · Vishal Deep\n"
        )
        st.markdown('<div style="margin-top:0.3rem;"></div>', unsafe_allow_html=True)
        dl1, dl2 = st.columns(2)
        dl1.download_button(
            label="⬇  Download Notes (.txt)",
            data=notes_txt,
            file_name="study_notes.txt",
            mime="text/plain",
            use_container_width=True,
        )
        dl2.button("📋  Copy Summary", use_container_width=True,
                   help="Select & copy the summary text above manually.")

# ── Close main two-column content wrap ──
st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION HISTORY (only if history exists)
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.history:
    st.markdown('<div class="content-wrap" style="padding-top:0;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:1rem; margin-top:0.5rem;">
      <h2 style="font-size:1.1rem; font-weight:700; color:rgba(255,255,255,0.75); letter-spacing:-0.02em;">Recent Summaries</h2>
      <span style="font-family:'JetBrains Mono',monospace; font-size:0.67rem; color:#06b6d4;
                   background:rgba(6,182,212,0.08); border:1px solid rgba(6,182,212,0.18);
                   padding:2px 9px; border-radius:5px;">This session</span>
    </div>
    """, unsafe_allow_html=True)

    for idx, h in enumerate(st.session_state.history):
        red_col = "#10b981" if h['reduction'] >= 40 else "#06b6d4"
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.6rem;
            backdrop-filter: blur(16px);
            display: flex;
            gap: 1.1rem;
            align-items: flex-start;
        ">
          <!-- Left: index + stats -->
          <div style="flex-shrink:0; text-align:center; min-width:52px;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:rgba(255,255,255,0.25);
                        background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
                        border-radius:6px; padding:3px 6px; margin-bottom:0.3rem;"># {idx+1}</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:1.1rem; font-weight:700;
                        color:{red_col}; line-height:1;">{h['reduction']:.0f}%</div>
            <div style="font-size:0.6rem; color:rgba(255,255,255,0.25); margin-top:2px;">reduced</div>
          </div>
          <!-- Right: snippet + summary preview -->
          <div style="flex:1; min-width:0;">
            <div style="font-size:0.7rem; color:rgba(255,255,255,0.28); margin-bottom:0.3rem;
                        font-family:'JetBrains Mono',monospace; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
              {h['snippet']}
            </div>
            <div style="font-size:0.88rem; color:rgba(255,255,255,0.72); line-height:1.55;
                        overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">
              {h['summary']}
            </div>
            <div style="margin-top:0.4rem; font-size:0.75rem; color:rgba(255,255,255,0.3);">
              <span style="color:rgba(255,255,255,0.4); font-weight:500;">{h['owc']}</span> words
              &rarr;
              <span style="color:#06b6d4; font-weight:500;">{h['swc']}</span> words
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CLEAN FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="content-wrap" style="padding-top:0; padding-bottom:0.5rem;">
  <div style="border-top: 1px solid rgba(255,255,255,0.06); margin-top: 1rem; padding-top: 1.2rem; padding-bottom: 0.8rem;
       text-align:center; font-family:'JetBrains Mono',monospace; font-size:0.68rem;
       color:rgba(255,255,255,0.25); letter-spacing:0.04em;">
    Smart Study Notes Generator &nbsp;&middot;&nbsp; Vishal Deep &nbsp;&middot;&nbsp; Python + Streamlit + Hugging Face BART
  </div>
</div>
""", unsafe_allow_html=True)
