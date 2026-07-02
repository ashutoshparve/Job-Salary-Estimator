import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import os
import logging

os.makedirs("logs", exist_ok=True)
os.makedirs("model", exist_ok=True)

logging.basicConfig(
    filename="logs/training.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)


def generate_sample_data(n=1000) -> pd.DataFrame:
    np.random.seed(42)

    records = []

    # Realistic salary rules — location and company tier affect salary
    city_multiplier = {
        'bangalore': 1.30, 'mumbai': 1.25, 'delhi': 1.20,
        'hyderabad': 1.15, 'pune': 1.10, 'chennai': 1.05, 'kolkata': 0.90
    }
    company_tier = {
        'Google': 1.5, 'Microsoft': 1.45, 'Amazon': 1.40,
        'Flipkart': 1.25, 'Swiggy': 1.20, 'Zomato': 1.15,
        'Accenture': 1.05, 'Cognizant': 1.0, 'Capgemini': 0.95,
        'IBM': 1.0, 'Infosys': 0.90, 'TCS': 0.88,
        'Wipro': 0.87, 'HCL': 0.86, 'Tech Mahindra': 0.85
    }
    base_salary = {
        'data analyst': 6.0,
        'software engineer': 8.0,
        'python developer': 7.5,
        'data scientist': 10.0,
        'backend developer': 8.5,
        'machine learning engineer': 12.0
    }

    job_titles = list(base_salary.keys())
    locations = list(city_multiplier.keys())
    companies = list(company_tier.keys())

    for _ in range(n):
        title = np.random.choice(job_titles)
        location = np.random.choice(locations)
        company = np.random.choice(companies)

        salary = (
            base_salary[title]
            * city_multiplier[location]
            * company_tier[company]
            * np.random.uniform(0.85, 1.15)  # small noise
        )

        records.append({
            'job_title': title,
            'company': company,
            'location': location,
            'salary_lpa': round(salary, 1),
        })

    df = pd.DataFrame(records)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/cleaned_jobs.csv", index=False)
    logging.info(f"Generated {n} realistic sample records")
    return df

def train_model():
    # Load data
    if os.path.exists("data/cleaned_jobs.csv"):
        df = pd.read_csv("data/cleaned_jobs.csv")
        logging.info(f"Loaded {len(df)} rows from cleaned_jobs.csv")
    else:
        print("No data found — generating sample data...")
        df = generate_sample_data()

    print(f"Training on {len(df)} records...")

    # Features and target
    features = ['job_title', 'location', 'company']
    target = 'salary_lpa'

    df = df.dropna(subset=features + [target])

    # Encode categorical columns
    encoders = {}
    for col in features:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    X = df[features]
    y = df[target]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nModel Performance:")
    print(f"  Mean Absolute Error : ₹{mae:.2f} LPA")
    print(f"  R² Score            : {r2:.2f} ({r2*100:.1f}% accuracy)")

    logging.info(f"Model trained — MAE: {mae:.2f}, R2: {r2:.2f}")

    # Save model and encoders
    with open("model/model.pkl", "wb") as f:
        pickle.dump({"model": model, "encoders": encoders, "features": features}, f)

    print(f"\n✅ Model saved to model/model.pkl")
    logging.info("Model saved successfully")


if __name__ == "__main__":
    train_model()