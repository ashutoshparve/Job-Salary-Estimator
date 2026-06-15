from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import logging
import os
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import log_user_query

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

app = FastAPI(
    title="Job Salary Estimator API",
    description="Predicts job salaries based on role, location and company",
    version="1.0.0"
)

# Load model
with open("model/model.pkl", "rb") as f:
    data = pickle.load(f)
    model = data["model"]
    encoders = data["encoders"]
    features = data["features"]


class PredictionRequest(BaseModel):
    job_title: str
    location: str
    company: str


class PredictionResponse(BaseModel):
    job_title: str
    location: str
    company: str
    predicted_salary_lpa: float
    timestamp: str


@app.get("/")
def home():
    return {"message": "Job Salary Estimator API is running!"}


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/predict", response_model=PredictionResponse)
def predict_salary(request: PredictionRequest):
    try:
        # Encode input using saved encoders
        encoded = []
        for col in features:
            value = getattr(request, col).lower().strip()
            le = encoders[col]
            if value not in le.classes_:
                # Use most similar known class if unknown input
                value = le.classes_[0]
            encoded.append(le.transform([value])[0])

        # Make prediction
        input_array = np.array(encoded).reshape(1, -1)
        predicted_salary = round(float(model.predict(input_array)[0]), 2)

        # Log to database
        log_user_query(
            job_title=request.job_title,
            location=request.location,
            experience_years=0,
            predicted_salary=predicted_salary
        )

        logging.info(
            f"Prediction: {request.job_title} | {request.location} | "
            f"{request.company} → ₹{predicted_salary} LPA"
        )

        return PredictionResponse(
            job_title=request.job_title,
            location=request.location,
            company=request.company,
            predicted_salary_lpa=predicted_salary,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs/titles")
def get_job_titles():
    return {"job_titles": list(encoders["job_title"].classes_)}


@app.get("/jobs/locations")
def get_locations():
    return {"locations": list(encoders["location"].classes_)}


@app.get("/jobs/companies")
def get_companies():
    return {"companies": list(encoders["company"].classes_)}