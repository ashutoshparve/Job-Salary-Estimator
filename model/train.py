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

    job_titles = [
        'data analyst', 'software engineer', 'python developer',
        'data scientist', 'backend developer', 'machine learning engineer'
    ]
    locations = ['mumbai', 'bangalore', 'hyderabad', 'pune', 'delhi', 'chennai', 'kolkata']
    companies = [
        'Infosys', 'TCS', 'Wipro', 'HCL', 'Tech Mahindra',
        'Accenture', 'IBM', 'Capgemini', 'Cognizant', 'Amazon',
        'Google', 'Microsoft', 'Flipkart', 'Swiggy', 'Zomato'
    ]

    salary_map = {
        'data analyst': (3, 10),
        'software engineer': (4, 18),
        'python developer': (4, 16),
        'data scientist': (6, 20),
        'backend developer': (5, 18),
        'machine learning engineer': (8, 25)
    }

    titles = np.random.choice(job_titles, n)
    salaries = [round(np.random.uniform(*salary_map[t]), 1) for t in titles]

    df = pd.DataFrame({
        'job_title': titles,
        'company': np.random.choice(companies, n),
        'location': np.random.choice(locations, n),
        'salary_lpa': salaries,
    })

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/cleaned_jobs.csv", index=False)
    logging.info(f"Generated {n} sample records")
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