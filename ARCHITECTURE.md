# Architecture

## System Overview


## Services

| Service | Technology | URL |
|---|---|---|
| Frontend | Streamlit | https://salary-estimator-frontend.onrender.com |
| Backend API | FastAPI + Uvicorn | https://job-salary-estimator.onrender.com |
| Database | PostgreSQL 17 | Render Cloud |

## Data Flow

1. User selects job title, location, company on Streamlit
2. Streamlit sends POST request to FastAPI `/predict`
3. FastAPI loads `model.pkl` and encodes the input
4. Random Forest predicts salary in ~80ms
5. FastAPI logs the query to `user_queries` table in PostgreSQL
6. FastAPI returns predicted salary to Streamlit
7. Streamlit displays result with market range visualization

## Database Schema

### job_listings
Stores training data scraped from job listings.
| Column | Type | Description |
|---|---|---|
| id | SERIAL | Primary key |
| job_title | VARCHAR | Role name |
| company | VARCHAR | Company name |
| location | VARCHAR | City |
| salary_lpa | FLOAT | Annual salary in LPA |
| scraped_at | TIMESTAMP | When it was collected |

### user_queries
Logs every prediction made through the app.
| Column | Type | Description |
|---|---|---|
| id | SERIAL | Primary key |
| job_title | VARCHAR | Queried role |
| location | VARCHAR | Queried city |
| experience_years | FLOAT | Years of experience |
| predicted_salary | FLOAT | Model's prediction |
| queried_at | TIMESTAMP | When query was made |