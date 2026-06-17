import streamlit as st
import requests
import pickle
import os

st.set_page_config(
    page_title="Job Salary Estimator",
    page_icon="💼",
    layout="centered"
)


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


@st.cache_data
def load_options():
    """Load dropdown options directly from the saved model."""
    with open("model/model.pkl", "rb") as f:
        data = pickle.load(f)
        encoders = data["encoders"]
    return {
        "job_titles": sorted(list(encoders["job_title"].classes_)),
        "locations": sorted(list(encoders["location"].classes_)),
        "companies": sorted(list(encoders["company"].classes_)),
    }


# Header
st.title("💼 Job Salary Estimator")
st.markdown("Get an instant salary estimate based on job role, location, and company.")
st.divider()

options = load_options()

# Input form
col1, col2 = st.columns(2)

with col1:
    job_title = st.selectbox("Job Title", options["job_titles"])
    location = st.selectbox("Location", options["locations"])

with col2:
    company = st.selectbox("Company", options["companies"])

st.write("")

if st.button("Predict Salary", type="primary", use_container_width=True):
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={
                "job_title": job_title,
                "location": location,
                "company": company
            },
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            salary = result["predicted_salary_lpa"]

            st.success("Prediction complete!")
            st.metric(
                label="Estimated Annual Salary",
                value=f"₹{salary} LPA"
            )
            st.caption(f"Based on: {job_title.title()} • {location.title()} • {company}")
        else:
            st.error("Something went wrong with the prediction. Please try again.")

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to the API. Make sure the FastAPI server is running (uvicorn api.main:app --reload)")
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()
st.caption("Built with Python, FastAPI, PostgreSQL, Scikit-Learn & Streamlit")