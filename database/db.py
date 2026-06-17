import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(
    filename="logs/db.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

from urllib.parse import quote_plus
DATABASE_URL = os.getenv("DATABASE_URL") or f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_engine():
    """Create and return a SQLAlchemy engine."""
    try:
        engine = create_engine(DATABASE_URL)
        logging.info("Database engine created successfully")
        return engine
    except Exception as e:
        logging.error(f"Failed to create engine: {e}")
        raise


def test_connection():
    """Test if the database connection works."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        logging.info("Connection test passed")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        logging.error(f"Connection test failed: {e}")


def load_jobs_to_db(csv_path="data/cleaned_jobs.csv"):
    """Load cleaned job listings CSV into the job_listings table."""
    try:
        df = pd.read_csv(csv_path)
        engine = get_engine()
        df.to_sql("job_listings", engine, if_exists="append", index=False)
        print(f"✅ Loaded {len(df)} rows into job_listings table")
        logging.info(f"Loaded {len(df)} rows into job_listings")
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        logging.error(f"Failed to load data: {e}")


def log_user_query(job_title, location, experience_years, predicted_salary):
    """Log every prediction request into user_queries table."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO user_queries 
                    (job_title, location, experience_years, predicted_salary)
                    VALUES (:job_title, :location, :experience_years, :predicted_salary)
                """),
                {
                    "job_title": job_title,
                    "location": location,
                    "experience_years": experience_years,
                    "predicted_salary": predicted_salary
                }
            )
            conn.commit()
        logging.info(f"Logged query: {job_title} | {location} | {experience_years}yrs | ₹{predicted_salary}LPA")
    except Exception as e:
        logging.error(f"Failed to log query: {e}")


if __name__ == "__main__":
    test_connection()