import streamlit as st
import requests
import pickle
import os

st.set_page_config(
    page_title="Salary Estimator",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0B1426; color: #F2F0E8; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.5rem; padding-bottom: 3rem; max-width: 1100px; }

.eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #2DD4A8;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.eyebrow::before {
    content: "";
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #2DD4A8;
    box-shadow: 0 0 8px #2DD4A8;
    display: inline-block;
}
.headline {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.6rem;
    line-height: 1.1;
    color: #F2F0E8;
    margin-bottom: 0.5rem;
}
.subhead {
    font-size: 1rem;
    color: #8C9AB3;
    max-width: 540px;
    margin-bottom: 2rem;
}
label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase;
    color: #8C9AB3 !important;
}
div[data-baseweb="select"] > div {
    background: #16223A !important;
    border: 1px solid #233152 !important;
    border-radius: 8px !important;
}
div[data-baseweb="select"] span { color: #F2F0E8 !important; }
.stButton > button {
    background: #2DD4A8;
    color: #08130F;
    border: none;
    border-radius: 8px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.7rem 0;
    width: 100%;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: #3EE8BC;
    box-shadow: 0 0 24px rgba(45,212,168,0.35);
}
.result-empty {
    text-align: center;
    padding: 3.5rem 1.5rem;
    color: #5B6B82;
}
.result-empty-icon { font-size: 2rem; margin-bottom: 0.8rem; color: #233152; }
.result-empty-text { font-size: 0.88rem; line-height: 1.5; }
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #5B6B82;
    margin-bottom: 0.5rem;
}
.salary-num {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 3.2rem;
    color: #2DD4A8;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.salary-unit {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    color: #5B6B82;
    margin-bottom: 1.2rem;
}
.salary-meta {
    font-size: 0.85rem;
    color: #8C9AB3;
    margin-bottom: 1.6rem;
    line-height: 1.5;
}
.salary-meta b { color: #F2F0E8; font-weight: 500; }
.band-labels {
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #5B6B82;
    margin-bottom: 5px;
}
.band-track {
    position: relative;
    height: 8px;
    border-radius: 4px;
    background: linear-gradient(90deg, #16223A 0%, #2DD4A8 50%, #16223A 100%);
    margin-bottom: 4px;
}
.band-marker {
    position: absolute;
    top: -5px;
    width: 18px; height: 18px;
    border-radius: 50%;
    background: #E8A33D;
    border: 3px solid #101B30;
    box-shadow: 0 0 0 1px #E8A33D;
    transform: translateX(-50%);
}
.foot {
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid #1A2A45;
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #5B6B82;
    letter-spacing: 0.04em;
}
.status-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #2DD4A8;
    margin-right: 5px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_options():
    with open("model/model.pkl", "rb") as f:
        data = pickle.load(f)
        encoders = data["encoders"]
    return {
        "job_titles": sorted(list(encoders["job_title"].classes_)),
        "locations":  sorted(list(encoders["location"].classes_)),
        "companies":  sorted(list(encoders["company"].classes_)),
    }


if "result" not in st.session_state:
    st.session_state.result = None

options = load_options()

st.markdown('<div class="eyebrow">Live model · Random Forest Regressor</div>', unsafe_allow_html=True)
st.markdown('<div class="headline">What should this role pay?</div>', unsafe_allow_html=True)
st.markdown('<div class="subhead">Enter a role, location, and company to get an instant salary estimate, benchmarked against market data.</div>', unsafe_allow_html=True)

left, right = st.columns([1, 1.15], gap="medium")

with left:
    with st.container(border=True):
        st.markdown('<div class="section-label">Role parameters</div>', unsafe_allow_html=True)
        job_title = st.selectbox("Job title", options["job_titles"])
        location  = st.selectbox("Location",  options["locations"])
        company   = st.selectbox("Company",   options["companies"])
        st.write("")
        predict_clicked = st.button("Estimate salary →")

if predict_clicked:
    try:
        resp = requests.post(
            f"{API_URL}/predict",
            json={"job_title": job_title, "location": location, "company": company},
            timeout=20
        )
        if resp.status_code == 200:
            st.session_state.result = resp.json()
        else:
            st.session_state.result = {"error": "Prediction failed. Try a different combination."}
    except requests.exceptions.ConnectionError:
        st.session_state.result = {"error": f"Cannot reach API. It may be waking up — try again in 30s."}
    except Exception as e:
        st.session_state.result = {"error": str(e)}

with right:
    result = st.session_state.result
    with st.container(border=True):
        if result is None:
            st.markdown("""
            <div class="result-empty">
                <div class="result-empty-icon">◇</div>
                <div class="section-label" style="text-align:center; margin-bottom:0.6rem;">Estimate</div>
                <div class="result-empty-text">Set your role parameters on the left and click Estimate salary to see the result here.</div>
            </div>
            """, unsafe_allow_html=True)

        elif "error" in result:
            st.markdown(f"""
            <div class="result-empty">
                <div class="result-empty-icon">⚠</div>
                <div class="result-empty-text">{result['error']}</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            salary = result["predicted_salary_lpa"]
            low    = round(salary * 0.78, 1)
            high   = round(salary * 1.28, 1)

            st.markdown('<div class="section-label">Estimate</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="salary-num">₹{salary}</div>', unsafe_allow_html=True)
            st.markdown('<div class="salary-unit">LPA · estimated annual</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="salary-meta">'
                f'<b>{result["job_title"].title()}</b> &nbsp;·&nbsp; '
                f'{result["location"].title()} &nbsp;·&nbsp; {result["company"]}'
                f'</div>',
                unsafe_allow_html=True
            )
            st.markdown(f"""
            <div>
                <div class="band-labels">
                    <span>₹{low} LPA</span>
                    <span>MARKET RANGE</span>
                    <span>₹{high} LPA</span>
                </div>
                <div class="band-track">
                    <div class="band-marker" style="left:50%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("""
<div class="foot">
    <div><span class="status-dot"></span>API connected</div>
    <div>Python · FastAPI · PostgreSQL · Scikit-Learn · Streamlit</div>
</div>
""", unsafe_allow_html=True)