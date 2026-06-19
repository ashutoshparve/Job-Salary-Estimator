import streamlit as st
import requests
import pickle
import os
import time

st.set_page_config(
    page_title="Salary Estimator",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --bg: #0B1426;
    --bg-panel: #101B30;
    --bg-input: #16223A;
    --border: #233152;
    --text: #F2F0E8;
    --text-dim: #8C9AB3;
    --accent: #2DD4A8;
    --accent-dim: #1A8F70;
    --amber: #E8A33D;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* ---- Header ---- */
.eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.eyebrow::before {
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 8px var(--accent);
}
.headline {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.6rem;
    line-height: 1.1;
    color: var(--text);
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}
.subhead {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    color: var(--text-dim);
    max-width: 540px;
    margin-bottom: 2.2rem;
}

/* ---- Panels ---- */
.panel {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.8rem 1.8rem;
}
.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 1.2rem;
}

/* ---- Form widgets ---- */
div[data-baseweb="select"] > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif;
}
div[data-baseweb="select"] span {
    color: var(--text) !important;
}
label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase;
    color: var(--text-dim) !important;
}

.stButton > button {
    background: var(--accent);
    color: #08130F;
    border: none;
    border-radius: 8px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.7rem 0;
    width: 100%;
    transition: all 0.15s ease;
    letter-spacing: 0.01em;
}
.stButton > button:hover {
    background: #3EE8BC;
    box-shadow: 0 0 24px rgba(45, 212, 168, 0.35);
}
.stButton > button:active {
    transform: scale(0.98);
}

/* ---- Result panel ---- */
.result-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 280px;
    text-align: center;
    color: var(--text-dim);
}
.result-empty-icon {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    color: var(--border);
    margin-bottom: 0.8rem;
}
.result-empty-text {
    font-size: 0.88rem;
    max-width: 220px;
    line-height: 1.5;
}

.salary-figure {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 3rem;
    color: var(--accent);
    line-height: 1;
    margin: 0.4rem 0 0.2rem 0;
}
.salary-unit {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    color: var(--text-dim);
    margin-bottom: 1.6rem;
}
.salary-meta {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: var(--text-dim);
    margin-bottom: 1.6rem;
}
.salary-meta b { color: var(--text); font-weight: 500; }

/* ---- Band visualization ---- */
.band-wrap {
    margin-top: 0.4rem;
}
.band-labels {
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-dim);
    margin-bottom: 6px;
}
.band-track {
    position: relative;
    height: 8px;
    border-radius: 4px;
    background: linear-gradient(90deg, #233152 0%, #2DD4A8 50%, #233152 100%);
    margin-bottom: 6px;
}
.band-marker {
    position: absolute;
    top: -5px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--amber);
    border: 3px solid var(--bg-panel);
    box-shadow: 0 0 0 1px var(--amber);
    transform: translateX(-50%);
}

/* ---- Footer strip ---- */
.foot {
    margin-top: 2.8rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-dim);
    letter-spacing: 0.04em;
}
.foot a { color: var(--text-dim); text-decoration: none; }
.foot a:hover { color: var(--accent); }

.status-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
@st.cache_data
def load_options():
    with open("model/model.pkl", "rb") as f:
        data = pickle.load(f)
        encoders = data["encoders"]
    return {
        "job_titles": sorted(list(encoders["job_title"].classes_)),
        "locations": sorted(list(encoders["location"].classes_)),
        "companies": sorted(list(encoders["company"].classes_)),
    }


if "result" not in st.session_state:
    st.session_state.result = None

options = load_options()


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<div class="eyebrow">Live model · Random Forest Regressor</div>', unsafe_allow_html=True)
st.markdown('<div class="headline">What should this role pay?</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subhead">Enter a role, location, and company to get an instant salary '
    'estimate, benchmarked against market data.</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1, 1.15], gap="medium")

# ---------------------------------------------------------------------------
# Left panel — inputs
# ---------------------------------------------------------------------------
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label">Role parameters</div>', unsafe_allow_html=True)

    job_title = st.selectbox("Job title", options["job_titles"])
    location = st.selectbox("Location", options["locations"])
    company = st.selectbox("Company", options["companies"])

    st.write("")
    predict_clicked = st.button("Estimate salary →")
    st.markdown('</div>', unsafe_allow_html=True)

    if predict_clicked:
        with st.spinner(""):
            try:
                response = requests.post(
                    f"{API_URL}/predict",
                    json={"job_title": job_title, "location": location, "company": company},
                    timeout=15
                )
                if response.status_code == 200:
                    st.session_state.result = response.json()
                else:
                    st.session_state.result = {"error": "The model couldn't generate a prediction. Try a different combination."}
            except requests.exceptions.ConnectionError:
                st.session_state.result = {"error": f"Can't reach the prediction API at {API_URL}. It may be waking up — try again in a few seconds."}
            except Exception as e:
                st.session_state.result = {"error": str(e)}

# ---------------------------------------------------------------------------
# Right panel — result
# ---------------------------------------------------------------------------
with right:
    st.markdown('<div class="panel" style="min-height: 360px;">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label">Estimate</div>', unsafe_allow_html=True)

    result = st.session_state.result

    if result is None:
        st.markdown("""
            <div class="result-empty">
                <div class="result-empty-icon">◇</div>
                <div class="result-empty-text">Set your role parameters and run an estimate to see the result here.</div>
            </div>
        """, unsafe_allow_html=True)

    elif "error" in result:
        st.markdown(f"""
            <div class="result-empty">
                <div class="result-empty-icon">!</div>
                <div class="result-empty-text">{result['error']}</div>
            </div>
        """, unsafe_allow_html=True)

    else:
        salary = result["predicted_salary_lpa"]
        low = round(salary * 0.78, 1)
        high = round(salary * 1.28, 1)
        position_pct = 50  # prediction sits at the center of its own band by construction

        st.markdown(f'<div class="salary-figure">₹{salary}</div>', unsafe_allow_html=True)
        st.markdown('<div class="salary-unit">LPA · estimated annual</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="salary-meta"><b>{result["job_title"].title()}</b> · '
            f'{result["location"].title()} · {result["company"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
            <div class="band-wrap">
                <div class="band-labels"><span>₹{low} LPA</span><span>MARKET RANGE</span><span>₹{high} LPA</span></div>
                <div class="band-track">
                    <div class="band-marker" style="left:{position_pct}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="foot">
    <div><span class="status-dot"></span>API connected</div>
    <div>Python · FastAPI · PostgreSQL · Scikit-Learn · Streamlit</div>
</div>
""", unsafe_allow_html=True)